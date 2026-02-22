"""Generate baseline time series forecasts and save to JSON."""

import json
from pathlib import Path

from value_forecasting.baselines import (
    run_arima_forecast,
    run_naive_forecast,
    run_linear_forecast,
    run_ets_forecast,
)
from value_forecasting.gss_variables import GSS_VARIABLES, HISTORICAL_TRAJECTORIES


def main():
    """Generate and save baseline forecasts for all variables."""
    variables = list(HISTORICAL_TRAJECTORIES.keys())
    cutoff_year = 2022
    target_years = [2024, 2030, 2050, 2100]

    results = {
        "cutoff_year": cutoff_year,
        "target_years": target_years,
        "method": "logit_transform",
        "models": {},
    }

    # Generate forecasts for each model
    for model_name, forecast_fn in [
        ("naive", run_naive_forecast),
        ("linear", run_linear_forecast),
        ("arima", run_arima_forecast),
        ("ets", run_ets_forecast),
    ]:
        model_results = {}

        for var in variables:
            forecasts = forecast_fn(var, cutoff_year, target_years)

            if not forecasts:
                continue

            var_info = GSS_VARIABLES.get(var, {})
            var_results = {
                "description": var_info.get("description", var),
                "forecasts": {},
            }

            for f in forecasts:
                var_results["forecasts"][f.target_year] = {
                    "point": round(f.point_estimate, 1),
                    "lower": round(f.lower_bound, 1),
                    "upper": round(f.upper_bound, 1),
                }

            model_results[var] = var_results

        results["models"][model_name] = model_results

    # Save to JSON
    output_path = Path(__file__).parent.parent / "data" / "baseline_forecasts.json"
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)

    print(f"Saved baseline forecasts to {output_path}")
    print(f"  - {len(variables)} variables")
    print(f"  - {len(target_years)} target years: {target_years}")
    print(f"  - 4 models: naive, linear, arima, ets")


if __name__ == "__main__":
    main()
