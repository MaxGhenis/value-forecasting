# Value Forecasting

Can LLMs predict how human values evolve over time?

This repo tests whether language models can forecast moral/value change trajectories using historical survey data as ground truth.

## Hypothesis

If LLMs have learned patterns about how values evolve—generational replacement, exposure effects, information cascades—they might predict value trajectories better than simple extrapolation.

## Method

1. **Select GSS variables** with significant historical change
2. **Prompt LLMs** with context available up to a cutoff year (e.g., 2000)
3. **Generate predictions** for support levels in future years (2005, 2010, 2015, 2020)
4. **Compare** predictions to actual GSS data
5. **Calculate** calibration and accuracy metrics

## Target Variables

| Variable | Question | Change Pattern |
|----------|----------|----------------|
| HOMOSEX | "Is homosexual sex wrong?" | Strong liberalization |
| GRASS | "Should marijuana be legal?" | Strong liberalization |
| FEPOL | "Women not suited for politics" | Steady decline |
| PREMARSX | "Is premarital sex wrong?" | Moderate liberalization |
| CAPPUN | "Favor death penalty?" | Fluctuation then decline |

## Key Design Choices

- **No fine-tuning**: Use base models or API models with careful prompting to avoid contaminating with post-cutoff moral attitudes
- **Uncertainty quantification**: Ask for probability distributions, not point estimates
- **Multiple cutoff years**: Test generalization across different historical periods
- **Baselines**: Compare against naive extrapolation and demographic shift models

## Installation

```bash
uv venv
source .venv/bin/activate
uv pip install -e .
```

## Usage

```bash
# Download GSS data
python scripts/download_gss.py

# Run forecasting experiment
python scripts/forecast.py --cutoff 2000 --target HOMOSEX

# Evaluate results
python scripts/evaluate.py
```

## Results

*Experiment in progress*

## References

- General Social Survey: https://gss.norc.org/
- Argyle et al. (2023): Silicon sampling methodology
- Society in Silico: https://society-in-silico.org/
