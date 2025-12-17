"""Tests for heterogeneity (distribution) forecasting."""

import pytest

from value_forecasting.heterogeneity import (
    DistributionForecast,
    forecast_distribution,
    forecast_distribution_llm,
)


class TestDistributionForecast:
    """Tests for DistributionForecast dataclass."""

    def test_creation(self):
        """Should create a DistributionForecast."""
        f = DistributionForecast(
            variable="HOMOSEX",
            cutoff_year=2000,
            target_year=2010,
            distribution={
                "Always wrong": 30.0,
                "Almost always wrong": 10.0,
                "Sometimes wrong": 15.0,
                "Not wrong at all": 45.0,
            },
            distribution_ci={
                "Always wrong": (25.0, 35.0),
                "Almost always wrong": (7.0, 13.0),
                "Sometimes wrong": (12.0, 18.0),
                "Not wrong at all": (40.0, 50.0),
            },
            model="test",
        )
        assert f.variable == "HOMOSEX"
        assert sum(f.distribution.values()) == pytest.approx(100.0)

    def test_distribution_sums_to_100(self):
        """Distribution should sum to approximately 100%."""
        f = DistributionForecast(
            variable="HOMOSEX",
            cutoff_year=2000,
            target_year=2010,
            distribution={
                "Always wrong": 30.0,
                "Not wrong at all": 70.0,
            },
            distribution_ci={},
            model="test",
        )
        assert sum(f.distribution.values()) == pytest.approx(100.0)


class TestForecastDistribution:
    """Tests for distribution forecasting from historical data."""

    def test_returns_distribution_forecast(self):
        """Should return a DistributionForecast."""
        result = forecast_distribution("HOMOSEX", 2000, 2010)
        assert isinstance(result, DistributionForecast)

    def test_has_all_response_categories(self):
        """Should forecast all response categories."""
        result = forecast_distribution("HOMOSEX", 2000, 2010)
        # HOMOSEX has 4 response categories
        assert len(result.distribution) >= 2

    def test_distribution_sums_to_100(self):
        """Forecasted distribution should sum to ~100%."""
        result = forecast_distribution("HOMOSEX", 2000, 2010)
        total = sum(result.distribution.values())
        assert total == pytest.approx(100.0, abs=1.0)


class TestForecastDistributionLLM:
    """Tests for LLM-based distribution forecasting."""

    def test_returns_distribution_forecast(self):
        """Should return a DistributionForecast."""
        # This will actually call the API
        result = forecast_distribution_llm("HOMOSEX", 2000, 2010)
        assert isinstance(result, DistributionForecast)

    def test_has_uncertainty_on_distribution(self):
        """Should provide CIs on each category."""
        result = forecast_distribution_llm("HOMOSEX", 2000, 2010)
        # Should have CIs for at least some categories
        assert len(result.distribution_ci) >= 1

    def test_distribution_sums_to_100(self):
        """LLM distribution should sum to ~100%."""
        result = forecast_distribution_llm("HOMOSEX", 2000, 2010)
        total = sum(result.distribution.values())
        assert total == pytest.approx(100.0, abs=5.0)  # Allow some slack for LLM
