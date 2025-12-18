# Value Forecasting Project

## Overview

This project investigates whether LLMs can forecast long-term trajectories of human values using General Social Survey (GSS) data. The research has implications for AI alignment - understanding how well AI systems can predict value change helps inform whether we can rely on such predictions for alignment decisions.

## Key Research Questions

1. Can LLMs forecast value trajectories better than traditional time series methods?
2. How should we quantify and calibrate uncertainty in LLM forecasts?
3. What do LLM forecasts suggest about long-term value trajectories (2030, 2050, 2100)?

## Project Structure

```
value-forecasting/
├── app/                    # React visualization app (Vite + Recharts)
├── data/                   # GSS data and forecast outputs
│   ├── calibration_*.json  # Holdout validation results
│   └── longterm_*.json     # Calibrated long-term forecasts
├── paper/                  # Academic paper (Markdown + MyST)
│   ├── 01-introduction.md
│   ├── 02-related-work.md
│   ├── 03-methods.md
│   ├── 04-results.md
│   ├── 05-discussion.md
│   ├── 06-conclusion.md
│   └── 07-appendix.md
├── scripts/                # Python scripts
│   └── calibrated_forecast.py  # Main forecasting script
├── src/                    # Python package (if needed)
└── tests/                  # pytest tests
```

## Technical Details

### Calibration Method (EMOS)
- **Ensemble Model Output Statistics** - post-hoc calibration from weather forecasting literature
- Elicit quantiles (10th, 25th, 50th, 75th, 90th percentiles) from LLM
- Fit Gaussian to quantiles, then calibrate spread to minimize CRPS on holdout
- Current spread multiplier: **1.21** (CIs should be 21% wider than raw LLM output)

### Key Variables (GSS)
- HOMOSEX: Same-sex relations not wrong (flagship variable)
- GRASS: Marijuana legalization
- PREMARSX: Premarital sex
- ABANY: Abortion for any reason
- Plus 13 more social/political variables

### Holdout Validation
- Training cutoff: 2021 GSS
- Holdout: 2024 GSS
- HOMOSEX: Predicted 63%, Actual 55% (first reversal in 30+ years)
- GRASS: Predicted 70%, Actual 68% (within CI)

### Long-term Forecasts (GPT-4o, calibrated 80% CIs)
| Variable | 2024 Actual | 2030 | 2050 | 2100 |
|----------|-------------|------|------|------|
| HOMOSEX | 55% | 66% [57,75] | 75% [64,86] | 80% [69,91] |
| GRASS | 68% | 72% [57,87] | 80% [57,100] | 80% [57,100] |

## Current State

### Completed
- Paper draft with all major sections
- EMOS-calibrated forecasts for 17 variables through 2100
- React app with uncertainty visualization
- Holdout validation showing calibration approach works

### In Progress / Next Steps
- Submit to AI safety venue (potential: NeurIPS workshop, AAAI symposium)
- Compare multiple LLM models (Claude, Gemini, etc.)
- Add more variables or time horizons
- Deploy React app to web

## Commands

### Running the Forecast Script
```bash
cd /Users/maxghenis/value-forecasting
source .venv/bin/activate
python scripts/calibrated_forecast.py
```

### Running the React App
```bash
cd app
bun install
bun run dev
# Opens at http://localhost:5173 or 5174
```

### Building the Paper
```bash
# Uses MyST for scientific markdown
myst build
```

## Key Decisions Made

1. **Dropped heterogeneity** - Response distribution forecasting was complex and not core to the paper
2. **Focus on long-term** - Short-term (1-year) predictions are noisy; 50-year trends are the story
3. **EMOS calibration** - Simple, well-established method with 20 years of precedent
4. **80% CIs** - Standard for probabilistic forecasting; easier to interpret than 90%

## API Keys Required
- OPENAI_API_KEY for GPT-4o forecasting
- Cost tracking shows ~$0.09 per full run (17 variables × 4 horizons)

## Referee Feedback Summary
All 5 reviewers recommended Minor Revision/Accept after addressing:
- Added full prompts to appendix
- Clarified normative framework
- Added AI forecasting literature (Halawi et al., CRPS, calibration)
- Expanded methods section with all 16 variables
