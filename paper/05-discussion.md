---
title: Discussion
---

## Why Did HOMOSEX Reverse?

The reversal in attitudes toward same-sex relationships is the most striking finding. After 30+ years of steady increase, acceptance dropped 7 points from 2021 to 2024. What explains this?

**Political polarization**: PRRI's 2023 American Values Atlas found similar declines and attributed them to partisan divergence [@prri2024]. Republican support for LGBTQ+ rights dropped 7 points while Democratic support remained stable. State-level anti-LGBTQ legislation may have "amped up the volume" on these issues.

**Backlash dynamics**: As LGBTQ+ people became more visible—with record numbers identifying as LGBTQ+ and expanded legal protections—this may have triggered counter-mobilization [@pbs2024]. This pattern is consistent with historical research on social movement backlash [@luker1984abortion; @fetner2008us].

**Generational patterns disrupted**: The reversal was largest among young adults (18-29), dropping 10 points. This contradicts simple generational replacement models where younger cohorts drive liberalization [@inglehart1997modernization]. Something changed among young people specifically—possibly political sorting or social media effects.

**Survey methodology**: The GSS shifted to web-based surveys post-COVID [@gss2024]. While NORC has implemented weighting to adjust for mode effects, some of the observed change could reflect measurement differences rather than true attitude shifts.

## Implications for Value Forecasting

Our results suggest that LLMs can capture historical trends but fail to predict inflection points. This has important implications:

**Extrapolation is not forecasting**: LLMs excel at pattern matching—seeing decades of liberalization, they predict more liberalization. But genuine forecasting requires modeling the causal mechanisms that could reverse trends.

**Backlash dynamics are key**: Social change appears to follow backlash-prone trajectories. Progress in one direction mobilizes opposition, creating non-monotonic paths. Forecasting models need to identify when progress triggers counter-reactions.

**Uncertainty is larger than confidence intervals suggest**: Both LLMs and baselines produced confidence intervals that were far too narrow. The 2024 HOMOSEX actual (55%) fell outside GPT-4o's 90% CI [66, 72] by a large margin. This suggests fundamental uncertainty about value trajectories that current methods fail to capture.

**Heterogeneity matters**: Different values moved in different directions (HOMOSEX down, ABANY up). Different demographic groups moved at different rates. Any alignment target based on forecasted values must account for this heterogeneity, not assume convergence.

## Implications for AI Alignment

The proposal to align AI to forecasted post-reflection values faces challenges:

1. **Forecasting is harder than trend extrapolation**: Current LLMs cannot predict when trends will reverse. Using their forecasts as alignment targets could point AI toward values that won't materialize.

2. **Which time horizon?**: Our 2030 forecast is already questionable given 2024 data. Long-term forecasts (2100) compound this uncertainty. The "long reflection" may not produce the values we predict.

3. **Backlash could be amplified**: If AI systems are aligned to forecasted liberal values and deploy accordingly, this could trigger additional backlash—a feedback loop that further invalidates the forecasts.

4. **Distribution over distributions**: Given uncertainty, alignment targets should be distributions over possible value distributions, with appropriate hedging across scenarios.

Despite these challenges, the core idea—that alignment should account for value evolution—remains important [@gabriel2020artificial; @danaher2021axiological]. Current approaches that treat values as static may be more wrong than imperfect forecasts.

## Limitations

**Sample size**: We tested on six GSS variables and two clean forecast points. More extensive testing across variables, countries, and time periods is needed.

**Model selection**: We tested only OpenAI and Anthropic models. Open-source models (Llama, Mistral) with documented training cutoffs could provide additional clean tests.

**Causality**: The income-values correlation doesn't establish causation. Rising incomes could shift values, or other factors could drive both.

**Survey effects**: GSS methodology changed post-COVID (web surveys, different sampling). Some observed changes may reflect measurement rather than true attitude shifts.

**U.S. focus**: The GSS covers only American attitudes. Value trajectories in other countries may differ substantially.
