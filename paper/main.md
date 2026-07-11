---
title: "Do language models forecast value change, or recall it? A pre-registered evaluation on the 2024 General Social Survey"
short_title: "Do language models forecast value change, or recall it?"
authors:
  - name: Max Ghenis
    email: mghenis@gmail.com
    corresponding: true
date: 2026-07-11
keywords:
  - value forecasting
  - AI alignment
  - data contamination
  - calibration
  - General Social Survey
numbering:
  heading_2: true
  heading_3: true
bibliography:
  - references.bib
exports:
  - format: pdf
    template: ./template
    output: main.pdf
---

+++ {"part": "abstract"}

Whether machine systems can forecast the trajectory of human values is an empirically testable question with direct relevance to AI alignment: any proposal to align systems toward where values are heading needs the forecasting step to be accurate and, above all, honestly uncertain. We report a pre-registered evaluation against the 2024 General Social Survey: we forecast 20 attitude items from survey-weighted history through 2022, controlled training-data contamination with vendor-stated model cutoffs, and committed the analysis plan before any of its model calls. The 2024 wave was an unusually severe test — 8 of 20 items reversed their pre-2022 trend, four by the largest single-wave decline in their recorded series. At the aligned two-year horizon, every arm's point forecast for the same-sex-relations item landed between 60.2 and 66.5 against an actual of 55.9; no language model beat last-value persistence on accuracy (MAE 3.15 vs. 3.58–4.07 across pre-registered arms, n = 20); and clean-arm 90% intervals covered 50–55% of actuals while the naive and linear baselines' intervals covered 90%. An anonymization probe traces much of the "LLM forecasting skill" that identity-conditioned backtests report to item identity rather than learned dynamics: naming the item moved one model's long-horizon forecast by 30.5 points, and anonymization erased its edge over the strongest classical baseline that ran — the design contrast that turns a naive pilot's 2.4$\times$ "LLM beats the baseline" headline into this paper's negative result. We recommend anonymized-series reporting and strictly forward pre-registration as protocol standards, note that vendor model retirements are closing the window for retrospective clean evaluation, and outline forward-registered arms for GSS 2026 and 2028.

+++

## Introduction

A recurring proposal in AI alignment is to point systems not at a snapshot of present human preferences but at where human values are heading — post-reflection, post-deliberation, or simply later [@danaher2021; @macaskill2020]. Every version of that proposal contains an empirical subroutine: something must *forecast* value change, and if that step is unreliable — or worse, confidently wrong — alignment targets built on it inherit the failure. Unlike most alignment desiderata, this one is directly gradeable against half a century of resolved value measurement [@gneiting2007]. Large language models look like natural candidates: they have absorbed most of the written record of value change, and a growing "silicon sampling" literature reports that they reproduce human survey responses [@argyle2023; @santurkar2023; @durmus2023] and, in some studies, predict them. But the same property makes them treacherous to evaluate — a model that has *read about* the liberalization of American attitudes can reproduce it on demand, and a backtest that asks a model to "predict" survey waves inside its training window cannot distinguish forecasting from recall [@roberts2023]. Geopolitical LLM forecasting adopted a strictly forward evaluation standard for exactly this reason [@halawi2024]; value forecasting has not.

This paper reports what we believe is the first pre-registered, contamination-controlled evaluation of value forecasting with current models. We committed the design to a public repository before any forecasting API call (commit `0ec5fd3`, 2026-07-10) and stated falsifiable expectations in advance. The holdout is the 2024 wave of the General Social Survey (GSS), whose microdata first became public in 2025 — after every "clean" arm's vendor-stated training cutoff — and it was an unusually severe test: 8 of the 20 items we track reversed their pre-2022 trend, four posting the largest single-wave decline in their item's recorded history.

Three results follow: nothing beat last-value persistence on the aligned two-year horizon (best clean LLM MAE 3.92 vs. naive 3.15; the clean-arm gaps resolve under paired uncertainty, the contaminated arm's does not); the calibration failure split flat from trend-following, not classical from neural (clean LLM 90% intervals covered 50–55% of actuals and a corrected trend-following classical baseline 60%, against 90% for naive and linear); and an anonymization probe shows that the apparent LLM skill identity-conditioned designs report rides largely on item identity — naming the item moved one model's long-horizon "forecast" by 30.5 points and flipped the sign of its edge over the strongest classical baseline that ran. We close with protocol recommendations, a note on the closing window for retrospective clean evaluation, and a planned forward registration against GSS 2026 and 2028.

## Related work

**Silicon sampling, forecasting, and contamination.** @argyle2023 introduced LLMs conditioned on demographic personas as simulated survey samples; follow-on work measures whose opinions models reflect within the United States [@santurkar2023] and across countries [@durmus2023], fine-tunes models to predict opinion distributions [@suh2025], and extends the paradigm to prediction proper — retrodicting GSS attitudes across waves and imputing unasked items [@kim2023], or forecasting survey responses from media diets [@chu2023]. That literature mostly evaluates *reproduction* of measured opinion inside the model's training window — and when the target sits inside the training window and the design names the item, reproduction and forecasting are observationally confounded. @yang2024 make the adjacent case for social prediction generally: apparent LLM skill can ride on input shortcut features and collapse when they are removed. Geopolitical LLM forecasting solved the analogous problem by evaluating only on questions that resolve after data collection [@halawi2024]; we apply that discipline to value change, where survey resolution lags make strictly forward designs slow and a verified-cutoff retrospective design the practical intermediate. @roberts2023 exploit training cutoffs as a natural experiment and document benchmark performance tracking a problem's presence in training data rather than its difficulty; our anonymization probe is the survey-series analogue, measuring, item by item, how much of a "forecast" the name contributes.

**Calibration and scoring.** Proper scoring rules make honest probabilistic reporting the unique optimum [@gneiting2007], and the alignment-relevant property of a value forecast is less its point accuracy than its calibration: a system acting on a 90% interval that covers half the time is confidently wrong about the values it is optimizing around. Documented sycophancy pressure in preference-trained models [@sharma2023] is one mechanism for systematically narrow, agreeable intervals; scoring against resolved outcomes removes that gradient, though it does not constrain off-distribution behavior and inherits the performativity of any published social forecast [@perdomo2020].

## Pre-registered design

We committed the full plan — including five falsifiable expectations that the results below score — before any forecasting call of this evaluation (`ea-rewrite-2026-07/PREANALYSIS_PLAN.md`, commit `0ec5fd3`); results landed in later commits (first: `5823b96`). We summarize it here, and we state plainly what this registration does and does not bind. GSS 2024 was public when we wrote the plan — the plan itself quotes the HOMOSEX outcome as a sanity gate — so the registration makes the *models*, not the analyst, blind to 2024. It fixes prompts, arms, items, metrics, and expectations before any model output existed, which forecloses model-output-contingent analysis choices; it cannot rule out outcome-aware item selection, which we return to in the limitations.

### Data

We use the GSS cumulative microdata file, 1972–2024, Release 2 [@davern2025gss], with survey weights (`wtssall` for years ≤ 2018; `wtssnrps`, NORC's recommended non-response-adjusted weight, for 2021–2024). For each item we compute the weighted percent giving a pre-specified target response among substantive responses, requiring at least 50 unweighted valid responses per wave, at least 6 waves, and presence in the 2024 wave. Of the 22 pre-registered candidates, MARHOMO does not exist in the Release 2 cumulative file and produced no series (the plan promised to record deviations in `gss_series.json`; that note was missed, so we record the deviation here), and SPKHOMO extracted but lacks a 2024 wave — leaving **n = 20** for every full-item-set analysis. The set deliberately mixes monotonic (e.g., HOMOSEX, GRASS), stable (e.g., POLVIEWS, GUNLAW), and thermostatic (e.g., EQWLTH, NATHEAL) trajectories. A pre-registered sanity gate — the computed HOMOSEX "not wrong at all" share must land near 61% in 2022 and 55% in 2024 — guards the weight and recode logic (computed: 62.7 and 55.9).

**Holdout.** NORC fielded GSS 2024 from April to December 2024 and first released public microdata in 2025. A model whose vendor-stated training cutoff predates the end of fieldwork therefore cannot have seen any 2024 response.

### Horizons

**Primary, aligned:** history through 2022 $\rightarrow$ forecast 2024. All tested models' training knowledge covers published GSS results through 2022, so shown history matches each clean arm's knowledge horizon: no clean arm can gain by recalling waves we did not show it, and the comparison with classical baselines is fair with respect to GSS history (the LLMs retain item semantics and post-2022 world knowledge that univariate baselines lack; the contaminated arm may know the target itself, which is its job as a check). **Long, deliberately confounded:** history through 2010 $\rightarrow$ forecast 2024, where each model's training covers 2012–2022 outcomes we did *not show* it. The long horizon exists to measure the recall effect — the anonymization probe dissects it; we do not use it to rank forecasting skill.

### Arms, baselines, and probes

We pre-registered three model arms, recording each vendor-stated training cutoff in the committed record (the plan and audit for these arms; the robustness results carry cutoffs with source URLs): **clean, headline** — `gpt-5-mini` (cutoff 2024-05-31; reasoning_effort=minimal, seed 1930); **clean, robustness** — `gpt-4o` (cutoff 2023-10; temperature 0, seed 1930); **contaminated** — `claude-opus-4-8` (cutoff 2026-01; default settings; the plan labels it a "ceiling," but it functions as a memorization check, not a performance bound). Each forecast is a single draw returning JSON `{point, lo90, hi90}`; the prompt contains the weighted series by year plus, in the identified condition, the GSS item description, and instructs the model to reason only from the shown series. The contaminated arm is a deliberate internal check: its training window includes the GSS 2024 release itself, so a large accuracy edge — especially on reversals — would flag memorization leaking through the "reason only from the series" instruction.

**Baselines.** We compute four baselines on the logit scale with 90% intervals, indexing waves as equal steps (as registered; GSS waves fall one to three years apart): naive (last value, random-walk interval), linear (OLS prediction interval — the plan registered t-based intervals, but the code used the normal critical value 1.645, a slight narrowing we disclose rather than patch; coverage is unaffected at 18/20), ARIMA(1,1,0) (model interval), and ETS/Holt. The registered ETS run failed silently: our code passed a bare array where statsmodels' `ETSModel` prediction interface requires an indexed series, and the coded fallback returned the naive forecast for all 20 items — a caller-side input error, not a library bug. The registered record therefore contains three distinct baselines with ETS duplicating naive; [](#sec-results) reports a corrected ETS as a labeled post-registration computation.

**Probes.** (a) *Anonymized series:* we re-ran the headline clean model on every item with identity stripped — no name or description, just "an anonymized US national survey attitude item" and the numbers — at both cutoffs. (b) *Distribution arm:* we elicited full response-category distributions for HOMOSEX, PREMARSX, and POLVIEWS and scored them by total-variation (TV) distance.

**Metrics.** MAE; mean signed error (bias, forecast minus actual); 90% interval coverage and mean width (diagnostics, not a proper joint score — wider intervals mechanically cover more; the forward registration of [](#sec-planned) adds an interval score); and MAE within ex-post 2024-behavior strata (reversal / continuation / stable), with n inline everywhere. Budget: a hard \$25 cap; actual pre-registered spend \$0.19 across 166 calls.

(sec-results)=
## Results

### GSS 2024 reversed eight of twenty trends

A mechanical rule, fixed in the committed analysis code (the plan registered the three strata; the thresholds are the code's), classifies each item's 2024 behavior relative to its recent trend: an item whose last five waves through 2022 trended up by more than 0.2 points/year but fell more than 2 points in 2024 (or the mirror image) is a *reversal*; |change| ≤ 2 points is *stable*; trend-consistent moves larger than 2 points are *continuations* (the code's residual branch also maps to stable; no item hit it). Waves fall one to three calendar years apart, so "single-wave" changes span unequal intervals. Eight items reversed: PRAYER (approve school-prayer ban, −8.4 points), HOMOSEX (same-sex relations not wrong at all, −6.8), NATRACE (spending too little on Black Americans, −6.7), FEFAM (reject traditional gender roles, −6.5), GRASS (marijuana legal, −5.7), PREMARSX (−3.3), FEPOL (−2.8), and POLVIEWS (liberal identification, −2.04, just past the 2-point band). Three continued (health spending +5.5, interpersonal fairness −3.6, welfare spending +2.7) and nine were stable; the five largest moves in the wave were all reversals. These classify changes in weighted point estimates, not tested population changes: under simple-random-sampling standard errors from the committed wave sizes — which understate true survey uncertainty, since they carry no design effects — six of the eight reversal changes clear a 95% interval and two (FEPOL, POLVIEWS) do not (`results/uncertainty.json`).

:::{figure} ../ea-rewrite-2026-07/figures/fig1_reversals.png
:name: fig-reversals
:width: 100%

The 20 GSS series, 1972–2024 (survey-weighted percent giving the target response; free y-scales). Red marks the 2022$\rightarrow$2024 segment for the eight trend reversals; annotations give the 2022$\rightarrow$2024 change in points; asterisks mark the four largest-ever single-wave declines.
:::

Four of the eight reversals are the largest single-wave decline ever recorded for that item: PRAYER (−8.4 against a prior record of −6.9 across 27 waves since 1974), HOMOSEX (−6.8 vs. −2.5, 30 waves since 1973), FEFAM (−6.5 vs. −6.0, 24 waves since 1977), and GRASS (−5.7 vs. −4.8, 29 waves since 1973). The HOMOSEX series illustrates the severity: the share saying same-sex relations are "not wrong at all" rose from 11.4% (1973) to 62.7% (2022) with no wave-over-wave drop larger than 2.5 points, then fell to 55.9% (unweighted valid n = 2,125). External polling corroborates the direction: PRRI measured same-sex-marriage support falling 69% to 67% over 2022–2023, with Republican support for nondiscrimination protections down 7 points (66% to 59%) [@prri2024]. GSS methodology also changed after 2018 (mixed web and in-person modes), which NORC flags as a possible contributor to level shifts — though a mode artifact would have to be selective to produce trend-consistent rises on some items and record declines on others in the same wave.

### Accuracy and calibration at the aligned horizon

[](#tbl-main) reports the pre-registered arms at the aligned horizon (history ≤ 2022 $\rightarrow$ 2024, n = 20); [](#fig-scatter) adds the post-registration robustness arms.

```{table} Aligned horizon (history ≤ 2022 $\rightarrow$ 2024, n = 20). Coverage is the fraction of items whose 2024 actual fell inside the arm's 90% interval; width is the mean interval width in points; the final column is MAE over the 8 reversal items. We omit the registered ETS run, which duplicated naive for all items; the corrected ETS appears in the text and [](#fig-scatter).
:name: tbl-main

| Arm | MAE | Bias | 90% coverage | Mean width | MAE, reversals |
|---|---|---|---|---|---|
| naive (last value) | **3.15** | +1.91 | 0.90 (18/20) | 12.0 | 5.26 |
| linear | 4.07 | +0.03 | 0.90 (18/20) | 15.1 | 3.41 |
| ARIMA(1,1,0) | 3.58 | +2.22 | 0.80 (16/20) | 11.6 | 5.28 |
| gpt-5-mini (clean) | 4.07 | +2.20 | **0.55 (11/20)** | 8.6 | 6.30 |
| gpt-4o (clean) | 3.92 | +2.50 | **0.50 (10/20)** | 7.6 | 6.11 |
| claude-opus-4-8 (contam.) | 3.58 | +1.81 | 0.80 (16/20) | 11.0 | 5.42 |
```

Three findings.

1. **Nothing beat persistence.** The best clean LLM (gpt-4o, 3.92) trailed the last-value baseline (3.15), n = 20; the headline clean arm's ratio to the best simple baseline was 1.29. Every arm carried positive bias (linear's +0.03 ≈ 0) — the signature of extrapolating liberalization into a wave that reversed it.
2. **The LLMs missed reversals by more than persistence did** (6.1–6.3 points on the eight reversal items vs. naive's 5.3; a descriptive contrast — n = 8, paired p ≈ 0.3), with no compensating edge on stable items (1.6–1.7 vs. 1.0).
3. **LLM intervals were confidently wrong, and so was the corrected classical trend-follower.** Clean-arm 90% intervals averaged 7.6–8.6 points wide and covered 50–55%; the flat naive interval and the full-series linear interval covered exactly 18/20 at 11.6–15.1 points wide, with ARIMA at 16/20. Re-running the registered ETS specification with its one-line input fix — a labeled post-registration computation, deterministic given the committed series (`results/ets_corrected.json`) — gives MAE 4.33, coverage 12/20, width 11.0, and a HOMOSEX miss at 64.9 [59.2, 70.1]: a classical, trend-following interval model with LLM-grade under-coverage. The honest split is therefore not classical versus neural but *flat versus trend-following*: persistence-type intervals were honest, models that extrapolate the trend — ETS and every LLM arm — were confidently wrong on a reversal wave, and linear stayed honest only via 15-point-wide intervals. On this task, knowing that you don't know was worth more than any dynamics the models had learned.

Paired uncertainty (post-registration, seeded; `results/uncertainty.json`): naive's accuracy edge resolves against the clean arms — gpt-5-mini +0.92 points (paired-bootstrap 95% CI +0.14 to +1.64), gpt-4o +0.77 (+0.06 to +1.40) — but not against the contaminated arm (claude-opus-4-8 +0.43, −0.06 to +0.90), so the supported ordering claim is that *no arm beat persistence*, not that persistence beat every arm. The under-coverage is unambiguous: 11/20 and 10/20 against a nominal 0.90 (exact binomial p < 10⁻⁴), and on every item where a clean arm and naive disagreed about coverage, naive was the one that covered (7:0 and 8:0 discordant pairs).

:::{figure} ../ea-rewrite-2026-07/figures/fig2_accuracy_calibration.png
:name: fig-scatter
:width: 58%

Accuracy versus calibration, aligned horizon (n = 20 unless marked). The flat naive and full-series linear intervals sit at nominal coverage; every trend-following arm — the LLMs, the post-registration o3 and effort-sweep arms, and the corrected ETS (a classical model) — sits below it. † The high-effort arm completed 11 of 20 items. ARIMA and claude-opus-4-8 coincide at (3.58, 0.80); the registered ETS run duplicated naive and is not shown separately.
:::

### The reversal everyone missed

```{table} HOMOSEX ("not wrong at all"), history through 2022 $\rightarrow$ 2024. Actual: 55.9 (weighted; unweighted valid n = 2,125).
:name: tbl-homosex

| Forecaster | Point | 90% interval | Covers 55.9? |
|---|---|---|---|
| naive | 62.7 | [56.8, 68.3] | no |
| linear | 60.2 | [49.2, 70.3] | yes — width 21.1 |
| ARIMA(1,1,0) | 63.1 | [56.4, 69.3] | no |
| gpt-5-mini (clean) | 66.5 | [62.0, 70.5] | no |
| gpt-4o (clean) | 64.5 | [61.0, 68.0] | no |
| claude-opus-4-8 (contam.) | 64.0 | [59.0, 69.0] | no |
```

Every point forecast landed between 60.2 and 66.5 against an actual of 55.9 ([](#tbl-homosex)); the only interval containing the truth (linear) owed its coverage to width — 21 points — though its full-series-trend point did sit 2.5 points below the 2022 value, the largest downturn any arm priced in. The anonymized clean run's 67.0 [61, 73] misses too — at this horizon the failure is dynamics, not item identity. Across all eight reversal items, 90% intervals covered the actual 6/8 (naive), 7/8 (linear), and 6/8 (ARIMA) times, against 1/8 (gpt-5-mini), 0/8 (gpt-4o), and 4/8 (claude-opus-4-8).

### Where identified "skill" comes from: the anonymization probe

At the aligned horizon, stripping item identity barely matters: the mean |identified − anonymized| point difference is 1.0 point (n = 20), and the model trails naive either way (4.07 identified, 4.62 anonymized, vs. 3.15). At the 2010 cutoff — 14 years of un-shown history inside the model's training data — identity moves forecasts a mean of 4.5 points, and the items that move most are the famous ones ([](#fig-anon)): HOMOSEX +30.5 (78.0 identified vs. 47.5 anonymized, actual 55.9), GRASS +17.0, PREMARSX +9.5, FEFAM +9.0.

:::{figure} ../ea-rewrite-2026-07/figures/fig3_anonymization.png
:name: fig-anon
:width: 58%

The anonymization probe at the 2010 cutoff: gpt-5-mini's 2024 forecast per item, identified (filled) vs. anonymized (ring), sorted by the gap (labeled where ≥ 5 points). The four largest gaps are the set's best-known liberalization trajectories; where the marks coincide, the name added nothing.
:::

The HOMOSEX case rewards attention. We showed the named model data through 2010 (42.7%) and told it to reason only from the series; it answered 78 — a level the GSS series has never reached, 15 points above the 2022 value in its training data; the name appears to have pulled in the level of adjacent, differently-worded series (Gallup's acceptance questions run well above the GSS's four-category "not wrong at all" share), a confusion worth auditing for in any identified-series design. Anonymized, the same model extrapolated the same numbers to 47.5. Actual: 55.9. Both wrong, 30.5 points apart.

In aggregate at the 2010 cutoff, the identified model beats naive by 1.30 points of MAE (7.25 vs. 8.55, n = 20); anonymized, the edge shrinks to 0.82 (7.73 vs. 8.55). Against the strongest classical baseline that ran at that horizon (ARIMA, 7.66), the identified edge of +0.41 flips to −0.07 under anonymization — and the corrected ETS (5.52 at this horizon) beats the identified LLM outright, so the pre-registered "edge over the best baseline" existed only relative to the baselines that ran. We had pre-registered "the edge collapses under anonymization"; the honest reading is *partial* — the edge over naive shrinks by roughly a third (the aggregate identified−anonymized gap itself is small against its uncertainty: +0.48 points, bootstrap 95% CI −1.56 to +2.24), the edge over the best running baseline disappears, and the sharp evidence is per-item: individual identified forecasts move by up to 30.5 points on the name alone. The probe is also conservative in one direction and leaky in the other: anonymization removes legitimate item semantics along with memorized history, and the retained calendar years and values may still identify famous trajectories — so the gap bounds identity dependence, not recall specifically.

The contaminated arm tells the same story from the other side. At the aligned horizon claude-opus-4-8 shows no memorization signature: MAE 3.58 vs. the clean arm's 4.07 (n = 20), a miss on HOMOSEX like everyone else, 4/8 reversal coverage. At the 2010 cutoff its advantage is what recall of un-shown history predicts: MAE 4.18 vs. the clean arms' 5.83–7.25 (n = 20), with reversal-item MAE 2.89 vs. their 4.22–7.39 (n = 8) — consistent with "forecasting" history it has read about, though the arm also differs in family and capability, so it corroborates the recall account rather than isolating it.

Finally, the distribution arm (exploratory; three items, two models): asked for full response-category distributions for 2024, both models produced shapes close to the truth — total-variation distance 0.081 on HOMOSEX (both), 0.054/0.043 on PREMARSX (gpt-5-mini/claude), 0.021/0.027 on POLVIEWS — but freezing the 2022 distribution does as well or better (mean TV 0.047 vs. their 0.052 and 0.050; persistence wins two of three items). The models' distributional shapes add nothing over persistence, and their top-category errors (+8.1 and +3.4 to +5.4 points on the two sexual-morality items) slide in the same trend-following direction as everywhere else.

(sec-robustness)=
### Post-registration robustness arms

Three anticipated objections cost almost nothing to check, so we ran them after registration as labeled robustness arms — separate result files, the pre-registered record untouched; same items, prompts, and metrics, at the aligned horizon.

```{table} Post-registration robustness arms, aligned horizon (vendor-stated cutoffs: o3 2024-06-01, gpt-5-mini 2024-05-31 — both clean). Reference points from the pre-registered record: naive 3.15 MAE / 0.90 coverage; gpt-5-mini (minimal) 4.07 / 0.55. A session crash truncated the high-effort arm: 12 items attempted, one parse failure, 11 scored; its metrics are over that subset.
:name: tbl-robust

| Arm | MAE (n) | 90% coverage | MAE, reversals | HOMOSEX (actual 55.9) |
|---|---|---|---|---|
| o3, default effort | 3.93 (20) | 0.75 (15/20) | 6.26 | 65.0 [59.0, 71.0] — miss |
| gpt-5-mini, medium effort | 4.16 (20) | 0.75 (15/20) | 7.11 | 65.2 [60.0, 70.4] — miss |
| gpt-5-mini, high effort | 4.21 (11) | 0.64 (7/11) | 7.03 | 66.3 [62.1, 70.5] — miss |
```

**"Use a reasoning model."** o3 — the strongest reasoning model available to us whose stated cutoff predates the end of GSS 2024 fieldwork — posts higher empirical coverage than the pre-registered clean arms (0.75 vs. 0.50–0.55; suggestive rather than resolved, discordant-pair p = 0.125) but stays detectably under-covered (binomial p = 0.043), trails persistence (3.93 vs. 3.15, n = 20), and misses the reversal.

**"You ran the LLM at minimal effort."** Raising gpt-5-mini's reasoning effort bought no improvement: 4.07 (minimal, n = 20) $\rightarrow$ 4.16 (medium, n = 20) $\rightarrow$ 4.21 (high; partial arm, n = 11), and on the 11 items the high arm completed the sweep reads 3.91 $\rightarrow$ 3.93 $\rightarrow$ 4.21 against naive's 2.56 — differences well inside paired noise, in the unhelpful direction. Deliberation converged on the same wrong prior ([](#fig-scatter)).

**"Add a clean Anthropic arm."** Impossible at evaluation time, and the reason generalizes: by then Anthropic had retired from the first-party API every Claude snapshot whose training cutoff predates the end of GSS 2024 fieldwork (claude-3-5-sonnet-20241022 returns 404; retired October 28, 2025 [@anthropic2026deprecations]). The population of models anyone can ever cleanly test on a given holdout shrinks as vendors deprecate old snapshots — retrospective clean evaluation has a **closing window**. We skipped a planned DeepSeek open-weights arm for the mirror-image reason: the vendor documents no training cutoff, so we could not label the arm clean at all.

The robustness arms cost roughly another dollar (the committed cost file records \$0.88 across 30 calls for the high-effort segment; the same session crash destroyed the o3 and medium-effort cost logs, though the committed results file preserves every call's parsed output).

(sec-scorecard)=
### Scorecard against the pre-registered expectations

[](#tbl-scorecard) scores each expectation committed in the pre-analysis plan against its outcome: three confirmed, one failed as stated, one partial. Expectations 3–5 carried informal tolerances ("within ~1 pt," "≈," "collapses"); we report the realized quantities beside each verdict so readers can apply their own thresholds.

```{table} The five falsifiable expectations we committed before any forecasting call (commit 0ec5fd3), and their outcomes.
:name: tbl-scorecard

| # | Pre-registered expectation | Outcome |
|---|---|---|
| 1 | All arms miss the HOMOSEX reversal (point ≥ 60 vs. actual ≈ 55) | **Confirmed** — points 60.2–66.5 vs. 55.9; linear's 21-point interval did contain the actual |
| 2 | Overconfidence replicates: 90% coverage < 0.90 for every arm | **Failed as stated** — LLM arms under-covered (0.50–0.80) while naive and linear hit 0.90 exactly; the corrected post-registration ETS also under-covered (0.60) |
| 3 | Clean LLM within ~1 point of the best simple baseline; no "LLM $\gg$ baselines" | **Confirmed** — 4.07 vs. 3.15, Δ = 0.92, LLM on the worse side |
| 4 | Contaminated ≈ clean at the aligned horizon; no reversal-nailing | **Confirmed** — 3.58 vs. 4.07; HOMOSEX missed; 4/8 reversal coverage |
| 5 | Long-horizon identified edge collapses under anonymization | **Partial** — edge over naive 1.30 $\rightarrow$ 0.82; edge over ARIMA +0.41 $\rightarrow$ −0.07; per-item swings up to 30.5 points |
```

## The result a naive design produces

Before building the controls, we ran this task the way much of the LLM-simulation literature runs it: item names shown, forecast targets inside the model's training window, no survey weights, two variables. That pilot produced a language model beating its baseline by 2.4× on MAE (12.5 vs. 30.2 over 14 forecasts on n = 2 items, targets 2000–2021 from cutoffs in 1990/2000; its only baseline was linear extrapolation) — a publication-ready number, structurally similar to numbers the literature is publishing. The pilot's raw forecasts are preserved at `archive/pilot/forecasts.json`. Each of its findings, traced through the controlled design:

- **"LLM beats the baseline 2.4×" (MAE 12.5 vs. 30.2).** Two named items with targets 2000–2021, inside the training window, against a single weak baseline, produced it. It does not replicate: clean LLM 4.07 vs. naive 3.15 (ratio 1.29, LLM worse), n = 20.
- **"Everyone is overconfident" (LLM 43%, baselines 36% coverage).** The same design plus degenerate baseline intervals produced it. Half survives: LLMs cover 50–55% at 90% nominal; proper classical intervals cover 90%.
- **"LLMs capture non-linear dynamics baselines miss."** The 1990$\rightarrow$2021 HOMOSEX run — dynamics the model had read about — produced it. Anonymization erases the long-horizon edge over the best baseline.
- **"Trajectories reverse and trend-followers miss it."** GPT-4o vs. GSS 2024, run before the microdata release, produced it. It replicates, now pre-registered: 8/20 reversals; every arm missed HOMOSEX.

The same pilot included a calibrated long-horizon projection placing same-sex-relations acceptance at 66 by 2030 (80% CI [57, 75]); GSS 2024's 55.9 already sits below that interval's floor. A design of this shape asks a model to "forecast" years it has read about, on items it can name, and reports recall as skill. The one thing it got right — trajectories reverse and trend-extrapolators miss it — we pre-registered this time (expectation 1), and it confirmed exactly.

## Discussion

**Protocol recommendations.** Two changes would let the LLM-as-social-forecaster literature grade itself honestly. First, *anonymized-series reporting*: any retrospective claim that an LLM predicts opinion, elections, or social-science outcomes should report the anonymized-series number beside the identified one — the gap bounds how much of the claimed skill depended on item identity rather than the shown series. It is cheap (one extra run) and imperfect in both directions: anonymization also removes legitimate item semantics, and the retained years and values may still identify famous series. Second, *strictly forward pre-registration*, the standard geopolitical LLM forecasting already meets [@halawi2024]: no contamination argument is possible about data that does not yet exist.

**The closing window.** Retrospective clean evaluation additionally depends on vendors keeping old snapshots available. They do not: Anthropic had retired every snapshot cleanly positioned for the GSS 2024 holdout from the first-party API by evaluation time [@anthropic2026deprecations], and open-weight alternatives without vendor-documented cutoffs cannot earn a clean label either. Each wave's set of cleanly testable models shrinks monotonically; forward registration and open-weight models with documented provenance are the durable fixes.

**What the failure means for value-forecasting-as-alignment-target.** Using a forecast distribution of human values as an alignment input requires, at minimum, that the forecasting machinery beat trivial baselines and cover at its stated rate. At the two-year horizon nothing we tested clears the first bar and no LLM arm clears the second — while persistence *with honestly wide intervals* performs exactly as advertised (18/20 at 90% nominal). A system aligned in 2022 to "acceptance keeps rising, 90% sure" would have been confidently wrong, within two years, about the direction of the value it was optimizing around. The distribution arm (exploratory, three items) fits the same pattern: model shapes match the truth about as well as a frozen 2022 distribution does, while the top-category level slides with the broken trend — so the case for distributional targets with calibrated uncertainty rests on the coverage results, not on any demonstrated distributional skill, and the normative step remains human [@macaskill2020].

**A contamination-proof instrument.** Every retrospective design above still leans on cutoff bookkeeping, because every modern LLM has read the polling record we test it on. Vintage-corpus models remove the problem at the root: Talkie-1930 is a 13B model pretrained exclusively on 260B tokens of pre-1931 text [@levine2026], alongside the time-locked Ranke-4B family (cutoffs 1913–1946) [@goettlich2025] and TypewriterLM (pre-1913) [@luo2026]; @underwood2025 argue that escaping hindsight requires period pretraining, not fine-tuning. For value forecasting a 1930 cutoff is a feature: Gallup's first national polls date to 1935 and the GSS to 1972, so the *entire quantitative polling record* is out-of-sample — ninety years of resolved actuals versus the single clean wave available here. The obstacle is elicitation, not knowledge: the Talkie-1930 base model approaches GPT-3-175B on arithmetic under log-probability scoring while its instruction-tuned variant scores 4.9% (strict, 5-shot) on GSM8K vs. 17.8% for same-size LLaMA-13B [@ghenis2026talkie], and our exploratory Gallup-style probes of the chat layer hit the same wall (outputs in the repository). The natural design is *sensor mode*: read attitude signals from the vintage model via log-probability scoring under period framings; let a modern model, blinded to named post-1930 facts, generate hypotheses and calibrated forecasts; grade the pipeline on the 1936–2024 record under proper scoring rules. Whether attitude knowledge survives extraction the way arithmetic does is the open question, and the first to answer.

## Limitations

Twenty items, one country, one survey program, one holdout wave: the 2024 reversals may reflect period shocks that say little about longer-horizon forecastability, and n = 20 gives little power to separate LLM arms from one another. The items also share that single wave and its shock, so errors are cross-correlated — clean-arm under-coverage concentrates in the reversal cluster (10/12 covered on non-reversal items) — and wave-level calibration claims carry an effective n well below 20; the defense is that naive and linear absorbed the same shock at 6/8 and 7/8. The registration is outcome-aware: GSS 2024 was public before we committed the plan, and the analyst assembling the item mix could observe 2024 — the items are the standard GSS attitude canon, chosen for their pre-2022 shape mix, but readers should weigh this. We took one draw per forecast, with seeds where the API supports them, and did not quantify sampling variance in the models; we score against published weighted point estimates, whose own sampling error we treat only approximately (§4.1). The headline clean arm ran at minimal reasoning effort — the effort sweep and o3 arms address this post hoc, one of them partial (n = 11) — the registered ETS run silently duplicated naive (corrected post hoc in §4.2), and contrary to the plan's logging promise we retained parsed outputs rather than raw completions. GSS mode changes after 2018 may contribute level shifts to the very reversals every arm missed, though the direction-selective pattern argues against a pure mode artifact; cutoff labels rest on unauditable vendor self-reports; and the ex-post strata describe 2024 behavior, not forecast inputs.

(sec-planned)=
## Planned: forward registration for GSS 2026 and 2028

**Status: planned, pending author confirmation — this section is not itself a registration.** The binding registration will be a separate commit specifying items, arms, elicitation, and scoring before GSS 2026 fieldwork begins.

The natural next step is the design no contamination argument can touch: point forecasts, 90% intervals, and full response distributions for all 20 items (plus any newly qualifying items), for GSS 2026 and 2028, committed publicly before the data exist — from classical baselines, current LLMs at fixed settings, and any externally submitted system — which we will score by this paper's metrics plus a proper scoring rule on the distributional forecasts [@gneiting2007]. The forward registration will also archive full raw API responses, correcting this study's parsed-outputs-only logging. The repository issue tracker accepts external arms; open-weight submissions are especially welcome, since they remain re-runnable after vendor retirements.

## Reproducibility

The public repository holds everything needed to reproduce the tables and figures: the pre-analysis plan (`0ec5fd3`, committed before any forecasting call of this evaluation), the extraction/baseline/forecast/analysis/figure code including the exact prompt templates (`ea-rewrite-2026-07/code/`), parsed model outputs and error records (we retained parsed outputs rather than raw completion text — a deviation from the plan's logging promise that the forward registration corrects), per-arm token usage and costs, and the result JSONs (`ea-rewrite-2026-07/results/`, including the post-registration `ets_corrected.json` and `uncertainty.json`) from which we draw every number in the pre-registered and post-registration analyses; the pilot's raw forecasts live at `archive/pilot/forecasts.json`. We do not commit the GSS microdata (NORC distributes them [@davern2025gss]); the extraction script regenerates the weighted series from the public cumulative file. Total API spend: \$0.19 for the pre-registered arms (166 calls) plus roughly \$1 for the robustness arms. Thanks to the NORC GSS team for the cumulative file and documentation; errors are mine.
