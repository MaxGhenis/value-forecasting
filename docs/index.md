---
title: Value forecasting
---

# Value forecasting

Can anything — language models included — forecast how measured human values change?

This project ran a **pre-registered, contamination-controlled evaluation** against the 2024 General Social Survey: we forecast 20 attitude items from survey-weighted history through 2022, verified model training cutoffs against the holdout's release date, and committed the analysis plan before any forecasting call.

**Headlines.** GSS 2024 reversed 8 of 20 pre-2022 trends (four by the largest single-wave decline ever recorded for the item). Nothing beat last-value persistence (naive MAE 3.15 vs. 3.58–4.07 for the LLM arms, n = 20); clean LLM 90% intervals covered 50–55% of actuals while the naive and linear baselines' intervals covered 90%; and an anonymization probe showed that identity-conditioned backtests measure recall blended with extrapolation — naming the item moved one long-horizon forecast by 30.5 points.

- **[The paper](../paper/main.md)** — full design, results, and protocol recommendations
- **[Results summary](https://github.com/MaxGhenis/value-forecasting/blob/ea-post-rewrite-2026-07/ea-rewrite-2026-07/RESULTS.md)** — every table, tracing to committed JSONs
- **[Pre-analysis plan](https://github.com/MaxGhenis/value-forecasting/blob/ea-post-rewrite-2026-07/ea-rewrite-2026-07/PREANALYSIS_PLAN.md)** — committed before any model call
