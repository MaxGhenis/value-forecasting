---
title: Related Work
---

## Moral Change and Axiological Futurism

Philosophers have long studied how moral views evolve. @singer1981expanding proposed that the "expanding circle" of moral concern—from kin to tribe to nation to humanity—represents a consistent pattern in moral progress. @pinker2011better documented declining violence across history, attributing it partly to expanding empathy and reason.

More recently, @danaher2021axiological introduced "axiological futurism" as a systematic field studying future human values. This work asks: What are the best predictors of value change? Can we identify patterns that inform expectations about future values? Our work operationalizes these questions empirically.

@macaskill2014normative developed decision theory for acting under "normative uncertainty"—uncertainty about which moral framework is correct. Value forecasting can be seen as quantifying this uncertainty: rather than philosophical argument about which values are correct, we estimate probability distributions over future values.

## AI Alignment Approaches

Current alignment approaches typically assume known values. RLHF [@christiano2017deep; @ouyang2022training] trains systems to match human feedback, implicitly treating current preferences as the target. Constitutional AI [@bai2022constitutional] specifies principles (be helpful, harmless, honest) that systems should follow.

@gabriel2020artificial argues that the "central challenge for theorists is not to identify 'true' moral principles for AI; rather, it is to identify fair principles for alignment" given reasonable disagreement. Our approach sidesteps this by forecasting the distribution of values rather than selecting one framework.

@dafoe2020cooperative highlights that alignment alone is insufficient—systems must also cooperate. Value forecasting could identify which value systems facilitate cooperation, informing both what to align toward and how.

## LLMs for Survey Prediction

Recent work demonstrates that LLMs can reproduce survey response patterns. @argyle2023out showed that LLMs fine-tuned on demographic information can simulate human subpopulations ("silicon samples"), reproducing voting patterns at 85%+ accuracy. This suggests LLMs learn genuine patterns about human attitudes, not just surface-level text statistics.

@hewitt2024predicting found GPT-4 can predict experimental treatment effects in social science studies with r=0.85 correlation to actual results. This indicates LLMs have learned causal patterns in human behavior, not just correlations.

The SubPOP project fine-tuned LLMs on GSS data, achieving 69% accuracy on opinion prediction [@subpop2025]. However, this work focused on cross-sectional prediction (predicting opinions at a given time), not temporal forecasting (predicting how opinions will change).

Our work extends this line by testing whether LLMs can predict opinion *trajectories*—not just what people think now, but how that will change over years and decades.

## AI Forecasting and Calibration

A growing literature evaluates LLMs as forecasters against human prediction benchmarks. @halawi2024approaching developed a retrieval-augmented LLM system that approaches human forecaster accuracy on competitive platforms like Metaculus and Good Judgment Open. Their system achieves RMS calibration error of 0.042 compared to 0.038 for the human crowd aggregate—near parity. Critically, this required both fine-tuning and ensemble aggregation; base models under zero-shot prompting were poorly calibrated.

Forecasting platforms like Metaculus provide benchmarks for evaluating AI predictions using proper scoring rules. The Brier score—where lower is better and 0.25 represents random guessing—has become standard. Early GPT-4 models achieved ~0.25 (random baseline), while GPT-3-level models performed worse than random due to overconfidence [@metaculus2024]. Recent models like o1 and o3 show significant improvements.

The FOReCAst benchmark [@forecast2024] explicitly evaluates both forecasting accuracy and confidence calibration, built entirely from Metaculus questions with clear resolution criteria. Key findings: aggregating forecasts from multiple sources substantially improves performance, with median predictions achieving Brier scores (~0.12) comparable to the best individual AI systems.

For uncertainty quantification, the literature suggests temperature sampling alone does not yield calibrated probabilities. More principled approaches include: (1) ensemble aggregation across models or prompts, (2) fine-tuning on proper scoring rules, and (3) post-hoc calibration using held-out data. We adopt model ensembling as the most practical approach for expressing uncertainty over long-term value forecasts.

## Backlash and Counter-Mobilization

Political scientists have documented that social progress often triggers backlash. @luker1984abortion showed how abortion rights mobilized counter-movements. @fetner2008us documented how LGBTQ+ visibility provoked organized opposition.

More recently, @prri2024 found declining support for LGBTQ+ rights across multiple measures after years of steady increase, with the sharpest drops among Republicans and young people. @pbs2024 attributed this to counter-mobilization as LGBTQ+ people "identify more publicly and assert their rights."

This literature suggests that value trajectories may be non-monotonic: progress in one direction can trigger resistance that reverses or slows change. A key question for value forecasting is whether LLMs can predict these inflection points.
