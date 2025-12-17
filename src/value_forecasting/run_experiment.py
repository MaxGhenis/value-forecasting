"""Run the value forecasting experiment."""

import json
from pathlib import Path

from value_forecasting import (
    HISTORICAL_TRAJECTORIES,
    ForecastResult,
    evaluate_model,
    run_baseline_forecast,
    run_forecast,
)


def run_experiment(
    variables: list[str] | None = None,
    cutoff_years: list[int] | None = None,
    use_llm: bool = True,
) -> dict:
    """
    Run the value forecasting experiment.

    Args:
        variables: GSS variables to test (default: HOMOSEX, GRASS)
        cutoff_years: Years to use as training cutoffs (default: 1990, 2000)
        use_llm: Whether to run LLM forecasts (requires API key)

    Returns:
        Dictionary of results by model
    """
    if variables is None:
        variables = ["HOMOSEX", "GRASS"]
    if cutoff_years is None:
        cutoff_years = [1990, 2000]

    results = {"baseline": [], "llm": []}

    for variable in variables:
        trajectory = HISTORICAL_TRAJECTORIES.get(variable, {})
        available_years = sorted(trajectory.keys())

        for cutoff in cutoff_years:
            # Find target years (post-cutoff years with data)
            target_years = [y for y in available_years if y > cutoff]
            if not target_years:
                continue

            print(f"\n{variable} @ cutoff {cutoff} -> targets {target_years}")

            # Baseline forecasts
            baseline_forecasts = run_baseline_forecast(variable, cutoff, target_years)
            for f in baseline_forecasts:
                actual = trajectory.get(f.target_year)
                if actual is not None:
                    results["baseline"].append(
                        ForecastResult(
                            variable=f.variable,
                            cutoff_year=f.cutoff_year,
                            target_year=f.target_year,
                            predicted=f.point_estimate,
                            actual=actual,
                            lower=f.lower_bound,
                            upper=f.upper_bound,
                            model=f.model,
                        )
                    )
                    print(
                        f"  Baseline {f.target_year}: "
                        f"pred={f.point_estimate:.1f}% "
                        f"[{f.lower_bound:.1f}, {f.upper_bound:.1f}], "
                        f"actual={actual}%"
                    )

            # LLM forecasts
            if use_llm:
                try:
                    llm_forecasts = run_forecast(variable, cutoff, target_years)
                    for f in llm_forecasts:
                        actual = trajectory.get(f.target_year)
                        if actual is not None:
                            results["llm"].append(
                                ForecastResult(
                                    variable=f.variable,
                                    cutoff_year=f.cutoff_year,
                                    target_year=f.target_year,
                                    predicted=f.point_estimate,
                                    actual=actual,
                                    lower=f.lower_bound,
                                    upper=f.upper_bound,
                                    model=f.model,
                                )
                            )
                            print(
                                f"  LLM {f.target_year}: "
                                f"pred={f.point_estimate:.1f}% "
                                f"[{f.lower_bound:.1f}, {f.upper_bound:.1f}], "
                                f"actual={actual}%"
                            )
                except Exception as e:
                    print(f"  LLM forecast failed: {e}")

    # Evaluate
    print("\n" + "=" * 50)
    print("EVALUATION")
    print("=" * 50)

    for model_name, model_results in results.items():
        if model_results:
            metrics = evaluate_model(model_results)
            print(f"\n{model_name.upper()}:")
            print(f"  N forecasts: {metrics['n_forecasts']}")
            print(f"  MAE: {metrics['mae']:.1f}%")
            print(f"  RMSE: {metrics['rmse']:.1f}%")
            print(f"  Bias: {metrics['bias']:.1f}%")
            print(f"  Coverage (90% CI): {metrics['coverage_90']:.1%}")
            print(f"  Calibration error: {metrics['calibration_error']:.1%}")

    return results


def main():
    """Run experiment and save results."""
    results = run_experiment(use_llm=True)

    # Save results
    output_dir = Path("results")
    output_dir.mkdir(exist_ok=True)

    # Convert to serializable format
    serializable = {}
    for model, forecasts in results.items():
        serializable[model] = [
            {
                "variable": f.variable,
                "cutoff_year": f.cutoff_year,
                "target_year": f.target_year,
                "predicted": f.predicted,
                "actual": f.actual,
                "lower": f.lower,
                "upper": f.upper,
                "model": f.model,
            }
            for f in forecasts
        ]

    with open(output_dir / "forecasts.json", "w") as f:
        json.dump(serializable, f, indent=2)

    print(f"\nResults saved to {output_dir}/forecasts.json")


if __name__ == "__main__":
    main()
