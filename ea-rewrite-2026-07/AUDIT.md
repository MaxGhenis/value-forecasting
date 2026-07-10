# Phase 1 audit — value-forecasting repo (2026-07 rewrite)

Written on branch `ea-post-rewrite-2026-07`. Purpose: inventory what exists, what
is reproducible, what GSS extracts are present, and what the `talkie_cuda` results
contain, before re-running experiments with current models.

## Canonical clone

Two local clones exist, both with remote `github.com/MaxGhenis/value-forecasting.git`:

| Path | HEAD | State |
|---|---|---|
| `~/value-forecasting` | `23257de` (2026-02-22) | **Canonical.** `main == origin/main` (0/0 ahead-behind). Holds the 594 MB GSS microdata, forecast JSONs, `paper/`, and the untracked `talkie_cuda` results. |
| `~/MaxGhenis/value-forecasting` | `0fd24e6` (2025-12-16) | Stale (behind origin). Not used. |

`~/value-forecasting`'s working tree is dirty (deleted `.beads/*`, untracked
`results/` and `scripts/talkie_modal_cuda_*.py`), so this rewrite uses a fresh
worktree off `origin/main`:
`~/value-forecasting-worktrees/ea-post-rewrite-2026-07` (branch `ea-post-rewrite-2026-07`).
Analysis reads the microdata and venv from `~/value-forecasting` by absolute path.

## Existing forecasting experiments

All under `~/value-forecasting`. Reproducible given `data/gss7224_r2.dta` and
`OPENAI_API_KEY`; the venv (`.venv`, Python 3.14) needed `pyreadstat` + `statsmodels`
added.

| File | What it does | Reuse? |
|---|---|---|
| `scripts/extract_gss_time_series.py` | % "liberal" response by year, 16 vars. **Unweighted** (`n_liberal/len(vals)`), fragile string-matching on categorical labels. | Rebuild (add survey weights). |
| `scripts/extract_gss_trajectories.py` | Produces `data/trajectories.json` (17 vars, full series + summary). Also unweighted. | Rebuild. |
| `scripts/generate_baseline_forecasts.py` → `data/baseline_forecasts.json` | naive / linear / ARIMA / ETS baselines, logit-transformed, cutoff 2022, targets 2030–2100. | Reuse method; retarget to 2024 holdout. |
| `scripts/run_forecast_experiment.py` | Point forecasts, `gpt-3.5-turbo-instruct` / `gpt-4o`. Documents `MODEL_CUTOFFS`. Prompt puts the model "in year {cutoff}". | Rebuild with current models + JSON CI. |
| `scripts/calibrated_forecast.py` → `data/calibration_gpt-4o_2021_2024.json`, `data/longterm_gpt-4o_calibrated.json` | EMOS quantile elicitation + CRPS spread calibration on gpt-4o. Produced spread multiplier **1.207** ("CIs need 21% widening"). | Reference; re-derive coverage per arm. |
| `results/forecasts.json` | The **old n=2 experiment**: HOMOSEX + GRASS only, cutoffs 1990/2000, LLM = `claude-sonnet-4-20250514`, baseline = `linear_extrapolation`. This is the basis of the EA draft's "2.2×" claim. | Superseded. |
| `app/` | React (Vite + Recharts) viz of the forecasts. | Untouched. |
| `paper/*.md` | MyST academic paper (16-var version). | Reference only. |

### Methodological issues found in the existing pipeline

1. **Unweighted estimates.** All series are simple response counts; GSS requires
   survey weights (`wtssall` through 2018, `wtssnrps`/`wtssps` for 2021+). The
   published `54.7%` HOMOSEX-2024 figure is unweighted. Rebuild computes weighted
   shares and sanity-checks against known values.
2. **Contamination of the *conditioning*, not just the target.** `run_forecast_experiment.py`
   shows a model only history ≤ cutoff (e.g. 2010) but the model's own training
   knowledge extends to its cutoff (gpt-4o → Oct 2023; it already "knows" GSS
   2012–2022). A 2010→2024 "forecast" therefore lets the model recall 2012–2022
   actuals it wasn't shown. This inflates the apparent LLM edge on long horizons.
   The 2026-07 design fixes this (primary test aligns shown-history with model
   knowledge: ≤2022 → 2024) and quantifies the recall effect with an
   anonymized-series probe.
3. **Small-n relative-performance framing.** The EA draft's "LLM beats ETS by 2.2×"
   came from `results/forecasts.json` (n=2 variables). Every relative claim in the
   rewrite carries its baseline + n inline.

## GSS data extracts present (`~/value-forecasting/data/`, all gitignored except JSONs)

| File | Size | Notes |
|---|---|---|
| `gss7224_r2.dta` | 594 MB | Cumulative GSS 1972–2024, **Release 2** (Oct 2025). Untracked (gitignored). |
| `GSS 2024 Codebook R2.pdf`, `... Whats New R2.pdf`, `... Release Variables R2.pdf`, `Release Notes 7224 R2.pdf` | — | R2 = Oct 2025. Release notes confirm R1 was an earlier 2025 release; NORC is now at R3. R2's disclosure-driven category reductions affect demographic vars only (EARNRS, HISPANIC, …), **not** the attitude items used here. |
| `trajectories.json` (tracked) | 16 KB | 17-var unweighted series; HOMOSEX last_value 54.7 (2024), GRASS 68.5. |
| `baseline_forecasts.json` (tracked) | 38 KB | naive/linear/arima/ets, cutoff 2022. |
| `calibration_gpt-4o_2021_2024.json`, `longterm_gpt-4o_calibrated.json`, `experiment_gpt-3.5-turbo-instruct_2010_2024.json` (tracked) | — | Prior LLM runs. |

## `talkie_cuda` results (`~/value-forecasting/results/talkie_cuda/`, 45 MB, untracked)

18 result JSONs + raw logs from 2026-04-29 Modal/CUDA (A100-40GB) runs of the
`talkie-1930-13b` base and instruction-tuned checkpoints (and the `talkie-web-13b`
modern-web twin). These are the experimental substrate behind Max's published blog
post `maxghenis.com/blog/talkie-1930-math-evals` and the `github.com/MaxGhenis/talkie-evals`
repo. Contents:

- `gsm8k_eval_*` — GSM8K runs (zero-shot / 5-shot; strict + flexible parsers).
- `arithmetic_eval_*` — EleutherAI/OpenAI arithmetic suite, three models, log-likelihood scoring.
- `gallup_majority_*`, `gallup_prompt_search_*`, `gallup_sanity_*` — **opinion-elicitation probes**: attempts to get Talkie-1930 to answer Gallup-style attitude questions. Directly relevant to the post's "vintage LLM as attitude instrument" section — they show the elicitation layer, not the knowledge layer, is the bottleneck.
- `comprehension_suite_*`, `format_search_*`, `explanation_ablation_*`, `support_share_search_*`, `targeted_support_prompt_*`, `unprimed_support_ablation_*`, `disambiguate_*` — prompt/format sensitivity probes.

Published headline numbers (from the blog post, which the rewrite cites verbatim):
Talkie-1930-13b base ≈ GPT-3-175B on rote arithmetic completion (42.7% overall on
the 10-task suite; 91.6% on 2-digit addition), but 4.9% strict / 7.2% flexible on
5-shot GSM8K vs 17.8% for same-size LLaMA-13B — a capability split at the
elicitation layer, not the knowledge layer.

**Decision:** the 45 MB `talkie_cuda` tree is Max's pre-existing artifact and is not
committed to this branch (it would bloat the repo and lives canonically in
`talkie-evals`). It is documented here and cited via the blog post.

## Contamination reference (verified 2026-07-10)

| Model | Knowledge cutoff | Clean for GSS 2024 (released 2025)? | Role |
|---|---|---|---|
| `gpt-5-mini` | 2024-05-31 (OpenAI API docs) | **Yes** — cutoff strictly predates the 2025 release | Headline clean arm |
| `gpt-4o` | 2023-10 | Yes | Clean robustness arm |
| `claude-opus-4-8` | 2026-01 | **No** — cutoff postdates release | Contaminated capability-ceiling arm |

GSS wave release timing (for labeling any arm clean/contaminated):
GSS 2021 ≈ Nov 2021; GSS 2022 ≈ 2023; **GSS 2024 first public microdata = 2025**
(field period Apr–Dec 2024; R2 = Oct 2025). The old draft/paper's "released late
2024" is incorrect and is corrected in the rewrite.

## Known errors in the old EA draft to fix (per task brief + this audit)

1. The "1986: 32%" same-sex-**marriage** figure is unsourced. Use properly sourced
   series (Gallup marriage support starts 1996 at 27%; GSS `MARHOMO` starts 1988 at ~11–12%).
2. Every relative-performance claim must carry baseline + n inline (fixes the "2.2×
   vs ETS on n=2" framing).
3. GSS `HOMOSEX` "not wrong at all" trajectory is ~61%→55% (2022→2024); never 72%
   (that is Gallup's differently-worded acceptance series).
