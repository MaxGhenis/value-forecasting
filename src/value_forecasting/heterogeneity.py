"""Heterogeneity (distribution) forecasting."""

import json
import re
from dataclasses import dataclass, field

from anthropic import Anthropic

from value_forecasting.gss_variables import GSS_VARIABLES


@dataclass
class DistributionForecast:
    """A forecast of the full response distribution with uncertainty."""

    variable: str
    cutoff_year: int
    target_year: int
    distribution: dict[str, float]  # response -> percentage
    distribution_ci: dict[str, tuple[float, float]]  # response -> (lower, upper)
    model: str
    raw_response: str = ""


# Historical full distributions for key variables
# Source: GSS Data Explorer aggregations
HISTORICAL_DISTRIBUTIONS = {
    "HOMOSEX": {
        1990: {
            "Always wrong": 73,
            "Almost always wrong": 5,
            "Sometimes wrong": 6,
            "Not wrong at all": 13,
            "Other/DK": 3,
        },
        2000: {
            "Always wrong": 55,
            "Almost always wrong": 5,
            "Sometimes wrong": 10,
            "Not wrong at all": 27,
            "Other/DK": 3,
        },
        2010: {
            "Always wrong": 44,
            "Almost always wrong": 4,
            "Sometimes wrong": 9,
            "Not wrong at all": 41,
            "Other/DK": 2,
        },
        2018: {
            "Always wrong": 30,
            "Almost always wrong": 4,
            "Sometimes wrong": 7,
            "Not wrong at all": 58,
            "Other/DK": 1,
        },
    },
    "GRASS": {
        1990: {
            "Legal": 16,
            "Not legal": 81,
            "Other/DK": 3,
        },
        2000: {
            "Legal": 31,
            "Not legal": 66,
            "Other/DK": 3,
        },
        2010: {
            "Legal": 44,
            "Not legal": 53,
            "Other/DK": 3,
        },
        2018: {
            "Legal": 61,
            "Not legal": 37,
            "Other/DK": 2,
        },
    },
}


def get_distribution_context(variable: str, cutoff_year: int) -> str:
    """Generate historical distribution context for prompting."""
    if variable not in GSS_VARIABLES:
        raise ValueError(f"Unknown variable: {variable}")

    var_info = GSS_VARIABLES[variable]
    distributions = HISTORICAL_DISTRIBUTIONS.get(variable, {})

    pre_cutoff = {y: d for y, d in distributions.items() if y <= cutoff_year}

    context = f"""Question: {var_info['question']}

Response options: {list(var_info['responses'].values())}

Historical response distributions (% for each response):
"""
    for year in sorted(pre_cutoff.keys()):
        dist = pre_cutoff[year]
        context += f"\n{year}:\n"
        for response, pct in dist.items():
            context += f"  - {response}: {pct}%\n"

    return context


def forecast_distribution(
    variable: str,
    cutoff_year: int,
    target_year: int,
) -> DistributionForecast:
    """
    Forecast full response distribution using linear extrapolation.

    Extrapolates each response category independently.
    """
    distributions = HISTORICAL_DISTRIBUTIONS.get(variable, {})
    pre_cutoff = {y: d for y, d in distributions.items() if y <= cutoff_year}

    if len(pre_cutoff) < 2:
        # Not enough data, return last known distribution
        if pre_cutoff:
            last_year = max(pre_cutoff.keys())
            return DistributionForecast(
                variable=variable,
                cutoff_year=cutoff_year,
                target_year=target_year,
                distribution=pre_cutoff[last_year],
                distribution_ci={},
                model="naive_distribution",
            )
        raise ValueError(f"No historical distribution data for {variable}")

    years = sorted(pre_cutoff.keys())
    categories = list(pre_cutoff[years[0]].keys())

    # Extrapolate each category
    predicted = {}
    predicted_ci = {}

    for category in categories:
        values = [pre_cutoff[y].get(category, 0) for y in years]

        # Simple linear regression
        n = len(years)
        sum_x = sum(years)
        sum_y = sum(values)
        sum_xy = sum(x * y for x, y in zip(years, values))
        sum_x2 = sum(x**2 for x in years)

        denom = n * sum_x2 - sum_x**2
        if abs(denom) < 1e-10:
            slope = 0
            intercept = sum_y / n
        else:
            slope = (n * sum_xy - sum_x * sum_y) / denom
            intercept = (sum_y - slope * sum_x) / n

        # Predict
        pred = slope * target_year + intercept
        pred = max(0, min(100, pred))

        # Estimate uncertainty
        preds_in_sample = [slope * y + intercept for y in years]
        residuals = [a - p for a, p in zip(values, preds_in_sample)]
        se = (sum(r**2 for r in residuals) / max(1, n - 2)) ** 0.5 if n > 2 else 3

        years_out = target_year - cutoff_year
        uncertainty = se * (1 + years_out * 0.05) * 1.645

        predicted[category] = pred
        predicted_ci[category] = (max(0, pred - uncertainty), min(100, pred + uncertainty))

    # Normalize to sum to 100
    total = sum(predicted.values())
    if total > 0:
        predicted = {k: v * 100 / total for k, v in predicted.items()}

    return DistributionForecast(
        variable=variable,
        cutoff_year=cutoff_year,
        target_year=target_year,
        distribution=predicted,
        distribution_ci=predicted_ci,
        model="linear_distribution",
    )


def forecast_distribution_llm(
    variable: str,
    cutoff_year: int,
    target_year: int,
    model: str = "claude-sonnet-4-20250514",
) -> DistributionForecast:
    """
    Forecast full response distribution using LLM.

    Asks the LLM to predict the entire distribution, not just one category.
    """
    client = Anthropic()

    context = get_distribution_context(variable, cutoff_year)
    var_info = GSS_VARIABLES[variable]
    responses = list(var_info["responses"].values())

    prompt = f"""{context}

You are a social scientist in {cutoff_year} analyzing trends in American public opinion.
Based ONLY on the historical distributions above and your knowledge of social change patterns
up to {cutoff_year}, predict the FULL response distribution in {target_year}.

For EACH response option, predict:
1. The percentage who will give that response
2. A 90% confidence interval

The percentages must sum to approximately 100%.

Response options to predict: {responses}

Respond in JSON format:
{{
    "predictions": {{
        "response_name": {{"estimate": XX, "lower": XX, "upper": XX}},
        ...
    }},
    "reasoning": "Brief explanation"
}}
"""

    system = f"""You are a social scientist conducting research in {cutoff_year}.
You have access only to information available up to {cutoff_year}.
Base predictions solely on historical patterns visible in the data provided."""

    response = client.messages.create(
        model=model,
        max_tokens=1024,
        system=system,
        messages=[{"role": "user", "content": prompt}],
    )

    raw_response = response.content[0].text

    # Extract JSON
    json_match = re.search(r"\{[\s\S]*\}", raw_response)
    if json_match:
        try:
            parsed = json.loads(json_match.group())
            predictions = parsed.get("predictions", {})

            distribution = {}
            distribution_ci = {}

            for resp_name, pred in predictions.items():
                if isinstance(pred, dict):
                    distribution[resp_name] = pred.get("estimate", 0)
                    distribution_ci[resp_name] = (
                        pred.get("lower", 0),
                        pred.get("upper", 100),
                    )

            return DistributionForecast(
                variable=variable,
                cutoff_year=cutoff_year,
                target_year=target_year,
                distribution=distribution,
                distribution_ci=distribution_ci,
                model=model,
                raw_response=raw_response,
            )
        except json.JSONDecodeError:
            pass

    # Fallback
    return DistributionForecast(
        variable=variable,
        cutoff_year=cutoff_year,
        target_year=target_year,
        distribution={},
        distribution_ci={},
        model=model,
        raw_response=raw_response,
    )
