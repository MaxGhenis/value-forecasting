# Project status

Last updated: 2026-11-09

## Current state

The pre-registered evaluation lives in `ea-rewrite-2026-07/`, and the paper (`paper/main.md`, built to `paper/main.pdf`) reports it. We committed the pre-analysis plan before any forecasting call (`0ec5fd3`). The repository keeps the December 2025 paper draft in `archive/paper-2024/`; it rests on an identity-conditioned pilot (n = 2, targets inside the training window) and long-horizon projections, and the paper supersedes it.

## Key findings (see `ea-rewrite-2026-07/RESULTS.md` for all tables)

1. **GSS 2024 reversed 8 of 20 pre-2022 trends**, four with the largest single-wave decline in the item's recorded series. HOMOSEX ("not wrong at all"): 62.7 (2022) → 55.9 (2024).
2. **Nothing beat naive persistence** at the aligned ≤2022→2024 horizon: naive MAE 3.15 vs. 3.58–4.07 for the pre-registered LLM arms and 3.93 for o3 (n = 20).
3. **Trend-followers' intervals ran too narrow**: clean-arm 90% intervals covered 50–55% and the corrected post-registration ETS 60%, against 90% for naive and linear (ARIMA 80%). Every arm missed the HOMOSEX reversal (points 60.2–66.5).
4. **Identity-conditioned "skill" rides largely on item identity**: anonymizing the series moved gpt-5-mini's 2010-cutoff HOMOSEX forecast 30.5 points (78.0 → 47.5) and flipped its edge over ARIMA (+0.41 → −0.07); the corrected ETS (5.52) beats the identified LLM (7.25) outright at that horizon.
5. Raising reasoning effort did not help (gpt-5-mini 4.07 → 4.16 → 4.21 MAE, the last on a partial n = 11 arm). Anthropic has retired every clean-eligible Claude snapshot from its first-party API, so the study has no clean Anthropic arm.

## Open items

- Publish the companion essay (`ea-rewrite-2026-07/post-draft.md`) and choose the paper's venue (arXiv cs.CY or a workshop).
- Forward pre-registration for GSS 2026 and 2028: paper §8 describes it as planned, pending the author's confirmation, with the binding registration as its own commit. NORC scheduled GSS 2026 fieldwork for May–November 2026, so §8's "before GSS 2026 fieldwork begins" can no longer hold, and the 2026 timing awaits the author's decision.
- Talkie-1930 sensor-mode evaluation when the GPT-3-level checkpoint ships (paper §6; `results/talkie_gallup_probes/`). As of 2026-11-09, talkie-lm.com lists only the April 2026 13B release.
- A resumed robustness run (the full high-effort arm, a DeepSeek arm and more anonymized runs) has not reached the repository. Adding it means re-running `05_robustness_analysis.py` and revising the effort-sweep numbers that the essay and paper quote.

## Environment

The [README](README.md#reproducing) lists the data download and the full pipeline. To recompute the metrics and figures from the committed inputs:

```bash
cd ea-rewrite-2026-07/code
python 04_analysis.py   # metrics -> results/analysis.json
python 06_figures.py    # figures -> ../figures/
cd ../..
myst build --pdf        # paper -> paper/main.pdf (template vendored in paper/template/)
```
