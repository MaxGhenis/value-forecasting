"""
08_uncertainty.py — POST-REGISTRATION uncertainty quantification for the paper.

Referee-prompted additions, all deterministic given the committed record
(seeded bootstrap): paired accuracy comparisons vs the naive baseline, exact
binomial coverage tests, discordant-pair (McNemar) coverage comparisons,
reversal-stratum paired contrasts, the effort sweep on the common completed
item subset, the identified-vs-anonymized aggregate contrast, and
simple-random-sampling standard errors for the eight 2022->2024 reversal
changes (no design effects, so these UNDERSTATE the true survey SEs).

Output: results/uncertainty.json — every uncertainty number quoted in the
paper comes from this file.
"""
import json
import subprocess
from pathlib import Path

import numpy as np
from scipy import stats

RES = Path(__file__).resolve().parents[1] / "results"
ana = json.loads((RES / "analysis.json").read_text())
base = json.loads((RES / "baselines.json").read_text())
llm = json.loads((RES / "llm_forecasts.json").read_text())
gss = json.loads((RES / "gss_series.json").read_text())["variables"]

# Pin the robustness forecasts to the commit that introduced them (601c272):
# the working tree may hold a later resumed run that is not part of the record
# this paper reports. Fall back to the file only if git is unavailable.
try:
    rob = json.loads(subprocess.run(
        ["git", "show", "601c272:ea-rewrite-2026-07/results/robustness_forecasts.json"],
        capture_output=True, text=True, check=True,
        cwd=Path(__file__).resolve().parents[1]).stdout)
except Exception:
    rob = json.loads((RES / "robustness_forecasts.json").read_text())

actual = {v: float(a) for v, a in ana["actual_2024"].items()}
strata = ana["strata"]
V = list(actual)
rng = np.random.default_rng(1930)
NBOOT = 20_000


def cell(arm, v, cut="2022"):
    if arm in ("naive", "linear", "arima", "ets"):
        m = base[v]["cutoffs"][cut]["methods"][arm]
    elif arm in ("o3", "gpt-5-mini-medium", "gpt-5-mini-high"):
        m = rob["point"][arm].get(v, {}).get(cut)
        if not m or "error" in m:
            return None
    elif arm == "gpt-5-mini-anon":
        m = llm["anon"]["gpt-5-mini"][v][cut]
    else:
        m = llm["point"][arm][v][cut]
    return m["point"], m["lo90"], m["hi90"]


def errs(arm, items, cut="2022"):
    return np.array([abs(cell(arm, v, cut)[0] - actual[v]) for v in items])


def covered(arm, v, cut="2022"):
    c = cell(arm, v, cut)
    if c is None:
        return None
    pt, lo, hi = c
    return bool(lo <= actual[v] <= hi)


def paired(arm, ref="naive", items=V, cut="2022"):
    d = errs(arm, items, cut) - errs(ref, items, cut)
    boots = np.array([rng.choice(d, len(d), replace=True).mean()
                      for _ in range(NBOOT)])
    lo, hi = np.percentile(boots, [2.5, 97.5])
    return {"n": len(d), "mean_delta": round(float(d.mean()), 2),
            "boot95": [round(float(lo), 2), round(float(hi), 2)],
            "t_p": round(float(stats.ttest_rel(errs(arm, items, cut),
                                               errs(ref, items, cut)).pvalue), 3),
            "wilcoxon_p": round(float(stats.wilcoxon(
                errs(arm, items, cut), errs(ref, items, cut)).pvalue), 3),
            "sign": [int((d > 0).sum()), int((d < 0).sum())]}


out = {"kind": "post-registration uncertainty quantification (seeded bootstrap, "
               "exact tests); SRS change SEs carry no design effects and "
               "understate true survey uncertainty",
       "seed": 1930, "n_boot": NBOOT}

# 1. paired MAE vs naive, aligned horizon
out["paired_mae_vs_naive_2022"] = {a: paired(a) for a in
                                   ["gpt-5-mini", "gpt-4o", "claude-opus-4-8"]}

# 2. coverage vs nominal (exact binomial) and vs naive (discordant pairs)
cov_tests = {}
for arm, k in [("gpt-5-mini", None), ("gpt-4o", None), ("claude-opus-4-8", None),
               ("o3", None)]:
    cs = [covered(arm, v) for v in V]
    cs = [c for c in cs if c is not None]
    k = sum(cs)
    cov_tests[arm] = {"covered": f"{k}/{len(cs)}",
                      "binom_p_vs_0.90": float(f"{stats.binomtest(k, len(cs), 0.90).pvalue:.2g}")}
    n01 = sum(1 for v in V if covered("naive", v) and covered(arm, v) is False)
    n10 = sum(1 for v in V if not covered("naive", v) and covered(arm, v) is True)
    cov_tests[arm]["discordant_vs_naive"] = [n01, n10]
    cov_tests[arm]["mcnemar_p"] = round(float(
        stats.binomtest(min(n01, n10), n01 + n10, 0.5).pvalue), 3) if n01 + n10 else None
out["coverage_tests_2022"] = cov_tests
n01 = sum(1 for v in V if covered("o3", v) and not covered("gpt-5-mini", v))
n10 = sum(1 for v in V if not covered("o3", v) and covered("gpt-5-mini", v))
out["o3_vs_gpt5mini_minimal_coverage"] = {
    "discordant": [n01, n10],
    "mcnemar_p": round(float(stats.binomtest(min(n01, n10), n01 + n10, 0.5).pvalue), 3)}

# 3. coverage on the 12 non-reversal items
nonrev = [v for v in V if strata[v]["class"] != "reversal"]
out["nonreversal_coverage_2022"] = {
    a: f"{sum(covered(a, v) for v in nonrev)}/{len(nonrev)}"
    for a in ["gpt-5-mini", "gpt-4o"]}

# 4. reversal-stratum paired contrast (descriptive; n = 8)
rev = [v for v in V if strata[v]["class"] == "reversal"]
out["paired_reversal_mae_vs_naive"] = {a: paired(a, items=rev)
                                       for a in ["gpt-5-mini", "gpt-4o"]}

# 5. effort sweep on the common completed subset (committed high-effort cells)
sub = [v for v in V if cell("gpt-5-mini-high", v) is not None]
out["effort_sweep_common_subset"] = {
    "items": sub, "n": len(sub),
    "mae": {"minimal": round(float(errs("gpt-5-mini", sub).mean()), 2),
            "medium": round(float(errs("gpt-5-mini-medium", sub).mean()), 2),
            "high": round(float(errs("gpt-5-mini-high", sub).mean()), 2),
            "naive": round(float(errs("naive", sub).mean()), 2)}}

# 6. identified vs anonymized aggregate (2010 cutoff), paired bootstrap
d = errs("gpt-5-mini-anon", V, "2010") - errs("gpt-5-mini", V, "2010")
boots = np.array([rng.choice(d, len(d), replace=True).mean() for _ in range(NBOOT)])
out["anon_minus_identified_mae_2010"] = {
    "mean_delta": round(float(d.mean()), 2),
    "boot95": [round(float(np.percentile(boots, 2.5)), 2),
               round(float(np.percentile(boots, 97.5)), 2)]}

# 7. SRS standard errors for the eight reversal changes (no design effects)
srs = {}
for v in rev:
    n22, n24 = gss[v]["n"]["2022"], gss[v]["n"]["2024"]
    p22, p24 = gss[v]["series"]["2022"] / 100, gss[v]["series"]["2024"] / 100
    se = 100 * np.sqrt(p22 * (1 - p22) / n22 + p24 * (1 - p24) / n24)
    ch = strata[v]["change24"]
    srs[v] = {"change": ch, "srs_se": round(float(se), 2),
              "ci95": [round(ch - 1.96 * se, 2), round(ch + 1.96 * se, 2)],
              "crosses_zero": bool(ch - 1.96 * se < 0 < ch + 1.96 * se)}
out["reversal_change_srs"] = srs

(RES / "uncertainty.json").write_text(json.dumps(out, indent=2))
print(json.dumps({k: v for k, v in out.items()
                  if k in ("paired_mae_vs_naive_2022", "effort_sweep_common_subset",
                           "anon_minus_identified_mae_2010")}, indent=1))
print("crossing zero:", [v for v, d in srs.items() if d["crosses_zero"]])
