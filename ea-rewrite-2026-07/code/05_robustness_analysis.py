"""
05_robustness_analysis.py — metrics for the POST-REGISTRATION robustness arms.

Extends 04_analysis.py to the arms produced by 05_robustness_forecasts.py, scored
against the SAME committed actuals, strata, and baselines. The pre-registered arms'
numbers are read verbatim from results/analysis.json (never recomputed) so the
comparison basis is identical; only the new arms are computed here.

Computes, per new arm and horizon: MAE / bias / medAE / 90% coverage / mean width;
MAE stratified by 2024 behavior (reversal / continuation / stable); the identified-
vs-anonymized probe; and HOMOSEX-specific point + interval with reversal-catch.

Output: results/robustness_analysis.json (+ printed aggregate table).
"""
import json
from pathlib import Path
import numpy as np

RES = Path(__file__).resolve().parents[1] / "results"
pre = json.loads((RES / "analysis.json").read_text())          # pre-registered record
rob = json.loads((RES / "robustness_forecasts.json").read_text())
robcost = json.loads((RES / "robustness_costs.json").read_text())

actual = {v: float(a) for v, a in pre["actual_2024"].items()}   # committed actuals
strata = pre["strata"]                                          # committed strata
fvars = list(actual)
NAIVE_MAE = 3.15                                                 # committed naive/ETS baseline
HOMOSEX_2024 = actual["HOMOSEX"]                                # 55.94

PRE_ARMS = ["naive", "linear", "arima", "ets", "gpt-5-mini", "gpt-4o", "claude-opus-4-8"]
ROB_ARMS = [a for a in ["o3", "gpt-5-mini-medium", "gpt-5-mini-high", "deepseek-v4-flash"]
            if a in rob.get("point", {})]

def rob_point(arm, v, cut):
    m = rob["point"].get(arm, {}).get(v, {}).get(cut)
    if not m or "error" in m:
        return None
    return m["point"], m["lo90"], m["hi90"]

def metrics(arm, cut):
    e, cov, wid, byc = [], [], [], {"reversal": [], "continuation": [], "stable": []}
    for v in fvars:
        f = rob_point(arm, v, cut)
        if f is None:
            continue
        pt, lo, hi = f; a = actual[v]
        err = pt - a
        e.append(err); cov.append(lo <= a <= hi); wid.append(hi - lo)
        byc[strata[v]["class"]].append(abs(err))
    if not e:
        return {"n": 0, "mae": None, "bias": None, "medae": None, "cov90": None,
                "width90": None, "mae_by_class": {c: None for c in byc}}
    e = np.array(e)
    return {"n": len(e), "mae": round(float(np.mean(np.abs(e))), 2),
            "bias": round(float(np.mean(e)), 2),
            "medae": round(float(np.median(np.abs(e))), 2),
            "cov90": round(float(np.mean(cov)), 3),
            "width90": round(float(np.mean(wid)), 2),
            "mae_by_class": {c: (round(float(np.mean(x)), 2) if x else None)
                             for c, x in byc.items()}}

def anon_mae(arm, cut):
    e = []
    for v in fvars:
        m = rob["anon"].get(arm, {}).get(v, {}).get(cut)
        if not m or "error" in m:
            continue
        e.append(abs(m["point"] - actual[v]))
    return (round(float(np.mean(e)), 2), len(e)) if e else (None, 0)

out = {"kind": "post-registration robustness analysis (paired with pre-registered analysis.json)",
       "cutoffs": rob.get("meta", {}).get("cutoffs", {}),
       "unavailable": rob.get("meta", {}).get("unavailable", {}),
       "actual_2024_HOMOSEX": HOMOSEX_2024,
       "committed_naive_mae_2022": NAIVE_MAE,
       "metrics": {"2022": {}, "2010": {}},
       "anon_probe": {}, "homosex": {}, "headline_checks": {}, "costs": robcost}

# ---- metrics for new arms; pre-registered arms copied verbatim from analysis.json ----
for cut in ("2022", "2010"):
    for a in PRE_ARMS:
        out["metrics"][cut][a] = pre["metrics"][cut][a]
    for a in ROB_ARMS:
        out["metrics"][cut][a] = metrics(a, cut)

# ---- anonymized-vs-identified probe (new arms; committed gpt-5-mini pulled from analysis.json) ----
for cut in ("2022", "2010"):
    out["anon_probe"][cut] = {}
    for a in ROB_ARMS:
        ident = out["metrics"][cut][a]["mae"]
        anon, n = anon_mae(a, cut)
        out["anon_probe"][cut][a] = {
            "identified_mae": ident, "anon_mae": anon, "n": n,
            "edge_over_naive_identified": (round(NAIVE_MAE - ident, 2) if ident is not None else None),
            "edge_over_naive_anon": (round(pre["metrics"][cut]["naive"]["mae"] - anon, 2)
                                     if anon is not None else None)}
    # committed gpt-5-mini(minimal) probe, verbatim, for side-by-side
    out["anon_probe"][cut]["gpt-5-mini(minimal, pre-registered)"] = pre["anon_probe"][cut]

# ---- HOMOSEX-specific point + interval, reversal catch (actual 55.94) ----
for cut in ("2022", "2010"):
    out["homosex"][cut] = {}
    for a in ROB_ARMS:
        f = rob_point(a, "HOMOSEX", cut)
        if f is None:
            out["homosex"][cut][a] = None; continue
        pt, lo, hi = f
        out["homosex"][cut][a] = {"point": pt, "lo90": lo, "hi90": hi,
                                  "abs_err": round(abs(pt - HOMOSEX_2024), 2),
                                  "interval_covers_5594": bool(lo <= HOMOSEX_2024 <= hi)}
    # pre-registered arms' HOMOSEX 2022 points (from headline_checks), for reference
    out["homosex"][cut]["_pre_registered_points"] = (
        pre["headline_checks"]["homosex_pred_2022cut"] if cut == "2022" else "see analysis.json")

# ---- headline checks: beat naive? honest coverage? HOMOSEX reversal caught? ----
m22 = out["metrics"]["2022"]
for a in ROB_ARMS:
    mm = m22[a]
    hx = out["homosex"]["2022"][a]
    out["headline_checks"][a] = {
        "mae_2022": mm["mae"],
        "beats_naive_3.15": (mm["mae"] is not None and mm["mae"] < NAIVE_MAE),
        "cov90_2022": mm["cov90"],
        "honest_coverage_>=0.90": (mm["cov90"] is not None and mm["cov90"] >= 0.90),
        "reversal_subset_mae_2022": mm["mae_by_class"]["reversal"],
        "homosex_point_2022": (hx["point"] if hx else None),
        "homosex_interval_covers_5594_2022": (hx["interval_covers_5594"] if hx else None),
    }

(RES / "robustness_analysis.json").write_text(json.dumps(out, indent=2))

# ---------------- printed aggregate table ----------------
def row(a, m):
    c = m["mae_by_class"]
    def s(x): return "  -  " if x is None else f"{x:>5}"
    mae = "  -  " if m["mae"] is None else f"{m['mae']:>5}"
    bias = "  -  " if m["bias"] is None else f"{m['bias']:>+5}"
    cov = "  -  " if m["cov90"] is None else f"{m['cov90']:>5}"
    wid = "  -  " if m["width90"] is None else f"{m['width90']:>5}"
    print(f"{a:26s} {m['n']:>2} {mae} {bias} {cov} {wid}   "
          f"{s(c['reversal'])}/{s(c['continuation'])}/{s(c['stable'])}")

ALL = PRE_ARMS + ROB_ARMS
LBL = {"gpt-5-mini": "gpt-5-mini (minimal) *PRE-REG"}
for cut, title in (("2022", "PRIMARY / aligned: history <=2022 -> 2024"),
                   ("2010", "LONG horizon: history <=2010 -> 2024")):
    print(f"\n== {title} ==")
    print(f"{'arm':26s} {'n':>2} {'MAE':>5} {'bias':>5} {'cov90':>5} {'wid':>5}   MAE[rev/cont/stab]")
    for a in ALL:
        row(LBL.get(a, a), out["metrics"][cut][a])

print("\n== Anonymized-vs-identified probe (edge over naive; +=better than naive) ==")
for cut in ("2022", "2010"):
    print(f"  -- cut {cut} --")
    for a, p in out["anon_probe"][cut].items():
        if a.startswith("gpt-5-mini(minimal"):
            print(f"    {a:34s} ident={p['gpt5mini_identified_mae']} anon={p['gpt5mini_anon_mae']} "
                  f"edge_id={p['edge_over_naive_identified']} edge_anon={p['edge_over_naive_anon']}")
        else:
            print(f"    {a:34s} ident={p['identified_mae']} anon={p['anon_mae']} "
                  f"edge_id={p['edge_over_naive_identified']} edge_anon={p['edge_over_naive_anon']}")

print(f"\n== HOMOSEX (actual 2024 = {HOMOSEX_2024}); did point/interval catch the reversal? ==")
for cut in ("2022", "2010"):
    print(f"  -- cut {cut} --")
    for a in ROB_ARMS:
        h = out["homosex"][cut][a]
        if h:
            print(f"    {a:22s} point={h['point']:>5} [{h['lo90']:>5},{h['hi90']:>5}] "
                  f"abs_err={h['abs_err']:>5}  covers 55.94: {h['interval_covers_5594']}")

print("\n== Headline checks (2022 aligned) ==")
for a in ROB_ARMS:
    h = out["headline_checks"][a]
    print(f"  {a:22s} MAE={h['mae_2022']} beats_naive(3.15)={h['beats_naive_3.15']} "
          f"cov90={h['cov90_2022']} honest(>=.90)={h['honest_coverage_>=0.90']} "
          f"rev_MAE={h['reversal_subset_mae_2022']} HOMOSEXpt={h['homosex_point_2022']}")

arm_costs = {m: c for m, c in robcost.items() if isinstance(c, dict) and "usd" in c}
tot = sum(c["usd"] for c in arm_costs.values())
est = robcost.get("lost_segment_estimate", {}).get("est_total_usd", 0)
print(f"\n== Cost == measured ${tot:.4f} + estimated lost segment ${est:.4f} = ${tot+est:.4f}")
for m, c in arm_costs.items():
    print(f"  {m:22s} {c['calls']:3d} calls  ${c['usd']:.4f}")
if out["unavailable"]:
    print("\n== Unavailable arms ==")
    for k, v in out["unavailable"].items():
        print(f"  {k}: {v.get('status')} — {v.get('error','')[:80]}")
