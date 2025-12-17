---
title: Conclusion
---

We proposed treating AI alignment partly as a forecasting problem: rather than assuming we know correct values or deferring indefinitely to current preferences, predict where human values converge as material and informational constraints are lifted. Using the General Social Survey (1972-2024) as ground truth, we tested whether language models can forecast value trajectories.

## Key Findings

**LLMs capture long-term value trends**: In retrospective tests, LLMs beat time series baselines by 2.2× on MAE, suggesting they have learned meaningful patterns about value evolution—patterns that simple extrapolation misses.

**The 48-year liberalization trend is robust**: HOMOSEX acceptance rose from 11% (1973) to 62% (2021), a 51-point increase representing one of the largest documented shifts in human values. This occurred across cohorts, regions, and (eventually) political parties.

**Short-term fluctuations reflect measurement and context**: The 2024 dip to 55% occurred during a polarized election year with a survey mode change. Such fluctuations are expected in any time series; they don't invalidate the underlying trend any more than a cold week invalidates climate change.

**The income-values gradient provides empirical grounding for post-scarcity projections**: Higher-income respondents—who face fewer material constraints—show systematically more liberal values (67% vs. 43% for HOMOSEX). This 24-point gap represents the "headroom" for value evolution as AI-driven abundance reduces scarcity for the broader population.

**Heterogeneity persists**: Different values move at different rates; different demographic groups hold different views. Alignment targets should be distributions over values, conditioned on scenarios, not point estimates.

## Implications for AI Alignment

The core insight is methodological: **alignment targets should be conditional forecasts, not snapshots**.

Current RLHF anchors AI to contemporary preferences shaped by contemporary constraints—information limits, time pressure, material scarcity, political manipulation. This approach systematically biases alignment toward values that may not persist as conditions change.

Value forecasting asks a different question: what would people value if given time to reflect, access to information, and freedom from material desperation? The income gradient suggests this isn't purely hypothetical—we can observe how values differ when constraints vary.

For practical alignment, we recommend:
1. **Conditional scenario modeling**: Forecast values under specified conditions (abundance, deliberation, information access) rather than specific dates
2. **Distribution targets**: Maintain uncertainty over value distributions; prefer actions robust across scenarios
3. **Demographic weighting**: Use income gradients to approximate post-scarcity conditions
4. **Continuous updating**: Treat forecasts as hypotheses to update as new survey data arrives
5. **Democratic governance**: Ensure forecasting assumptions are transparent and subject to public input

## Future Work

**Longer forecast horizons with older models**: The strongest test of value forecasting uses models with older training cutoffs to predict further into the future. GPT-3.5-turbo-instruct (September 2021 cutoff) could forecast GSS 2022 and 2024—a 3-year horizon. Even older models (davinci-002, GPT-2) could test 5-10 year forecasts. If LLMs can predict multi-year value trajectories from a 2019 starting point, the case for long-term conditional forecasting strengthens considerably.

**Additional directions**:
- Expand to World Values Survey and European Social Survey for cross-national validation
- Test base models without RLHF to rule out training contamination
- Develop formal models linking economic conditions to value trajectories
- Build ensemble methods with proper uncertainty calibration
- Create standardized benchmarks for value forecasting
- Explicitly condition forecasts on economic scenarios and compare predictions

## Conclusion

The question "what values should AI be aligned with?" has no purely philosophical answer. But it does have an empirical component: we can study how values evolve and what conditions influence that evolution. The General Social Survey provides 50+ years of evidence that human values change predictably as conditions change.

AI systems will shape those conditions profoundly. Alignment that ignores value evolution—treating current preferences as fixed—will systematically diverge from the values of humans living under AI-transformed conditions. Value forecasting, grounded in empirical data about how values respond to changing material circumstances, offers a more principled foundation for alignment than either philosophical idealization or static preference polling.

The veil of scarcity is lifting. The question is whether AI alignment will lift with it.

## Code and Data Availability

All code is available at [github.com/maxghenis/value-forecasting](https://github.com/maxghenis/value-forecasting). GSS data is available from NORC at [gss.norc.org](https://gss.norc.org).
