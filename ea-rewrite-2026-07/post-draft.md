# Value forecasting for AI alignment: Pre-registered tests and a missed reversal

*Epistemic status: pre-registered empirical results plus a research proposal I hold more loosely. The experiments are small — 20 survey items, one holdout wave, one draw per forecast, $0.19 of API spend — but the [analysis plan](https://github.com/maxghenis/value-forecasting/blob/ea-post-rewrite-2026-07/ea-rewrite-2026-07/PREANALYSIS_PLAN.md) was committed before any forecasting call, and all code, prompts, and raw results are [public](https://github.com/maxghenis/value-forecasting/tree/ea-post-rewrite-2026-07/ea-rewrite-2026-07). Before this, I drafted — but never published — a version claiming LLMs beat time-series baselines on value forecasting by 2.2x; that number came from two variables and a leaky design, and it did not survive the controls here. This is the version with the controls, and the near-miss is part of the argument.*

**Summary:**

- In the 2024 General Social Survey, 8 of the 20 attitude items I track reversed their pre-2022 trend. Four posted the largest single-wave decline in their item's recorded history: approval of the school-prayer ban −8.4 points, acceptance of same-sex relations −6.8, rejection of traditional gender roles −6.5, marijuana legalization −5.7.
- I pre-registered a forecasting test on that wave: three LLMs against classical time-series baselines, shown history through 2022, forecasting 2024, with training-cutoff contamination controlled. Every arm's point forecast missed the same-sex-relations reversal (predictions 60.2–66.5 vs. actual 55.9), and last-value persistence beat every LLM on overall accuracy (MAE 3.15 vs. 3.58–4.07 points, n = 20).
- The LLMs' 90% intervals covered the truth 50–55% of the time (clean arms); properly computed classical intervals covered 90%. My earlier claim that "everyone is overconfident" was half right — the LLMs are.
- An anonymization probe explains where earlier "LLM forecasting skill" came from: with the item named, gpt-5-mini "forecast" the same-sex-relations series from 2010 data at 78; with the identity stripped, 47.5. A 30.5-point swing from the variable name alone. Identity-conditioned backtests inside a model's training window measure recall blended with extrapolation, not forecasting.
- The alignment proposal survives in a narrower, more testable form: treat the *forecast distribution* of post-reflection human values — with calibrated uncertainty at two levels — as an alignment target, validate the forecasting machinery against history, and use vintage-corpus LLMs (training data ending in 1930) as the contamination-proof instrument. The entire polling era is out-of-sample for them.

## Eight of twenty values reversed

Since 1973 the General Social Survey has asked Americans whether same-sex relations are wrong. The survey-weighted share answering "not wrong at all" rose from 11.4% to 62.7% between 1973 and 2022, with no wave-over-wave drop larger than 2.5 points along the way.

In 2024 it fell 6.8 points, to 55.9% (n = 2,125 valid responses). That is the largest decline in the item's 51-year history, and it was not alone. I extracted 20 GSS attitude items with a 2024 wave from the [cumulative 1972–2024 microdata](https://gss.norc.org/) (survey-weighted; details in the [results summary](https://github.com/maxghenis/value-forecasting/blob/ea-post-rewrite-2026-07/ea-rewrite-2026-07/RESULTS.md)) and classified each by a mechanical rule: an item whose last five waves through 2022 trended up by more than 0.2 points/year but fell more than 2 points in 2024 (or the mirror image) counts as a reversal.

Eight of twenty reversed:

| Item | Target response | 2022 | 2024 | Change |
|---|---|---|---|---|
| PRAYER | Approve ban on required school prayer | 54.1 | 45.7 | **−8.4** |
| HOMOSEX | Same-sex relations not wrong at all | 62.7 | 55.9 | **−6.8** |
| NATRACE | Spending too little on Black Americans | 53.2 | 46.5 | −6.7 |
| FEFAM | Disagree women should tend home | 74.7 | 68.2 | **−6.5** |
| GRASS | Marijuana should be legal | 72.2 | 66.5 | **−5.7** |
| PREMARSX | Premarital sex not wrong at all | 68.8 | 65.6 | −3.3 |
| FEPOL | Disagree men better suited for politics | 84.8 | 82.0 | −2.8 |
| POLVIEWS | Identify as liberal (1–3 of 7) | 29.5 | 27.5 | −2.0 |

The four bolded changes are the largest single-wave declines those items have ever recorded (across 24–30 waves each). Every sexual-morality and gender-role item in the set fell. Meanwhile three items continued their trend (support for health spending rose 5.5 points) and nine stayed within 2 points; abortion-for-any-reason ticked up 1.2. Values did not move in lockstep — but the five largest moves in the wave were all trend reversals.

External polling corroborates the direction: [PRRI's American Values Atlas](https://www.prri.org/research/views-on-lgbtq-rights-in-all-50-states/) measured same-sex-marriage support falling from 69% to 67% between 2022 and 2023, with Republican support for nondiscrimination protections down 7 points (66% to 59%), and attributes the declines to partisan polarization and legislative backlash. (GSS methodology also changed after 2018 — mixed web and in-person modes — which NORC flags as a possible contributor to level shifts. It would have to be a selective one to produce trend-consistent rises on some items and record declines on others in the same wave.)

If you hold the prior that dominated both my earlier draft and, as it turns out, every model I tested — *liberalization continues* — GSS 2024 is new information.

## Every arm missed it

Here was the pre-registered test. Show each forecaster the weighted series through 2022 and ask for 2024 — a point estimate and a 90% interval. GSS 2024 microdata first became public in 2025, so each model's training cutoff determines whether it could have seen the answer:

| Arm | Cutoff | Status |
|---|---|---|
| gpt-5-mini (headline) | May 2024 | Clean — cutoff predates the 2025 release and the end of fieldwork |
| gpt-4o (robustness) | Oct 2023 | Clean |
| claude-opus-4-8 (ceiling) | Jan 2026 | Deliberately contaminated — a check, see below |

All three models know GSS history through 2022 from training, and that is exactly what they were shown — so the clean arms compete with the baselines on equal information. Baselines: last-value persistence ("naive"), OLS on the logit scale ("linear"), and ARIMA(1,1,0), each with proper 90% intervals. (A fourth baseline, ETS/Holt, silently fell back to naive for all 20 items due to a statsmodels bug I found only afterward; it's reported as a duplicate of naive.)

The item everyone watched:

| Forecaster | HOMOSEX 2024 point | 90% interval | Actual: 55.9 |
|---|---|---|---|
| Naive (last value) | 62.7 | [56.8, 68.3] | miss |
| Linear | 60.2 | [49.2, 70.3] | covered — by a 21-point-wide interval |
| ARIMA | 63.1 | [56.4, 69.3] | miss |
| gpt-5-mini | 66.5 | [62.0, 70.5] | miss |
| gpt-4o | 64.5 | [61.0, 68.0] | miss |
| claude-opus-4-8 | 64.0 | [59.0, 69.0] | miss |

Every point forecast landed between 60.2 and 66.5 against an actual of 55.9. All three LLM intervals excluded the truth; the only interval that contained it did so through width, not foresight. Across all eight reversal items, the LLMs' 90% intervals covered the actual 1/8 (gpt-5-mini), 0/8 (gpt-4o), and 4/8 (claude) times, against 6–7/8 for the classical baselines.

Aggregates over all 20 items, aligned horizon:

| Arm | MAE (pts) | 90% coverage | Mean interval width | MAE on the 8 reversals |
|---|---|---|---|---|
| **Naive** | **3.15** | 0.90 (18/20) | 12.0 | 5.3 |
| Linear | 4.07 | 0.90 (18/20) | 15.1 | 3.4 |
| ARIMA | 3.58 | 0.80 (16/20) | 11.6 | 5.3 |
| gpt-5-mini (clean) | 4.07 | 0.55 (11/20) | 8.6 | 6.3 |
| gpt-4o (clean) | 3.92 | 0.50 (10/20) | 7.6 | 6.1 |
| claude-opus-4-8 (contaminated) | 3.58 | 0.80 (16/20) | 11.0 | 5.4 |

Three reads:

1. **Nothing beat persistence.** The best clean LLM's MAE was 3.92 (gpt-4o) vs. naive's 3.15, n = 20. The cheapest possible forecast — "2024 equals 2022" — won.
2. **The LLMs missed reversals by more than persistence did.** On the eight reversal items the clean LLMs erred 6.1–6.3 points against naive's 5.3: they extrapolated the recent trend, and the trend broke. Their edge on the nine stable items (1.6–1.7 vs. naive's 1.0) didn't exist either.
3. **LLM intervals were confidently wrong.** Clean-arm 90% intervals averaged 7.6–8.6 points wide and covered half the time. The classical intervals averaged 12–15 points wide and covered at their nominal rate. On this task, knowing that you don't know was worth more than any dynamics the models had learned.

The whole experiment cost $0.19 in API calls (166 of them); every prompt and raw completion is in the repo.

## The claim I almost published

An earlier draft of this post — written before these controls, never published — reported that an LLM beat the best time-series baseline by 2.2x on mean absolute error. I'm including its claims here because the way they fell apart is the most useful thing in this post: every one of them looked publication-ready, and at least one of them is structurally identical to results that *are* being published in the LLM-simulation literature. Here is what happened to each once I tightened the design:

| Draft claim | Test that produced it | What the pre-registered version found |
|---|---|---|
| "LLM beats best baseline 2.2x" (MAE 12.5 vs. 28.1) | n = 2 items (HOMOSEX, GRASS), item names shown, forecast targets 2000–2021 — all *inside* the model's training window | Does not replicate. On a clean, aligned design: clean LLM MAE 4.07 vs. naive 3.15 (ratio 1.29, LLM worse), n = 20 |
| "Everyone is overconfident — LLM CIs covered 43%, baselines 36%" | Same leaky design; degenerate baseline intervals | Half survives. LLMs covered 50–55% at 90% nominal (n = 20); properly computed classical intervals covered 90% |
| "LLMs capture non-linear dynamics baselines miss" | The 1990→2021 HOMOSEX run — where the model had read about the liberalization it was "predicting" | See next section: strip the item name and the long-horizon edge over the best classical baseline disappears |
| "Value trajectories can reverse and trend-followers will miss it" | GPT-4o vs. GSS 2024, run before the 2024 microdata release | Replicates, now with pre-registration: every arm missed the HOMOSEX reversal; 8/20 items reversed |

(The earlier numbers were also computed without survey weights; everything here uses NORC's recommended weights.) The same era of work included a calibrated GPT-4o run that produced the long-horizon projections the proposal leaned on — same-sex-relations acceptance at 66 by 2030 (80% CI [57, 75]), 80 by 2100. GSS 2024's 55.9 already sits below that 2030 interval's floor.

The old experiment asked a model to "forecast" years it had already read about, on items it could name, and I interpreted its recall as skill. I flagged contamination as a concern in that draft and ran what I thought was a control — a clean 2024 holdout — but kept the headline number from the contaminated design. The right response to noticing that was to rebuild the experiment, so that is what this is.

Credit in the other direction: the one thing the old draft got right — reversals happen and trend-extrapolators miss them — turned out to be the *most* important feature of the new data, and I pre-registered it this time ("all arms miss the HOMOSEX reversal; point ≥ 60 vs. actual ≈ 55"). It confirmed exactly.

## Where the apparent LLM skill came from

The new design includes the control the old one lacked. I re-ran the clean model (gpt-5-mini) on every item with the identity stripped — no item name, no description, just "an anonymized US national survey attitude item" and the numeric series — and compared against the identified version, at two cutoffs:

- **Cutoff 2022 (shown history = model knowledge):** identity barely matters. Mean |identified − anonymized| difference: 1.0 point over 20 items. Named or anonymous, the model trails naive persistence (4.07 and 4.62 vs. 3.15).
- **Cutoff 2010 (14 years of un-shown history the model has read about):** identity moves forecasts a mean of 4.5 points, and the items that move most are the famous ones. HOMOSEX: 78.0 identified vs. 47.5 anonymized — a 30.5-point swing from the name alone. GRASS: +17.0. PREMARSX: +9.5. FEFAM: +9.0.

The HOMOSEX case deserves the detail. The model was shown data through 2010 (42.7%) and told to reason only from the series. Named, it answered 78 — a level the GSS series has never reached, 15 points above the 2022 value that sits in its training data. It didn't even recall accurately; the name appears to have pulled in the level of adjacent, differently-worded series (Gallup's acceptance questions run well above the GSS's four-category "not wrong at all" share — a confusion I specifically had to audit my own earlier drafts for). Anonymized, the same model extrapolated the same numbers to 47.5. Actual: 55.9. Both wrong, 30.5 points apart.

In aggregate at the 2010 cutoff, the identified model beats naive by 1.30 points MAE; anonymized, the edge shrinks to 0.82 (n = 20). Against the strongest classical baseline (ARIMA, MAE 7.66), the identified edge of +0.41 flips to −0.07 anonymized. I pre-registered "the edge collapses under anonymization"; the honest scorecard entry is *partial* — it shrinks by about a third against naive, vanishes against the best baseline, and per-item identified forecasts move by up to 30 points on the name.

The contamination arm tells the same story from the other side. claude-opus-4-8's training window (through Jan 2026) includes the GSS 2024 release itself. At the aligned horizon it shows no memorization signature — MAE 3.58 vs. the clean arm's 4.07 (n = 20), and it misses HOMOSEX at 64.0 [59, 69] like everyone else. But at the 2010 cutoff it posts MAE 4.18 vs. the clean arms' 5.83–7.25 (n = 20), with reversal-item error of 2.9 vs. their 4.2–7.4 (n = 8) — it "forecasts" the history it wasn't shown, because it read about it.

The methodological upshot generalizes beyond my project. A growing literature evaluates LLMs by "predicting" survey results, elections, and social-science findings from before their training cutoffs, descended from the silicon-sampling work of [Argyle et al. (2023)](https://arxiv.org/abs/2209.06899). Retrospective evaluations of named series inside the training window are recall tests reported as forecasting results. Two protocols fix this: **anonymized series** (cheap, imperfect — the dynamics themselves may be memorized) and **strictly forward pre-registration** (airtight). [Halawi et al. (2024)](https://arxiv.org/abs/2402.18563) already hold LLM geopolitical forecasting to the forward standard; value forecasting should meet it too.

## The proposal, updated

The proposal I still believe, stated more carefully than my earlier draft stated it:

1. **Validate the machinery historically.** Test whether any system — LLM, statistical, hybrid — can forecast distributions of human values out-of-sample, under contamination controls. This is now partially done, with a negative interim result at the 2-year horizon: nothing I tested beat persistence (best clean LLM 3.92 vs. naive 3.15 MAE, n = 20), and reversals went unforecast by every arm.
2. **Forecast the distribution, not the point.** The target of a mature version is not "X% will hold value V" but the joint distribution of post-reflection values, with uncertainty carried at two levels: *aleatoric* — real heterogeneity across people, which you model rather than average away — and *epistemic* — your uncertainty about that distribution, expressed in intervals that cover at their stated rate.
3. **Treat that forecast distribution as an alignment input.** An AI whose objectives respect a calibrated distribution over where reflective human values are heading — hedging across value systems weighted by forecast mass, flagging actions that are catastrophic under any high-mass system, preserving option value where the distribution is wide — is a different and, I think, better-specified target than an AI aligned to a 2026 preference snapshot.

My experiment already touches both uncertainty levels, and the results cut in opposite directions. On aleatoric structure, the models are decent: asked for the full four-category response distribution of HOMOSEX in 2024, both tested models produced shapes within total-variation distance 0.08 of the truth (0.02–0.05 on the other two items) — while still putting the top category 8 points too high, the same trend-following miss as the point forecasts. On epistemic honesty, they failed: 90% intervals covering 50–55% of the time is exactly the property an alignment-relevant forecast cannot have. The 2024 wave is a proof by example: a system aligned to "acceptance keeps rising, 90% sure" would have been confidently wrong about the direction of the value it was optimizing around within two years.

This reframes rather than kills the proposal. Point-trajectory extrapolation is precisely what failed; a distributional target with honest intervals is what the failure argues for. But it raises the bar for step 1: any claim that a system can forecast values now needs to beat persistence, cover at its stated rate, and survive anonymization — inline, with baselines and n attached.

## Objections

**"Your own results show values aren't forecastable."** At the 2-year horizon, nothing beat persistence — but persistence *plus honestly wide intervals* performed exactly as advertised (18/20 coverage at 90%). That is a usable forecast; it says "expect roughly today's values, and hold real uncertainty either way." Whether skill exists at longer horizons, where generational replacement dominates period shocks, is open — my long-horizon test was confounded by design, which is the point of building the clean instrument below. If deeper unpredictability wins, the framework degrades gracefully: the intervals widen until they're honest, and the alignment-relevant output becomes "do not lock anything in."

**"Forecasting values is moral relativism."** A forecast of what humans will value after reflection is an empirical claim, not an endorsement. Deciding what to *do* with that forecast — whether to align to it, override parts of it, or weight populations — is a normative step this program does not and cannot automate. It stays with humans; the forecast just makes one input to it explicit and gradeable.

**"Who defines 'reflection'?"** The weakest link, unchanged from my earlier draft. GSS drift is not idealized reflection — 2024's reversals may reflect polarization dynamics more than deliberation, which is partly why forecasting them is hard. What historical validation actually tests is the prerequisite: can anything predict measured value change at all? Operationalizing "post-reflection" (deliberative-polling outcomes? values after exposure to arguments?) is a separate, harder design problem, and any choice smuggles in assumptions that should be stated rather than hidden.

**"A good value-change model is a manipulation manual."** Yes — [performative prediction](https://arxiv.org/abs/2002.06673) with the sign flipped: the better and more public the forecast, the more it invites steering toward or away from itself. I don't have a clean answer. Publishing evaluation protocols and calibration results (which help everyone check claims) while being slower about capability recipes seems like the right default, and human aggregation of the forecast into decisions is a partial firewall. This concern weighs against the research program's scale, not its existence — the actors best positioned to steer values are not waiting for my GSS holdout study.

## The instrument: Models that have never read a poll

Everything above still leans on training-cutoff bookkeeping and anonymization tricks, because every modern LLM has read the polling record it's being tested on. There is now a clean instrument: LLMs pretrained exclusively on historical text.

[Talkie-1930](https://talkie-lm.com/introducing-talkie) (Nick Levine, David Duvenaud, and Alec Radford) is a 13B model trained on 260B tokens of pre-1931 English text. It has company: the [Ranke-4B family](https://github.com/DGoettlich/history-llms) of time-locked models with cutoffs from 1913 to 1946, and [TypewriterLM](https://arxiv.org/abs/2606.02991), 7B trained on pre-1913 text. [Underwood, Nelson, and Wilkens (2025)](https://arxiv.org/abs/2505.00030) supply the motivation from the research side: fine-tuning a modern model to sound historical doesn't remove its hindsight; "pretraining on period prose may be required" to simulate historical perspectives credibly.

The field clusters before 1946, and the reason is rights, not compute: US copyright runs 95 years, so as of 2026 everything published through 1930 is public domain, and each later year of cutoff adds licensing where earlier years just add scanning. The Talkie team reports its historical corpus can grow to over a trillion tokens and says it is training a GPT-3-level model for release this summer.

A 1930 cutoff sounds prohibitive for value forecasting until you notice what it excludes. Gallup's first national polls: 1935. The GSS: 1972. A pre-1931 model has read no poll it could parrot — the entire quantitative record of public opinion is out-of-sample. Where my GSS experiment scraped together one clean holdout wave, a 1930-cutoff model can be graded on ninety years of actuals — every reversal, plateau, and backlash in the polling record, orders of magnitude more resolved items than my twenty. The problem that dominated this post, whether the model already knows the answer, does not arise.

The catch is elicitation, and I've measured it. [I evaluated Talkie-1930 on arithmetic earlier this year](https://maxghenis.com/blog/talkie-1930-math-evals): the base model matches or exceeds GPT-3-175B on most tasks of the 2020 arithmetic suite — a log-probability benchmark — while the instruction-tuned model scores 4.9% (strict, 5-shot) on GSM8K word problems, against 17.8% for same-size LLaMA-13B. The knowledge is in there; asking nicely fails to surface it. My unpublished probes of Gallup-style attitude questions hit the same wall at the chat layer.

So the design is *sensor mode*, not oracle mode:

- **The vintage model is a measurement device.** Don't ask it to role-play a pollster. Score candidate statements under period framings and read log-probabilities — the protocol that already works for its arithmetic — to extract attitude signals a 1930 informant would give.
- **A modern model is the blinded reasoner.** It sees anonymized series and the sensor's readouts, proposes hypotheses about mechanisms (cohort replacement, thermostatic response, backlash), and makes the calibrated forecasts — without ever touching a named post-1930 fact.
- **Ninety years of actuals grade the pipeline**, under proper scoring rules, with the reversal items weighted for exactly the failure mode every model I tested exhibited on GSS 2024.

Whether the attitude knowledge survives the trip out of a 1930 base model the way arithmetic does is an open empirical question — that's the first experiment for the summer checkpoint.

## Why forecasting is a workable training objective

There's an alignment argument for forecasting that goes beyond using forecasts as targets, and it's worth stating plainly.

RLHF trains models toward responses people rate highly. [Sharma et al. (2023)](https://arxiv.org/abs/2310.13548) document where that gradient leads: systems that agree with users at the expense of accuracy, because responses matching a user's views get rated higher. The reward signal itself pays for flattery.

Forecasting against resolved outcomes pays differently. Under a strictly proper scoring rule (Brier score, log score — Gneiting and Raftery 2007 is the standard treatment), the unique way to maximize expected score is to report your actual belief, calibrated. There is no gradient toward telling anyone what they want to hear, because no one's approval enters the loss. Reality grades the work. A training regime built on graded forecasts is one of the few places where "be honest about what you believe, including your uncertainty" is not a norm you hope generalizes but the literal optimum of the objective. My results make the modest empirical version of this point: the arms trained to please (90% intervals covering 50–55%) were beaten on calibration by arithmetic on residuals (90%).

Four things this does not solve:

1. **Inner alignment.** A system can achieve excellent scores on-distribution while representing something other than truthful reporting; proper scoring shapes incentives, not internals, and says nothing about behavior off-distribution.
2. **Performative prediction.** Value forecasts that are believed can move values. Scoring rules assume the outcome is exogenous to the report; at scale, it isn't.
3. **Dual use.** As above — the same model that forecasts value change well tells you where to push.
4. **The normative step.** A calibrated distribution over post-reflection values is an input. Choosing what to align to given that distribution — whose values, aggregated how, with what side-constraints — is a human decision this program informs and cannot make.

## What happens next

Three commitments, in increasing order of infrastructure required:

1. **Forward pre-registration against GSS 2026 and 2028.** Point forecasts and 90% intervals for all 20 items (plus full response distributions for the ordinal ones), from me, from baseline models, and from any LLM anyone cares to submit — committed publicly before the data exist. No contamination argument is possible about data that hasn't been collected. If you work on LLM forecasting and want to add an arm, the repo issue tracker is open.
2. **Sensor-mode evaluation of the summer Talkie checkpoint.** First test: can log-probability elicitation recover known 1930s-era attitude signals where chat elicitation fails, the way it does for arithmetic? If yes: forecast the polling era, 1936 onward, and grade.
3. **Anonymization as default protocol.** Any retrospective "LLM predicts public opinion" result I produce — and, I'd argue, anyone else's — should report the anonymized-series number next to the identified one. The gap between them is a direct measurement of how much of the claimed skill is recall. In my case that gap was the difference between publishing a 2.2x claim and publishing this post instead.

Code, data extracts, prompts, raw model outputs, and the pre-analysis plan: [github.com/maxghenis/value-forecasting](https://github.com/maxghenis/value-forecasting), branch `ea-post-rewrite-2026-07`, directory `ea-rewrite-2026-07/`.

In 2022, acceptance of same-sex relations stood at 62.7%, and every classical method I ran, plus three modern language models, put 2024 in the low-to-mid 60s. It came in at 55.9. The models were sure; the naive baseline was appropriately unsure; nobody was right. That is the current state of value forecasting, measured as carefully as I know how — and the reason the next claims in this area, mine included, should arrive pre-registered.

---

*This revises the value-forecasting chapter of a book I'm writing, [Society in Silico](https://society-in-silico.org). Feedback welcome, especially from people working on forecasting evaluation, survey methodology, and alignment targets — and criticism of the pre-analysis plan before I register the 2026 forecasts.*

**References without inline links:** Gneiting, T. & Raftery, A. E. (2007). "Strictly proper scoring rules, prediction, and estimation." *Journal of the American Statistical Association* 102(477): 359–378. · Danaher, J. (2021). "Axiological futurism: The systematic study of the future of values." *Futures*. · MacAskill, W., Bykvist, K. & Ord, T. (2020). *Moral Uncertainty*. Oxford University Press.
