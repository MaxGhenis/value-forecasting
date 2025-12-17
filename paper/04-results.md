---
title: Results
---

## Historical Validation: LLMs Outperform Baselines

We first tested whether LLMs can predict historical value changes better than time series baselines. Using cutoffs of 1990 and 2000, we predicted values for subsequent years.

:::{table} Model Performance on Historical Forecasting
:label: tbl:historical

| Model | MAE | Coverage (90% CI) | Bias |
|-------|-----|-------------------|------|
| Naive | 31.4% | 7.1% | -31.4% |
| Linear | 30.2% | 35.7% | -30.2% |
| ARIMA | 31.4% | 50.0% | -31.4% |
| ETS (Holt) | 28.1% | 28.6% | -7.1% |
| **Claude (LLM)** | **12.5%** | 42.9% | -12.4% |

:::

The LLM outperformed the best baseline (ETS) by 2.2× on MAE. All models showed negative bias, underestimating the pace of liberalization. All models were overconfident, with coverage well below the target 90%.

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

## Long-Term Forecasts

We also generated long-term forecasts to test the core proposal of forecasting to "post-reflection" values:

:::{table} GPT-4o Long-Term Forecasts
:label: tbl:longterm

| Variable | 2030 | 2050 | 2075 | 2100 |
|----------|------|------|------|------|
| HOMOSEX | 68% [60,76] | 75% [65,85] | 80% [68,92] | 85% [70,100] |
| GRASS | 75% [70,80] | 85% [78,92] | 90% [82,98] | 92% [84,100] |

:::

The model predicts continued liberalization with widening uncertainty. However, given that the 2024 actual (55%) already falls below the 2030 prediction (68%), these long-term forecasts are questionable.

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
