---
title: Methodology
---

# Methodology

## Data Source: General Social Survey

The [General Social Survey (GSS)](https://gss.norc.org/) has tracked American opinions since 1972, providing ideal ground truth for value forecasting experiments.

### Variables Used

| Variable | Question | First Year | Pattern |
|----------|----------|------------|---------|
| HOMOSEX | Attitudes toward same-sex relations | 1973 | Strong liberalization |
| GRASS | Marijuana legalization support | 1973 | Strong liberalization |
| FEPOL | Women suited for politics | 1974 | Steady increase |
| PREMARSX | Premarital sex attitudes | 1972 | Moderate liberalization |
| CAPPUN | Death penalty support | 1972 | Fluctuation then decline |

## Forecasting Approach

### LLM Forecasting

We prompt language models with:
1. The survey question
2. Historical data up to a cutoff year
3. Instructions to predict future values with uncertainty

**Key design choice**: We use base models or carefully prompt to avoid contaminating predictions with post-cutoff moral attitudes.

### Baseline: Linear Extrapolation

Simple linear regression on pre-cutoff data, with uncertainty bands that widen for further predictions.

## Evaluation Metrics

### Mean Absolute Error (MAE)
Average absolute difference between predicted and actual percentages.

### Coverage (Calibration)
For 90% confidence intervals, what fraction of actual values fall within the intervals?
- Well-calibrated: ~90% coverage
- Overconfident: <90% coverage
- Underconfident: >90% coverage

## Experimental Design

### Cutoff Years Tested
- 1990 → predict 2000, 2010, 2018
- 2000 → predict 2010, 2018

### Models Tested
- Claude Sonnet
- Linear extrapolation baseline
