"""Value Forecasting - Testing LLM ability to predict moral change."""

from value_forecasting.evaluation import (
    ForecastResult,
    calculate_calibration,
    calculate_coverage,
    calculate_mae,
    evaluate_model,
)
from value_forecasting.forecaster import (
    Forecast,
    create_forecast_prompt,
    run_baseline_forecast,
    run_forecast,
)
from value_forecasting.gss_variables import (
    GSS_VARIABLES,
    HISTORICAL_TRAJECTORIES,
    get_historical_context,
)

__version__ = "0.1.0"
__all__ = [
    "Forecast",
    "ForecastResult",
    "GSS_VARIABLES",
    "HISTORICAL_TRAJECTORIES",
    "calculate_calibration",
    "calculate_coverage",
    "calculate_mae",
    "create_forecast_prompt",
    "evaluate_model",
    "get_historical_context",
    "run_baseline_forecast",
    "run_forecast",
]
