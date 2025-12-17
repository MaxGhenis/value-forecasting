---
title: Value Forecasting
---

# Can LLMs Forecast Human Value Evolution?

This project tests whether language models can predict how human values change over time, using historical survey data as ground truth.

## Motivation

Current AI alignment approaches face a fundamental challenge: human values are contested, evolving, and uncertain. What if we could forecast where values are heading?

This project tests a key premise: **can LLMs predict moral change trajectories?**

## Method

1. **Select GSS variables** with significant historical change
2. **Prompt LLMs** with context available up to a cutoff year (e.g., 2000)
3. **Generate predictions** for support levels in future years
4. **Compare** predictions to actual GSS data
5. **Calculate** calibration and accuracy metrics

## Key Questions

- Can LLMs predict value trajectories better than simple linear extrapolation?
- Are LLM predictions well-calibrated (do 90% CIs cover 90% of outcomes)?
- Which value changes are most predictable?

## Installation

```bash
uv pip install value-forecasting
```

Or from source:

```bash
git clone https://github.com/maxghenis/value-forecasting
cd value-forecasting
uv pip install -e ".[dev]"
```

## Quick Start

```python
from value_forecasting import (
    run_forecast,
    run_baseline_forecast,
    HISTORICAL_TRAJECTORIES,
)

# Run LLM forecast
forecasts = run_forecast("HOMOSEX", cutoff_year=2000, target_years=[2010, 2020])

# Compare to baseline
baseline = run_baseline_forecast("HOMOSEX", cutoff_year=2000, target_years=[2010, 2020])

# Get actual values
actual = HISTORICAL_TRAJECTORIES["HOMOSEX"]
print(f"Actual 2010: {actual[2010]}%, 2018: {actual[2018]}%")
```
