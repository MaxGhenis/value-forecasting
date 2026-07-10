"""
04_analysis.py — metrics for every arm vs the GSS 2024 holdout.

Computes MAE / bias / median AE / 90% coverage / mean interval width per arm and
horizon; MAE stratified by 2024 behavior (reversal / continuation / stable);
the anonymized-series probe; and distribution-arm total-variation distance.
Output: results/analysis.json (+ printed summary).
"""
import json
from pathlib import Path
import numpy as np

RES = Path(__file__).resolve().parents[1] / "results"
gss = json.loads((RES / "gss_series.json").read_text())
base = json.loads((RES / "baselines.json").read_text())
llm = json.loads((RES / "llm_forecasts.json").read_text())

V = gss["variables"]
fvars = [v for v in V if 2024 in {int(y) for y in V[v]["series"]}]
def series(v): return {int(y): val for y, val in V[v]["series"].items()}
actual = {v: series(v)[2024] for v in fvars}
BASE_ARMS = ["naive", "linear", "arima", "ets"]
LLM_ARMS = ["gpt-5-mini", "gpt-4o", "claude-opus-4-8"]
ARMS = BASE_ARMS + LLM_ARMS

def forecast(arm, v, cut):
    try:
        if arm in BASE_ARMS:
            m = base[v]["cutoffs"][cut]["methods"][arm]
        else:
            m = llm["point"][arm][v][cut]
        if "error" in m: return None
        return m["point"], m["lo90"], m["hi90"]
    except (KeyError, TypeError):
        return None

# ---- 2024-behavior stratification (descriptive; not a forecast input) ----
strata = {}
for v in fvars:
    s = series(v)
    pre_year = max(y for y in s if y <= 2022)
    pre = s[pre_year]; ch = round(s[2024] - pre, 2)
    recent = sorted(y for y in s if y <= 2022)[-5:]
    slope = np.polyfit(recent, [s[y] for y in recent], 1)[0]  # pts/yr
    if slope > 0.2 and ch < -2: cls = "reversal"
    elif slope < -0.2 and ch > 2: cls = "reversal"
    elif abs(ch) <= 2: cls = "stable"
    elif (slope > 0.2 and ch > 0) or (slope < -0.2 and ch < 0): cls = "continuation"
    else: cls = "stable"
    strata[v] = {"pre_year": pre_year, "pre": pre, "change24": ch,
                 "recent_slope": round(float(slope), 3), "class": cls}

def metrics(arm, cut):
    e, cov, wid, byc = [], [], [], {"reversal": [], "continuation": [], "stable": []}
    for v in fvars:
        f = forecast(arm, v, cut)
        if f is None: continue
        pt, lo, hi = f; a = actual[v]
        err = pt - a
        e.append(err); cov.append(lo <= a <= hi); wid.append(hi - lo)
        byc[strata[v]["class"]].append(abs(err))
    e = np.array(e)
    return {"n": len(e), "mae": round(np.mean(np.abs(e)), 2), "bias": round(np.mean(e), 2),
            "medae": round(float(np.median(np.abs(e))), 2),
            "cov90": round(float(np.mean(cov)), 3), "width90": round(float(np.mean(wid)), 2),
            "mae_by_class": {c: (round(np.mean(x), 2) if x else None) for c, x in byc.items()}}

out = {"n_vars": len(fvars), "actual_2024": actual, "strata": strata,
       "class_counts": {c: sum(1 for v in fvars if strata[v]["class"] == c)
                        for c in ["reversal", "continuation", "stable"]},
       "metrics": {}}
for cut in ("2022", "2010"):
    out["metrics"][cut] = {arm: metrics(arm, cut) for arm in ARMS}

# ---- anonymized probe ----
def arm_mae(fdict, cut):
    e = []
    for v in fvars:
        m = fdict.get(v, {}).get(cut)
        if not m or "error" in m: continue
        e.append(abs(m["point"] - actual[v]))
    return round(np.mean(e), 2), len(e)
out["anon_probe"] = {}
for cut in ("2022", "2010"):
    ident_mae = out["metrics"][cut]["gpt-5-mini"]["mae"]
    anon_mae, n = arm_mae(llm["anon"]["gpt-5-mini"], cut)
    naive_mae = out["metrics"][cut]["naive"]["mae"]
    out["anon_probe"][cut] = {
        "gpt5mini_identified_mae": ident_mae, "gpt5mini_anon_mae": anon_mae,
        "naive_mae": naive_mae, "n": n,
        "edge_over_naive_identified": round(naive_mae - ident_mae, 2),
        "edge_over_naive_anon": round(naive_mae - anon_mae, 2)}

# ---- distribution arm ----
out["distribution"] = {}
for v in ["HOMOSEX", "PREMARSX", "POLVIEWS"]:
    act = gss["distributions"][v]["by_year"]["2024"]
    labels = gss["distributions"][v]["labels"]
    rec = {"actual_2024": act, "arms": {}}
    for arm in ["gpt-5-mini", "claude-opus-4-8"]:
        pred = llm["distribution"].get(arm, {}).get(v)
        if not pred or "error" in pred: continue
        tv = 0.5 * sum(abs(pred.get(k, 0) - act[k]) for k in labels) / 100
        rec["arms"][arm] = {"pred": pred, "tv_distance": round(tv, 4),
                            "topcat_err": round(pred.get(labels[-1], 0) - act[labels[-1]], 2)}
    out["distribution"][v] = rec

# ---- headline replication checks ----
m22 = out["metrics"]["2022"]
best_simple = min(("naive", "ets"), key=lambda a: m22[a]["mae"])
out["headline_checks"] = {
    "homosex_2024_actual": actual["HOMOSEX"],
    "homosex_pred_2022cut": {a: forecast(a, "HOMOSEX", "2022")[0] for a in ARMS},
    "clean_gpt5mini_mae_2022": m22["gpt-5-mini"]["mae"],
    "best_simple_baseline_2022": best_simple,
    "best_simple_baseline_mae_2022": m22[best_simple]["mae"],
    "ratio_gpt5mini_over_bestsimple": round(m22["gpt-5-mini"]["mae"] / m22[best_simple]["mae"], 2),
    "all_cov90_below_0.9_at_2022": all(m22[a]["cov90"] < 0.9 for a in ARMS),
}
(RES / "analysis.json").write_text(json.dumps(out, indent=2))

# ---- printed summary ----
print(f"n={len(fvars)} vars. Class counts: {out['class_counts']}")
print("\n== Primary (aligned) horizon: history <=2022 -> forecast 2024 ==")
print(f"{'arm':16s} {'n':>2} {'MAE':>5} {'bias':>6} {'cov90':>6} {'width':>6}  MAE[rev/cont/stab]")
for a in ARMS:
    m = m22[a]; c = m["mae_by_class"]
    print(f"{a:16s} {m['n']:>2} {m['mae']:>5} {m['bias']:>+6} {m['cov90']:>6} {m['width90']:>6}"
          f"   {c['reversal']}/{c['continuation']}/{c['stable']}")
print("\n== Long horizon: history <=2010 -> forecast 2024 ==")
for a in ARMS:
    m = out["metrics"]["2010"][a]
    print(f"{a:16s} n={m['n']} MAE={m['mae']} bias={m['bias']:+} cov90={m['cov90']} width={m['width90']}")
print("\n== Anonymized-series probe (gpt-5-mini) ==")
for cut, p in out["anon_probe"].items():
    print(f"  cut{cut}: identified MAE={p['gpt5mini_identified_mae']}  anon MAE={p['gpt5mini_anon_mae']}"
          f"  naive MAE={p['naive_mae']}  edge(ident)={p['edge_over_naive_identified']}"
          f"  edge(anon)={p['edge_over_naive_anon']}")
print("\n== Distribution arm (TV distance to actual 2024) ==")
for v, r in out["distribution"].items():
    for arm, d in r["arms"].items():
        print(f"  {v:9s} {arm:16s} TV={d['tv_distance']}  top-cat err={d['topcat_err']:+}")
print(f"\nHOMOSEX 2024 actual={actual['HOMOSEX']}, preds={out['headline_checks']['homosex_pred_2022cut']}")
print(f"clean gpt-5-mini MAE={m22['gpt-5-mini']['mae']} vs best simple ({best_simple}) "
      f"{m22[best_simple]['mae']} -> ratio {out['headline_checks']['ratio_gpt5mini_over_bestsimple']}x")
