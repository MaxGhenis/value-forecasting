"""Tests for evaluation metrics."""

import pytest

from value_forecasting.evaluation import (
    calculate_calibration,
    calculate_mae,
    calculate_coverage,
    ForecastResult,
)


class TestForecastResult:
    """Tests for ForecastResult dataclass."""

    def test_creation(self):
        """Should create a ForecastResult."""
        result = ForecastResult(
            variable="HOMOSEX",
            cutoff_year=2000,
            target_year=2010,
            predicted=35.0,
            actual=41.0,
            lower=25.0,
            upper=45.0,
            model="test",
        )
        assert result.error == pytest.approx(-6.0)  # predicted - actual
        assert result.in_interval is True


class TestCalculateMAE:
    """Tests for Mean Absolute Error calculation."""

    def test_perfect_predictions(self):
        """MAE should be 0 for perfect predictions."""
        results = [
            ForecastResult("X", 2000, 2010, 50.0, 50.0, 40.0, 60.0, "test"),
            ForecastResult("X", 2000, 2020, 60.0, 60.0, 50.0, 70.0, "test"),
        ]
        assert calculate_mae(results) == 0.0

    def test_known_mae(self):
        """MAE should match hand calculation."""
        results = [
            ForecastResult("X", 2000, 2010, 50.0, 40.0, 30.0, 70.0, "test"),  # error = 10
            ForecastResult("X", 2000, 2020, 60.0, 70.0, 50.0, 70.0, "test"),  # error = 10
        ]
        assert calculate_mae(results) == 10.0

    def test_empty_list(self):
        """Should handle empty list gracefully."""
        assert calculate_mae([]) == 0.0


class TestCalculateCoverage:
    """Tests for confidence interval coverage calculation."""

    def test_perfect_coverage(self):
        """Coverage should be 1.0 if all actuals in intervals."""
        results = [
            ForecastResult("X", 2000, 2010, 50.0, 50.0, 40.0, 60.0, "test"),
            ForecastResult("X", 2000, 2020, 60.0, 55.0, 50.0, 70.0, "test"),
        ]
        assert calculate_coverage(results) == 1.0

    def test_no_coverage(self):
        """Coverage should be 0.0 if no actuals in intervals."""
        results = [
            ForecastResult("X", 2000, 2010, 50.0, 10.0, 40.0, 60.0, "test"),
            ForecastResult("X", 2000, 2020, 60.0, 90.0, 50.0, 70.0, "test"),
        ]
        assert calculate_coverage(results) == 0.0

    def test_partial_coverage(self):
        """Coverage should be fraction of predictions covering actual."""
        results = [
            ForecastResult("X", 2000, 2010, 50.0, 50.0, 40.0, 60.0, "test"),  # in
            ForecastResult("X", 2000, 2020, 60.0, 90.0, 50.0, 70.0, "test"),  # out
        ]
        assert calculate_coverage(results) == 0.5


class TestCalculateCalibration:
    """Tests for calibration score."""

    def test_calibration_for_90_percent_intervals(self):
        """For 90% CIs, good calibration means ~90% coverage."""
        # Create 10 results, 9 in interval, 1 out
        results = [
            ForecastResult("X", 2000, y, 50.0, 50.0, 40.0, 60.0, "test")
            for y in range(2001, 2010)
        ] + [
            ForecastResult("X", 2000, 2010, 50.0, 10.0, 40.0, 60.0, "test")  # out
        ]
        calibration = calculate_calibration(results, target_coverage=0.90)
        # 90% coverage vs 90% target = well calibrated
        assert calibration == pytest.approx(0.0, abs=0.01)

    def test_overconfident_model(self):
        """Overconfident model should have positive calibration error."""
        # All predictions miss - 0% coverage for 90% CI
        results = [
            ForecastResult("X", 2000, 2010, 50.0, 10.0, 40.0, 60.0, "test"),
            ForecastResult("X", 2000, 2020, 60.0, 90.0, 50.0, 70.0, "test"),
        ]
        calibration = calculate_calibration(results, target_coverage=0.90)
        # 0% coverage vs 90% target = very overconfident
        assert calibration > 0.5
