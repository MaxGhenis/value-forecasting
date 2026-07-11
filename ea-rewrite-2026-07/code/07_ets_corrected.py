"""
07_ets_corrected.py — POST-REGISTRATION CORRECTION of the registered ETS baseline.

The registered run (02_baselines.py) passed a bare numpy array to statsmodels'
ETSModel; get_prediction then raises AttributeError ('numpy.ndarray' object has
no attribute 'index') and the coded fallback silently returned the naive
forecast for all 20 items. This was a caller-side input-type error, not a
statsmodels bug. The fix is one line: wrap the identical data in an indexed
pandas Series. Everything else — logit transform, additive error/trend,
undamped, wave-step horizon, 90% interval, inverse-logit — is the registered
specification unchanged. Deterministic given the committed series, so this
correction involves no researcher degrees of freedom.

Output: results/ets_corrected.json (per-item forecasts + aggregates, both
cutoffs), scored against the committed actuals in analysis.json.
"""
import json
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
from statsmodels.tsa.exponential_smoothing.ets import ETSModel

RES = Path(__file__).resolve().parents[1] / "results"
gss = json.loads((RES / "gss_series.json").read_text())["variables"]
ana = json.loads((RES / "analysis.json").read_text())
actual = {v: float(a) for v, a in ana["actual_2024"].items()}
strata = ana["strata"]


def logit(p):
    p = np.clip(np.asarray(p, float), 0.3, 99.7) / 100.0
    return np.log(p / (1 - p))


def inv(x):
    return float(100.0 / (1.0 + np.exp(-np.asarray(x, float))))


out = {"kind": ("post-registration corrected implementation of the registered "
                "ETS/Holt baseline (pandas-Series input; spec otherwise unchanged)"),
       "cutoffs": {}}

for cutoff in (2022, 2010):
    per, e, cov, wid = {}, [], [], []
    byc = {"reversal": [], "continuation": [], "stable": []}
    for v in actual:
        series = {int(y): x for y, x in gss[v]["series"].items()}
        yrs = sorted(y for y in series if y <= cutoff)
        if len(yrs) < 4:
            continue
        hl = pd.Series(logit([series[y] for y in yrs]))          # the one-line fix
        h = sum(1 for y in series if cutoff < y <= 2024)
        r = ETSModel(hl, trend="add", error="add", damped_trend=False).fit(disp=False)
        n = len(hl)
        sf = r.get_prediction(start=n, end=n + h - 1).summary_frame(alpha=0.10)
        row = sf.iloc[-1]
        pt, lo, hi = inv(row["mean"]), inv(row["pi_lower"]), inv(row["pi_upper"])
        a = actual[v]
        per[v] = {"point": round(pt, 2), "lo90": round(lo, 2), "hi90": round(hi, 2),
                  "abs_err": round(abs(pt - a), 2), "covers": bool(lo <= a <= hi)}
        e.append(pt - a); cov.append(lo <= a <= hi); wid.append(hi - lo)
        byc[strata[v]["class"]].append(abs(pt - a))
    e = np.array(e)
    out["cutoffs"][str(cutoff)] = {
        "per_item": per,
        "n": len(e),
        "mae": round(float(np.mean(np.abs(e))), 2),
        "bias": round(float(np.mean(e)), 2),
        "cov90": round(float(np.mean(cov)), 3),
        "n_covered": int(np.sum(cov)),
        "width90": round(float(np.mean(wid)), 2),
        "mae_by_class": {c: (round(float(np.mean(x)), 2) if x else None)
                         for c, x in byc.items()},
    }

(RES / "ets_corrected.json").write_text(json.dumps(out, indent=2))
for cut, m in out["cutoffs"].items():
    print(f"cutoff {cut}: n={m['n']} MAE {m['mae']} cov {m['n_covered']}/{m['n']} "
          f"width {m['width90']} HOMOSEX {m['per_item']['HOMOSEX']}")
