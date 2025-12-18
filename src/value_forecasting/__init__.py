"""Value Forecasting - Testing LLM ability to predict moral change."""

from value_forecasting.baselines import (
    run_arima_forecast,
    run_ets_forecast,
    run_naive_forecast,
)
from value_forecasting.calibration import (
    CalibratedForecast,
    QuantileForecast,
    apply_calibration,
    calibrate_spread,
    calculate_coverage,
    compute_crps,
    mean_crps,
    quantiles_to_gaussian,
)
from value_forecasting.evaluation import (
    ForecastResult,
    calculate_calibration,
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
from value_forecasting.models import (
    ModelComparisonResult,
    ModelConfig,
    SUPPORTED_MODELS,
    calculate_cost,
    compare_models,
    create_client,
    elicit_quantiles,
    get_model_config,
    parse_quantiles_response,
)

__version__ = "0.1.0"
__all__ = [
    # Calibration
    "CalibratedForecast",
    "QuantileForecast",
    "apply_calibration",
    "calibrate_spread",
    "calculate_coverage",
    "compute_crps",
    "mean_crps",
    "quantiles_to_gaussian",
    # Models
    "ModelComparisonResult",
    "ModelConfig",
    "SUPPORTED_MODELS",
    "calculate_cost",
    "compare_models",
    "create_client",
    "elicit_quantiles",
    "get_model_config",
    "parse_quantiles_response",
    # Legacy
    "DistributionForecast",
    "Forecast",
    "ForecastResult",
    "GSS_VARIABLES",
    "HISTORICAL_TRAJECTORIES",
    "calculate_calibration",
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
