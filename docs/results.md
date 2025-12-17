---
title: Results
---

# Results

## Summary

| Model | MAE | RMSE | Bias | Coverage (90% CI) | Calibration Error |
|-------|-----|------|------|-------------------|-------------------|
| Linear Baseline | 30.2% | 33.2% | -30.2% | 35.7% | 54.3% |
| **Claude (LLM)** | **12.5%** | **15.0%** | -12.4% | 42.9% | 47.1% |

**Key finding**: The LLM outperforms linear extrapolation by **2.4x** on mean absolute error.

## Detailed Results by Variable

### HOMOSEX (Same-sex relations)

GSS Question: "What about sexual relations between two adults of the same sex - do you think it is always wrong, almost always wrong, wrong only sometimes, or not wrong at all?"

**Cutoff: 1990**

| Target Year | Baseline | LLM | Actual |
|-------------|----------|-----|--------|
| 2000 | 14.6% [8.8, 20.4] | 18.0% [12.0, 25.0] | 27% |
| 2010 | 15.6% [6.9, 24.4] | 28.0% [18.0, 40.0] | 41% |
| 2018 | 16.5% [5.4, 27.5] | 42.0% [28.0, 58.0] | 58% |
| 2021 | 16.8% [4.9, 28.7] | 48.0% [32.0, 65.0] | 64% |

**Cutoff: 2000**

| Target Year | Baseline | LLM | Actual |
|-------------|----------|-----|--------|
| 2010 | 29.0% [13.7, 44.3] | 42.0% [35.0, 50.0] | 41% |
| 2018 | 33.2% [11.8, 54.7] | 55.0% [45.0, 65.0] | 58% |
| 2021 | 34.8% [11.0, 58.6] | 60.0% [50.0, 70.0] | 64% |

### GRASS (Marijuana legalization)

GSS Question: "Do you think the use of marijuana should be made legal or not?"

**Cutoff: 1990**

| Target Year | Baseline | LLM | Actual |
|-------------|----------|-----|--------|
| 2000 | 15.7% [0.0, 35.0] | 22.0% [18.0, 28.0] | 31% |
| 2010 | 13.4% [0.0, 42.4] | 28.0% [22.0, 35.0] | 44% |
| 2018 | 11.6% [0.0, 48.4] | 35.0% [28.0, 43.0] | 61% |
| 2021 | 11.0% [0.0, 50.6] | 38.0% [30.0, 47.0] | 68% |

**Cutoff: 2000**

| Target Year | Baseline | LLM | Actual |
|-------------|----------|-----|--------|
| 2010 | 30.0% [7.2, 52.7] | 42.0% [35.0, 50.0] | 44% |
| 2018 | 32.3% [0.4, 64.2] | 48.0% [38.0, 58.0] | 61% |
| 2021 | 33.2% [0.0, 68.5] | 51.0% [40.0, 62.0] | 68% |

## Analysis

### LLMs Capture Non-Linear Dynamics

The baseline (linear extrapolation) essentially predicted no change for HOMOSEX from 1990—it extrapolated from essentially flat data (11% in 1973, 13% in 1990) and missed the subsequent acceleration.

The LLM correctly identified that liberalization was accelerating and predicted the direction and approximate magnitude of change.

### Both Models Are Overconfident

For 90% confidence intervals, we'd expect 90% of actual values to fall within the bounds. Instead:
- Baseline: 35.7% coverage (very overconfident)
- LLM: 42.9% coverage (still overconfident)

This suggests uncertainty bounds need to be approximately 2x wider.

### Systematic Underestimation

Both models underestimated the pace of liberalization:
- Baseline bias: -30.2% (severely underestimated)
- LLM bias: -12.4% (moderately underestimated)

## Limitations

1. **Small sample**: Only 2 variables, 14 total forecast points
2. **RLHF contamination**: Claude has been trained on post-cutoff data, which may include moral attitudes
3. **Selection bias**: We tested values that liberalized; need to test stable/declining values
4. **Simple prompting**: More sophisticated approaches might improve results

## Raw Data

See `results/forecasts.json` for the complete dataset.
