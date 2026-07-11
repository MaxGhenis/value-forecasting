---
title: Results
---

# Results

Full tables live in [RESULTS.md](https://github.com/MaxGhenis/value-forecasting/blob/ea-post-rewrite-2026-07/ea-rewrite-2026-07/RESULTS.md); every number traces to the committed JSONs in `ea-rewrite-2026-07/results/`. Aligned horizon (history ≤ 2022 → 2024, n = 20):

| Arm | MAE | 90% coverage |
|---|---|---|
| naive (last value) | **3.15** | 0.90 (18/20) |
| linear | 4.07 | 0.90 (18/20) |
| ARIMA(1,1,0) | 3.58 | 0.80 (16/20) |
| gpt-5-mini (clean) | 4.07 | 0.55 (11/20) |
| gpt-4o (clean) | 3.92 | 0.50 (10/20) |
| claude-opus-4-8 (contaminated) | 3.58 | 0.80 (16/20) |
| o3 (clean, post-registration) | 3.93 | 0.75 (15/20) |

Eight of twenty items reversed their pre-2022 trend in 2024; every arm's HOMOSEX point forecast landed at 60.2–66.5 against an actual of 55.9. At the 2010 cutoff, anonymizing the series moved gpt-5-mini's HOMOSEX "forecast" from 78.0 to 47.5 — a 30.5-point swing from the item name alone — and its edge over the best classical baseline (ARIMA) flipped from +0.41 to −0.07.

See [the paper](../paper/main.md) for figures, the pre-registered scorecard, and protocol recommendations.
