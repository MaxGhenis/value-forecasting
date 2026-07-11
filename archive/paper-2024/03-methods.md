---
title: Methods
---

## Data: General Social Survey

We use the General Social Survey (GSS), conducted by NORC at the University of Chicago since 1972. The GSS is one of the most widely used data sources in social science, with over 75,000 respondents across 35 survey waves through 2024.

We test 16 variables spanning social values, economic attitudes, and social trust:

:::{table} GSS Variables Analyzed (16 total)
:label: tbl:variables

| Variable | Topic | Liberal Response |
|----------|-------|------------------|
| HOMOSEX | Same-sex relations | "Not wrong at all" |
| GRASS | Marijuana legalization | "Legal" |
| PREMARSX | Premarital sex | "Not wrong at all" |
| ABANY | Abortion for any reason | "Yes" |
| FEPOL | Women in politics | "Disagree" (women unsuited) |
| CAPPUN | Death penalty | "Oppose" |
| GUNLAW | Gun permits | "Favor" |
| NATRACE | Spending on race issues | "Too little" |
| NATEDUC | Spending on education | "Too little" |
| NATENVIR | Spending on environment | "Too little" |
| NATHEAL | Spending on health | "Too little" |
| EQWLTH | Government reduce inequality | Top 3 of 7-point scale |
| HELPPOOR | Government help poor | Top 2 of 5-point scale |
| TRUST | Social trust | "Can trust" |
| FAIR | Fairness of others | "Try to be fair" |
| POLVIEWS | Self-identified liberal | Liberal side (1-3 of 7) |
| PRAYER | School prayer ban | "Approve" |

:::

Full variable definitions, response codings, and preprocessing details in Appendix B.

We downloaded the cumulative GSS data file (gss7224_r2.dta) containing all respondents from 1972-2024. For each variable, we calculated the percentage giving the "liberal" or "progressive" response among those with valid responses (excluding "don't know" and refusals). Years with fewer than 50 valid responses were excluded.

### Mode Effects and Survey Methodology

The GSS has undergone significant methodological changes:

| Period | Mode | Notes |
|--------|------|-------|
| 1972-2020 | Face-to-face | Standard in-person interviews |
| 2021 | Mixed | COVID-era combination of web/phone/in-person |
| 2022-2024 | Web-push | Primarily web with push-to-web methodology |

**Implications**: Web surveys may reduce social desirability bias, yielding more candid responses on sensitive topics [@kreuter2008social]. Some portion of observed changes between 2021 and 2024 may reflect measurement differences rather than true attitude shifts. We do not attempt statistical adjustment for mode effects, as NORC has not released official crosswalk estimates. We note this as a limitation throughout.

## Models

### Language Models

We tested three language models with different training cutoffs:

1. **gpt-3.5-turbo-instruct** (OpenAI): Training cutoff September 2021. This model cannot have seen GSS 2021 data (released November 2021) or later.

2. **GPT-4o** (OpenAI): Training cutoff October 2023. This model cannot have seen GSS 2024 data (collected April-December 2024).

3. **Claude Sonnet** (Anthropic): Training cutoff early 2024. Used for initial experiments but potentially contaminated with recent GSS data.

For each forecast, we prompted the model with:
- Historical data formatted as year-percentage pairs
- The variable description
- Instructions to predict a single number
- Temperature set to 0 (deterministic)
- A system prompt establishing temporal context

**Example prompt (GPT-4o)**:
```
System: You are a social scientist in 2021. You predict survey trends based on historical data.

User: Based on historical General Social Survey data, predict the percentage of Americans
who will say "Same-sex relations not wrong" in 2024.

Historical data (% giving this response):
  1973: 11%  1990: 13%  2000: 29%  2010: 42%  2018: 57%  2021: 62%

Predict only a single number between 0 and 100.
```

Confidence intervals were elicited in a separate prompt. Full prompt templates and parameters in Appendix A.

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
