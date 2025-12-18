# Project Status

Last updated: December 17, 2024

## Current State: Ready for Submission

The paper draft is complete with all major sections. Five simulated referee reviews recommended "Minor Revision/Accept" after addressing feedback.

## Recent Work (December 2024)

### Completed
1. **EMOS Calibration** (`scripts/calibrated_forecast.py`)
   - Quantile elicitation from GPT-4o (10th, 25th, 50th, 75th, 90th percentiles)
   - CRPS-based post-hoc calibration
   - Spread multiplier: 1.21x (CIs need to be 21% wider)
   - Raw 50% coverage: 47% → needs calibration

2. **Long-term Forecasts** (`data/longterm_gpt-4o_calibrated.json`)
   - 17 GSS variables through 2030, 2050, 2075, 2100
   - Calibrated 80% confidence intervals
   - Key forecast: HOMOSEX reaches 80% by 2100 [69-91% CI]

3. **React Visualization App** (`app/`)
   - Shows historical data + calibrated forecasts
   - 2024 holdout validation (actual vs predicted)
   - Uncertainty bands through 2100
   - Toggle between HOMOSEX and GRASS variables

4. **Paper Revisions** (`paper/`)
   - Added AI forecasting literature (Halawi et al., CRPS)
   - Expanded methods with all 16 variables
   - Full prompts in appendix
   - Governance/normative sections

### Key Files
- `scripts/calibrated_forecast.py` - Main forecasting with cost tracking (~$0.09/run)
- `data/calibration_gpt-4o_2021_2024.json` - Holdout validation results
- `data/longterm_gpt-4o_calibrated.json` - Calibrated long-term forecasts
- `app/src/App.tsx` - React visualization

## Open Tasks

```bash
bd ready  # See available work
```

- Compare multiple LLM models (Claude, Gemini)
- Deploy React app to web
- Submit paper to AI safety venue
- Set up JupyterBook 2.0 for results

## Key Findings

1. **LLMs outperform baselines** - 2.2x lower MAE than time series methods
2. **Short-term prediction is hard** - HOMOSEX reversed unexpectedly in 2024
3. **Long-term trends may be more reliable** - 50-year trajectory shows +44 points
4. **Calibration is necessary** - Raw LLM CIs are 21% too narrow

## Environment Setup

```bash
cd /Users/maxghenis/value-forecasting
source .venv/bin/activate
export OPENAI_API_KEY="..."  # Required for forecasting

# Run forecast
python scripts/calibrated_forecast.py

# Run app
cd app && bun run dev
```
