# Value forecasting project

## Overview

Tests whether anything — LLMs included — can forecast measured human value change, using the General Social Survey as ground truth. Alignment framing: a system aligned to a forecast of where values are heading needs that forecast to be accurate and calibrated; this project measures whether it can be, under pre-registration and contamination controls.

## Current reality (2026-07)

The canonical experiment is the **2026-07 pre-registered rewrite** in `ea-rewrite-2026-07/`:

- Pre-analysis plan committed before any forecasting call (commit `0ec5fd3`): 20 GSS items, survey-weighted, aligned horizon (history ≤ 2022 → forecast 2024), clean vs. contaminated arms by vendor-stated cutoffs, anonymization probe, hard $25 budget cap.
- **Results** (all in `ea-rewrite-2026-07/RESULTS.md` and `results/*.json`): GSS 2024 reversed 8/20 trends (4 largest-ever single-wave declines); naive persistence MAE 3.15 beat every LLM arm (3.58–4.07 pre-registered, o3 3.93); clean LLM 90% CIs covered 50–55% vs. 90% for naive/linear (ARIMA 80%); every arm missed the HOMOSEX reversal (60.2–66.5 vs. actual 55.9); anonymization moved the identified 2010-cutoff HOMOSEX forecast 30.5 points and flipped the LLM-vs-ARIMA edge.
- **Paper**: `paper/main.md` (MyST) → `paper/main.pdf`; build with `myst build --pdf paper/main.md` (LaTeX template vendored in `paper/template/`). Figures from `ea-rewrite-2026-07/code/06_figures.py`.
- Companion essay draft: `ea-rewrite-2026-07/post-draft.md`.

## Superseded — do not cite or resurrect

`archive/paper-2024/` (old paper), old `scripts/` pipeline, and `data/longterm_*` / `data/calibration_*` JSONs rest on a **leaky pilot design**: named items, forecast targets inside the model's training window, n = 2, unweighted shares, plus EMOS-calibrated long-term projections (e.g., "HOMOSEX 80% by 2100"). The controlled design reverses the pilot's headline ("LLM beats the baseline 2.4x", 12.5 vs. 30.2 per `archive/pilot/forecasts.json` — the "2.2x/28.1" in old drafts does not reproduce → LLM 4.07 vs. naive 3.15, n = 20). Never quote the pilot's numbers as findings; they appear only as a design-contrast exhibit.

## Numbers discipline

- Every quantitative claim traces to `ea-rewrite-2026-07/results/*.json`; relative-performance claims carry baseline and n inline.
- HOMOSEX "not wrong at all" 2022 → 2024 is **62.7 → 55.9** (weighted). Never 72% (that's Gallup's differently-worded series); never the unweighted 54.7.
- The gpt-5-mini **high-effort robustness arm is partial (n = 11 of 20; 12 attempted, 1 parse failure)** — say so whenever quoting its 4.21 MAE / 7-of-11 coverage.
- Post-registration artifacts: `results/ets_corrected.json` (registered ETS with the input fix: aligned 4.33 MAE / 12-of-20 coverage; long 5.52) and `results/uncertainty.json` (paired CIs — claude-vs-naive spans zero, so say "no arm beat persistence," not "persistence beat every arm").
- GSS 2024 microdata first became public in 2025 (not late 2024); clean/contaminated labels follow vendor-stated cutoffs recorded in `results/robustness_analysis.json`.

## Structure

```
value-forecasting/
├── paper/                  # current paper (main.md, main.pdf, references.bib, template/)
├── ea-rewrite-2026-07/     # pre-registered experiment: plan, RESULTS.md, code/, results/, figures/
├── archive/paper-2024/     # superseded draft — do not cite
├── app/                    # React viz app (predates rewrite)
├── data/                   # GSS microdata (gitignored) + legacy JSONs
├── docs/                   # short site pages pointing at paper + RESULTS
└── scripts/                # legacy pipeline (superseded by ea-rewrite-2026-07/code/)
```

Data and venv live in the canonical clone `~/value-forecasting` (`data/gss7224_r2.dta`, `.venv`); worktrees read them by absolute path.

## Next steps

- Publish the essay; pick the paper venue (arXiv cs.CY + workshop shortlist in session notes).
- Forward pre-registration for GSS 2026/2028 — paper §8 says planned pending Max's explicit confirmation; the binding registration must be its own commit before GSS 2026 fieldwork begins.
- Talkie-1930 sensor-mode attitude evaluation at the summer checkpoint (log-prob elicitation; the probes in `results/talkie_gallup_probes/` already show chat elicitation failing).
- Working tree holds an uncommitted resumed robustness run (full n = 20 high-effort arm, DeepSeek arm, more anon probes) — committing it requires re-running `05_robustness_analysis.py` and updating the numbers quoted in the post and paper.
