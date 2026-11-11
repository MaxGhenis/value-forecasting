---
title: Methodology
---

# Methodology

We committed the design to [PREANALYSIS_PLAN.md](https://github.com/MaxGhenis/value-forecasting/blob/0ec5fd3/ea-rewrite-2026-07/PREANALYSIS_PLAN.md) before any forecasting call, and [the paper](../paper/main.md) describes it in full.

- **Data:** GSS cumulative 1972–2024 (Release 2), survey-weighted target-response shares for 20 attitude items (≥ 50 valid responses per wave, ≥ 6 waves, present in 2024).
- **Holdout:** GSS 2024, whose microdata NORC first released in 2025. We label each arm clean or contaminated by the vendor's stated training cutoff relative to the end of 2024 fieldwork.
- **Aligned horizon:** models see history through 2022, matching their training knowledge, and forecast 2024 with a point and a 90% interval; we compute the naive, linear and ARIMA baselines on the logit scale.
- **Probes:** we re-run the forecasts with each item's identity stripped, to separate dynamics from recall, and run a contaminated model as a memorization check.

The repository keeps a two-item pilot (named items, forecast targets inside the training window, unweighted shares) in `archive/` as a design contrast, and the paper traces each of its findings through the controlled design.
