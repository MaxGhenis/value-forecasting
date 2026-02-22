"""
EMOS-style calibration for LLM forecasts.

Ensemble Model Output Statistics (EMOS) calibration:
1. Elicit quantile forecasts from LLM
2. Convert quantiles to Gaussian parameters
3. Compute CRPS on holdout data
4. Find spread multiplier that minimizes CRPS
5. Apply calibration to future forecasts
"""

from dataclasses import dataclass

import numpy as np
from scipy.optimize import minimize_scalar
from scipy.stats import norm


@dataclass
class QuantileForecast:
    """Raw quantile forecast from LLM."""

    q10: float
    q25: float
    q50: float
    q75: float
    q90: float


@dataclass
class CalibratedForecast:
    """Calibrated forecast with uncertainty."""

    median: float
    raw_std: float
    calibrated_std: float
    ci_lower: float  # 80% CI lower bound
    ci_upper: float  # 80% CI upper bound


def compute_crps(actual: float, mu: float, sig: float) -> float:
    """
    Compute Continuous Ranked Probability Score for a Gaussian forecast.

    CRPS is a proper scoring rule that rewards both accuracy and calibration.
    Lower is better.

    Args:
        actual: The actual observed value
        mu: Forecast mean
        sig: Forecast standard deviation

    Returns:
        CRPS value (non-negative)
    """
    if sig <= 0:
        sig = 0.01  # Prevent division by zero

    z = (actual - mu) / sig
    crps = sig * (z * (2 * norm.cdf(z) - 1) + 2 * norm.pdf(z) - 1 / np.sqrt(np.pi))
    return float(crps)


def quantiles_to_gaussian(quantiles: QuantileForecast) -> tuple[float, float]:
    """
    Convert quantile forecast to Gaussian parameters (mean, std).

    Uses median as mean and IQR-based std estimate.
    For a normal distribution: IQR ≈ 1.35 * std

    Args:
        quantiles: QuantileForecast with q10, q25, q50, q75, q90

    Returns:
        Tuple of (mean, std)
    """
    median = quantiles.q50
    iqr = quantiles.q75 - quantiles.q25

    if iqr > 0:
        std = iqr / 1.35
    else:
        # Fallback: use q90-q10 range (covers ~80% for normal)
        # For normal, q90-q10 ≈ 2.56 * std
        full_range = quantiles.q90 - quantiles.q10
        if full_range > 0:
            std = full_range / 2.56
        else:
            std = 5.0  # Default uncertainty

    return median, std


def calibrate_spread(
    forecasts: list[tuple[float, float]], actuals: list[float]
) -> tuple[float, float]:
    """
    Find spread multiplier that minimizes mean CRPS.

    Args:
        forecasts: List of (mean, std) tuples from LLM
        actuals: List of actual observed values

    Returns:
        Tuple of (optimal spread multiplier, calibrated mean CRPS)
    """
    if len(forecasts) != len(actuals):
        raise ValueError("forecasts and actuals must have same length")

    if len(forecasts) == 0:
        return 1.0, 0.0

    def objective(sigma_mult: float) -> float:
        total_crps = 0.0
        for (mu, sig), actual in zip(forecasts, actuals):
            total_crps += compute_crps(actual, mu, sig * sigma_mult)
        return total_crps / len(actuals)

    result = minimize_scalar(objective, bounds=(0.1, 10.0), method="bounded")
    return float(result.x), float(result.fun)


def apply_calibration(
    quantiles: QuantileForecast, spread_mult: float, ci_level: float = 0.80
) -> CalibratedForecast:
    """
    Apply calibration to a quantile forecast.

    Args:
        quantiles: Raw quantile forecast from LLM
        spread_mult: Spread multiplier from calibration
        ci_level: Confidence interval level (default 0.80 for 80% CI)

    Returns:
        CalibratedForecast with adjusted uncertainty
    """
    mu, raw_std = quantiles_to_gaussian(quantiles)
    calibrated_std = raw_std * spread_mult

    # z-score for CI level (e.g., 1.28 for 80% CI)
    z = norm.ppf((1 + ci_level) / 2)

    return CalibratedForecast(
        median=mu,
        raw_std=raw_std,
        calibrated_std=calibrated_std,
        ci_lower=mu - z * calibrated_std,
        ci_upper=mu + z * calibrated_std,
    )


def calculate_coverage(
    forecasts: list[CalibratedForecast], actuals: list[float]
) -> float:
    """
    Calculate coverage: fraction of actuals within confidence intervals.

    Args:
        forecasts: List of calibrated forecasts
        actuals: List of actual values

    Returns:
        Coverage fraction (0 to 1)
    """
    if len(forecasts) != len(actuals):
        raise ValueError("forecasts and actuals must have same length")

    if len(forecasts) == 0:
        return 0.0

    in_ci = sum(
        1 for f, a in zip(forecasts, actuals) if f.ci_lower <= a <= f.ci_upper
    )
    return in_ci / len(forecasts)


def mean_crps(
    forecasts: list[CalibratedForecast], actuals: list[float]
) -> float:
    """
    Calculate mean CRPS across all forecasts.

    Args:
        forecasts: List of calibrated forecasts
        actuals: List of actual values

    Returns:
        Mean CRPS value
    """
    if len(forecasts) != len(actuals):
        raise ValueError("forecasts and actuals must have same length")

    if len(forecasts) == 0:
        return 0.0

    total = sum(
        compute_crps(a, f.median, f.calibrated_std)
        for f, a in zip(forecasts, actuals)
    )
    return total / len(forecasts)
