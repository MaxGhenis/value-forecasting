---
title: Conclusion
---

We proposed treating AI alignment partly as a forecasting problem: rather than assuming we know correct values or deferring indefinitely to current preferences, predict where human values converge as material and informational constraints are lifted. Using the General Social Survey (1972-2024) as ground truth, we tested whether language models can forecast value trajectories.

## What We Found

**LLMs partially capture value trends**: In retrospective tests across 16 GSS variables (2010→2024), LLMs beat the naive baseline by 1.44× on MAE (6.4 vs 9.2 points) and correctly predicted direction in 94% of cases. This suggests LLMs have learned patterns about value evolution beyond simple extrapolation.

**But they miss reversals**: GPT-4o predicted 69% HOMOSEX acceptance for 2024; the actual value was 55%—a 7-point decline from 2021 that the model completely missed. This demonstrates a fundamental limitation: LLMs extrapolate trends but fail when structural conditions shift.

**Long-term trends are robust, short-term fluctuations are not**: HOMOSEX acceptance rose from 11% (1973) to 62% (2021)—a 51-point increase over 48 years. The 2024 dip to 55% occurred during a polarized election year with a survey mode change. Whether this represents temporary noise or a sustained reversal remains unknown.

**Income correlates with values**: Higher-income respondents show more liberal values (67% vs. 43% for HOMOSEX by income quartile). This 24-point gap is consistent with post-materialism theory but does not establish causation.

**Heterogeneity persists**: Different values moved in different directions (HOMOSEX down, ABANY up). Different demographic groups hold different views. Any alignment approach must contend with this genuine diversity.

## Implications for AI Alignment

### What This Work Establishes

This paper establishes a **research program**, not an alignment solution. We demonstrate:

1. **Empirical testability**: Value forecasting can be validated against real survey data, unlike purely philosophical approaches
2. **Partial predictability**: LLMs capture some patterns in value evolution, though imperfectly
3. **The limits of trend extrapolation**: Reversals and non-monotonic dynamics exist and are hard to predict

### What This Work Does NOT Establish

We do not claim:
- That LLMs can reliably predict long-term value trajectories (the 2024 reversal disproves this)
- That forecasted values have normative authority (prediction ≠ prescription)
- That we know how to translate value distributions into alignment targets (this is a separate problem)

### The Normative Framework

Value forecasting provides **empirical information** for democratic deliberation, not **normative authority** for alignment decisions. Even if we accurately predict that post-scarcity values would endorse X, this doesn't automatically justify aligning AI to X. The forecast is one input among many—alongside current preferences, philosophical argument, and democratic process.

The question "what will people value?" is distinct from "what should AI do?" Conflating these would be paternalistic—using predicted future preferences to override present democratic choices.

### Tentative Recommendations

If value forecasting develops into a more reliable methodology, we suggest:
1. **Condition on scenarios, not dates**: Forecast values under specified conditions (abundance, deliberation, information access)
2. **Report full distributions**: Maintain uncertainty over value heterogeneity; avoid point estimates
3. **Continuous validation**: Update forecasts as new survey data arrives; track calibration
4. **Democratic governance**: Ensure forecasting assumptions are transparent and subject to public input

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

The question "what values should AI be aligned with?" has no purely philosophical answer. It has an empirical component: we can study how values evolve and what conditions influence that evolution. The GSS provides 50+ years of evidence that values change—sometimes predictably, sometimes not.

This paper shows that LLMs capture *some* patterns in value evolution, but miss reversals and structural shifts. The 2024 HOMOSEX decline demonstrates that even short-term forecasts fail when political and social conditions change. This is a cautionary result, not a success story.

Yet the research program remains valuable. Alignment that treats values as fixed will systematically misalign with humans living under different conditions. We need tools to anticipate value evolution—tools that are empirically grounded and honestly calibrated.

Value forecasting is one candidate tool, but it requires substantial development before practical use: better uncertainty quantification, longer forecast horizons, validation against diverse variables and countries, and—crucially—governance frameworks that prevent misuse.

The veil of scarcity may be lifting. Whether AI alignment can responsibly lift with it remains an open question.

## Code and Data Availability

All code is available at [github.com/maxghenis/value-forecasting](https://github.com/maxghenis/value-forecasting). GSS data is available from NORC at [gss.norc.org](https://gss.norc.org).
