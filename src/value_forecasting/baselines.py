"""Time series baseline forecasters."""

import warnings

import numpy as np

from value_forecasting.forecaster import Forecast
from value_forecasting.gss_variables import HISTORICAL_TRAJECTORIES


def run_naive_forecast(
    variable: str,
    cutoff_year: int,
    target_years: list[int],
) -> list[Forecast]:
    """
    Naive baseline: predict the last observed value.

    Uncertainty: historical standard deviation of changes.
    """
    trajectory = HISTORICAL_TRAJECTORIES.get(variable, {})
    pre_cutoff = {y: v for y, v in trajectory.items() if y <= cutoff_year}

    if not pre_cutoff:
        return []

    years = sorted(pre_cutoff.keys())
    last_value = pre_cutoff[years[-1]]

    # Estimate uncertainty from historical volatility
    if len(years) >= 2:
        changes = [
            pre_cutoff[years[i]] - pre_cutoff[years[i - 1]]
            for i in range(1, len(years))
        ]
        std = np.std(changes) if changes else 5.0
    else:
        std = 5.0

    forecasts = []
    for target_year in target_years:
        years_out = target_year - cutoff_year
        # Uncertainty grows with time
        uncertainty = std * np.sqrt(years_out / 10) * 1.645  # 90% CI

        forecasts.append(
            Forecast(
                variable=variable,
                cutoff_year=cutoff_year,
                target_year=target_year,
                point_estimate=last_value,
                lower_bound=max(0, last_value - uncertainty),
                upper_bound=min(100, last_value + uncertainty),
                model="naive",
                raw_response=f"Last value: {last_value}",
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
    ARIMA baseline forecast.

    Uses statsmodels ARIMA with specified order.
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

    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            model = ARIMA(values, order=order)
            fit = model.fit()

        forecasts = []
        for target_year in target_years:
            steps_ahead = len([y for y in target_years if y <= target_year])

            # Get forecast with confidence interval
            forecast_result = fit.get_forecast(steps=max(target_years) - years[-1])
            pred = forecast_result.predicted_mean
            conf_int = forecast_result.conf_int(alpha=0.10)  # 90% CI

            idx = target_year - years[-1] - 1
            if idx < 0 or idx >= len(pred):
                continue

            point = float(pred.iloc[idx]) if hasattr(pred, 'iloc') else float(pred[idx])
            lower = float(conf_int.iloc[idx, 0]) if hasattr(conf_int, 'iloc') else float(conf_int[idx, 0])
            upper = float(conf_int.iloc[idx, 1]) if hasattr(conf_int, 'iloc') else float(conf_int[idx, 1])

            forecasts.append(
                Forecast(
                    variable=variable,
                    cutoff_year=cutoff_year,
                    target_year=target_year,
                    point_estimate=max(0, min(100, point)),
                    lower_bound=max(0, lower),
                    upper_bound=min(100, upper),
                    model=f"arima{order}",
                    raw_response=str(fit.summary()),
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
    Exponential Smoothing (ETS) baseline forecast.

    Uses Holt's linear trend method.
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

    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            # Holt's linear trend
            model = ExponentialSmoothing(
                values,
                trend="add",
                seasonal=None,
            )
            fit = model.fit()

        forecasts = []
        max_steps = max(target_years) - years[-1]
        predictions = fit.forecast(max_steps)

        # Estimate prediction intervals using residual variance
        residuals = fit.resid
        sigma = np.std(residuals) if len(residuals) > 1 else 5.0

        for target_year in target_years:
            idx = target_year - years[-1] - 1
            if idx < 0 or idx >= len(predictions):
                continue

            point = float(predictions.iloc[idx]) if hasattr(predictions, 'iloc') else float(predictions[idx])

            # Uncertainty grows with horizon
            steps = idx + 1
            uncertainty = sigma * np.sqrt(steps) * 1.645  # 90% CI

            forecasts.append(
                Forecast(
                    variable=variable,
                    cutoff_year=cutoff_year,
                    target_year=target_year,
                    point_estimate=max(0, min(100, point)),
                    lower_bound=max(0, point - uncertainty),
                    upper_bound=min(100, point + uncertainty),
                    model="ets_holt",
                    raw_response=f"ETS forecast: {point:.1f}",
                )
            )

        return forecasts

    except Exception as e:
        warnings.warn(f"ETS failed: {e}")
        return []
