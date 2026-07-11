---
title: Methodology
---

# Methodology

The current design is pre-registered in [PREANALYSIS_PLAN.md](https://github.com/MaxGhenis/value-forecasting/blob/ea-post-rewrite-2026-07/ea-rewrite-2026-07/PREANALYSIS_PLAN.md) (committed before any forecasting call) and described in full in [the paper](../paper/main.md). In brief:

- **Data:** GSS cumulative 1972–2024 (Release 2), survey-weighted target-response shares for 20 attitude items (≥ 50 valid responses per wave, ≥ 6 waves, present in 2024).
- **Holdout:** GSS 2024 (microdata first public in 2025). Arms are labeled clean or contaminated by the vendor's stated training cutoff relative to the end of 2024 fieldwork.
- **Aligned horizon:** models see history through 2022 — matching their training knowledge — and forecast 2024 with a point and a 90% interval, against naive/linear/ARIMA baselines computed on the logit scale.
- **Probes:** an anonymized-series re-run (item identity stripped) to separate dynamics from recall, and a contaminated-model arm as an internal memorization check.

An earlier pipeline (named items, forecast targets inside the training window, n = 2, unweighted) is preserved under `archive/paper-2024/` as a design-contrast exhibit only.
