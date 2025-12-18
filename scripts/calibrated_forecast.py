"""
Calibrated value forecasting with quantile elicitation and CRPS optimization.

Uses EMOS-style post-hoc calibration:
1. Elicit quantile forecasts from LLM
2. Compute CRPS on holdout (GSS 2024)
3. Find spread multiplier that minimizes CRPS
4. Apply to long-term forecasts
"""

import json
import re
import numpy as np
from pathlib import Path
from scipy.optimize import minimize_scalar
from openai import OpenAI

# Cost per 1M tokens (as of Dec 2024)
MODEL_COSTS = {
    "gpt-4o": {"input": 2.50, "output": 10.00},
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    "gpt-3.5-turbo": {"input": 0.50, "output": 1.50},
    "gpt-3.5-turbo-instruct": {"input": 1.50, "output": 2.00},
}

# Global cost tracker
cost_tracker = {"input_tokens": 0, "output_tokens": 0, "total_cost": 0.0}


def track_cost(response, model: str):
    """Track API costs from response usage."""
    if not hasattr(response, 'usage') or response.usage is None:
        return

    input_tokens = response.usage.prompt_tokens
    output_tokens = response.usage.completion_tokens

    cost_tracker["input_tokens"] += input_tokens
    cost_tracker["output_tokens"] += output_tokens

    if model in MODEL_COSTS:
        cost = (input_tokens * MODEL_COSTS[model]["input"] / 1_000_000 +
                output_tokens * MODEL_COSTS[model]["output"] / 1_000_000)
        cost_tracker["total_cost"] += cost


def print_cost_summary():
    """Print cost summary."""
    print(f"\n{'='*50}")
    print("API Cost Summary:")
    print(f"  Input tokens:  {cost_tracker['input_tokens']:,}")
    print(f"  Output tokens: {cost_tracker['output_tokens']:,}")
    print(f"  Total cost:    ${cost_tracker['total_cost']:.4f}")
    print(f"{'='*50}")


# Try to import properscoring, fall back to manual CRPS if not available
try:
    from properscoring import crps_gaussian
    HAS_PROPERSCORING = True
except ImportError:
    HAS_PROPERSCORING = False
    print("Warning: properscoring not installed. Using manual CRPS computation.")


def crps_gaussian_manual(actual, mu, sig):
    """Manual CRPS for Gaussian distribution (if properscoring not available)."""
    from scipy.stats import norm
    z = (actual - mu) / sig
    return sig * (z * (2 * norm.cdf(z) - 1) + 2 * norm.pdf(z) - 1 / np.sqrt(np.pi))


def compute_crps(actual, mu, sig):
    """Compute CRPS for a Gaussian forecast."""
    if HAS_PROPERSCORING:
        return crps_gaussian(actual, mu=mu, sig=sig)
    return crps_gaussian_manual(actual, mu, sig)


def load_trajectories(path: str = "data/trajectories.json") -> dict:
    """Load trajectories from JSON file."""
    with open(path) as f:
        data = json.load(f)
    return data["variables"]


def elicit_quantiles(client, var: str, desc: str, history: str,
                     target_year: int, model: str = "gpt-4o") -> dict | None:
    """
    Elicit quantile forecast from LLM.

    Returns dict with keys: q10, q25, q50, q75, q90
    """
    system = f"""You are a social scientist forecasting survey trends.
Provide quantile predictions - values you're X% confident the actual will be BELOW."""

    user = f"""Based on historical General Social Survey data, forecast the distribution of
"{desc}" (% giving this response) in {target_year}.

Historical data:
{history}

Provide your forecast as 5 quantiles (values the actual will be BELOW with given probability):
- 10th percentile (10% chance actual is below this):
- 25th percentile (25% chance actual is below this):
- 50th percentile (median, 50% chance actual is below this):
- 75th percentile (75% chance actual is below this):
- 90th percentile (90% chance actual is below this):

Respond with ONLY 5 numbers, one per line, no other text."""

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user}
            ],
            max_tokens=100,
            temperature=0
        )
        track_cost(response, model)
        text = response.choices[0].message.content.strip()

        # Parse 5 numbers from response
        numbers = re.findall(r'(\d+(?:\.\d+)?)', text)
        if len(numbers) >= 5:
            quantiles = [float(n) for n in numbers[:5]]
            # Ensure monotonicity
            quantiles = sorted(quantiles)
            return {
                "q10": quantiles[0],
                "q25": quantiles[1],
                "q50": quantiles[2],
                "q75": quantiles[3],
                "q90": quantiles[4],
            }
    except Exception as e:
        print(f"  Error for {var}: {e}")
    return None


def quantiles_to_gaussian(quantiles: dict) -> tuple[float, float]:
    """
    Convert quantile forecast to Gaussian parameters (mean, std).

    Uses median as mean and IQR-based std estimate.
    """
    median = quantiles["q50"]
    # IQR = q75 - q25, for normal distribution IQR ≈ 1.35 * std
    iqr = quantiles["q75"] - quantiles["q25"]
    std = iqr / 1.35 if iqr > 0 else 5.0  # fallback
    return median, std


def get_historical_context(var_data: dict, cutoff_year: int) -> tuple[str, dict]:
    """Build historical context string up to cutoff year."""
    traj = var_data["trajectory"]
    pre_cutoff = {int(y): round(v) for y, v in traj.items() if int(y) <= cutoff_year}

    if len(pre_cutoff) < 2:
        return None, None

    history = "\n".join([f"  {y}: {v}%" for y, v in sorted(pre_cutoff.items())])
    return history, pre_cutoff


def calibrate_spread(forecasts: list[tuple[float, float]], actuals: list[float]) -> float:
    """
    Find spread multiplier that minimizes mean CRPS.

    Args:
        forecasts: List of (mean, std) tuples
        actuals: List of actual values

    Returns:
        Optimal spread multiplier
    """
    def objective(sigma_mult):
        total_crps = 0
        for (mu, sig), actual in zip(forecasts, actuals):
            total_crps += compute_crps(actual, mu, sig * sigma_mult)
        return total_crps / len(actuals)

    result = minimize_scalar(objective, bounds=(0.1, 10.0), method='bounded')
    return result.x, result.fun


def run_calibration_experiment(trajectories: dict, model: str,
                                cutoff_year: int, target_year: int,
                                client: OpenAI) -> dict:
    """
    Run calibration experiment:
    1. Get quantile forecasts for all variables
    2. Compute raw CRPS
    3. Find optimal spread multiplier
    4. Report calibrated CRPS
    """
    results = []
    forecasts = []
    actuals = []

    for var, data in trajectories.items():
        history, pre_cutoff = get_historical_context(data, cutoff_year)
        if history is None:
            continue

        # Check if we have actual target year data
        traj = {int(y): v for y, v in data["trajectory"].items()}
        if target_year not in traj:
            continue
        actual = traj[target_year]

        print(f"Forecasting {var}...")
        quantiles = elicit_quantiles(client, var, data["description"],
                                      history, target_year, model)

        if quantiles is None:
            print(f"  Failed to get quantiles for {var}")
            continue

        mu, sig = quantiles_to_gaussian(quantiles)
        raw_crps = compute_crps(actual, mu, sig)

        results.append({
            "variable": var,
            "description": data["description"],
            "actual": actual,
            "quantiles": quantiles,
            "gaussian_mu": mu,
            "gaussian_sig": sig,
            "raw_crps": raw_crps,
        })

        forecasts.append((mu, sig))
        actuals.append(actual)

        print(f"  Actual: {actual:.1f}%, Median: {mu:.1f}%, Std: {sig:.1f}, CRPS: {raw_crps:.2f}")

    # Calibration
    if len(forecasts) >= 3:
        spread_mult, calibrated_crps = calibrate_spread(forecasts, actuals)
        print(f"\n{'='*50}")
        print(f"Calibration Results:")
        print(f"  Optimal spread multiplier: {spread_mult:.2f}")
        print(f"  Raw mean CRPS: {np.mean([r['raw_crps'] for r in results]):.2f}")
        print(f"  Calibrated mean CRPS: {calibrated_crps:.2f}")

        # Compute coverage at different levels
        for level, (q_low, q_high) in [
            (50, ("q25", "q75")),
            (80, ("q10", "q90")),
        ]:
            coverage = sum(
                1 for r in results
                if r["quantiles"][q_low] <= r["actual"] <= r["quantiles"][q_high]
            ) / len(results)
            print(f"  Raw {level}% interval coverage: {coverage*100:.0f}%")
    else:
        spread_mult = 1.0
        calibrated_crps = None

    return {
        "model": model,
        "cutoff_year": cutoff_year,
        "target_year": target_year,
        "results": results,
        "spread_multiplier": spread_mult,
        "raw_mean_crps": np.mean([r["raw_crps"] for r in results]),
        "calibrated_mean_crps": calibrated_crps,
        "n_variables": len(results),
    }


def generate_long_term_forecasts(client, trajectories: dict, model: str,
                                  target_years: list[int], spread_mult: float) -> list[dict]:
    """Generate calibrated long-term forecasts."""
    long_term = []

    # Use all available data as history
    cutoff_year = 2024

    for var, data in trajectories.items():
        history, _ = get_historical_context(data, cutoff_year)
        if history is None:
            continue

        var_forecasts = {"variable": var, "description": data["description"]}

        for target_year in target_years:
            print(f"Forecasting {var} for {target_year}...")
            quantiles = elicit_quantiles(client, var, data["description"],
                                          history, target_year, model)

            if quantiles:
                mu, sig = quantiles_to_gaussian(quantiles)
                # Apply calibration
                calibrated_sig = sig * spread_mult

                var_forecasts[f"y{target_year}"] = {
                    "median": mu,
                    "raw_std": sig,
                    "calibrated_std": calibrated_sig,
                    "calibrated_80_ci": [
                        mu - 1.28 * calibrated_sig,
                        mu + 1.28 * calibrated_sig
                    ],
                    "quantiles": quantiles,
                }

        long_term.append(var_forecasts)

    return long_term


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="gpt-4o")
    parser.add_argument("--cutoff", type=int, default=2021)
    parser.add_argument("--target", type=int, default=2024)
    parser.add_argument("--data", default="data/trajectories.json")
    parser.add_argument("--long-term", action="store_true",
                        help="Also generate long-term forecasts")
    args = parser.parse_args()

    client = OpenAI()
    trajectories = load_trajectories(args.data)

    print(f"Loaded {len(trajectories)} variables")
    print(f"Running calibration: {args.model} predicting {args.target} from {args.cutoff}")
    print("="*50)

    # Run calibration experiment
    calibration = run_calibration_experiment(
        trajectories, args.model, args.cutoff, args.target, client
    )

    # Save calibration results
    output_path = f"data/calibration_{args.model}_{args.cutoff}_{args.target}.json"
    with open(output_path, "w") as f:
        json.dump(calibration, f, indent=2)
    print(f"\nSaved calibration to {output_path}")

    # Print cost after calibration
    print_cost_summary()

    # Optional: generate long-term forecasts with calibration
    if args.long_term and calibration["spread_multiplier"]:
        print("\n" + "="*50)
        print("Generating calibrated long-term forecasts...")

        long_term = generate_long_term_forecasts(
            client, trajectories, args.model,
            target_years=[2030, 2050, 2075, 2100],
            spread_mult=calibration["spread_multiplier"]
        )

        output_path = f"data/longterm_{args.model}_calibrated.json"
        with open(output_path, "w") as f:
            json.dump({
                "model": args.model,
                "calibration_spread": calibration["spread_multiplier"],
                "forecasts": long_term,
            }, f, indent=2)
        print(f"Saved long-term forecasts to {output_path}")

    # Print cost summary
    print_cost_summary()
