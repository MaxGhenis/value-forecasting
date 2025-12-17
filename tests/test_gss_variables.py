"""Tests for GSS variable definitions and historical data."""

import pytest

from value_forecasting.gss_variables import (
    GSS_VARIABLES,
    HISTORICAL_TRAJECTORIES,
    get_historical_context,
)


class TestGSSVariables:
    """Tests for GSS variable definitions."""

    def test_gss_variables_has_required_keys(self):
        """Each variable should have required metadata."""
        required_keys = {"question", "responses", "liberal_response", "first_year", "description"}
        for var_name, var_info in GSS_VARIABLES.items():
            assert required_keys.issubset(var_info.keys()), f"{var_name} missing keys"

    def test_homosex_variable_exists(self):
        """HOMOSEX is a key test variable."""
        assert "HOMOSEX" in GSS_VARIABLES
        assert GSS_VARIABLES["HOMOSEX"]["first_year"] == 1973

    def test_grass_variable_exists(self):
        """GRASS (marijuana) is a key test variable."""
        assert "GRASS" in GSS_VARIABLES
        assert GSS_VARIABLES["GRASS"]["first_year"] == 1973

    def test_liberal_response_in_valid_range(self):
        """Liberal response should be a valid response code."""
        for var_name, var_info in GSS_VARIABLES.items():
            assert var_info["liberal_response"] in var_info["responses"], (
                f"{var_name} liberal_response not in responses"
            )


class TestHistoricalTrajectories:
    """Tests for historical trajectory data."""

    def test_trajectories_have_multiple_years(self):
        """Each trajectory should have multiple data points."""
        for var_name, trajectory in HISTORICAL_TRAJECTORIES.items():
            assert len(trajectory) >= 3, f"{var_name} needs more data points"

    def test_homosex_shows_liberalization(self):
        """HOMOSEX should show increasing liberal response over time."""
        trajectory = HISTORICAL_TRAJECTORIES["HOMOSEX"]
        years = sorted(trajectory.keys())
        # Overall trend should be increasing
        assert trajectory[years[-1]] > trajectory[years[0]]

    def test_grass_shows_liberalization(self):
        """GRASS should show increasing support for legalization."""
        trajectory = HISTORICAL_TRAJECTORIES["GRASS"]
        years = sorted(trajectory.keys())
        assert trajectory[years[-1]] > trajectory[years[0]]

    def test_values_are_percentages(self):
        """All values should be valid percentages (0-100)."""
        for var_name, trajectory in HISTORICAL_TRAJECTORIES.items():
            for year, value in trajectory.items():
                assert 0 <= value <= 100, f"{var_name} {year}: {value} not a valid %"


class TestGetHistoricalContext:
    """Tests for context generation function."""

    def test_returns_string(self):
        """Should return a string."""
        context = get_historical_context("HOMOSEX", 2000)
        assert isinstance(context, str)

    def test_includes_question(self):
        """Context should include the survey question."""
        context = get_historical_context("HOMOSEX", 2000)
        assert "sexual relations" in context.lower()

    def test_filters_by_cutoff_year(self):
        """Context should only include data up to cutoff year."""
        context = get_historical_context("HOMOSEX", 2000)
        # Should include 1990 but not 2010
        assert "1990:" in context or "1990 " in context
        assert "2010" not in context

    def test_raises_for_unknown_variable(self):
        """Should raise ValueError for unknown variables."""
        with pytest.raises(ValueError):
            get_historical_context("NONEXISTENT", 2000)

    def test_different_cutoffs_produce_different_context(self):
        """Different cutoff years should produce different context."""
        context_1990 = get_historical_context("HOMOSEX", 1990)
        context_2010 = get_historical_context("HOMOSEX", 2010)
        # 2010 context should be longer (more data points)
        assert len(context_2010) > len(context_1990)
