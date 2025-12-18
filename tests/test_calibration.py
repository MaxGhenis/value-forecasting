"""Tests for EMOS calibration module."""

import numpy as np
import pytest

from value_forecasting.calibration import (
    compute_crps,
    quantiles_to_gaussian,
    calibrate_spread,
    apply_calibration,
    QuantileForecast,
    CalibratedForecast,
)


class TestCRPS:
    """Tests for CRPS computation."""

    def test_crps_perfect_forecast(self):
        """CRPS should be 0 when forecast mean equals actual."""
        # With very small std, CRPS approaches 0 when mu = actual
        crps = compute_crps(actual=50.0, mu=50.0, sig=0.1)
        assert crps < 0.1

    def test_crps_increases_with_error(self):
        """CRPS should increase as forecast deviates from actual."""
        crps_close = compute_crps(actual=50.0, mu=52.0, sig=5.0)
        crps_far = compute_crps(actual=50.0, mu=60.0, sig=5.0)
        assert crps_far > crps_close

    def test_crps_decreases_with_uncertainty(self):
        """For biased forecasts, wider uncertainty can improve CRPS."""
        # If we're wrong, being more uncertain is better
        crps_narrow = compute_crps(actual=50.0, mu=60.0, sig=2.0)
        crps_wide = compute_crps(actual=50.0, mu=60.0, sig=10.0)
        assert crps_wide < crps_narrow

    def test_crps_non_negative(self):
        """CRPS should always be non-negative."""
        for _ in range(100):
            actual = np.random.uniform(0, 100)
            mu = np.random.uniform(0, 100)
            sig = np.random.uniform(0.1, 20)
            crps = compute_crps(actual, mu, sig)
            assert crps >= 0


class TestQuantilesToGaussian:
    """Tests for converting quantile forecasts to Gaussian parameters."""

    def test_median_becomes_mean(self):
        """The median quantile should become the Gaussian mean."""
        quantiles = QuantileForecast(q10=40, q25=45, q50=50, q75=55, q90=60)
        mu, sig = quantiles_to_gaussian(quantiles)
        assert mu == 50

    def test_iqr_determines_std(self):
        """IQR should determine standard deviation (IQR ≈ 1.35*std for normal)."""
        quantiles = QuantileForecast(q10=40, q25=45, q50=50, q75=55, q90=60)
        mu, sig = quantiles_to_gaussian(quantiles)
        expected_std = (55 - 45) / 1.35
        assert abs(sig - expected_std) < 0.01

    def test_zero_iqr_fallback(self):
        """Should have fallback std when IQR is 0."""
        quantiles = QuantileForecast(q10=50, q25=50, q50=50, q75=50, q90=50)
        mu, sig = quantiles_to_gaussian(quantiles)
        assert sig > 0  # Should have some default uncertainty


class TestCalibrateSpread:
    """Tests for finding optimal spread multiplier."""

    def test_calibration_finds_improvement(self):
        """Calibration should find multiplier that improves (or maintains) CRPS."""
        # Forecasts that are overconfident (too narrow)
        forecasts = [
            (50.0, 2.0),  # Actually ~48
            (60.0, 2.0),  # Actually ~58
            (70.0, 2.0),  # Actually ~67
        ]
        actuals = [48.0, 58.0, 67.0]

        spread_mult, calibrated_crps = calibrate_spread(forecasts, actuals)

        # Original CRPS with narrow uncertainty
        original_crps = np.mean([
            compute_crps(a, mu, sig)
            for (mu, sig), a in zip(forecasts, actuals)
        ])

        assert calibrated_crps <= original_crps

    def test_calibration_multiplier_bounds(self):
        """Spread multiplier should be within reasonable bounds."""
        forecasts = [(50.0, 5.0), (60.0, 5.0), (70.0, 5.0)]
        actuals = [48.0, 58.0, 72.0]

        spread_mult, _ = calibrate_spread(forecasts, actuals)

        assert 0.1 <= spread_mult <= 10.0

    def test_well_calibrated_multiplier_near_one(self):
        """Well-calibrated forecasts should have multiplier near 1."""
        # Generate "well-calibrated" forecasts
        np.random.seed(42)
        forecasts = []
        actuals = []
        for _ in range(20):
            mu = np.random.uniform(30, 70)
            sig = 5.0
            actual = np.random.normal(mu, sig)
            forecasts.append((mu, sig))
            actuals.append(actual)

        spread_mult, _ = calibrate_spread(forecasts, actuals)

        # Should be close to 1.0 for well-calibrated forecasts
        assert 0.7 <= spread_mult <= 1.5


class TestApplyCalibration:
    """Tests for applying calibration to forecasts."""

    def test_apply_calibration_widens_ci(self):
        """Applying calibration with mult > 1 should widen confidence intervals."""
        quantiles = QuantileForecast(q10=40, q25=45, q50=50, q75=55, q90=60)
        spread_mult = 1.5

        calibrated = apply_calibration(quantiles, spread_mult)

        # CI should be wider
        original_ci_width = 60 - 40  # q90 - q10
        calibrated_ci_width = calibrated.ci_upper - calibrated.ci_lower
        assert calibrated_ci_width > original_ci_width

    def test_apply_calibration_preserves_median(self):
        """Calibration should preserve the median estimate."""
        quantiles = QuantileForecast(q10=40, q25=45, q50=50, q75=55, q90=60)
        spread_mult = 1.5

        calibrated = apply_calibration(quantiles, spread_mult)

        assert calibrated.median == 50

    def test_calibrated_forecast_dataclass(self):
        """CalibratedForecast should have all required fields."""
        quantiles = QuantileForecast(q10=40, q25=45, q50=50, q75=55, q90=60)
        calibrated = apply_calibration(quantiles, spread_mult=1.21)

        assert hasattr(calibrated, 'median')
        assert hasattr(calibrated, 'raw_std')
        assert hasattr(calibrated, 'calibrated_std')
        assert hasattr(calibrated, 'ci_lower')
        assert hasattr(calibrated, 'ci_upper')


class TestCoverageMetrics:
    """Tests for coverage calculation."""

    def test_coverage_80_percent(self):
        """80% CI should contain ~80% of actuals for well-calibrated forecasts."""
        from value_forecasting.calibration import calculate_coverage

        # Generate well-calibrated forecasts
        np.random.seed(123)
        forecasts = []
        actuals = []
        for _ in range(100):
            mu = np.random.uniform(30, 70)
            sig = 5.0
            actual = np.random.normal(mu, sig)
            forecasts.append(CalibratedForecast(
                median=mu,
                raw_std=sig,
                calibrated_std=sig,
                ci_lower=mu - 1.28 * sig,  # 80% CI
                ci_upper=mu + 1.28 * sig,
            ))
            actuals.append(actual)

        coverage = calculate_coverage(forecasts, actuals)

        # Should be close to 80% (allow some sampling variance)
        assert 0.70 <= coverage <= 0.90


class TestIntegration:
    """Integration tests for full calibration workflow."""

    def test_full_calibration_workflow(self):
        """Test complete calibration from quantiles to calibrated forecast."""
        # Simulate LLM quantile outputs
        raw_quantiles = [
            QuantileForecast(q10=58, q25=60, q50=63, q75=66, q90=68),
            QuantileForecast(q10=62, q25=66, q50=70, q75=74, q90=78),
            QuantileForecast(q10=60, q25=63, q50=66, q75=69, q90=72),
        ]
        actuals = [54.7, 68.5, 65.2]

        # Convert to Gaussian
        forecasts = [quantiles_to_gaussian(q) for q in raw_quantiles]

        # Calibrate
        spread_mult, _ = calibrate_spread(forecasts, actuals)

        # Apply calibration
        calibrated = [apply_calibration(q, spread_mult) for q in raw_quantiles]

        # Check that calibrated forecasts have wider CIs
        for raw, cal in zip(raw_quantiles, calibrated):
            raw_width = raw.q90 - raw.q10
            cal_width = cal.ci_upper - cal.ci_lower
            if spread_mult > 1:
                assert cal_width > raw_width
