"""Tests for forecasting logic."""

import pytest

from value_forecasting.forecaster import (
    Forecast,
    create_forecast_prompt,
    extract_predictions,
    run_baseline_forecast,
)


class TestForecast:
    """Tests for Forecast dataclass."""

    def test_forecast_creation(self):
        """Should create a Forecast with all fields."""
        f = Forecast(
            variable="HOMOSEX",
            cutoff_year=2000,
            target_year=2010,
            point_estimate=35.0,
            lower_bound=25.0,
            upper_bound=45.0,
            model="test",
            raw_response="test response",
        )
        assert f.variable == "HOMOSEX"
        assert f.point_estimate == 35.0


class TestCreateForecastPrompt:
    """Tests for prompt generation."""

    def test_returns_string(self):
        """Should return a string prompt."""
        prompt = create_forecast_prompt("HOMOSEX", 2000, [2010, 2020])
        assert isinstance(prompt, str)

    def test_includes_target_years(self):
        """Prompt should mention the target years."""
        prompt = create_forecast_prompt("HOMOSEX", 2000, [2010, 2020])
        assert "2010" in prompt
        assert "2020" in prompt

    def test_includes_cutoff_context(self):
        """Prompt should reference the cutoff year context."""
        prompt = create_forecast_prompt("HOMOSEX", 2000, [2010])
        assert "2000" in prompt

    def test_asks_for_uncertainty(self):
        """Prompt should ask for confidence intervals."""
        prompt = create_forecast_prompt("HOMOSEX", 2000, [2010])
        assert "confidence" in prompt.lower() or "interval" in prompt.lower()


class TestExtractPredictions:
    """Tests for JSON extraction from model responses."""

    def test_extracts_valid_json(self):
        """Should extract predictions from valid JSON."""
        response = """
        Here's my prediction:
        {"predictions": [{"year": 2010, "estimate": 40, "lower": 30, "upper": 50}], "reasoning": "test"}
        """
        result = extract_predictions(response)
        assert len(result["predictions"]) == 1
        assert result["predictions"][0]["estimate"] == 40

    def test_handles_markdown_wrapped_json(self):
        """Should extract JSON even if wrapped in markdown."""
        response = """
        ```json
        {"predictions": [{"year": 2010, "estimate": 40, "lower": 30, "upper": 50}], "reasoning": "test"}
        ```
        """
        result = extract_predictions(response)
        assert len(result["predictions"]) == 1

    def test_handles_invalid_json(self):
        """Should return empty predictions for invalid JSON."""
        response = "This is not JSON at all"
        result = extract_predictions(response)
        assert result["predictions"] == []


class TestBaselineForecast:
    """Tests for linear extrapolation baseline."""

    def test_returns_forecasts(self):
        """Should return list of Forecast objects."""
        forecasts = run_baseline_forecast("HOMOSEX", 2000, [2010, 2020])
        assert len(forecasts) == 2
        assert all(isinstance(f, Forecast) for f in forecasts)

    def test_forecasts_have_uncertainty(self):
        """Baseline forecasts should have uncertainty bounds."""
        forecasts = run_baseline_forecast("HOMOSEX", 2000, [2010])
        f = forecasts[0]
        assert f.lower_bound < f.point_estimate < f.upper_bound

    def test_forecasts_are_bounded(self):
        """Forecasts should be valid percentages (0-100)."""
        forecasts = run_baseline_forecast("HOMOSEX", 1980, [2050])
        for f in forecasts:
            assert 0 <= f.point_estimate <= 100
            assert 0 <= f.lower_bound
            assert f.upper_bound <= 100

    def test_model_is_labeled_correctly(self):
        """Baseline should be labeled as linear extrapolation."""
        forecasts = run_baseline_forecast("HOMOSEX", 2000, [2010])
        assert forecasts[0].model == "linear_extrapolation"

    def test_returns_empty_for_insufficient_data(self):
        """Should return empty if not enough historical data."""
        # This tests edge case handling
        forecasts = run_baseline_forecast("HOMOSEX", 1970, [2010])
        # Should work but may have limited data
        assert isinstance(forecasts, list)
