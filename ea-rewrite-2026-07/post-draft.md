# Value forecasting for AI alignment: pre-registered tests and a missed reversal

*Epistemic status: pre-registered empirical results plus a research proposal I hold more loosely. I kept the experiments small: 20 survey items, one holdout wave, one draw per forecast, $0.19 of API spend. I committed the [analysis plan](https://github.com/maxghenis/value-forecasting/blob/0ec5fd3/ea-rewrite-2026-07/PREANALYSIS_PLAN.md) before any forecasting call, and the [repository](https://github.com/maxghenis/value-forecasting/tree/main/ea-rewrite-2026-07) holds the code, prompts, parsed model outputs and results. A pilot with the evaluation choices common in LLM-simulation work (named items, targets inside the training window, n = 2, one weak baseline) produced a 2.4x "LLM beats the baseline" result. Under the controlled design, no LLM beat last-value persistence.*

## Summary

- In the 2024 General Social Survey, 8 of the 20 attitude items I track reversed their pre-2022 trend. Four posted the largest single-wave decline in their item's recorded history: approval of the school-prayer ban −8.4 points, acceptance of same-sex relations −6.8, rejection of traditional gender roles −6.5, marijuana legalization −5.7.
- I pre-registered a forecasting test on that wave, in which three LLMs and classical time-series baselines forecast 2024 from the series through 2022. I labeled each model clean or contaminated by its stated training cutoff. Every arm's point forecast missed the same-sex-relations reversal (predictions 60.2–66.5 vs. actual 55.9), and no LLM beat last-value persistence on overall accuracy (MAE 3.15 vs. 3.58–4.07 points, n = 20).
- The LLMs' 90% intervals covered the truth 50–55% of the time (clean arms); the properly computed naive and linear intervals covered 90% (ARIMA: 80%).
- An anonymization probe explains where earlier "LLM forecasting skill" came from. With the item named, gpt-5-mini "forecast" the same-sex-relations series from 2010 data at 78; with the identity stripped, it said 47.5, so the name alone moved the forecast 30.5 points. Identity-conditioned backtests inside a model's training window measure recall blended with extrapolation, not forecasting.
- The alignment proposal survives in a narrower, more testable form: treat the forecast distribution of post-reflection human values, with calibrated uncertainty at two levels, as an alignment target, and validate the forecasting machinery against history. Vintage-corpus LLMs, trained on text ending in 1930, offer the contamination-proof instrument; for them the whole polling era lies outside the training data.

## Eight of twenty values reversed

Since 1973 the General Social Survey has asked Americans whether same-sex relations are wrong. The survey-weighted share answering "not wrong at all" rose from 11.4% to 62.7% between 1973 and 2022, with no wave-over-wave drop larger than 2.5 points along the way.

In 2024 it fell 6.8 points, to 55.9% (n = 2,125 valid responses), the largest decline in the item's 51-year history, and other items fell with it. I extracted 20 GSS attitude items with a 2024 wave from the [cumulative 1972–2024 microdata](https://gss.norc.org/) (survey-weighted; details in the [results summary](https://github.com/maxghenis/value-forecasting/blob/main/ea-rewrite-2026-07/RESULTS.md)) and classified each by a mechanical rule. An item whose last five waves through 2022 trended up by more than 0.2 points/year but fell more than 2 points in 2024 (or the mirror image) counts as a reversal.

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

The four bolded items posted the largest single-wave declines in their 24–30 waves of history. Every sexual-morality and gender-role item in the set fell. Meanwhile three items continued their trend (support for health spending rose 5.5 points) and nine stayed within 2 points; abortion-for-any-reason ticked up 1.2. Values did not move in lockstep, but trend reversals made up the five largest moves in the wave.

External polling corroborates the direction. [PRRI's American Values Atlas](https://www.prri.org/research/views-on-lgbtq-rights-in-all-50-states/) measured same-sex-marriage support falling from 69% to 67% between 2022 and 2023, with Republican support for nondiscrimination protections down 7 points (66% to 59%). PRRI attributes the declines to partisan polarization and legislative backlash. (GSS methodology also changed after 2018 — mixed web and in-person modes — which NORC flags as a possible contributor to level shifts. A mode effect would have to act selectively to produce trend-consistent rises on some items and record declines on others in the same wave.)

Every language model I tested forecast further gains in same-sex-relations acceptance; if you expected the same, GSS 2024 brings new information.

## Every arm missed it

In the pre-registered test, I showed each forecaster the weighted series through 2022 and asked for a 2024 point estimate and 90% interval. GSS 2024 microdata first became public in 2025, so each model's training cutoff determines whether it could have seen the answer:

| Arm | Cutoff | Status |
|---|---|---|
| gpt-5-mini (headline) | May 2024 | Clean — cutoff predates the 2025 release and the end of fieldwork |
| gpt-4o (robustness) | Oct 2023 | Clean |
| claude-opus-4-8 (ceiling) | Jan 2026 | Deliberately contaminated — a check, see below |

All three models know GSS history through 2022 from training, and I showed them that same span, so the clean arms compete with the baselines on equal information. Three baselines ran beside them, each with proper 90% intervals: last-value persistence ("naive"), OLS on the logit scale ("linear"), and ARIMA(1,1,0). (A fourth baseline, ETS/Holt, silently fell back to naive for all 20 items, because my ETS call passed a bare array where statsmodels wants an indexed series. I found the bug only afterward, so the registered results report ETS as a duplicate of naive; the repo holds a corrected re-run, whose MAE of 4.33 also trails naive's.)

For HOMOSEX, the item everyone watched, the forecasts ran:

| Forecaster | HOMOSEX 2024 point | 90% interval | Actual: 55.9 |
|---|---|---|---|
| Naive (last value) | 62.7 | [56.8, 68.3] | miss |
| Linear | 60.2 | [49.2, 70.3] | covered — by a 21-point-wide interval |
| ARIMA | 63.1 | [56.4, 69.3] | miss |
| gpt-5-mini | 66.5 | [62.0, 70.5] | miss |
| gpt-4o | 64.5 | [61.0, 68.0] | miss |
| claude-opus-4-8 | 64.0 | [59.0, 69.0] | miss |

Every point forecast landed between 60.2 and 66.5 against an actual of 55.9. All three LLM intervals excluded the truth; the only interval that contained it did so through width, not foresight. Across all eight reversal items, the LLMs' 90% intervals covered the actual 1/8 (gpt-5-mini), 0/8 (gpt-4o), and 4/8 (claude) times, against 6–7/8 for the classical baselines.

Over all 20 items at the aligned horizon, the arms scored:

| Arm | MAE (pts) | 90% coverage | Mean interval width | MAE on the 8 reversals |
|---|---|---|---|---|
| **Naive** | **3.15** | 0.90 (18/20) | 12.0 | 5.3 |
| Linear | 4.07 | 0.90 (18/20) | 15.1 | 3.4 |
| ARIMA | 3.58 | 0.80 (16/20) | 11.6 | 5.3 |
| gpt-5-mini (clean) | 4.07 | 0.55 (11/20) | 8.6 | 6.3 |
| gpt-4o (clean) | 3.92 | 0.50 (10/20) | 7.6 | 6.1 |
| claude-opus-4-8 (contaminated) | 3.58 | 0.80 (16/20) | 11.0 | 5.4 |

1. **Nothing beat persistence.** The best clean LLM's MAE, 3.92 (gpt-4o), exceeded naive's 3.15, n = 20. The cheapest possible forecast, "2024 equals 2022", beat both clean LLMs by more than sampling noise (paired bootstrap), while the contaminated arm's gap to it spans zero.
2. **The LLMs missed reversals by more than persistence did.** On the eight reversal items the clean LLMs extrapolated the recent trend, the trend broke, and they erred 6.1–6.3 points against naive's 5.3, a gap that eight items cannot resolve. On the nine stable items they also trailed, 1.6–1.7 against naive's 1.0.
3. **LLM intervals ran too narrow.** Clean-arm 90% intervals averaged 7.6–8.6 points wide and covered half the time. The naive and linear intervals averaged 12–15 points wide and covered at their nominal rate (ARIMA: 80%). On this task, knowing that you don't know beat any dynamics the models had learned.

The whole experiment cost $0.19 in API calls (166 of them); the repo holds the prompt code and every parsed output.

### Post-registration robustness arms

I could check three objections cheaply, so I ran them after registration as labeled robustness arms, in separate results files that leave the pre-registered record untouched:

- **"Use a reasoning model."** o3, whose stated training cutoff (June 1, 2024) makes it a clean arm, posted MAE 3.93 vs. naive's 3.15 (n = 20) and erred 6.26 points on the reversal items. Its 90% intervals covered 75%, above the pre-registered clean arms' 50–55% but short of 90%, and it put HOMOSEX at 65.0 [59.0, 71.0], a miss. It still claimed too much certainty, trailed persistence and followed the trend that broke.
- **"You ran the LLM at minimal effort."** At medium reasoning effort, gpt-5-mini posted MAE 4.16. At high effort, on the 11 of 20 items that completed before a session crash, it posted 4.21, with coverage at 64%. Neither beat minimal effort's 4.07; more reasoning budget bought longer deliberation toward the same wrong prior.
- **"Add a clean Anthropic arm."** Anthropic has retired from its first-party API every Claude snapshot whose training cutoff predates the end of GSS 2024 fieldwork (claude-3-5-sonnet-20241022 now returns 404; retired October 2025). As vendors deprecate old snapshots, the set of models anyone can test cleanly on a given wave shrinks, so retrospective clean evaluation has a closing window. Forward pre-registration avoids the problem, and so do open-weights arms, which never retire. (I skipped a DeepSeek arm for the mirror-image reason: DeepSeek documents no training cutoff, so I could not label it clean.)

The robustness arms cost roughly another dollar. A session crash mid-run lost the cost logs for the o3 and medium-effort segments, but the results file keeps every call's parsed output.

## The result a naive design produces

Before building the controls, I ran this task the way much of the LLM-simulation literature runs it: item names shown, forecast targets inside the model's training window, no survey weights, two variables. That pilot produced an LLM beating its single baseline, linear extrapolation, by 2.4x on mean absolute error. I could have published that number, and it resembles results that others have published. The controlled design tested each of the pilot's findings:

| Pilot finding | Design that produced it | What the pre-registered version found |
|---|---|---|
| "LLM beats the baseline 2.4x" (MAE 12.5 vs. 30.2, single linear-extrapolation baseline) | n = 2 items (HOMOSEX, GRASS), item names shown, forecast targets 2000–2021 — all *inside* the model's training window | Does not replicate. On a clean, aligned design, the headline clean LLM ties the linear baseline (MAE 4.07 each) and trails naive persistence (3.15), n = 20 |
| "Everyone is overconfident — LLM CIs covered 43%, baselines 36%" | Same leaky design; degenerate baseline intervals | Half survives. LLMs covered 50–55% at 90% nominal (n = 20); properly computed classical intervals covered 90% |
| "LLMs capture non-linear dynamics baselines miss" | The 1990→2021 HOMOSEX run — where the model had read about the liberalization it was "predicting" | See next section: strip the item name and the long-horizon edge over the best classical baseline disappears |
| "Value trajectories can reverse and trend-followers will miss it" | GPT-4o forecast GSS 2024 from history through 2021; its stated training cutoff (October 2023) predates that wave | Replicates, now with pre-registration: every arm missed the HOMOSEX reversal; 8/20 items reversed |

(I ran the pilot on unweighted shares and the controlled design on NORC's recommended weights.) In the pilot, GPT-4o also made calibrated long-horizon projections. Its prompt showed the series through 2024, ending at 55% (unweighted), yet it put same-sex-relations acceptance at 66 in 2030 and 80 in 2100. The floor of its 80% interval for 2030, 57, exceeds the 2024 reading it had just seen ([`data/longterm_gpt-4o_calibrated.json`](https://github.com/maxghenis/value-forecasting/blob/main/data/longterm_gpt-4o_calibrated.json)).

A design like that asks a model to "forecast" years it has already read about, on items it can name, and reports recall as skill. I had flagged contamination as a concern and run one clean test, the 2024 holdout, but the headline number still came from the leaky design. So I rebuilt the experiment with the controls load-bearing.

The pilot got one thing right: reversals happen, and trend-extrapolators miss them. This time I pre-registered that expectation ("all arms miss the HOMOSEX reversal; point ≥ 60 vs. actual ≈ 55"), and every arm missed; no point forecast fell below 60.2.

## Where the apparent LLM skill came from

The new design includes the control the old one lacked. I re-ran the clean model (gpt-5-mini) on every item with the identity stripped: no item name and no description, only "an anonymized US national survey attitude item" and the numeric series. I compared the result against the identified version at two cutoffs:

- **Cutoff 2022 (shown history = model knowledge):** identity barely matters. Identified and anonymized forecasts differ by a mean of 1.0 point over 20 items. Named or anonymous, the model trails naive persistence (4.07 and 4.62 vs. 3.15).
- **Cutoff 2010 (14 years of un-shown history the model has read about):** identity moves forecasts a mean of 4.5 points, and the famous items move most. The name alone raises the forecast by 30.5 points on HOMOSEX (78.0 identified vs. 47.5 anonymized), 17.0 on GRASS, 9.5 on PREMARSX and 9.0 on FEFAM.

On HOMOSEX, I showed the model data through 2010 (42.7%) and told it to reason only from the series. Named, it answered 78, a level the GSS series has never reached and 15 points above the 2022 value in its training data. The name seems to have retrieved the wrong series, pulling in the level of adjacent, differently worded ones. Gallup's acceptance questions run well above the GSS's four-category "not wrong at all" share, a confusion worth auditing for in any identified-series design. Anonymized, the same model extrapolated the same numbers to 47.5. GSS 2024 recorded 55.9, so both forecasts missed, 30.5 points apart.

In aggregate at the 2010 cutoff, the identified model beats naive by 1.30 points MAE; anonymized, the edge shrinks to 0.82 (n = 20). Against the strongest classical baseline (ARIMA, MAE 7.66), the identified edge of +0.41 flips to −0.07 anonymized. I pre-registered "the edge collapses under anonymization", and the scorecard marks it partial. The edge shrinks by about a third against naive and vanishes against the best baseline, while per-item identified forecasts move by up to 30 points on the name.

The contamination arm tells the same story from the other side. The training window of claude-opus-4-8 (through Jan 2026) includes the GSS 2024 release itself. At the aligned horizon it shows no memorization signature — MAE 3.58 vs. the headline clean arm's 4.07 (n = 20), and it misses HOMOSEX at 64.0 [59, 69] like everyone else. But at the 2010 cutoff it posts MAE 4.18 vs. the clean arms' 5.83–7.25 (n = 20), with reversal-item error of 2.9 vs. their 4.2–7.4 (n = 8). Recall of the history it wasn't shown would produce that gap, though the arm also differs from the clean ones in model family and capability.

A growing literature, descended from the silicon-sampling work of [Argyle et al. (2023)](https://arxiv.org/abs/2209.06899), evaluates LLMs by "predicting" survey results, elections, and social-science findings from before their training cutoffs. Retrospective evaluations of named series inside the training window test recall and report it as forecasting. Two protocols fix the problem: **anonymized series** (cheap but imperfect, since a model may have memorized the dynamics themselves) and **strictly forward pre-registration** (airtight). [Halawi et al. (2024)](https://arxiv.org/abs/2402.18563) already hold LLM geopolitical forecasting to the forward standard; value forecasting should meet it too.

## The proposal

1. **Validate the machinery historically.** Test whether any system — LLM, statistical, hybrid — can forecast distributions of human values out-of-sample, under contamination controls. The GSS 2024 test does part of this and returns a negative interim result at the 2-year horizon. Nothing I tested beat persistence (best clean LLM 3.92 vs. naive 3.15 MAE, n = 20), and every arm's point forecast missed the HOMOSEX reversal.
2. **Forecast the distribution, not the point.** A mature version targets not "X% will hold value V" but the joint distribution of post-reflection values, with uncertainty at two levels. *Aleatoric* uncertainty reflects real heterogeneity across people, which you model rather than average away. *Epistemic* uncertainty concerns what you don't know about that distribution, and it belongs in intervals that cover at their stated rate.
3. **Treat that forecast distribution as an alignment input.** Aligning an AI to a calibrated distribution over where reflective human values will head gives it a different and, I think, better-specified target than a 2026 preference snapshot. Such an AI would hedge across value systems weighted by forecast mass, flag actions that any high-mass value system would judge catastrophic, and preserve option value where the distribution runs wide.

My experiment touches both uncertainty levels. When I asked for full 2024 response distributions on three items, both tested models produced shapes within total-variation distance 0.02–0.08 of the truth. The 2022 distribution carried forward (0.03–0.07) beat both on two of the three items. On HOMOSEX they put the top category 8 points too high, the same trend-following miss as the point forecasts. The clean models' point intervals failed the epistemic test: an alignment-relevant forecast cannot have 90% intervals that cover 50–55% of the time. The 2024 wave shows why: a system aligned to "acceptance keeps rising, 90% sure" would, within two years, have confidently backed the wrong direction for the value it optimized around.

The result reframes the proposal rather than killing it. Point-trajectory extrapolation failed, and the failure argues for a distributional target with honest intervals. It also raises the bar for step 1: any claim that a system forecasts values now needs to beat persistence, cover at its stated rate and survive anonymization, with baselines and n reported inline.

## Objections

**"Your own results show values aren't forecastable."** At the 2-year horizon, nothing beat persistence, but persistence plus honestly wide intervals covered at its stated rate (18/20 at 90%). That gives a usable forecast: "expect roughly today's values, and hold real uncertainty either way." Whether skill exists at longer horizons, where generational replacement dominates period shocks, remains open. I confounded my long-horizon test by design, and the clean instrument below removes that confound. If deeper unpredictability wins, the framework degrades gracefully: the intervals widen to honest widths, and the alignment-relevant output becomes "do not lock anything in."

**"Forecasting values is moral relativism."** A forecast of what humans will value after reflection makes an empirical claim and endorses nothing. This program does not and cannot automate the normative step of deciding what to do with that forecast: whether to align to it, override parts of it, or weight populations. Humans keep that step, and the forecast makes one input to it explicit and gradeable.

**"Who defines 'reflection'?"** This objection hits the proposal's weakest link. GSS drift does not track idealized reflection: 2024's reversals may reflect polarization dynamics more than deliberation, and that may make them harder to forecast. Historical validation tests the prerequisite: can anything predict measured value change at all? Operationalizing "post-reflection" (deliberative-polling outcomes? values after exposure to arguments?) poses a separate, harder design problem, and any choice smuggles in assumptions that the designer should state rather than hide.

**"A good value-change model is a manipulation manual."** Yes, by the logic of [performative prediction](https://arxiv.org/abs/2002.06673) with the sign flipped: the better and more public the forecast, the more it invites steering toward or away from itself. I don't have a clean answer. I would default to publishing evaluation protocols and calibration results, which help everyone check claims, while moving slower on capability recipes; human aggregation of the forecast into decisions offers a partial firewall. This concern weighs against the research program's scale, not its existence — the actors best positioned to steer values are not waiting for my GSS holdout study.

## The instrument: models that have never read a poll

Every design above still leans on training-cutoff bookkeeping and anonymization tricks, because every modern LLM has read the polling record I test it on. LLMs pretrained only on historical text now offer a clean instrument.

Nick Levine, David Duvenaud, and Alec Radford trained [Talkie-1930](https://talkie-lm.com/introducing-talkie), a 13B model, on 260B tokens of pre-1931 English text. It has company: the [Ranke-4B family](https://github.com/DGoettlich/history-llms) of time-locked models with cutoffs from 1913 to 1946, and [TypewriterLM](https://arxiv.org/abs/2606.02991), 7B trained on pre-1913 text. [Underwood, Nelson, and Wilkens (2025)](https://arxiv.org/abs/2505.00030) supply the motivation from the research side: fine-tuning a modern model to sound historical doesn't remove its hindsight; "pretraining on period prose may be required" to simulate historical perspectives credibly.

The field clusters before 1946 because of rights, not compute. US copyright runs 95 years, so as of 2026 everything published through 1930 has entered the public domain, and each later year of cutoff adds licensing where earlier years just add scanning. The Talkie team reports that its historical corpus can grow past a trillion tokens and that it is training a GPT-3-level model.

A 1930 cutoff sounds prohibitive for value forecasting until you notice what it excludes. Gallup ran its first national polls in 1935, and the GSS began in 1972. A pre-1931 model has read no poll it could parrot, so the entire quantitative record of public opinion lies outside its training data. Where my GSS experiment scraped together one clean holdout wave, a 1930-cutoff model faces ninety years of actuals: every reversal, plateau and backlash in the polling record, orders of magnitude more items than my twenty. The question that dominated my GSS test, whether the model already knows the answer, does not arise.

The catch lies in elicitation, and I've measured it. [I evaluated Talkie-1930 on arithmetic earlier this year](https://maxghenis.com/blog/talkie-1930-math-evals). On the 2020 arithmetic suite, a log-probability benchmark, the base model matches or exceeds GPT-3-175B on most tasks. On GSM8K word problems, the instruction-tuned model scores 4.9% (strict, 5-shot), against 17.8% for the same-size LLaMA-13B. The base model holds the knowledge; asking nicely fails to surface it. My [probes of Gallup-style attitude questions](https://github.com/maxghenis/value-forecasting/tree/main/ea-rewrite-2026-07/results/talkie_gallup_probes) hit the same wall at the chat layer.

So I propose *sensor mode*, not oracle mode:

- **Use the vintage model as a measurement device.** Don't ask it to role-play a pollster. Score candidate statements under period framings and read log-probabilities — the protocol that already works for its arithmetic — to extract attitude signals a 1930 informant would give.
- **Make a modern model the blinded reasoner.** It sees anonymized series and the sensor's readouts, proposes hypotheses about mechanisms (cohort replacement, thermostatic response, backlash), and makes the calibrated forecasts — without ever touching a named post-1930 fact.
- **Ninety years of actuals grade the pipeline**, under proper scoring rules, with extra weight on the reversal items, where the LLMs I tested mostly followed the trend that broke.

Nobody yet knows whether the attitude knowledge survives the trip out of a 1930 base model the way arithmetic does, and the first experiment on the next checkpoint will test it.

## Why forecasting is a workable training objective

Forecasting supports an alignment argument that goes beyond using forecasts as targets.

RLHF trains models toward responses people rate highly. [Sharma et al. (2023)](https://arxiv.org/abs/2310.13548) document where that gradient leads: systems that agree with users at the expense of accuracy, because people rate responses that match their views higher. The reward signal itself pays for flattery.

Forecasting against resolved outcomes pays differently. Under a strictly proper scoring rule (Brier score, log score; Gneiting and Raftery 2007 give the standard treatment), you maximize expected score only by reporting your actual belief, calibrated. No gradient pushes toward telling anyone what they want to hear, because no one's approval enters the loss. Reality grades the work. Training on graded forecasts offers one of the few settings where "be honest about what you believe, including your uncertainty" becomes the literal optimum of the objective, not a norm you hope generalizes. My results offer a modest empirical version: arithmetic on residuals (90% coverage) beat the arms trained to please (90% intervals covering 50–55%) on calibration.

Forecasting as an objective leaves four problems unsolved:

1. **Inner alignment.** A system can score well on-distribution while representing something other than truthful reporting; proper scoring shapes incentives, not internals, and says nothing about behavior off-distribution.
2. **Performative prediction.** Value forecasts that people believe can move values. Scoring rules assume the report leaves the outcome untouched; at scale, it won't.
3. **Dual use.** The same model that forecasts value change well tells you where to push.
4. **The normative step.** A calibrated distribution over post-reflection values supplies an input. Humans must choose what to align to given that distribution (whose values, aggregated how, with what side-constraints); this program informs that decision and cannot make it.

## What happens next

I plan three next steps, in increasing order of the infrastructure they require:

1. **Forward pre-registration against GSS 2026 and 2028.** Before NORC releases the data, I plan to publish point forecasts and 90% intervals for all 20 items, plus full response distributions for the ordinal ones. The registration would cover my own forecasts, baseline models and any LLM anyone cares to submit. No contamination argument can touch data that NORC has not yet released. If you work on LLM forecasting and want to add an arm, the repo's issue tracker takes submissions.
2. **Sensor-mode evaluation of the next Talkie checkpoint.** The first test asks whether log-probability elicitation recovers known 1930s-era attitude signals where chat elicitation fails, as it does for arithmetic. If it does, I would forecast the polling era from 1936 onward and grade the results.
3. **Anonymization as default protocol.** Any retrospective "LLM predicts public opinion" result I produce — and, I'd argue, anyone else's — should report the anonymized-series number next to the identified one. The gap between them bounds how much of the claimed skill rides on item identity rather than the shown series, and item identity was one of the design choices behind my pilot's publishable-looking 2.4x.

Code, data extracts, prompts, parsed model outputs and the pre-analysis plan live in [`ea-rewrite-2026-07/`](https://github.com/maxghenis/value-forecasting/tree/main/ea-rewrite-2026-07) of [github.com/maxghenis/value-forecasting](https://github.com/maxghenis/value-forecasting).

In 2022, acceptance of same-sex relations stood at 62.7%, and every classical method I ran, plus three modern language models, put 2024 in the low-to-mid 60s. It came in at 55.9. The models committed, the naive baseline hedged, and nobody got it right. Nothing I tested beat persistence over two years, and the next claims in this area, mine included, should arrive pre-registered.

---

*The value-forecasting research program comes from a book I'm writing, [Society in Silico](https://societyinsilico.com). I welcome feedback, especially from people working on forecasting evaluation, survey methodology, and alignment targets — and criticism of the pre-analysis plan before I register the 2026 forecasts.*

**References without inline links:** Gneiting, T. & Raftery, A. E. (2007). "Strictly proper scoring rules, prediction, and estimation." *Journal of the American Statistical Association* 102(477): 359–378. · Danaher, J. (2021). "Axiological futurism: The systematic study of the future of values." *Futures*. · MacAskill, W., Bykvist, K. & Ord, T. (2020). *Moral Uncertainty*. Oxford University Press.
