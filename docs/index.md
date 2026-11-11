---
title: Value forecasting
---

# Value forecasting

Can anything — language models included — forecast how measured human values change?

We ran a **pre-registered, contamination-controlled evaluation** against the 2024 General Social Survey. We forecast 20 attitude items from survey-weighted history through 2022 and labeled each model clean or contaminated by its vendor-stated training cutoff against the end of 2024 fieldwork. We committed the analysis plan before any forecasting call.

GSS 2024 reversed 8 of 20 pre-2022 trends, four with the largest single-wave decline in the item's series. Nothing beat last-value persistence: naive MAE 3.15 against 3.58–4.07 for the LLM arms, n = 20. The clean LLMs' 90% intervals covered 50–55% of actuals, while the naive and linear baselines' intervals covered 90%. An anonymization probe showed that identity-conditioned backtests measure recall blended with extrapolation: naming the item moved one long-horizon forecast by 30.5 points.

- **[The paper](../paper/main.md)** — full design, results, and protocol recommendations
- **[Results summary](https://github.com/MaxGhenis/value-forecasting/blob/main/ea-rewrite-2026-07/RESULTS.md)** — every table, with the committed JSON behind each number
- **[Pre-analysis plan](https://github.com/MaxGhenis/value-forecasting/blob/0ec5fd3/ea-rewrite-2026-07/PREANALYSIS_PLAN.md)** — the registered text, which we committed before any forecasting call
