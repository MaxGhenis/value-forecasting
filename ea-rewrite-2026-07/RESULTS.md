# Results summary — value forecasting rewrite (2026-07)

All numbers below come from the committed result files in `ea-rewrite-2026-07/results/`
(`gss_series.json`, `baselines.json`, `llm_forecasts.json`, `analysis.json`, `costs.json`).
The design was pre-registered in `PREANALYSIS_PLAN.md` and committed before any
forecasting API call; the repo audit is in `AUDIT.md`.

## Design

**Data.** GSS cumulative file 1972–2024, Release 2 (Oct 2025), survey-weighted
(`wtssall` for years ≤ 2018, `wtssnrps` for 2021+). For each item we forecast the
percent giving a pre-specified target response among substantive responses, requiring
≥ 50 unweighted valid responses per wave. 21 items extracted; 20 have a 2024 wave
(SPKHOMO does not), so **n = 20** everywhere below.

**Holdout.** GSS 2024 (fielded Apr–Dec 2024; first public microdata 2025).

**Horizons.**
- *Primary, aligned:* history through 2022 → forecast 2024. All three models' training
  knowledge covers GSS ≤ 2022, so shown history matches model knowledge and no arm can
  win by recalling un-shown waves.
- *Long, deliberately confounded:* history through 2010 → forecast 2024. Each model's
  training covers 2012–2022 (or later) history it was not shown; used only to measure
  the recall effect, via the anonymization probe.

**Arms.**

| Arm | Model (API id) | Knowledge cutoff | GSS-2024 status | Settings |
|---|---|---|---|---|
| Clean, headline | gpt-5-mini | 2024-05 | clean (cutoff predates 2025 release) | reasoning_effort=minimal, seed=1930 |
| Clean, robustness | gpt-4o | 2023-10 | clean | temperature=0, seed=1930 |
| Contaminated ceiling | claude-opus-4-8 | 2026-01 | contaminated (cutoff postdates release) | default |

One draw per forecast. Prompt: the weighted series by year plus (in the identified
condition) the GSS item description; the system prompt instructs the model to reason
only from the shown series and return `{point, lo90, hi90}` as JSON.

**Baselines** (on the logit scale, 90% intervals): naive (last value, random-walk
interval), linear (OLS with t-based PI), ARIMA(1,1,0), ETS/Holt.

> **ETS caveat:** the ETS prediction-interval extraction raises `AttributeError`
> under statsmodels 0.14.6 when given a bare numpy array (no pandas index), so the
> coded fallback returned the naive forecast for **all 20 variables**. In every table
> below, `ets` ≡ `naive`; there are effectively three distinct baselines.

**Probes.** (a) *Anonymized-series:* gpt-5-mini re-run with item identity stripped
("an anonymized US national survey attitude item"), both cutoffs. (b) *Distribution
arm:* full response-category distribution for HOMOSEX, PREMARSX, POLVIEWS
(gpt-5-mini and claude-opus-4-8), scored by total-variation distance.

## What GSS 2024 did (the 2024-behavior strata)

Mechanical classification (in `04_analysis.py`): slope over the last 5 waves ≤ 2022
vs the 2022→2024 change. Reversal = slope > +0.2 pt/yr and change < −2 pt (or the
mirror); stable = |change| ≤ 2 pt; continuation otherwise.

**Reversal (8):** PRAYER −8.35, HOMOSEX −6.78, NATRACE −6.68, FEFAM −6.45,
GRASS −5.69, PREMARSX −3.25, FEPOL −2.82, POLVIEWS −2.04.
**Continuation (3):** NATHEAL +5.45, FAIR −3.58, NATFARE +2.66.
**Stable (9):** the rest.

Four of the eight reversals are the largest single-wave decline in the item's entire
recorded series: PRAYER (−8.35 vs prior max −6.86, 27 waves since 1974), HOMOSEX
(−6.78 vs −2.47, 30 waves since 1973), FEFAM (−6.45 vs −5.97, 24 waves since 1977),
GRASS (−5.69 vs −4.79, 29 waves since 1973).

## Aggregate accuracy and calibration

### Primary horizon: ≤ 2022 → 2024 (clean; n = 20)

| Arm | MAE | Bias | Median AE | 90% CI coverage | Mean width | MAE rev / cont / stable |
|---|---|---|---|---|---|---|
| naive | **3.15** | +1.91 | 2.35 | 0.90 (18/20) | 12.01 | 5.26 / 3.90 / 1.03 |
| linear | 4.07 | +0.03 | 3.34 | 0.90 (18/20) | 15.05 | 3.41 / 5.36 / 4.23 |
| ARIMA(1,1,0) | 3.58 | +2.22 | 2.69 | 0.80 (16/20) | 11.61 | 5.28 / 4.82 / 1.65 |
| ETS (= naive; see caveat) | 3.15 | +1.91 | 2.35 | 0.90 (18/20) | 12.01 | 5.26 / 3.90 / 1.03 |
| gpt-5-mini (clean) | 4.07 | +2.20 | 3.85 | **0.55 (11/20)** | 8.63 | 6.30 / 5.14 / 1.73 |
| gpt-4o (clean) | 3.92 | +2.50 | 3.60 | **0.50 (10/20)** | 7.55 | 6.11 / 5.14 / 1.56 |
| claude-opus-4-8 (contam.) | 3.58 | +1.81 | 2.87 | 0.80 (16/20) | 11.03 | 5.42 / 5.48 / 1.31 |

- Clean gpt-5-mini MAE 4.07 vs best simple baseline (naive) 3.15 → ratio **1.29**
  (pre-registered check: within ~1 pt of the best simple baseline, on the worse side).
- Every arm has positive bias except linear ≈ 0: forecasts sat above the 2024 actuals
  on average.
- On the 8 reversal items, both clean LLMs (6.30, 6.11) erred more than naive
  persistence (5.26): they extrapolated recent trends and the trends broke.

### Long horizon: ≤ 2010 → 2024 (confounded by training knowledge; n = 20)

| Arm | MAE | Bias | 90% CI coverage | Mean width | MAE rev / cont / stable |
|---|---|---|---|---|---|
| naive | 8.55 | −6.03 | 0.95 (19/20) | 31.34 | 8.46 / 11.55 / 7.63 |
| linear | 7.68 | −2.09 | 0.55 (11/20) | 14.78 | 7.08 / 5.67 / 8.88 |
| ARIMA(1,1,0) | 7.66 | −5.33 | 0.80 (16/20) | 26.78 | 7.30 / 9.32 / 7.42 |
| ETS (= naive) | 8.55 | −6.03 | 0.95 (19/20) | 31.34 | 8.46 / 11.55 / 7.63 |
| gpt-5-mini | 7.25 | −1.58 | 0.50 (10/20) | 10.97 | 7.39 / 8.81 / 6.61 |
| gpt-4o | 5.83 | −2.52 | 0.55 (11/20) | 8.92 | 4.22 / 7.64 / 6.67 |
| claude-opus-4-8 | 4.18 | −1.38 | 0.90 (18/20) | 16.15 | 2.89 / 5.98 / 4.72 |

The ordering (claude 4.18 < gpt-4o 5.83 < gpt-5-mini 7.25 < baselines) tracks access
to un-shown history, most visibly in claude's reversal-class MAE of 2.89 — it "knows"
the 2012–2024 record it was not shown. This horizon exists to be dissected by the
probe below, not to rank forecasting skill.

## The reversal miss

**HOMOSEX** ("not wrong at all"): actual 2024 = **55.94** (weighted; unweighted valid
n = 2,125), down from 62.72 in 2022.

| Arm | Point | 90% interval | Contains actual? |
|---|---|---|---|
| naive / ETS | 62.72 | [56.77, 68.31] | no |
| linear | 60.22 | [49.20, 70.29] | **yes** (width 21.1) |
| ARIMA | 63.08 | [56.41, 69.28] | no |
| gpt-5-mini | 66.5 | [62.0, 70.5] | no |
| gpt-4o | 64.5 | [61.0, 68.0] | no |
| claude-opus-4-8 | 64.0 | [59.0, 69.0] | no |

Every point forecast landed in 60.2–66.5 against an actual of 55.9. The only interval
containing the truth (linear) did so by being 21 points wide, not by anticipating a
downturn. The anonymized gpt-5-mini run gave 67.0 [61, 73] — also a miss, so at the
aligned horizon the failure is dynamics, not item identity.

**90% CI coverage across the 8 reversal items (aligned horizon):**
naive 6/8 · linear 7/8 · ARIMA 6/8 · **gpt-5-mini 1/8 · gpt-4o 0/8 · claude 4/8**.

## Anonymized-series probe (gpt-5-mini)

| Cutoff | Identified MAE | Anonymized MAE | Naive MAE | Edge over naive (ident.) | Edge over naive (anon.) |
|---|---|---|---|---|---|
| 2022 | 4.07 | 4.62 | 3.15 | −0.92 | −1.47 |
| 2010 | 7.25 | 7.73 | 8.55 | +1.30 | +0.82 |

- Mean |identified − anonymized| point difference: **1.01 pt** at the 2022 cutoff vs
  **4.51 pt** at the 2010 cutoff (n = 20 each).
- Items moving ≥ 5 pt at the 2010 cutoff: HOMOSEX +30.5 (78.0 identified vs 47.5
  anonymized; actual 55.94), GRASS +17.0, PREMARSX +9.5, FEFAM +9.0 — the
  best-known liberalization trajectories in the set.
- Against the strongest classical baseline at 2010 (ARIMA, 7.66), the identified
  LLM's edge (+0.41) flips to −0.07 under anonymization.
- The pre-registered "collapse" prediction is therefore **partial**: the edge over
  naive shrinks by ~37% but stays positive; the edge over the best baseline
  disappears; individual identified "forecasts" move by up to 30.5 points on the
  item name alone.

## Contamination check (claude-opus-4-8)

At the aligned horizon the contaminated arm shows no memorization signature: MAE 3.58
vs clean gpt-5-mini's 4.07 (a 0.49-pt edge, both behind naive's 3.15), HOMOSEX at
64.0 [59, 69] (miss), 4/8 reversal coverage. At the long horizon its advantage
(4.18 vs 7.25, reversal MAE 2.89) is what recall of un-shown history predicts.

## Distribution arm (2024 full response distributions)

| Item | Arm | TV distance | Top-category error |
|---|---|---|---|
| HOMOSEX (4 cat.) | gpt-5-mini | 0.081 | +8.1 ("not wrong at all" 64 vs 55.9) |
| HOMOSEX | claude-opus-4-8 | 0.081 | +8.1 (64 vs 55.9) |
| PREMARSX (4 cat.) | gpt-5-mini | 0.054 | +5.4 |
| PREMARSX | claude-opus-4-8 | 0.043 | +3.4 |
| POLVIEWS (7 cat.) | gpt-5-mini | 0.021 | +0.4 |
| POLVIEWS | claude-opus-4-8 | 0.027 | −1.6 |

Category shapes are close (TV 0.02–0.08), but the top-category errors on the two
morality items reproduce the point arm's trend-continuation miss.

## Pre-registered expectations: scorecard

| # | Expectation | Outcome |
|---|---|---|
| 1 | All arms miss the HOMOSEX reversal (point ≥ 60 vs actual ≈ 55) | **Confirmed** — points 60.22–66.5 vs 55.94. (Linear's 21-pt-wide interval did contain the actual.) |
| 2 | Overconfidence replicates: 90% coverage < 0.90 for every arm | **Failed as stated** — LLM arms under-covered (0.50–0.80) but naive/linear/ETS hit 0.90 exactly. Only the LLMs are overconfident. |
| 3 | Clean LLM within ~1 pt of best simple baseline (no "LLM ≫ baselines") | **Confirmed** — 4.07 vs 3.15, Δ = 0.92 pt, LLM worse. |
| 4 | Contaminated ≈ clean at aligned horizon; no reversal-nailing | **Confirmed** — 3.58 vs 4.07; 4/8 reversal coverage; HOMOSEX missed. |
| 5 | Long-horizon identified edge collapses under anonymization | **Partial** — edge over naive 1.30 → 0.82; edge over ARIMA +0.41 → −0.07; per-item swings up to 30.5 pt. |

## Cost

| Model | Calls | Input tok | Output tok | USD |
|---|---|---|---|---|
| gpt-5-mini | 83 | 31,892 | 2,530 | $0.013 |
| gpt-4o | 40 | 15,688 | 1,040 | $0.050 |
| claude-opus-4-8 | 43 | 18,559 | 1,397 | $0.128 |
| **Total** | **166** | | | **$0.19** |

Budget cap was $25 with an abort guard; actual spend $0.19.

## Limitations

- One draw per forecast (seeds set where supported); LLM nondeterminism unquantified.
- gpt-5-mini ran at `reasoning_effort=minimal` in the pre-registered arm; see the
  post-registration robustness section below for medium/high effort.
- ETS fell back to naive for all items (statsmodels 0.14.6 PI-extraction bug above).
- Single holdout wave; the reversal/continuation/stable strata are ex-post
  descriptive labels, not forecast inputs.
- GSS moved to mixed web/phone/in-person modes after 2018; NORC documents mode
  effects, which may contribute to level shifts across waves.

## Post-registration robustness arms (added after registration; separate files)

Run after the pre-registered record was committed, to answer three anticipated
objections. Results in `robustness_forecasts.json` / `robustness_analysis.json` /
`robustness_costs.json`; the pre-registered files are untouched. Same protocol,
prompts, items, and metrics; aligned horizon (history ≤ 2022 → 2024, n = 20).

| Arm | Stated cutoff (vendor URL in results meta) | Label | MAE | 90% cov | Reversal MAE | HOMOSEX (actual 55.9) |
|---|---|---|---|---|---|---|
| o3 (default effort) | 2024-06-01 | clean | 3.93 | 0.75 | 6.26 | 65.0 [59.0, 71.0] — miss |
| gpt-5-mini, medium effort | 2024-05-31 | clean | 4.16 | 0.75 | 7.11 | 65.2 [60.0, 70.4] — miss |
| gpt-5-mini, high effort | 2024-05-31 | clean | 4.21 (n = 11) | 0.64 (7/11) | 7.03 | 66.3 [62.1, 70.5] — miss |

Reference points from the pre-registered arms: naive 3.15 MAE / 0.90 coverage;
gpt-5-mini-minimal 4.07 / 0.55.

Findings: (1) the strongest clean-eligible reasoning model posts higher empirical
coverage (0.75 vs 0.50–0.55) but still trails persistence and misses the reversal;
(2) raising gpt-5-mini's reasoning effort buys no improvement
(4.07 → 4.16 → 4.21, the last on the partial n = 11 arm; on the common 11-item
subset: 3.91 → 3.93 → 4.21 vs naive 2.56) — deliberation toward the same wrong prior;
(3) **no clean Anthropic arm is possible**: every Claude snapshot with a cutoff
≤ Dec 2024 has been retired from the API (claude-3-5-sonnet-20241022 → 404,
retired 2025-10-28 per Anthropic's model lifecycle) — the clean-evaluation window
closes as vendors deprecate snapshots; (4) a DeepSeek open-weights arm was skipped
because the vendor documents no training cutoff, so it cannot be labeled clean.

Cost: $0.88 measured across 30 calls (gpt-5-mini-high segment, per the committed
`robustness_costs.json`); the o3 and medium-effort segments' cost logging was lost
to a session crash mid-run (~$1 estimated total); every call's parsed output is
preserved in `robustness_forecasts.json`. The high-effort arm attempted 12 items,
with one parse failure, so 11 score; `robustness_analysis.json` is regenerated
from the committed forecasts (2026-07-11 — an earlier snapshot had scored n = 10
before the GUNLAW cell landed).

## Post-registration corrections and uncertainty (2026-07-11, referee-prompted)

- **Corrected ETS** (`code/07_ets_corrected.py` → `results/ets_corrected.json`):
  the registered run passed a bare array where statsmodels' ETSModel prediction
  interface needs an indexed series — a caller-side input error, not a library
  bug — so ETS silently duplicated naive. The registered spec with the one-line
  fix gives, aligned: MAE 4.33, coverage 12/20, width 11.0, HOMOSEX 64.9
  [59.2, 70.1] (miss); long horizon: MAE 5.52, coverage 13/20 — a classical
  trend-follower with LLM-grade under-coverage, and at the long horizon better
  than the identified gpt-5-mini (5.52 vs 7.25). The honest calibration split is
  flat vs trend-following, not classical vs LLM.
- **Uncertainty** (`code/08_uncertainty.py` → `results/uncertainty.json`):
  naive's MAE edge resolves against the clean arms (gpt-5-mini +0.92, boot 95%
  CI [+0.14, +1.64]; gpt-4o +0.77 [+0.06, +1.40]) but not claude-opus-4-8
  (+0.43 [−0.06, +0.90]) — say "no arm beat persistence," not "persistence beat
  every arm." Coverage: 11/20 and 10/20 vs nominal 0.90, binomial p < 1e-4;
  discordant pairs vs naive 7:0 and 8:0. Reversal-stratum MAE contrast is
  descriptive (n = 8, p ≈ 0.3). Under SRS SEs (no design effects), 6 of the 8
  reversal changes clear 95%; FEPOL and POLVIEWS do not.
- **Linear intervals**: the plan registered t-based; the code used z = 1.645
  (slightly narrow; coverage unchanged at 18/20). Disclosed, not patched.
- **Pilot artifact**: the n = 2 pilot's raw forecasts now live at
  `archive/pilot/forecasts.json`; its aggregates are LLM MAE 12.5 vs baseline
  30.2 (2.4x, only baseline = linear extrapolation), coverage 6/14 vs 5/14.
  The "2.2x / 28.1" figures quoted in earlier drafts do not reproduce from it.
