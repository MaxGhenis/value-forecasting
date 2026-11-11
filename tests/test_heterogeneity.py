"""Tests for heterogeneity (distribution) forecasting."""

import json
import os
from types import SimpleNamespace

import pytest

from value_forecasting import heterogeneity
from value_forecasting.gss_variables import GSS_VARIABLES
from value_forecasting.heterogeneity import (
    DistributionForecast,
    forecast_distribution,
    forecast_distribution_llm,
)

LIVE_API = os.environ.get("VALUE_FORECASTING_LIVE_API_TESTS") == "1"


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


class _FakeMessages:
    """Stands in for ``Anthropic().messages`` and records each request."""

    def __init__(self, text):
        self.text = text
        self.calls = []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        return SimpleNamespace(content=[SimpleNamespace(text=self.text)])


@pytest.fixture
def fake_reply(monkeypatch):
    """Route forecast_distribution_llm's client to a fake that returns ``text``."""

    def install(text):
        messages = _FakeMessages(text)
        client = SimpleNamespace(messages=messages)
        monkeypatch.setattr(heterogeneity, "Anthropic", lambda: client)
        return messages

    return install


class TestForecastDistributionLLMParsing:
    """forecast_distribution_llm against a fake Anthropic client (no network)."""

    def test_parses_estimates_and_intervals(self, fake_reply):
        reply = json.dumps(
            {
                "predictions": {
                    "Always wrong": {"estimate": 40, "lower": 35, "upper": 45},
                    "Not wrong at all": {"estimate": 60, "lower": 55, "upper": 65},
                },
                "reasoning": "trend",
            }
        )
        fake_reply("Forecast follows.\n" + reply)

        result = forecast_distribution_llm("HOMOSEX", 2000, 2010, model="fake-model")

        assert result.distribution == {"Always wrong": 40, "Not wrong at all": 60}
        assert result.distribution_ci == {
            "Always wrong": (35, 45),
            "Not wrong at all": (55, 65),
        }
        assert result.model == "fake-model"
        assert result.raw_response.startswith("Forecast follows.")

    def test_prompt_names_years_and_every_response_option(self, fake_reply):
        messages = fake_reply(json.dumps({"predictions": {}}))

        forecast_distribution_llm("HOMOSEX", 2000, 2010, model="fake-model")

        (call,) = messages.calls
        assert call["model"] == "fake-model"
        prompt = call["messages"][0]["content"]
        assert "up to 2000" in prompt
        assert "distribution in 2010" in prompt
        for option in GSS_VARIABLES["HOMOSEX"]["responses"].values():
            assert option in prompt

    def test_missing_interval_defaults_to_full_range(self, fake_reply):
        fake_reply(json.dumps({"predictions": {"Always wrong": {"estimate": 40}}}))

        result = forecast_distribution_llm("HOMOSEX", 2000, 2010)

        assert result.distribution == {"Always wrong": 40}
        assert result.distribution_ci == {"Always wrong": (0, 100)}

    def test_skips_predictions_that_are_not_objects(self, fake_reply):
        predictions = {"Always wrong": 40, "Not wrong at all": {"estimate": 60}}
        fake_reply(json.dumps({"predictions": predictions}))

        result = forecast_distribution_llm("HOMOSEX", 2000, 2010)

        assert result.distribution == {"Not wrong at all": 60}

    @pytest.mark.parametrize("reply", ["no json here", "{not valid json}"])
    def test_unparseable_reply_returns_empty_forecast(self, fake_reply, reply):
        fake_reply(reply)

        result = forecast_distribution_llm("HOMOSEX", 2000, 2010)

        assert result.distribution == {}
        assert result.distribution_ci == {}
        assert result.raw_response == reply


@pytest.mark.skipif(
    not LIVE_API,
    reason="calls the Anthropic API; set VALUE_FORECASTING_LIVE_API_TESTS=1 to run",
)
class TestForecastDistributionLLM:
    """Tests for LLM-based distribution forecasting."""

    def test_returns_distribution_forecast(self):
        """Should return a DistributionForecast."""
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
