---
title: Methods
---

## Data: General Social Survey

We use the General Social Survey (GSS), conducted by NORC at the University of Chicago since 1972. The GSS is one of the most widely used data sources in social science, with over 75,000 respondents across 35 survey waves through 2024.

We focus on six variables with long time series and significant historical change:

:::{table} GSS Variables Analyzed
:label: tbl:variables

| Variable | Question | Response (Liberal) | Years |
|----------|----------|-------------------|-------|
| HOMOSEX | Sexual relations between two adults of the same sex | "Not wrong at all" | 1973-2024 |
| GRASS | Should marijuana be made legal | "Legal" | 1973-2024 |
| ABANY | Should abortion be legal for any reason | "Yes" | 1977-2024 |
| PREMARSX | Is premarital sex wrong | "Not wrong at all" | 1972-2024 |
| CAPPUN | Favor death penalty for murder | "Oppose" | 1972-2024 |
| GUNLAW | Require police permit for guns | "Favor" | 1972-2024 |

:::

We downloaded the cumulative GSS data file (gss7224_r2.dta) containing all respondents from 1972-2024. For each variable, we calculated the percentage giving the "liberal" or "progressive" response among those with valid responses (excluding "don't know" and refusals).

## Models

### Language Models

We tested three language models with different training cutoffs:

1. **gpt-3.5-turbo-instruct** (OpenAI): Training cutoff September 2021. This model cannot have seen GSS 2021 data (released November 2021) or later.

2. **GPT-4o** (OpenAI): Training cutoff October 2023. This model cannot have seen GSS 2024 data (collected April-December 2024).

3. **Claude Sonnet** (Anthropic): Training cutoff early 2024. Used for initial experiments but potentially contaminated with recent GSS data.

For each forecast, we prompted the model with:
- The survey question
- Historical data up to a specified cutoff year
- Instructions to predict values for target years with 90% confidence intervals
- A system prompt establishing the temporal context ("You are a social scientist in {cutoff_year}")

### Baseline Models

We compared LLMs against standard time series forecasting methods:

1. **Naive**: Predict the last observed value. Uncertainty grows with forecast horizon.

2. **Linear extrapolation**: Ordinary least squares regression of values on year. Uncertainty based on residual standard error.

3. **ARIMA(1,1,0)**: Autoregressive integrated moving average with one AR term and one differencing operation.

4. **ETS (Holt)**: Exponential smoothing with linear trend (Holt's method).

## Evaluation

### Temporal Holdout Design

To avoid data leakage, we use strict temporal holdout:

1. Select a cutoff year (e.g., 2000, 2010, 2021)
2. Provide the model only with data before the cutoff
3. Generate predictions for years after the cutoff
4. Compare predictions to actual GSS values

For LLMs, we additionally verify that the model's training data predates the target values. GSS data release dates:
- GSS 2021: Released November 2021
- GSS 2022: Released May 2023
- GSS 2024: Released late 2024

### Metrics

We evaluate forecasts using:

**Mean Absolute Error (MAE)**:
$$\text{MAE} = \frac{1}{n}\sum_{i=1}^{n}|y_i - \hat{y}_i|$$

where $y_i$ is the actual value and $\hat{y}_i$ is the predicted value.

**Coverage**: The fraction of actual values falling within the 90% confidence interval. Well-calibrated forecasts should have ~90% coverage.

**Bias**: Mean signed error, indicating systematic over- or under-prediction:
$$\text{Bias} = \frac{1}{n}\sum_{i=1}^{n}(y_i - \hat{y}_i)$$

## Heterogeneity Analysis

Beyond aggregate forecasts, we analyze how attitudes vary by:
- **Party identification**: Democrat, Independent, Republican
- **Age group**: 18-29, 30-44, 45-64, 65+
- **Income quartile**: Based on family income in constant dollars

This enables testing whether LLMs can predict not just aggregate trends but shifts in the distribution of values across subgroups.
