"""
Multi-model support for value forecasting.

Supports OpenAI (GPT-4o, GPT-5) and Anthropic (Claude Opus, Sonnet) models.
"""

import re
from dataclasses import dataclass

from anthropic import Anthropic
from openai import OpenAI

from .calibration import QuantileForecast


@dataclass
class ModelConfig:
    """Configuration for a forecasting model."""

    name: str
    provider: str  # "openai" or "anthropic"
    model_id: str
    input_cost_per_million: float
    output_cost_per_million: float
    max_tokens: int = 150
    temperature: float = 0.0


@dataclass
class ModelComparisonResult:
    """Results from comparing a model's performance."""

    model: str
    raw_crps: float
    calibrated_crps: float
    spread_multiplier: float
    mae: float
    coverage_80: float
    total_cost: float


# Supported models with pricing (as of Dec 2024)
SUPPORTED_MODELS: dict[str, ModelConfig] = {
    # OpenAI models
    "gpt-4o": ModelConfig(
        name="gpt-4o",
        provider="openai",
        model_id="gpt-4o",
        input_cost_per_million=2.50,
        output_cost_per_million=10.00,
    ),
    "gpt-4o-mini": ModelConfig(
        name="gpt-4o-mini",
        provider="openai",
        model_id="gpt-4o-mini",
        input_cost_per_million=0.15,
        output_cost_per_million=0.60,
    ),
    "gpt-4.5-preview": ModelConfig(
        name="gpt-4.5-preview",
        provider="openai",
        model_id="gpt-4.5-preview",  # GPT-5 preview
        input_cost_per_million=75.00,
        output_cost_per_million=150.00,
    ),
    "o1": ModelConfig(
        name="o1",
        provider="openai",
        model_id="o1",
        input_cost_per_million=15.00,
        output_cost_per_million=60.00,
    ),
    "o1-mini": ModelConfig(
        name="o1-mini",
        provider="openai",
        model_id="o1-mini",
        input_cost_per_million=3.00,
        output_cost_per_million=12.00,
    ),
    # Anthropic models
    "claude-opus-4-20250514": ModelConfig(
        name="claude-opus-4-20250514",
        provider="anthropic",
        model_id="claude-opus-4-20250514",
        input_cost_per_million=15.00,
        output_cost_per_million=75.00,
    ),
    "claude-sonnet-4-20250514": ModelConfig(
        name="claude-sonnet-4-20250514",
        provider="anthropic",
        model_id="claude-sonnet-4-20250514",
        input_cost_per_million=3.00,
        output_cost_per_million=15.00,
    ),
    "claude-haiku-3-5-20241022": ModelConfig(
        name="claude-haiku-3-5-20241022",
        provider="anthropic",
        model_id="claude-3-5-haiku-20241022",
        input_cost_per_million=0.80,
        output_cost_per_million=4.00,
    ),
}


def get_model_config(model_name: str) -> ModelConfig:
    """Get configuration for a model by name."""
    if model_name not in SUPPORTED_MODELS:
        raise ValueError(
            f"Unknown model: {model_name}. "
            f"Supported: {list(SUPPORTED_MODELS.keys())}"
        )
    return SUPPORTED_MODELS[model_name]


def create_client(config: ModelConfig) -> OpenAI | Anthropic:
    """Create API client for the given model configuration."""
    if config.provider == "openai":
        return OpenAI()
    elif config.provider == "anthropic":
        return Anthropic()
    else:
        raise ValueError(f"Unknown provider: {config.provider}")


def calculate_cost(
    config: ModelConfig, input_tokens: int, output_tokens: int
) -> float:
    """Calculate API cost for given token usage."""
    input_cost = input_tokens * config.input_cost_per_million / 1_000_000
    output_cost = output_tokens * config.output_cost_per_million / 1_000_000
    return input_cost + output_cost


def parse_quantiles_response(response_text: str) -> QuantileForecast:
    """
    Parse quantile values from LLM response.

    Extracts 5 numeric values and ensures monotonicity.

    Args:
        response_text: Raw text response from LLM

    Returns:
        QuantileForecast with q10, q25, q50, q75, q90

    Raises:
        ValueError: If fewer than 5 numbers found
    """
    # Extract all numbers from response
    numbers = re.findall(r"(\d+(?:\.\d+)?)", response_text)

    if len(numbers) < 5:
        raise ValueError(
            f"Could not parse 5 quantiles from response. Found: {numbers}"
        )

    # Take first 5 numbers and convert to float
    quantiles = [float(n) for n in numbers[:5]]

    # Sort to ensure monotonicity
    quantiles = sorted(quantiles)

    return QuantileForecast(
        q10=quantiles[0],
        q25=quantiles[1],
        q50=quantiles[2],
        q75=quantiles[3],
        q90=quantiles[4],
    )


def _build_quantile_prompt(
    variable: str, description: str, history: str, target_year: int
) -> tuple[str, str]:
    """Build system and user prompts for quantile elicitation."""
    system = """You are a social scientist forecasting survey trends.
Provide quantile predictions - values you're X% confident the actual will be BELOW."""

    user = f"""Based on historical General Social Survey data, forecast the distribution of
"{description}" (% giving this response) in {target_year}.

Historical data:
{history}

Provide your forecast as 5 quantiles (values the actual will be BELOW with given probability):
- 10th percentile (10% chance actual is below this):
- 25th percentile (25% chance actual is below this):
- 50th percentile (median, 50% chance actual is below this):
- 75th percentile (75% chance actual is below this):
- 90th percentile (90% chance actual is below this):

Respond with ONLY 5 numbers, one per line, no other text."""

    return system, user


def elicit_quantiles(
    config: ModelConfig,
    client: OpenAI | Anthropic,
    variable: str,
    description: str,
    history: str,
    target_year: int,
) -> tuple[QuantileForecast | None, float]:
    """
    Elicit quantile forecast from an LLM.

    Args:
        config: Model configuration
        client: API client (OpenAI or Anthropic)
        variable: GSS variable name
        description: Human-readable description
        history: Historical data as string
        target_year: Year to forecast

    Returns:
        Tuple of (QuantileForecast or None if failed, cost in dollars)
    """
    system, user = _build_quantile_prompt(variable, description, history, target_year)

    try:
        if config.provider == "openai":
            response = client.chat.completions.create(
                model=config.model_id,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
                max_tokens=config.max_tokens,
                temperature=config.temperature,
            )
            text = response.choices[0].message.content.strip()
            input_tokens = response.usage.prompt_tokens
            output_tokens = response.usage.completion_tokens

        elif config.provider == "anthropic":
            response = client.messages.create(
                model=config.model_id,
                system=system,
                messages=[{"role": "user", "content": user}],
                max_tokens=config.max_tokens,
            )
            text = response.content[0].text.strip()
            input_tokens = response.usage.input_tokens
            output_tokens = response.usage.output_tokens

        else:
            raise ValueError(f"Unknown provider: {config.provider}")

        cost = calculate_cost(config, input_tokens, output_tokens)
        quantiles = parse_quantiles_response(text)

        return quantiles, cost

    except Exception as e:
        print(f"Error eliciting quantiles for {variable}: {e}")
        return None, 0.0


def compare_models(
    model_names: list[str],
    variables: dict,
    cutoff_year: int,
    target_year: int,
) -> list[ModelComparisonResult]:
    """
    Compare multiple models on the same forecasting task.

    Args:
        model_names: List of model names to compare
        variables: Dict of variable data with trajectories
        cutoff_year: Year to use as information cutoff
        target_year: Year to forecast (holdout)

    Returns:
        List of ModelComparisonResult for each model
    """
    from .calibration import (
        calibrate_spread,
        quantiles_to_gaussian,
        apply_calibration,
        calculate_coverage,
        compute_crps,
    )

    results = []

    for model_name in model_names:
        config = get_model_config(model_name)
        client = create_client(config)

        forecasts = []
        actuals = []
        quantile_forecasts = []
        total_cost = 0.0

        for var, data in variables.items():
            # Build history up to cutoff
            traj = {int(y): v for y, v in data["trajectory"].items()}
            if target_year not in traj:
                continue

            pre_cutoff = {y: v for y, v in traj.items() if y <= cutoff_year}
            if len(pre_cutoff) < 3:
                continue

            history = "\n".join(
                [f"  {y}: {round(v)}%" for y, v in sorted(pre_cutoff.items())]
            )

            quantiles, cost = elicit_quantiles(
                config=config,
                client=client,
                variable=var,
                description=data["description"],
                history=history,
                target_year=target_year,
            )

            if quantiles is None:
                continue

            total_cost += cost
            mu, sig = quantiles_to_gaussian(quantiles)
            forecasts.append((mu, sig))
            actuals.append(traj[target_year])
            quantile_forecasts.append(quantiles)

        if len(forecasts) < 3:
            print(f"Insufficient forecasts for {model_name}")
            continue

        # Calibrate
        spread_mult, calibrated_crps = calibrate_spread(forecasts, actuals)
        raw_crps = sum(
            compute_crps(a, mu, sig) for (mu, sig), a in zip(forecasts, actuals)
        ) / len(actuals)

        # Calculate MAE
        mae = sum(abs(mu - a) for (mu, _), a in zip(forecasts, actuals)) / len(actuals)

        # Calculate coverage with calibration
        calibrated = [apply_calibration(q, spread_mult) for q in quantile_forecasts]
        coverage = calculate_coverage(calibrated, actuals)

        results.append(
            ModelComparisonResult(
                model=model_name,
                raw_crps=raw_crps,
                calibrated_crps=calibrated_crps,
                spread_multiplier=spread_mult,
                mae=mae,
                coverage_80=coverage,
                total_cost=total_cost,
            )
        )

    return results
