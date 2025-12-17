---
title: Discussion
---

## Short-Term Fluctuations vs. Long-Term Trajectories

The 2024 HOMOSEX data shows a 7-point decline from 2021—notable, but it requires careful interpretation. Several factors suggest this may represent short-term noise rather than a fundamental trend reversal.

**Historical context**: HOMOSEX acceptance rose from 11% (1973) to 62% (2021)—a 51-point increase over 48 years. The 2024 reading of 55% remains well above any pre-2018 level. Even accepting the decline at face value, the long-term trajectory remains strongly positive. Similar short-term fluctuations occurred in 1990 (dropping from 14% to 13%) without reversing the broader trend.

**Measurement factors**: The GSS shifted to web-based surveys post-COVID [@gss2024]. Mode effects for sensitive questions are well-documented in survey methodology research. Web surveys may reduce social desirability bias, yielding more candid responses. Some portion of the observed change likely reflects measurement differences rather than true attitude shifts.

**Political context effects**: The 2024 data was collected during an unusually polarized election year with LGBTQ+ issues prominently politicized. Gallup's parallel tracking shows similar short-term softening [@gallup2024samesex]. These context effects may prove temporary as political salience fades.

**The key question for alignment**: Short-term fluctuations driven by political mobilization, survey mode effects, or measurement noise are largely irrelevant to the long-term value forecasting question. What matters is: *Where do values converge as material constraints are lifted and information access expands?*

## The Core Thesis: Values Under Scarcity Removal

The alignment-relevant question is not "what will values be in 2027?" but rather "what values would humanity hold after extended reflection under post-scarcity conditions?" This reframes value forecasting from short-term prediction to conditional projection.

**Inglehart's post-materialism thesis** provides theoretical grounding [@inglehart1997modernization]. As societies achieve material security, values shift from survival-oriented (order, security, hierarchy) toward self-expression (autonomy, tolerance, diversity). The GSS income gradient we observed—with higher-income quartiles showing more liberal values across variables—is consistent with this framework.

**The income-values relationship** is particularly important. If AI-driven productivity growth substantially increases material abundance, the income-values gradient suggests systematic value shifts. Our Q4 respondents (median income $139,000) showed 67% HOMOSEX acceptance vs. 43% for Q1 (median $7,700). This 24-point gap represents the "headroom" for value evolution as economic constraints relax.

**Conditional forecasting**: Rather than asking "what will happen?" we should ask "what would happen if...?" Key conditioning variables include:
- Material abundance (post-scarcity scenarios)
- Information access and quality
- Deliberation time and institutions
- Absence of political manipulation

Under these conditions, the 48-year liberalization trend—temporarily interrupted by a polarized election year—likely continues.

## Implications for Value Forecasting

Our results suggest LLMs capture long-term value trends effectively but are sensitive to short-term political noise. This has important implications for how value forecasting should be used in alignment:

**Condition on scenarios, not dates**: Rather than predicting "values in 2050," forecast "values given post-scarcity with democratic deliberation." This separates the forecasting question from unknowable political contingencies.

**Focus on robust long-term patterns**: The 48-year HOMOSEX liberalization trend (11%→62%) is robust; the 3-year fluctuation (62%→55%) is noise. Alignment should target the former, not overfit to the latter.

**Use income gradients as proxies for scarcity removal**: The 24-point gap between income quartiles provides empirical grounding for post-scarcity projections. High-income respondents today approximate the material conditions of average respondents under AI-driven abundance.

**Heterogeneity persists and matters**: Different values moved in different directions (HOMOSEX down temporarily, ABANY up). Different demographic groups hold different values. Alignment targets should be distributions over values, not point estimates—and should be robust across reasonable forecasting scenarios.

**Uncertainty quantification needs improvement**: Both LLMs and baselines produced confidence intervals that were too narrow. Future work should use ensemble methods, scenario analysis, and proper calibration to produce honest uncertainty bounds.

## Implications for AI Alignment

Value forecasting offers a principled approach to one of alignment's hardest questions: whose values, and when?

**Why forecast rather than use current values?** Current human preferences reflect current constraints—information limits, time pressure, material scarcity, political manipulation. RLHF on current preferences locks in these limitations. Value forecasting asks: what would people want if these constraints were relaxed?

**The income gradient provides empirical grounding**: We observe that higher-income individuals—who face fewer material constraints—hold systematically different values. This isn't just correlation; it suggests material conditions causally influence values. AI-driven abundance would shift the entire distribution.

**Conditional alignment**: Rather than aligning to a single forecasted value set, AI systems should:
1. Maintain uncertainty over value distributions
2. Condition on scenarios (post-scarcity, democratic deliberation, information access)
3. Prefer actions robust across plausible value futures
4. Update as new survey data arrives

**Governance implications**: Value forecasting is a technology that requires democratic oversight. Who specifies the conditioning scenarios? How are forecasts validated and updated? What role do diverse stakeholders play? These questions require institutional design, not just technical solutions.

**Complementing, not replacing, RLHF**: Value forecasting doesn't replace human feedback—it contextualizes it. Near-term RLHF handles current preferences; long-term forecasts provide aspirational targets. The combination is more robust than either alone.

The core insight remains: alignment that treats values as static will systematically misalign with the values of future humans who live under different conditions [@gabriel2020artificial; @danaher2021axiological].

## Limitations

**Sample size**: We tested on six GSS variables and two clean forecast points. More extensive testing across variables, countries, and time periods is needed.

**Model selection**: We tested only OpenAI and Anthropic models. Open-source models (Llama, Mistral) with documented training cutoffs could provide additional clean tests.

**Causality**: The income-values correlation doesn't establish causation. Rising incomes could shift values, or other factors could drive both.

**Survey effects**: GSS methodology changed post-COVID (web surveys, different sampling). Some observed changes may reflect measurement rather than true attitude shifts.

**U.S. focus**: The GSS covers only American attitudes. Value trajectories in other countries may differ substantially.
