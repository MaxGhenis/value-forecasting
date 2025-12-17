"""Core forecasting logic using LLMs."""

import json
import re
from dataclasses import dataclass

from anthropic import Anthropic
from openai import OpenAI

from .gss_variables import GSS_VARIABLES, get_historical_context


# Model cutoff dates for reference
MODEL_CUTOFFS = {
    "davinci-002": "Oct 2019",  # Original GPT-3
    "text-davinci-002": "June 2021",
    "text-davinci-003": "June 2021",
    "gpt-3.5-turbo-0301": "Sep 2021",
    "gpt-3.5-turbo": "Sep 2021",
    "gpt-4-0314": "Sep 2021",
    "claude-sonnet-4-20250514": "Early 2024",  # Contaminated for GSS 2021
}


@dataclass
class Forecast:
    """A single forecast with uncertainty."""

    variable: str
    cutoff_year: int
    target_year: int
    point_estimate: float
    lower_bound: float  # 90% CI
    upper_bound: float
    model: str
    raw_response: str


def create_forecast_prompt(
    variable: str,
    cutoff_year: int,
    target_years: list[int],
) -> str:
    """Create a prompt for value forecasting."""
    context = get_historical_context(variable, cutoff_year)
    var_info = GSS_VARIABLES[variable]

    prompt = f"""{context}

You are a social scientist in {cutoff_year} analyzing trends in American public opinion.
Based ONLY on the historical data above and your knowledge of social change patterns
up to {cutoff_year}, predict what percentage will give the liberal/progressive response
in future years.

For each target year, provide:
1. Your point estimate (%)
2. A 90% confidence interval (lower%, upper%)

Consider factors like:
- Generational replacement (younger cohorts replacing older ones)
- Social exposure and contact effects
- Information cascades and tipping points
- Historical patterns of moral change

Target years to predict: {target_years}

Respond in JSON format:
{{
    "predictions": [
        {{"year": YYYY, "estimate": XX, "lower": XX, "upper": XX}},
        ...
    ],
    "reasoning": "Brief explanation of your reasoning"
}}
"""
    return prompt


def extract_predictions(response_text: str) -> dict:
    """Extract JSON predictions from model response."""
    # Try to find JSON in the response
    json_match = re.search(r"\{[\s\S]*\}", response_text)
    if json_match:
        try:
            return json.loads(json_match.group())
        except json.JSONDecodeError:
            pass
    return {"predictions": [], "reasoning": "Failed to parse"}


def run_forecast(
    variable: str,
    cutoff_year: int,
    target_years: list[int],
    model: str = "claude-sonnet-4-20250514",
) -> list[Forecast]:
    """Run a forecast using Claude."""
    client = Anthropic()

    prompt = create_forecast_prompt(variable, cutoff_year, target_years)

    # System prompt to set temporal context
    system = f"""You are a social scientist conducting research in {cutoff_year}.
You have access only to information available up to {cutoff_year}.
You do not know what happened after {cutoff_year}.
Base your predictions solely on historical patterns visible in the data provided."""

    response = client.messages.create(
        model=model,
        max_tokens=1024,
        system=system,
        messages=[{"role": "user", "content": prompt}],
    )

    raw_response = response.content[0].text
    parsed = extract_predictions(raw_response)

    forecasts = []
    for pred in parsed.get("predictions", []):
        forecasts.append(
            Forecast(
                variable=variable,
                cutoff_year=cutoff_year,
                target_year=pred["year"],
                point_estimate=pred["estimate"],
                lower_bound=pred["lower"],
                upper_bound=pred["upper"],
                model=model,
                raw_response=raw_response,
            )
        )

    return forecasts


def run_forecast_openai(
    variable: str,
    cutoff_year: int,
    target_years: list[int],
    model: str = "gpt-3.5-turbo",
) -> list[Forecast]:
    """
    Run a forecast using OpenAI models.

    For proper temporal holdout, use models with training cutoffs BEFORE target years:
    - davinci-002 (Oct 2019): Can predict 2021, 2022
    - gpt-3.5-turbo (Sep 2021): Can predict 2022
    """
    client = OpenAI()

    prompt = create_forecast_prompt(variable, cutoff_year, target_years)
    system = f"""You are a social scientist conducting research in {cutoff_year}.
You have access only to information available up to {cutoff_year}.
You do not know what happened after {cutoff_year}.
Base your predictions solely on historical patterns visible in the data provided."""

    try:
        if model.startswith("davinci") or model.startswith("text-davinci"):
            # Completion API for older models
            full_prompt = f"{system}\n\n{prompt}"
            response = client.completions.create(
                model=model,
                prompt=full_prompt,
                max_tokens=1024,
                temperature=0.7,
            )
            raw_response = response.choices[0].text
        else:
            # Chat API for newer models
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=1024,
            )
            raw_response = response.choices[0].message.content

        parsed = extract_predictions(raw_response)

        forecasts = []
        for pred in parsed.get("predictions", []):
            forecasts.append(
                Forecast(
                    variable=variable,
                    cutoff_year=cutoff_year,
                    target_year=pred["year"],
                    point_estimate=pred["estimate"],
                    lower_bound=pred["lower"],
                    upper_bound=pred["upper"],
                    model=model,
                    raw_response=raw_response,
                )
            )

        return forecasts

    except Exception as e:
        print(f"OpenAI forecast failed: {e}")
        return []


def run_baseline_forecast(
    variable: str,
    cutoff_year: int,
    target_years: list[int],
) -> list[Forecast]:
    """Simple linear extrapolation baseline."""
    from .gss_variables import HISTORICAL_TRAJECTORIES

    trajectory = HISTORICAL_TRAJECTORIES.get(variable, {})
    pre_cutoff = {y: v for y, v in trajectory.items() if y <= cutoff_year}

    if len(pre_cutoff) < 2:
        return []

    # Simple linear regression
    years = sorted(pre_cutoff.keys())
    values = [pre_cutoff[y] for y in years]

    n = len(years)
    sum_x = sum(years)
    sum_y = sum(values)
    sum_xy = sum(x * y for x, y in zip(years, values))
    sum_x2 = sum(x**2 for x in years)

    slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x**2)
    intercept = (sum_y - slope * sum_x) / n

    # Calculate residual standard error for uncertainty
    predictions_in_sample = [slope * y + intercept for y in years]
    residuals = [actual - pred for actual, pred in zip(values, predictions_in_sample)]
    se = (sum(r**2 for r in residuals) / (n - 2)) ** 0.5 if n > 2 else 5

    forecasts = []
    for target_year in target_years:
        estimate = slope * target_year + intercept
        # Wider uncertainty for further predictions
        years_out = target_year - cutoff_year
        uncertainty = se * (1 + years_out * 0.1) * 1.645  # 90% CI

        forecasts.append(
            Forecast(
                variable=variable,
                cutoff_year=cutoff_year,
                target_year=target_year,
                point_estimate=max(0, min(100, estimate)),
                lower_bound=max(0, estimate - uncertainty),
                upper_bound=min(100, estimate + uncertainty),
                model="linear_extrapolation",
                raw_response=f"y = {slope:.2f}*x + {intercept:.2f}",
            )
        )

    return forecasts
