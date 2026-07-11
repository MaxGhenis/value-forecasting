---
title: Appendix
---

## A. Full Prompts and Parameters

### A.1 GPT-3.5-Turbo-Instruct (Completion API)

**Model**: `gpt-3.5-turbo-instruct`
**Temperature**: 0 (deterministic)
**Max tokens**: 20
**Training cutoff**: September 2021

**Prompt template**:
```
Historical GSS data for "{description}":
  {year1}: {value1}%
  {year2}: {value2}%
  ...
  {yearN}: {valueN}%

Predicted percentage for {target_year}:
```

**Example prompt** (HOMOSEX, 2010 cutoff):
```
Historical GSS data for "Same-sex relations not wrong":
  1980: 15%
  1990: 13%
  2000: 29%
  2010: 42%

Predicted percentage for 2024:
```

### A.2 GPT-4o (Chat API)

**Model**: `gpt-4o`
**Temperature**: 0 (deterministic)
**Max tokens**: 10
**Training cutoff**: October 2023

**System prompt**:
```
You are a social scientist in {cutoff_year}. You predict survey trends based on historical data.
```

**User prompt template**:
```
Based on historical General Social Survey data, predict the percentage of Americans who will say "{description}" in {target_year}.

Historical data (% giving this response):
{history}

Predict only a single number between 0 and 100.
```

**Example** (HOMOSEX, 2021 cutoff):
```
System: You are a social scientist in 2021. You predict survey trends based on historical data.

User: Based on historical General Social Survey data, predict the percentage of Americans who will say "Same-sex relations not wrong" in 2024.

Historical data (% giving this response):
  1973: 11%
  1980: 15%
  1990: 13%
  2000: 29%
  2010: 42%
  2018: 57%
  2021: 62%

Predict only a single number between 0 and 100.
```

### A.3 Confidence Interval Elicitation

For GPT-4o confidence intervals, we used a separate prompt:

```
System: You are a social scientist. Provide uncertainty estimates for survey predictions.

User: You predicted {predicted}% for "{description}" in {target_year}.
What is your 90% confidence interval? Provide the lower and upper bounds as two numbers.
```

**Note**: This two-stage approach may contribute to poor calibration, as the CI is generated post-hoc rather than jointly with the point estimate. Future work should explore direct probability elicitation or ensemble methods.

## B. Data Preprocessing

### B.1 GSS Data Source

- **File**: `gss7224_r2.dta` (Stata format)
- **Source**: NORC at University of Chicago (gss.norc.org)
- **Coverage**: 1972-2024, approximately 75,000 respondents

### B.2 Variable Coding

For each variable, we identified the "liberal" or "progressive" response:

| Variable | Code | Liberal Response | Values |
|----------|------|------------------|--------|
| HOMOSEX | "Not wrong at all" | 4 | 1-4 scale |
| GRASS | "Legal" | 1 | 1=Legal, 2=Not legal |
| PREMARSX | "Not wrong at all" | 4 | 1-4 scale |
| ABANY | "Yes" | 1 | 1=Yes, 2=No |
| CAPPUN | "Oppose" | 2 | 1=Favor, 2=Oppose |
| GUNLAW | "Favor" | 1 | 1=Favor, 2=Oppose |
| FEPOL | "Disagree" (women unsuited) | 2 | 1=Agree, 2=Disagree |
| NATRACE | "Too little" | 1 | 1-3 scale |
| NATEDUC | "Too little" | 1 | 1-3 scale |
| NATENVIR | "Too little" | 1 | 1-3 scale |
| NATHEAL | "Too little" | 1 | 1-3 scale |
| EQWLTH | Top 3 (gov reduce) | 1, 2, 3 | 1-7 scale |
| HELPPOOR | Top 2 (gov help) | 1, 2 | 1-5 scale |
| TRUST | "Can trust" | 1 | 1=Trust, 2=Can't trust |
| FAIR | "Try to be fair" | 1 | 1=Fair, 2=Take advantage |
| POLVIEWS | Liberal side | 1, 2, 3 | 1-7 scale |
| PRAYER | "Approve" (of ban) | 1 | 1=Approve, 2=Disapprove |

### B.3 Missing Data Handling

```python
# Filter valid responses (exclude DK, NA, refusals)
valid = col[col.notna() & (col > 0) & (col < 90)]
```

- Missing values (NA): Excluded
- "Don't know" responses: Typically coded as 8, 9, or 0; excluded via `col > 0` filter
- Refusals: Typically coded 98, 99; excluded via `col < 90` filter
- IAP (Inapplicable): Excluded as missing

### B.4 Minimum Sample Size

Years with fewer than 50 valid responses for a variable were excluded:
```python
if len(valid) >= min_n:  # min_n = 50
    liberal_pct = (valid.isin(liberal_vals).sum() / len(valid)) * 100
```

### B.5 Survey Mode Changes

The GSS has used different survey modes over time:

| Period | Mode | Notes |
|--------|------|-------|
| 1972-2020 | Face-to-face | Standard in-person interviews |
| 2021 | Mixed (COVID) | Combination of web/phone/in-person |
| 2022-2024 | Web-push | Primarily web with push-to-web |

**Mode effects concern**: Web surveys may reduce social desirability bias, yielding more candid responses on sensitive topics. This could contribute to the observed 2024 declines on some social issues.

**Our approach**: We do not attempt to statistically adjust for mode effects, as the GSS has not released official crosswalk estimates. We acknowledge this as a limitation and note that some observed change may reflect measurement differences rather than true attitude shifts.

## C. Reproducibility

### C.1 Code Availability

All code is available at: https://github.com/maxghenis/value-forecasting

Repository structure:
```
value-forecasting/
├── data/
│   ├── trajectories.json          # Extracted trajectories
│   └── experiment_*.json          # Saved experiment results
├── scripts/
│   ├── extract_gss_trajectories.py # Data extraction
│   └── run_forecast_experiment.py  # Main experiments
├── src/value_forecasting/
│   └── gss_variables.py           # Variable definitions
├── paper/                         # MyST markdown paper
└── pyproject.toml                 # Dependencies
```

### C.2 Dependencies

```toml
python = ">=3.10"
pandas = ">=2.0"
openai = ">=1.0"
```

Full dependency specification in `pyproject.toml`.

### C.3 Replication Instructions

1. **Obtain GSS data**: Download `gss7224_r2.dta` from https://gss.norc.org/get-the-data

2. **Extract trajectories**:
   ```bash
   python scripts/extract_gss_trajectories.py --data data/gss7224_r2.dta
   ```

3. **Run experiments**:
   ```bash
   export OPENAI_API_KEY=your_key
   python scripts/run_forecast_experiment.py --model gpt-3.5-turbo-instruct --cutoff 2010 --target 2024
   ```

### C.4 Computational Costs

- **API costs**: Approximately $2-5 for full 16-variable experiment using gpt-3.5-turbo-instruct
- **Runtime**: ~5 minutes for 16 variables

### C.5 Pre-Registration Status

This study was **not pre-registered**. Analyses should be considered exploratory. Specifically:

**Planned before data collection**:
- Testing whether LLMs could forecast GSS values
- Comparing to time series baselines
- Using temporal holdout design

**Decided during analysis**:
- Selection of specific cutoff years (2010)
- Income-values gradient analysis
- Demographic decomposition by party/age
- Framing around "veil of scarcity"

Future work should use formal pre-registration (OSF, AsPredicted) to distinguish confirmatory from exploratory analyses.

## D. All Variables Tested

We tested 16 GSS variables. Results for all variables are reported in Table 1 (main text). No variables were excluded from reporting.

Variables tested but not shown separately (included in aggregate statistics):
- All 16 variables listed in Table 1 received equal treatment in analysis
- No results were suppressed due to unfavorable outcomes

## E. Uncertainty Quantification Methodology

### E.1 LLM Confidence Intervals

**Method**: Two-stage prompting (point estimate, then CI request)
**Observed coverage**: 42.9% (well below nominal 90%)

**Known issues**:
1. Post-hoc CI generation may not reflect true model uncertainty
2. LLMs may not have well-calibrated internal probabilities
3. Prompting for "90% CI" may elicit range estimates rather than probabilistic bounds

**Future improvements**:
- Direct probability elicitation across multiple values
- Ensemble methods (multiple samples at temperature > 0)
- Calibration training on historical data

### E.2 Baseline Model Intervals

**Naive**: Standard error grows proportionally with forecast horizon
**Linear**: Prediction intervals from OLS residual standard error
**ARIMA/ETS**: Standard forecast uncertainty formulas from statsmodels

All baseline intervals also showed poor calibration (40-50% coverage), suggesting the underlying value trajectories have higher variance than any model captures.
