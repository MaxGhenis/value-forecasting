---
title: Results
---

## Multi-Variable Validation: 14-Year Forecasting Horizon

We tested value forecasting across 17 GSS variables using gpt-3.5-turbo-instruct (September 2021 training cutoff) to predict 2024 values from a 2010 baseline—a 14-year forecasting horizon.

:::{table} Multi-Variable Forecasting Results (2010→2024, all 16 variables tested)
:label: tbl:multivar

| Variable | 2010 | 2024 Actual | Predicted | Error | Dir |
|----------|------|-------------|-----------|-------|-----|
| PRAYER | 44% | 46% | 46% | 0 | ✓ |
| FEPOL | 79% | 82% | 81% | -1 | ✓ |
| NATEDUC | 72% | 76% | 75% | -1 | ✓ |
| GUNLAW | 74% | 70% | 72% | +2 | ✓ |
| POLVIEWS | 29% | 29% | 31% | +2 | ✗ |
| NATENVIR | 57% | 66% | 60% | -6 | ✓ |
| NATHEAL | 60% | 74% | 80% | +6 | ✓ |
| TRUST | 33% | 25% | 31% | +6 | ✓ |
| FAIR | 38% | 46% | 40% | -6 | ✓ |
| GRASS | 48% | 68% | 60% | -8 | ✓ |
| PREMARSX | 53% | 65% | 56% | -9 | ✓ |
| EQWLTH | 42% | 54% | 45% | -9 | ✓ |
| HELPPOOR | 28% | 39% | 30% | -9 | ✓ |
| CAPPUN | 32% | 40% | 30% | -10 | ✗ |
| ABANY | 44% | 60% | 46% | -14 | ✓ |
| NATRACE | 34% | 51% | 37% | -14 | ✓ |

:::

**Key findings across 16 variables:**
- **MAE: 6.4 percentage points** vs 9.2 for naive baseline
- **Improvement: 1.44×** over simply predicting the last observed value
- **Direction correct: 94%** (15/16 variables)
- **Bias: -4.4 points**—slight under-prediction of change magnitude

The model correctly captured the direction of change in nearly all cases, including the decline in social trust (TRUST: 33%→25%) and stability in gun permit support (GUNLAW: 74%→70%). The largest errors occurred on variables with rapid change (NATRACE, ABANY) where the model under-predicted the magnitude.

## Clean Test: GPT-4o Predicting GSS 2024

For a methodologically rigorous test, we used GPT-4o (training cutoff October 2023) to predict GSS 2024 data (collected April-December 2024). This ensures the model could not have seen the target values.

:::{table} GPT-4o Predictions vs. GSS 2024 Actual
:label: tbl:clean

| Variable | Prediction | 90% CI | Actual | Error |
|----------|------------|--------|--------|-------|
| HOMOSEX | 69% | [66, 72] | **54.7%** | +14.3% |
| GRASS | 73% | [70, 76] | 68.5% | +4.5% |

:::

**The model missed a major reversal.** HOMOSEX (acceptance of same-sex relationships) had increased steadily for decades: 13% (1990) → 27% (2000) → 42% (2010) → 62% (2021). GPT-4o extrapolated this trend, predicting 69% for 2024.

Instead, the actual value was 54.7%—a 7 percentage point drop from 2021 and the first reversal in over 30 years.

## Multi-Variable Analysis

The reversal was not isolated. We analyzed six GSS variables:

:::{table} GSS 2024 Results Across Variables
:label: tbl:multi

| Variable | 2018 | 2021 | 2022 | 2024 | Pattern |
|----------|------|------|------|------|---------|
| HOMOSEX | 57% | 62% | 61% | **55%** | ↓ Reversal |
| PREMARSX | 62% | 66% | 69% | **65%** | ↓ Peaked |
| NATRACE | 56% | 52% | 56% | **51%** | ↓ Declining |
| ABANY | 50% | 56% | 59% | **60%** | ↑ Rising |
| GUNLAW | 72% | 67% | 71% | 70% | → Stable |
| CAPPUN | 37% | 44% | 40% | 40% | → Stable |

:::

Values did not move in lockstep. While ABANY (abortion) continued rising post-Dobbs, HOMOSEX and NATRACE (spending on racial issues) reversed. This divergence would be missed by any model assuming "liberalization" as a general pattern.

## Demographic Decomposition

We analyzed HOMOSEX by party identification:

:::{table} HOMOSEX by Party (% "Not Wrong at All")
:label: tbl:party

| Year | Democrat | Independent | Republican |
|------|----------|-------------|------------|
| 2018 | 62% | 63% | 45% |
| 2021 | 76% | 59% | 43% |
| 2024 | 71% | 57% | 36% |
| **Change 2021→24** | **-5** | **-2** | **-7** |

:::

The reversal occurred across all party groups but was largest among Republicans (-7 points). This is consistent with backlash dynamics triggered by political mobilization.

By age group:

:::{table} HOMOSEX by Age (% "Not Wrong at All")
:label: tbl:age

| Year | 18-29 | 30-44 | 45-64 | 65+ |
|------|-------|-------|-------|-----|
| 2021 | 79% | 68% | 61% | 53% |
| 2024 | 69% | 61% | 51% | 45% |
| **Change** | **-10** | **-7** | **-10** | **-8** |

:::

The largest drops were among the youngest (18-29) and middle-aged (45-64) groups. This contradicts simple generational replacement models where younger cohorts drive liberalization.

## Long-Term Forecasts with Calibrated Uncertainty

We generated long-term forecasts using quantile elicitation and EMOS-style calibration [@gneiting2005calibrated]. For each variable, we elicited five quantiles (10th, 25th, 50th, 75th, 90th percentiles) and calibrated the uncertainty by optimizing CRPS on the 2024 holdout data.

**Calibration Results (17 variables, 2021→2024):**
- Optimal spread multiplier: **1.21** (CIs need 21% widening)
- Raw 50% interval coverage: 47% (target: 50%)
- Raw 80% interval coverage: 59% (target: 80%)
- Mean CRPS: 3.15 points

:::{table} Calibrated Long-Term Forecasts (GPT-4o)
:label: tbl:longterm

| Variable | 2024 Actual | 2030 | 2050 | 2100 |
|----------|-------------|------|------|------|
| HOMOSEX | 55% | 66% [57,75] | 75% [64,86] | 80% [69,91] |
| GRASS | 68% | 72% [57,87] | 80% [57,103] | 80% [57,103] |
| PREMARSX | 65% | 70% [59,81] | 80% [69,91] | 80% [69,91] |
| ABANY | 60% | 60% [51,69] | 60% [42,78] | 60% [37,83] |
| CAPPUN | 40% | 42% [33,51] | 45% [34,56] | 55% [32,78] |
| TRUST | 25% | 28% [21,35] | 27% [18,36] | 27% [18,36] |
| POLVIEWS | 29% | 30% [25,35] | 30% [23,37] | 31% [24,38] |

:::

Brackets show calibrated 80% confidence intervals.

**Key observations:**
- **HOMOSEX**: Model predicts recovery to 66% by 2030, 80% by 2100. But 2024 actual (55%) is already below the 2030 lower bound (57%), suggesting the model underestimates reversal risk.
- **ABANY**: Predicted stable at ~60%, unlike the continued rise the model predicted pre-2024.
- **TRUST**: Continued decline predicted (28%→27%), reflecting the long-term erosion of social trust.
- **Uncertainty widens with horizon**: 2100 intervals are appropriately wider than 2030.

These forecasts should be treated as registered predictions subject to future validation, not reliable projections. The 2024 calibration shows models are overconfident; longer horizons likely involve even greater uncertainty than shown.

## Income-Values Relationship

We found a strong gradient between income and values in GSS 2024:

:::{table} HOMOSEX by Income Quartile (2024)
:label: tbl:income

| Income Quartile | % Accept | Median Income |
|-----------------|----------|---------------|
| Q1 (lowest) | 43% | $7,700 |
| Q2 | 54% | $31,000 |
| Q3 | 61% | $56,000 |
| Q4 (highest) | 67% | $139,000 |

:::

This 24-point gap suggests economic conditions may influence values. Under AI-driven growth scenarios, rising incomes could shift values—though the direction and causality are uncertain.
