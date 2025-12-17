"""Value Forecasting - Testing LLM ability to predict moral change."""

from value_forecasting.baselines import (
    run_arima_forecast,
    run_ets_forecast,
    run_naive_forecast,
)
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
from value_forecasting.heterogeneity import (
    DistributionForecast,
    forecast_distribution,
    forecast_distribution_llm,
)

__version__ = "0.1.0"
__all__ = [
    "DistributionForecast",
    "Forecast",
    "ForecastResult",
    "GSS_VARIABLES",
    "HISTORICAL_TRAJECTORIES",
    "calculate_calibration",
    "calculate_coverage",
    "calculate_mae",
    "create_forecast_prompt",
    "evaluate_model",
    "forecast_distribution",
    "forecast_distribution_llm",
    "get_historical_context",
    "run_arima_forecast",
    "run_baseline_forecast",
    "run_ets_forecast",
    "run_forecast",
    "run_naive_forecast",
]
