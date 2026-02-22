"""Tests for multi-model forecasting support."""

import pytest
from unittest.mock import Mock, patch, MagicMock

from value_forecasting.models import (
    ModelConfig,
    SUPPORTED_MODELS,
    get_model_config,
    create_client,
    elicit_quantiles,
    parse_quantiles_response,
)
from value_forecasting.calibration import QuantileForecast


class TestModelConfig:
    """Tests for model configuration."""

    def test_supported_models_exist(self):
        """Should have configurations for major frontier models."""
        assert "gpt-4o" in SUPPORTED_MODELS
        assert "gpt-4.5-preview" in SUPPORTED_MODELS  # GPT-5 preview
        assert "claude-opus-4-20250514" in SUPPORTED_MODELS
        assert "claude-sonnet-4-20250514" in SUPPORTED_MODELS

    def test_model_config_has_required_fields(self):
        """ModelConfig should have provider, model_id, and costs."""
        config = get_model_config("gpt-4o")

        assert config.provider in ["openai", "anthropic"]
        assert config.model_id is not None
        assert config.input_cost_per_million >= 0
        assert config.output_cost_per_million >= 0

    def test_unknown_model_raises(self):
        """Should raise for unknown model names."""
        with pytest.raises(ValueError, match="Unknown model"):
            get_model_config("unknown-model-xyz")


class TestClientCreation:
    """Tests for API client creation."""

    @patch("value_forecasting.models.OpenAI")
    def test_creates_openai_client(self, mock_openai):
        """Should create OpenAI client for OpenAI models."""
        config = get_model_config("gpt-4o")
        client = create_client(config)

        mock_openai.assert_called_once()

    @patch("value_forecasting.models.Anthropic")
    def test_creates_anthropic_client(self, mock_anthropic):
        """Should create Anthropic client for Claude models."""
        config = get_model_config("claude-opus-4-20250514")
        client = create_client(config)

        mock_anthropic.assert_called_once()


class TestParseQuantiles:
    """Tests for parsing quantile responses from LLMs."""

    def test_parse_simple_numbers(self):
        """Should parse 5 numbers on separate lines."""
        response = """40
45
50
55
60"""
        quantiles = parse_quantiles_response(response)

        assert quantiles.q10 == 40
        assert quantiles.q25 == 45
        assert quantiles.q50 == 50
        assert quantiles.q75 == 55
        assert quantiles.q90 == 60

    def test_parse_with_percent_signs(self):
        """Should extract numbers even with percent signs."""
        response = """42%
48%
55%
62%
68%"""
        quantiles = parse_quantiles_response(response)

        assert quantiles.q10 == 42
        assert quantiles.q25 == 48
        assert quantiles.q50 == 55
        assert quantiles.q75 == 62
        assert quantiles.q90 == 68

    def test_parse_ensures_monotonicity(self):
        """Should sort values to ensure monotonicity."""
        response = """60
45
50
55
40"""
        quantiles = parse_quantiles_response(response)

        # Should be sorted
        assert quantiles.q10 <= quantiles.q25 <= quantiles.q50
        assert quantiles.q50 <= quantiles.q75 <= quantiles.q90

    def test_parse_with_decimals(self):
        """Should handle decimal values."""
        response = """42.5
48.3
55.0
62.7
68.9"""
        quantiles = parse_quantiles_response(response)

        assert quantiles.q10 == 42.5
        assert quantiles.q90 == 68.9

    def test_parse_insufficient_numbers_raises(self):
        """Should raise if fewer than 5 numbers found."""
        response = "50\n55\n60"

        with pytest.raises(ValueError, match="Could not parse"):
            parse_quantiles_response(response)


class TestElicitQuantiles:
    """Tests for quantile elicitation from LLMs."""

    @patch("value_forecasting.models.create_client")
    def test_elicit_openai_format(self, mock_create_client):
        """Should use correct format for OpenAI models."""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "40\n45\n50\n55\n60"
        mock_response.usage.prompt_tokens = 100
        mock_response.usage.completion_tokens = 20
        mock_client.chat.completions.create.return_value = mock_response
        mock_create_client.return_value = mock_client

        config = get_model_config("gpt-4o")
        quantiles, cost = elicit_quantiles(
            config=config,
            client=mock_client,
            variable="HOMOSEX",
            description="Same-sex relations not wrong",
            history="2000: 29%\n2010: 42%\n2021: 62%",
            target_year=2024,
        )

        assert quantiles is not None
        assert quantiles.q50 == 50
        assert cost >= 0

    @patch("value_forecasting.models.create_client")
    def test_elicit_anthropic_format(self, mock_create_client):
        """Should use correct format for Anthropic models."""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.content = [MagicMock()]
        mock_response.content[0].text = "40\n45\n50\n55\n60"
        mock_response.usage.input_tokens = 100
        mock_response.usage.output_tokens = 20
        mock_client.messages.create.return_value = mock_response
        mock_create_client.return_value = mock_client

        config = get_model_config("claude-opus-4-20250514")
        quantiles, cost = elicit_quantiles(
            config=config,
            client=mock_client,
            variable="HOMOSEX",
            description="Same-sex relations not wrong",
            history="2000: 29%\n2010: 42%\n2021: 62%",
            target_year=2024,
        )

        assert quantiles is not None
        assert quantiles.q50 == 50


class TestCostTracking:
    """Tests for API cost tracking."""

    def test_openai_cost_calculation(self):
        """Should correctly calculate OpenAI costs."""
        from value_forecasting.models import calculate_cost

        config = get_model_config("gpt-4o")
        cost = calculate_cost(config, input_tokens=1000, output_tokens=500)

        # gpt-4o: $2.50/M input, $10.00/M output
        expected = (1000 * 2.50 / 1_000_000) + (500 * 10.00 / 1_000_000)
        assert abs(cost - expected) < 0.0001

    def test_anthropic_cost_calculation(self):
        """Should correctly calculate Anthropic costs."""
        from value_forecasting.models import calculate_cost

        config = get_model_config("claude-opus-4-20250514")
        cost = calculate_cost(config, input_tokens=1000, output_tokens=500)

        # opus: $15/M input, $75/M output
        expected = (1000 * 15.0 / 1_000_000) + (500 * 75.0 / 1_000_000)
        assert abs(cost - expected) < 0.0001


class TestModelComparison:
    """Tests for comparing multiple models."""

    def test_model_comparison_structure(self):
        """Model comparison should return results for each model."""
        from value_forecasting.models import ModelComparisonResult

        result = ModelComparisonResult(
            model="gpt-4o",
            raw_crps=3.15,
            calibrated_crps=3.12,
            spread_multiplier=1.21,
            mae=5.2,
            coverage_80=0.75,
            total_cost=0.09,
        )

        assert result.model == "gpt-4o"
        assert result.raw_crps > 0
        assert result.spread_multiplier > 0
