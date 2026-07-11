---
title: Introduction
---

AI alignment—ensuring that artificial intelligence systems act in accordance with human values—faces a fundamental challenge: human values are not static. What societies consider morally acceptable changes across generations, sometimes dramatically. Slavery was widely accepted for millennia before abolition movements succeeded in the 19th century. Women's suffrage, interracial marriage, and LGBTQ+ rights have all undergone rapid shifts in public opinion within living memory.

Current approaches to AI alignment typically treat values as fixed targets. Reinforcement Learning from Human Feedback (RLHF) trains systems on contemporary human preferences [@christiano2017deep]. Constitutional AI defines principles the system should follow [@bai2022constitutional]. These approaches implicitly assume we know what values to align with—either our current values or a set of principles we can articulate in advance.

But if values evolve, which values should we use? Our current preferences may be biased, incomplete, or destined to change. Philosophers have proposed aligning AI to "idealized" values—what fully rational, fully informed agents would want [@macaskill2014normative]. This approach, while philosophically attractive, lacks empirical grounding: how do we compute what idealized agents would choose?

We propose a different framing: **treat value alignment partly as a forecasting problem**. Rather than asking "what are the correct values?" we ask "where are human values heading?" This transforms an intractable philosophical question into an empirical one. If AI systems can predict how values evolve—learning patterns from historical data—those predictions could inform alignment targets.

This approach offers several advantages:

1. **Empirically testable**: Unlike philosophical idealization, forecasting accuracy can be measured against actual value changes.

2. **Uncertainty-aware**: Forecasts naturally come with confidence intervals, acknowledging that we don't know future values with certainty.

3. **Heterogeneity-preserving**: Rather than assuming humanity converges to one value system, we can forecast the *distribution* of values across populations.

4. **Temporally grounded**: We align to projected post-reflection values rather than current, possibly transient preferences.

In this paper, we test the core empirical premise: **can language models forecast human value evolution?** We use the General Social Survey (GSS), which has tracked American public opinion since 1972, as ground truth. The GSS provides over 50 years of data on attitudes toward controversial topics—same-sex relationships, marijuana legalization, abortion, and more—enabling rigorous historical validation.

Our contributions are:

1. We establish a methodology for testing value forecasting using temporal holdout: train on data before a cutoff year, predict values after, validate against actual survey results.

2. We show that LLMs outperform time series baselines (linear extrapolation, ARIMA, exponential smoothing) by 2.2× on historical value prediction.

3. Using a methodologically clean test—GPT-4o predicting GSS 2024 data that postdates its training—we demonstrate a critical failure mode: the model predicted continued liberalization while actual values reversed.

4. We analyze the reversal, finding it occurred across demographic groups but was concentrated among Republicans and young adults, consistent with backlash dynamics.

5. We discuss implications for AI alignment: value forecasting may require predicting not just trends but inflection points where progress triggers counter-mobilization.

The remainder of this paper is organized as follows. Section 2 reviews related work on moral change, axiological futurism, and LLM-based survey prediction. Section 3 describes our data and methods. Section 4 presents results. Section 5 discusses implications and limitations. Section 6 concludes.
