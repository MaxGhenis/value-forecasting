"""Evaluation metrics for value forecasting."""

from dataclasses import dataclass, field


@dataclass
class ForecastResult:
    """A forecast with its actual outcome for evaluation."""

    variable: str
    cutoff_year: int
    target_year: int
    predicted: float
    actual: float
    lower: float  # 90% CI lower bound
    upper: float  # 90% CI upper bound
    model: str

    @property
    def error(self) -> float:
        """Signed error (predicted - actual)."""
        return self.predicted - self.actual

    @property
    def absolute_error(self) -> float:
        """Absolute error."""
        return abs(self.error)

    @property
    def in_interval(self) -> bool:
        """Whether actual value falls within the confidence interval."""
        return self.lower <= self.actual <= self.upper


def calculate_mae(results: list[ForecastResult]) -> float:
    """Calculate Mean Absolute Error across forecasts."""
    if not results:
        return 0.0
    return sum(r.absolute_error for r in results) / len(results)


def calculate_coverage(results: list[ForecastResult]) -> float:
    """Calculate fraction of actuals falling within confidence intervals."""
    if not results:
        return 0.0
    return sum(1 for r in results if r.in_interval) / len(results)


def calculate_calibration(
    results: list[ForecastResult],
    target_coverage: float = 0.90,
) -> float:
    """
    Calculate calibration error.

    For 90% confidence intervals, well-calibrated forecasts should have
    ~90% of actual values fall within the intervals.

    Returns absolute difference between actual coverage and target coverage.
    Lower is better (0 = perfectly calibrated).
    """
    if not results:
        return 0.0
    actual_coverage = calculate_coverage(results)
    return abs(target_coverage - actual_coverage)


def calculate_rmse(results: list[ForecastResult]) -> float:
    """Calculate Root Mean Square Error across forecasts."""
    if not results:
        return 0.0
    mse = sum(r.error**2 for r in results) / len(results)
    return mse**0.5


def calculate_bias(results: list[ForecastResult]) -> float:
    """Calculate mean signed error (positive = overestimates liberal response)."""
    if not results:
        return 0.0
    return sum(r.error for r in results) / len(results)


def evaluate_model(results: list[ForecastResult]) -> dict:
    """Calculate all evaluation metrics for a set of forecasts."""
    return {
        "n_forecasts": len(results),
        "mae": calculate_mae(results),
        "rmse": calculate_rmse(results),
        "bias": calculate_bias(results),
        "coverage_90": calculate_coverage(results),
        "calibration_error": calculate_calibration(results),
    }
