# Value forecasting

Can anything — language models included — forecast how measured human values change?

This repo holds a **pre-registered, contamination-controlled evaluation** of value forecasting against the 2024 General Social Survey, plus the paper and analysis code. We committed the analysis plan before any forecasting API call; every number in the paper traces to committed result JSONs.

## Headline results (aligned horizon: history ≤ 2022 → forecast 2024, n = 20 items)

- **GSS 2024 reversed 8 of 20 pre-2022 trends**, four by the largest single-wave decline in the item's recorded series (PRAYER −8.4, HOMOSEX −6.8, FEFAM −6.5, GRASS −5.7 points).
- **Nothing beat last-value persistence**: naive MAE 3.15 vs. 3.58–4.07 for the LLM arms (gpt-5-mini, gpt-4o, claude-opus-4-8) and 3.93 for o3.
- **LLM 90% intervals covered 50–55%** of actuals (clean arms); the naive and linear baselines' intervals covered 90% (ARIMA 80%).
- **Every arm missed the HOMOSEX reversal** (points 60.2–66.5 vs. actual 55.9).
- **An anonymization probe attributes identity-conditioned "LLM forecasting skill" to recall**: naming the item moved a long-horizon forecast by up to 30.5 points, and the LLM's edge over the best classical baseline flipped sign when the item was anonymized.

## Where things live

| Path | Contents |
|---|---|
| `paper/` | The paper (MyST source, `main.pdf`, references, local LaTeX template) |
| `ea-rewrite-2026-07/PREANALYSIS_PLAN.md` | Pre-registered design (committed before any model call, commit `0ec5fd3`) |
| `ea-rewrite-2026-07/RESULTS.md` | Full results summary, including post-registration robustness arms |
| `ea-rewrite-2026-07/code/` | Extraction, baselines, forecasts, analysis, figures (numbered scripts) |
| `ea-rewrite-2026-07/results/` | Committed result JSONs — every paper number traces here |
| `ea-rewrite-2026-07/figures/` | Paper figures (PDF/PNG/SVG) |
| `ea-rewrite-2026-07/post-draft.md` | Companion essay draft |
| `archive/paper-2024/` | Superseded 2024 paper draft (leaky pilot design; do not cite) |
| `app/` | React visualization app (predates the rewrite) |

## Reproducing

The repo does not include the GSS microdata (NORC distributes them); download the cumulative 1972–2024 file (Release 2) from [gss.norc.org](https://gss.norc.org/) to `data/gss7224_r2.dta`, then:

```bash
cd ea-rewrite-2026-07/code
python 01_extract_gss.py      # weighted series -> results/gss_series.json
python 02_baselines.py        # naive/linear/ARIMA/ETS -> results/baselines.json
python 03_llm_forecasts.py    # LLM arms (needs API keys; ~$0.19)
python 04_analysis.py         # metrics -> results/analysis.json
python 06_figures.py          # figures -> ../figures/
```

Build the paper: `myst build --pdf paper/main.md` (LaTeX required; the template is vendored in `paper/template/`).

## References

- General Social Survey: https://gss.norc.org/
- Halawi et al. (2024), forward LLM forecasting: https://arxiv.org/abs/2402.18563
- Argyle et al. (2023), silicon sampling: https://arxiv.org/abs/2209.06899
- Society in Silico: https://society-in-silico.org/
