# Project status

Last updated: 2026-07-11 (branch `ea-post-rewrite-2026-07`)

## Current state: pre-registered rewrite complete; paper drafted

The 2026-07 rewrite replaced the earlier pipeline end to end. The pre-analysis plan was committed before any forecasting call (`0ec5fd3`); results, robustness arms, figures, and a registered-report-style paper (`paper/main.md` → `paper/main.pdf`) are committed. The 2024 paper draft is archived at `archive/paper-2024/` — it rested on a leaky identity-conditioned pilot (n = 2, targets inside the training window) and EMOS long-term projections, and is superseded; do not cite or reuse its numbers.

## Key findings (see `ea-rewrite-2026-07/RESULTS.md` for all tables)

1. **GSS 2024 reversed 8 of 20 pre-2022 trends**; four were the largest single-wave decline in the item's recorded series. HOMOSEX ("not wrong at all"): 62.7 (2022) → 55.9 (2024).
2. **Nothing beat naive persistence** at the aligned ≤2022→2024 horizon: naive MAE 3.15 vs. 3.58–4.07 for the pre-registered LLM arms and 3.93 for o3 (n = 20).
3. **LLMs were confidently wrong**: clean-arm 90% intervals covered 50–55% vs. 90% for naive/linear intervals (ARIMA 80%). Every arm missed the HOMOSEX reversal (points 60.2–66.5).
4. **Identity-conditioned "skill" is largely recall**: anonymizing the series moved gpt-5-mini's 2010-cutoff HOMOSEX forecast 30.5 points (78.0 → 47.5) and flipped its edge over ARIMA (+0.41 → −0.07).
5. Raising reasoning effort did not help (gpt-5-mini 4.07 → 4.16 → 4.38 MAE, the last on a partial n = 10 arm); no clean Anthropic arm is possible — all clean-eligible Claude snapshots are retired from the first-party API.

## Open items

- Publish the companion essay (`ea-rewrite-2026-07/post-draft.md`) and decide the paper's venue (arXiv cs.CY / workshop).
- Forward pre-registration for GSS 2026/2028 (paper §8 is marked planned, pending Max's confirmation — it is not yet a registration).
- Talkie-1930 sensor-mode evaluation when the summer checkpoint ships (paper §6; `results/talkie_gallup_probes/`).
- Uncommitted working-tree files (`robustness_forecasts.json`, `robustness_costs.json`) contain a resumed robustness run (high-effort arm 20/20, a DeepSeek arm, extra anonymized runs) that postdates the committed analysis — decide whether to commit and re-run `05_robustness_analysis.py`, which would revise the effort-sweep numbers now quoted in the post and paper.

## Environment

```bash
cd /Users/maxghenis/value-forecasting   # canonical clone holds data/ and .venv
source .venv/bin/activate
export OPENAI_API_KEY=...               # only needed to re-run forecast arms

cd ea-rewrite-2026-07/code
python 04_analysis.py                   # recompute metrics from committed inputs
python 06_figures.py                    # regenerate figures

myst build --pdf paper/main.md          # build the paper (template vendored in paper/template/)
```
