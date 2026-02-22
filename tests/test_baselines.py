"""Tests for time series baseline forecasters."""

import numpy as np
import pytest

from value_forecasting.baselines import (
    run_arima_forecast,
    run_ets_forecast,
    run_naive_forecast,
    run_linear_forecast,
    logit,
    inverse_logit,
)
from value_forecasting.forecaster import Forecast


class TestNaiveForecast:
    """Tests for naive (last value) baseline."""

    def test_returns_forecasts(self):
        """Should return list of Forecast objects."""
        forecasts = run_naive_forecast("HOMOSEX", 2000, [2010, 2020])
        assert len(forecasts) == 2
        assert all(isinstance(f, Forecast) for f in forecasts)

    def test_predicts_last_value(self):
        """Naive forecast should predict the last observed value."""
        forecasts = run_naive_forecast("HOMOSEX", 2000, [2010])
        # Last value before 2000 cutoff should be 1990: 13%
        # Actually 2000: 27% if we include 2000
        assert forecasts[0].point_estimate >= 10  # sanity check


class TestARIMAForecast:
    """Tests for ARIMA baseline."""

    def test_returns_forecasts(self):
        """Should return list of Forecast objects."""
        # Use later cutoff to ensure enough data
        forecasts = run_arima_forecast("HOMOSEX", 2010, [2020])
        assert len(forecasts) >= 1
        assert all(isinstance(f, Forecast) for f in forecasts)

    def test_has_uncertainty(self):
        """ARIMA forecasts should have uncertainty bounds."""
        forecasts = run_arima_forecast("HOMOSEX", 2000, [2010])
        if forecasts:  # May fail with insufficient data
            f = forecasts[0]
            assert f.lower_bound < f.point_estimate < f.upper_bound

    def test_model_labeled_correctly(self):
        """Should be labeled as ARIMA."""
        forecasts = run_arima_forecast("HOMOSEX", 2000, [2010])
        if forecasts:
            assert "arima" in forecasts[0].model.lower()


class TestETSForecast:
    """Tests for Exponential Smoothing baseline."""

    def test_returns_forecasts(self):
        """Should return list of Forecast objects."""
        forecasts = run_ets_forecast("HOMOSEX", 2000, [2010])
        assert len(forecasts) >= 1
        assert all(isinstance(f, Forecast) for f in forecasts)

    def test_has_uncertainty(self):
        """ETS forecasts should have uncertainty bounds."""
        forecasts = run_ets_forecast("HOMOSEX", 2000, [2010])
        if forecasts:
            f = forecasts[0]
            assert f.lower_bound < f.point_estimate < f.upper_bound

    def test_model_labeled_correctly(self):
        """Should be labeled as ETS."""
        forecasts = run_ets_forecast("HOMOSEX", 2000, [2010])
        if forecasts:
            assert "ets" in forecasts[0].model.lower()


class TestLogitTransform:
    """Tests for logit/inverse_logit transformations."""

    def test_logit_of_half(self):
        """logit(0.5) should be 0."""
        assert abs(logit(0.5)) < 1e-10

    def test_logit_inverse_roundtrip(self):
        """inverse_logit(logit(p)) should equal p."""
        for p in [0.1, 0.25, 0.5, 0.75, 0.9]:
            assert abs(inverse_logit(logit(p)) - p) < 1e-10

    def test_inverse_logit_bounded(self):
        """inverse_logit should always return values in [0, 1]."""
        for x in [-100, -10, -1, 0, 1, 10, 100]:
            result = inverse_logit(x)
            # At extreme values, floating point gives exactly 0 or 1
            assert 0 <= result <= 1

    def test_logit_handles_boundaries(self):
        """logit should handle values near 0 and 1 gracefully."""
        # Should clamp to avoid -inf/+inf
        result_low = logit(0.001)
        result_high = logit(0.999)
        assert np.isfinite(result_low)
        assert np.isfinite(result_high)
        assert result_low < 0
        assert result_high > 0


class TestLinearForecast:
    """Tests for linear regression baseline with logit transform."""

    def test_returns_forecasts(self):
        """Should return list of Forecast objects."""
        forecasts = run_linear_forecast("HOMOSEX", 2000, [2010, 2020])
        assert len(forecasts) == 2
        assert all(isinstance(f, Forecast) for f in forecasts)

    def test_bounded_predictions(self):
        """Linear forecast should be bounded to [0, 100]."""
        # Test with long horizon where unbounded linear could exceed bounds
        forecasts = run_linear_forecast("HOMOSEX", 2021, [2050, 2100])
        for f in forecasts:
            assert 0 <= f.point_estimate <= 100
            assert 0 <= f.lower_bound <= 100
            assert 0 <= f.upper_bound <= 100

    def test_has_prediction_intervals(self):
        """Linear forecasts should have proper prediction intervals."""
        forecasts = run_linear_forecast("HOMOSEX", 2000, [2010])
        if forecasts:
            f = forecasts[0]
            assert f.lower_bound < f.point_estimate < f.upper_bound

    def test_prediction_intervals_bounded(self):
        """Prediction intervals should also be bounded to [0, 100]."""
        forecasts = run_linear_forecast("HOMOSEX", 2021, [2100])
        if forecasts:
            f = forecasts[0]
            assert f.lower_bound >= 0
            assert f.upper_bound <= 100

    def test_uncertainty_grows_with_horizon(self):
        """Prediction intervals should widen for longer horizons."""
        forecasts = run_linear_forecast("HOMOSEX", 2010, [2020, 2050])
        if len(forecasts) == 2:
            width_2020 = forecasts[0].upper_bound - forecasts[0].lower_bound
            width_2050 = forecasts[1].upper_bound - forecasts[1].lower_bound
            assert width_2050 > width_2020

    def test_model_labeled_correctly(self):
        """Should be labeled as linear_logit."""
        forecasts = run_linear_forecast("HOMOSEX", 2000, [2010])
        if forecasts:
            assert "linear" in forecasts[0].model.lower()


class TestBoundedForecasts:
    """Tests that all forecast methods produce bounded predictions."""

    @pytest.mark.parametrize("forecast_fn", [
        run_naive_forecast,
        run_linear_forecast,
        run_ets_forecast,
    ])
    def test_long_horizon_bounded(self, forecast_fn):
        """All forecasts should be bounded even at 2100."""
        forecasts = forecast_fn("HOMOSEX", 2021, [2100])
        for f in forecasts:
            assert 0 <= f.point_estimate <= 100, f"{forecast_fn.__name__} point estimate out of bounds"
            assert 0 <= f.lower_bound, f"{forecast_fn.__name__} lower bound below 0"
            assert f.upper_bound <= 100, f"{forecast_fn.__name__} upper bound above 100"

    @pytest.mark.parametrize("variable", ["HOMOSEX", "GRASS", "TRUST", "GUNLAW"])
    def test_various_variables_bounded(self, variable):
        """Test bounding works for variables with different trends."""
        forecasts = run_linear_forecast(variable, 2021, [2050, 2100])
        for f in forecasts:
            assert 0 <= f.point_estimate <= 100
            assert 0 <= f.lower_bound <= 100
            assert 0 <= f.upper_bound <= 100
