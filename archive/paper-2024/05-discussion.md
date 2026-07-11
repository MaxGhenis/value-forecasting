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

**Complementing, not replacing, RLHF**: Value forecasting doesn't replace human feedback—it contextualizes it. Near-term RLHF handles current preferences; long-term forecasts provide aspirational targets. The combination is more robust than either alone.

## Governance and Democratic Legitimacy

Value forecasting raises important governance questions that require institutional design, not just technical solutions.

**The legitimacy challenge**: Aligning AI to "projected post-reflection values" rather than current preferences involves choices about what counts as "reflection," what material conditions to assume, and how to weight different demographic groups. These are inherently political choices that encode power. A forecast conditioned on "post-scarcity with democratic deliberation" yields different values than one conditioned on "persistent inequality with polarized media."

**Who decides?** Key governance questions include:
- Who specifies conditioning scenarios (abundance vs. scarcity, deliberation vs. manipulation)?
- How are forecasts validated and updated as new data arrives?
- What role do diverse stakeholders—not just AI developers—play in setting forecast parameters?
- Under what conditions should forecasts influence deployed AI systems vs. remaining research outputs?

**Transparency requirements**: Any use of value forecasting in alignment should be transparent about:
1. The model and training cutoff used
2. The conditioning scenarios assumed
3. The demographic weighting applied
4. The uncertainty bounds and calibration track record
5. How forecasts integrate with other alignment approaches (RLHF, constitutional AI)

**Democratic oversight mechanisms**: We recommend:
- Public disclosure of forecasting methodology before deployment
- Regular validation against new survey data with public reporting
- Multi-stakeholder input on conditioning scenario specification
- Appeals processes when forecasts are contested
- Prohibition on using forecasts to justify overriding explicit contemporary preferences without democratic mandate

**The distinction between prediction and prescription**: Value forecasting provides *empirical information* about likely value trajectories; it does not provide *normative authority* for those values. Even if we predict post-reflection values would endorse X, this doesn't automatically justify aligning AI to X. The forecast informs democratic deliberation—it doesn't substitute for it [@gabriel2020artificial].

We treat forecasts as inputs to governance processes, not outputs that determine alignment targets. The methodology is descriptive; the application is normative and requires democratic legitimation.

The core insight remains: alignment that treats values as static will systematically misalign with the values of future humans who live under different conditions [@gabriel2020artificial; @danaher2021axiological].

## Limitations

**Exploratory nature**: This study was not pre-registered. All analyses should be considered exploratory. The framing evolved during analysis—we did not predict the 2024 HOMOSEX reversal, but rather discovered and explained it post-hoc. Future work should use formal pre-registration.

**Variable coverage**: We tested 16 GSS variables, all showing some historical change. Variables with stable trends or random-walk patterns were not systematically tested. Selection may inflate apparent LLM performance.

**Short forecast horizon**: Our cleanest test (GPT-4o predicting 2024) covers only 1-3 years. Claims about long-term forecasting (decades to centuries) are speculative extrapolation, not empirically validated. The 2024 reversal shows even short-term forecasts fail when structural conditions shift.

**Uncertainty calibration**: Both LLMs and baselines achieved only ~40-50% coverage for 90% confidence intervals. Our uncertainty estimates are not reliable. The separate-prompt approach to CI elicitation may contribute to poor calibration.

**Mode effects confound**: GSS shifted to web-based surveys post-COVID. Some observed 2021-2024 changes may reflect measurement differences rather than true attitude shifts. We cannot separate these effects.

**U.S. focus**: The GSS covers only American attitudes. Value trajectories vary across countries and cultures. Generalization to non-U.S. contexts is untested.

**Potential training data contamination**: While GPT-4o predicting GSS 2024 is a clean test, the gpt-3.5-turbo-instruct results (2010→2024) may be contaminated if the model encountered GSS trends during training. Testing with older base models would strengthen causal claims.

**Missing reward specification**: Even if forecasts were accurate, translating value distributions into alignment targets requires aggregation rules (vote? average? Pareto?) that we do not specify. Forecasting and specification are distinct problems.

**Income-values causality**: The correlation between income and liberal values doesn't establish that rising incomes cause value shifts. Education, urbanization, and other factors may confound this relationship.
