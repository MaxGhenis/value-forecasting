"""Time series baseline forecasters.

All forecasters use logit transformation to ensure predictions
are bounded to [0, 100] (valid proportions).
"""

import warnings

import numpy as np
from scipy import stats

from value_forecasting.forecaster import Forecast
from value_forecasting.gss_variables import HISTORICAL_TRAJECTORIES


# Logit transform functions for bounded forecasts
def logit(p: float, eps: float = 1e-6) -> float:
    """
    Logit transformation: log(p / (1-p)).

    Clamps input to (eps, 1-eps) to avoid -inf/+inf.
    Input p should be in (0, 1) representing a proportion.
    """
    p_clamped = np.clip(p, eps, 1 - eps)
    return np.log(p_clamped / (1 - p_clamped))


def inverse_logit(x: float) -> float:
    """
    Inverse logit (sigmoid): 1 / (1 + exp(-x)).

    Returns value in (0, 1).
    """
    return 1 / (1 + np.exp(-x))


def run_naive_forecast(
    variable: str,
    cutoff_year: int,
    target_years: list[int],
) -> list[Forecast]:
    """
    Naive baseline: predict the last observed value.

    Uses logit transformation for uncertainty intervals to ensure bounds.
    """
    trajectory = HISTORICAL_TRAJECTORIES.get(variable, {})
    pre_cutoff = {y: v for y, v in trajectory.items() if y <= cutoff_year}

    if not pre_cutoff:
        return []

    years = sorted(pre_cutoff.keys())
    last_value = pre_cutoff[years[-1]]

    # Convert to proportion
    p = last_value / 100.0

    # Estimate uncertainty in logit space from historical volatility
    if len(years) >= 2:
        # Transform to logit space for changes
        logit_values = [logit(pre_cutoff[y] / 100.0) for y in years]
        logit_changes = [
            logit_values[i] - logit_values[i - 1]
            for i in range(1, len(logit_values))
        ]
        logit_std = np.std(logit_changes) if logit_changes else 0.5
    else:
        logit_std = 0.5

    forecasts = []
    for target_year in target_years:
        years_out = target_year - cutoff_year
        # Uncertainty grows with sqrt of time in logit space
        logit_uncertainty = logit_std * np.sqrt(years_out / 10) * 1.645  # 90% CI

        # Point estimate stays at last value
        logit_p = logit(p)

        # Back-transform bounds
        lower_p = inverse_logit(logit_p - logit_uncertainty)
        upper_p = inverse_logit(logit_p + logit_uncertainty)

        forecasts.append(
            Forecast(
                variable=variable,
                cutoff_year=cutoff_year,
                target_year=target_year,
                point_estimate=last_value,
                lower_bound=lower_p * 100,
                upper_bound=upper_p * 100,
                model="naive",
                raw_response=f"Last value: {last_value}",
            )
        )

    return forecasts


def run_linear_forecast(
    variable: str,
    cutoff_year: int,
    target_years: list[int],
) -> list[Forecast]:
    """
    Linear regression baseline with logit transformation.

    Fits linear regression in logit space, then back-transforms
    predictions to ensure bounds in [0, 100].

    Prediction intervals account for both parameter uncertainty
    and residual variance.
    """
    trajectory = HISTORICAL_TRAJECTORIES.get(variable, {})
    pre_cutoff = {y: v for y, v in trajectory.items() if y <= cutoff_year}

    if len(pre_cutoff) < 3:
        return []

    years = np.array(sorted(pre_cutoff.keys()))
    values = np.array([pre_cutoff[y] for y in years])

    # Transform to logit space (proportions)
    logit_values = np.array([logit(v / 100.0) for v in values])

    # Center years for numerical stability
    year_mean = years.mean()
    years_centered = years - year_mean

    # Fit linear regression in logit space
    n = len(years)
    x = years_centered
    y = logit_values

    # OLS estimates
    x_mean = x.mean()
    y_mean = y.mean()

    slope = np.sum((x - x_mean) * (y - y_mean)) / np.sum((x - x_mean) ** 2)
    intercept = y_mean - slope * x_mean

    # Residuals and standard error
    y_pred = intercept + slope * x
    residuals = y - y_pred
    mse = np.sum(residuals ** 2) / (n - 2)
    se_residual = np.sqrt(mse)

    # Standard error of slope and intercept
    ss_x = np.sum((x - x_mean) ** 2)
    se_slope = se_residual / np.sqrt(ss_x)
    se_intercept = se_residual * np.sqrt(1 / n + x_mean ** 2 / ss_x)

    forecasts = []
    for target_year in target_years:
        x_new = target_year - year_mean

        # Point prediction in logit space
        logit_pred = intercept + slope * x_new

        # Prediction interval (accounts for parameter + residual uncertainty)
        # Using t-distribution for small samples
        t_crit = stats.t.ppf(0.95, df=n - 2)  # 90% CI

        # Standard error of prediction
        se_pred = se_residual * np.sqrt(
            1 + 1 / n + (x_new - x_mean) ** 2 / ss_x
        )

        logit_lower = logit_pred - t_crit * se_pred
        logit_upper = logit_pred + t_crit * se_pred

        # Back-transform to probability space
        point = inverse_logit(logit_pred) * 100
        lower = inverse_logit(logit_lower) * 100
        upper = inverse_logit(logit_upper) * 100

        forecasts.append(
            Forecast(
                variable=variable,
                cutoff_year=cutoff_year,
                target_year=target_year,
                point_estimate=point,
                lower_bound=lower,
                upper_bound=upper,
                model="linear_logit",
                raw_response=f"Logit linear: slope={slope:.4f}, intercept={intercept:.4f}",
            )
        )

    return forecasts


def run_arima_forecast(
    variable: str,
    cutoff_year: int,
    target_years: list[int],
    order: tuple[int, int, int] = (1, 1, 0),
) -> list[Forecast]:
    """
    ARIMA baseline forecast with logit transformation.

    Fits ARIMA in logit space to ensure bounded predictions.
    Default order (1,1,0) = AR(1) with differencing.
    """
    try:
        from statsmodels.tsa.arima.model import ARIMA
    except ImportError:
        warnings.warn("statsmodels not installed, skipping ARIMA")
        return []

    trajectory = HISTORICAL_TRAJECTORIES.get(variable, {})
    pre_cutoff = {y: v for y, v in trajectory.items() if y <= cutoff_year}

    if len(pre_cutoff) < 4:
        # Not enough data for ARIMA
        return []

    years = sorted(pre_cutoff.keys())
    values = [pre_cutoff[y] for y in years]

    # Transform to logit space
    logit_values = [logit(v / 100.0) for v in values]

    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            model = ARIMA(logit_values, order=order)
            fit = model.fit()

        forecasts = []
        # Get forecast with confidence interval
        max_steps = max(target_years) - years[-1]
        forecast_result = fit.get_forecast(steps=max_steps)
        logit_pred = forecast_result.predicted_mean
        logit_conf_int = forecast_result.conf_int(alpha=0.10)  # 90% CI

        for target_year in target_years:
            idx = target_year - years[-1] - 1
            if idx < 0 or idx >= len(logit_pred):
                continue

            logit_point = float(logit_pred.iloc[idx]) if hasattr(logit_pred, 'iloc') else float(logit_pred[idx])
            logit_lower = float(logit_conf_int.iloc[idx, 0]) if hasattr(logit_conf_int, 'iloc') else float(logit_conf_int[idx, 0])
            logit_upper = float(logit_conf_int.iloc[idx, 1]) if hasattr(logit_conf_int, 'iloc') else float(logit_conf_int[idx, 1])

            # Back-transform to probability space
            point = inverse_logit(logit_point) * 100
            lower = inverse_logit(logit_lower) * 100
            upper = inverse_logit(logit_upper) * 100

            forecasts.append(
                Forecast(
                    variable=variable,
                    cutoff_year=cutoff_year,
                    target_year=target_year,
                    point_estimate=point,
                    lower_bound=lower,
                    upper_bound=upper,
                    model="arima_logit",
                    raw_response=f"ARIMA{order} logit: {logit_point:.3f} -> {point:.1f}%",
                )
            )

        return forecasts

    except Exception as e:
        warnings.warn(f"ARIMA failed: {e}")
        return []


def run_ets_forecast(
    variable: str,
    cutoff_year: int,
    target_years: list[int],
) -> list[Forecast]:
    """
    Exponential Smoothing (ETS) baseline forecast with logit transformation.

    Fits Holt's linear trend method in logit space to ensure bounded predictions.
    """
    try:
        from statsmodels.tsa.holtwinters import ExponentialSmoothing
    except ImportError:
        warnings.warn("statsmodels not installed, skipping ETS")
        return []

    trajectory = HISTORICAL_TRAJECTORIES.get(variable, {})
    pre_cutoff = {y: v for y, v in trajectory.items() if y <= cutoff_year}

    if len(pre_cutoff) < 3:
        return []

    years = sorted(pre_cutoff.keys())
    values = [pre_cutoff[y] for y in years]

    # Transform to logit space
    logit_values = [logit(v / 100.0) for v in values]

    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            # Holt's linear trend in logit space
            model = ExponentialSmoothing(
                logit_values,
                trend="add",
                seasonal=None,
            )
            fit = model.fit()

        forecasts = []
        max_steps = max(target_years) - years[-1]
        logit_predictions = fit.forecast(max_steps)

        # Estimate prediction intervals using residual variance in logit space
        residuals = fit.resid
        logit_sigma = np.std(residuals) if len(residuals) > 1 else 0.5

        for target_year in target_years:
            idx = target_year - years[-1] - 1
            if idx < 0 or idx >= len(logit_predictions):
                continue

            logit_point = float(logit_predictions.iloc[idx]) if hasattr(logit_predictions, 'iloc') else float(logit_predictions[idx])

            # Uncertainty grows with horizon in logit space
            steps = idx + 1
            logit_uncertainty = logit_sigma * np.sqrt(steps) * 1.645  # 90% CI

            # Back-transform to probability space
            point = inverse_logit(logit_point) * 100
            lower = inverse_logit(logit_point - logit_uncertainty) * 100
            upper = inverse_logit(logit_point + logit_uncertainty) * 100

            forecasts.append(
                Forecast(
                    variable=variable,
                    cutoff_year=cutoff_year,
                    target_year=target_year,
                    point_estimate=point,
                    lower_bound=lower,
                    upper_bound=upper,
                    model="ets_logit",
                    raw_response=f"ETS logit forecast: {logit_point:.3f} -> {point:.1f}%",
                )
            )

        return forecasts

    except Exception as e:
        warnings.warn(f"ETS failed: {e}")
        return []
