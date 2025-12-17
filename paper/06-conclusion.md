---
title: Conclusion
---

We proposed treating AI alignment partly as a forecasting problem: rather than assuming we know correct values, predict where human values are heading. Using the General Social Survey (1972-2024) as ground truth, we tested whether language models can forecast value trajectories.

Our findings are mixed but informative:

1. **LLMs outperform baselines on historical data**: In retrospective tests, LLMs beat time series baselines by 2.2× on MAE, suggesting they have learned meaningful patterns about value evolution.

2. **But they fail on clean forward tests**: GPT-4o predicted 69% acceptance of same-sex relationships for 2024; the actual value was 55%—a reversal the model completely missed.

3. **Multiple values reversed or diverged**: HOMOSEX, PREMARSX, and NATRACE all declined from recent peaks, while ABANY continued rising. Values do not move in lockstep.

4. **The reversal was broad but uneven**: All party and age groups showed declines in HOMOSEX acceptance, but Republicans and young adults showed the largest drops.

5. **Economic gradients exist**: Higher-income respondents show more liberal values, suggesting economic conditions may influence attitudes—though causality is uncertain.

These results suggest that value forecasting is more challenging than trend extrapolation. LLMs learn patterns from historical data but fail to predict inflection points where progress triggers backlash. For AI alignment, this means:

- **Uncertainty is high**: Confidence intervals should be much wider than current methods produce.
- **Backlash matters**: Models need to predict not just trends but when progress triggers counter-mobilization.
- **Heterogeneity persists**: Alignment targets should be distributions over values, not single points.
- **Temporal horizons matter**: Near-term forecasts (2024) are already wrong; long-term forecasts (2100) compound this uncertainty.

Despite these challenges, the empirical approach has value. Philosophical debates about "correct" values may never resolve. Forecasting—even imperfect forecasting—provides a testable framework for thinking about value evolution. As forecasting methods improve, they could inform alignment targets that are grounded in data rather than intuition.

Future work should:
- Test across more variables, countries, and time periods
- Use base models without RLHF to avoid potential value contamination
- Develop methods to predict backlash dynamics and inflection points
- Condition forecasts on economic and political scenarios
- Model the full joint distribution of values across demographic groups

The question of what values to align AI toward remains open. But treating it as an empirical forecasting problem—rather than purely philosophical speculation—may be a productive path forward.

## Code and Data Availability

All code is available at [github.com/maxghenis/value-forecasting](https://github.com/maxghenis/value-forecasting). GSS data is available from NORC at [gss.norc.org](https://gss.norc.org).
