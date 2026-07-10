# Pre-analysis plan — value forecasting with current models (2026-07)

Pre-registered before any forecasting API call. Committed first; results follow.

## Questions

1. On a **strictly clean** held-out wave (GSS 2024, released 2025), can a current
   LLM whose training cutoff predates the release forecast attitude shares better
   than standard time-series baselines?
2. Does the "everyone is overconfident" calibration finding replicate?
3. Do LLMs miss trajectory **inflections** (e.g. the HOMOSEX reversal)?
4. How much of any LLM edge on long horizons is learned dynamics vs **memorized
   item history** (anonymized-series probe)?

## Data and estimation

- Source: `~/value-forecasting/data/gss7224_r2.dta` (cumulative GSS 1972–2024, R2).
- **Survey-weighted** annual shares. Weight: `wtssall` for years ≤ 2018;
  `wtssnrps` (non-response-adjusted, probability subsample) for 2021/2022/2024
  (NORC's recommended post-2018 weight). Fallback to `wtssps` then unweighted if a
  weight column is missing for a wave; the choice used is recorded per wave.
- For each variable-year: share giving the specified response among valid responses
  (exclude DK/refused/NA/IAP). Require **≥ 50 unweighted valid n** in a wave to use
  it; require the variable to be present in **2024** and to have **≥ 6 waves** total.
- Sanity gate: computed HOMOSEX "not wrong at all" must land ≈ 61% (2022) and ≈ 55%
  (2024); if not, the weight/recode is wrong.

## Variables (pre-registered candidate set; availability trims to the final set)

Deliberate mix of monotonic, stable, and non-monotonic cases. "Target response" =
the share we forecast.

| Var | Target response | Ex-ante shape (≤2022) |
|---|---|---|
| HOMOSEX | not wrong at all | monotonic ↑ |
| GRASS | should be legal | monotonic ↑ |
| PREMARSX | not wrong at all | ↑ then plateau |
| MARHOMO | agree same-sex couples may marry | monotonic ↑ (from 1988) |
| FEFAM | disagree (woman need not tend home) | monotonic ↑ |
| FEPOL | disagree (women suited for politics) | ↑ then plateau |
| SPKHOMO | allowed to speak | monotonic ↑ (ceiling) |
| SPKATH | allowed to speak | monotonic ↑ |
| ABANY | yes (any reason) | ↑ |
| CAPPUN | oppose death penalty | ↑ to ~2016 then flat |
| POLVIEWS | liberal side (1–3 of 7) | stable |
| EQWLTH | govt reduce differences (1–3 of 7) | thermostatic |
| HELPPOOR | govt should help (1–2 of 5) | thermostatic |
| GUNLAW | favor permit | stable / slight ↓ |
| NATRACE | too little (assistance to Black Americans) | thermostatic |
| NATENVIR | too little (environment) | thermostatic |
| NATFARE | too little (welfare) | thermostatic (low) |
| NATHEAL | too little (health) | thermostatic |
| NATEDUC | too little (education) | stable-high |
| TRUST | most people can be trusted | ↓ |
| FAIR | people try to be fair | ↓ |
| PRAYER | approve ban on school prayer | stable |

Codings verified against the microdata value labels at extraction; any deviation
is recorded in `results/gss_series.json`.

Two ex-post stratifications for error analysis (descriptive, not forecast inputs):
(a) ex-ante class from the ≤2022 OLS slope + R²; (b) 2024 behavior vs the ≤2022
trend: **continuation / reversal / stable**.

## Forecasting design

- **Primary (clean & fair):** history through **2022** → forecast **2024**. The
  shown history matches each model's own knowledge horizon (all three models know
  GSS ≤ 2022), so the LLM cannot beat baselines by recalling un-shown waves.
- **Long horizon (illustrative):** history through **2010** → forecast **2024**.
  Here the LLM's training knowledge (≤ its cutoff) covers 2012–2022, which it was
  not shown — deliberately confounded, to be dissected by the probe below.
- **Distribution arm:** full response-category distribution for ordinal items
  (HOMOSEX 4 cats; PREMARSX 4 cats; POLVIEWS 7 cats) — clean vs contaminated.
- **Anonymized-series probe:** re-run the clean LLM with variable identity stripped
  (numeric series + only "a US attitude item, higher = more of the target response";
  no name/description). If the LLM edge survives anonymization it is dynamics; if it
  collapses it was memorized identity/history.

## Model arms and contamination labels

| Arm | Model | Cutoff | GSS-2024 status | Settings |
|---|---|---|---|---|
| Clean (headline) | `gpt-5-mini` | 2024-05 | clean | reasoning_effort=minimal, seed=1930 |
| Clean (robustness) | `gpt-4o` | 2023-10 | clean | temperature=0, seed=1930 |
| Contaminated (ceiling) | `claude-opus-4-8` | 2026-01 | contaminated | default |

Baselines (computed on the weighted series, one point + 90% interval each):
**naive** (last value; interval from historical first-difference SD), **linear**
(OLS on logit scale, t-based PI), **ARIMA(1,1,0)** (statsmodels, model PI),
**ETS/Holt** (additive trend, model PI). Baselines index by wave sequence and
forecast the step(s) to 2024.

## Metrics (every arm, n reported inline everywhere)

- Point: **MAE**, **bias** (mean signed error), median AE, over the n variables.
- Calibration: **90% CI coverage** (fraction with actual ∈ [lo,hi]) + mean width.
- Decomposition: MAE within {continuation, reversal, stable} strata.
- Distribution arm: mean per-category MAE and **total-variation distance**
  (½ Σ|p̂−p|) vs actual, clean vs contaminated.
- Probe: identified vs anonymized MAE and edge-over-naive for `gpt-5-mini`.

Every LLM-vs-baseline comparison is stated as "MAE X vs <baseline> Y (ratio),
n = N", never a bare multiple.

## Pre-registered expectations (falsifiable)

1. All arms miss the HOMOSEX 2024 reversal (point ≥ 60%; actual ≈ 55%).
2. Overconfidence replicates: 90% coverage < 0.90 for every arm.
3. On the aligned clean horizon, the clean LLM's MAE is **within ~1 pt** of the best
   simple baseline (naive/ETS) — the old "LLM ≫ baselines" does **not** replicate
   once horizon is aligned and n is large.
4. Contaminated Claude ≈ clean gpt-5-mini on accuracy (internal contamination
   check). A large Claude edge that nails reversals would flag memorization.
5. On the long horizon, the identified LLM shows an edge over baselines that
   **collapses** under anonymization.

Whatever the outcome, it is reported as-is; failed predictions are stated plainly.

## Budget, logging, reproducibility

- Hard cap **$25** total API spend; expected ≪ $2. Per-call token usage and
  per-arm cost logged to `results/costs.json` using published prices
  (gpt-5-mini $0.25/$2.00, gpt-4o $2.50/$10.00, claude-opus-4-8 $5/$25 per 1M).
  If the right design needed more than $25, stop and report rather than exceed.
- One draw per forecast (LLM nondeterminism noted as a caveat); seeds set where the
  API supports them. All prompts + raw completions saved to `results/`.
- Code in `ea-rewrite-2026-07/code/`, outputs in `ea-rewrite-2026-07/results/`,
  run with `~/value-forecasting/.venv/bin/python`.
