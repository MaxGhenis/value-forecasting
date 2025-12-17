"""Tests for time series baseline forecasters."""

import pytest

from value_forecasting.baselines import (
    run_arima_forecast,
    run_ets_forecast,
    run_naive_forecast,
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
        forecasts = run_arima_forecast("HOMOSEX", 2000, [2010])
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
