"""
02_baselines.py — time-series baselines for the 2024 holdout.

For each variable (that has a 2024 wave) and each cutoff (2022 aligned, 2010 long),
produce a point forecast + 90% interval for 2024 from four methods: naive,
linear (OLS), ARIMA(1,1,0), ETS(Holt). All on the logit scale, back-transformed.
Horizon h = number of real GSS waves in (cutoff, 2024] for that variable.

Output: results/baselines.json
"""
import json, warnings
from pathlib import Path
import numpy as np
warnings.filterwarnings("ignore")
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.exponential_smoothing.ets import ETSModel

RES = Path(__file__).resolve().parents[1] / "results"
Z = 1.6448536269514722  # 90% two-sided

def logit(p):
    p = np.clip(np.asarray(p, float), 0.3, 99.7) / 100.0
    return np.log(p / (1 - p))
def inv(x):
    return float(100.0 / (1.0 + np.exp(-np.asarray(x, float))))

def naive(hist_logit, h):
    pt = hist_logit[-1]
    d = np.diff(hist_logit)
    sd = np.std(d, ddof=1) if len(d) > 1 else 0.5
    half = Z * sd * np.sqrt(h)
    return pt, pt - half, pt + half

def linear(years, hist_logit, target_year):
    x = np.asarray(years, float); y = np.asarray(hist_logit, float); n = len(x)
    xb = x.mean(); Sxx = ((x - xb) ** 2).sum()
    b = ((x - xb) * (y - y.mean())).sum() / Sxx
    a = y.mean() - b * xb
    yhat = a + b * x; s = np.sqrt(((y - yhat) ** 2).sum() / (n - 2))
    x0 = target_year; mu = a + b * x0
    se = s * np.sqrt(1 + 1 / n + (x0 - xb) ** 2 / Sxx)
    return mu, mu - Z * se, mu + Z * se

def arima(hist_logit, h):
    for order in [(1, 1, 0), (0, 1, 0)]:
        try:
            r = ARIMA(np.asarray(hist_logit, float), order=order).fit()
            fc = r.get_forecast(h); ci = fc.conf_int(alpha=0.10)
            return float(fc.predicted_mean[-1]), float(ci[-1, 0]), float(ci[-1, 1])
        except Exception:
            continue
    return naive(hist_logit, h)

def ets(hist_logit, h):
    try:
        r = ETSModel(np.asarray(hist_logit, float), trend="add",
                     error="add", damped_trend=False).fit(disp=False)
        n = len(hist_logit)
        sf = r.get_prediction(start=n, end=n + h - 1).summary_frame(alpha=0.10)
        row = sf.iloc[-1]
        return float(row["mean"]), float(row["pi_lower"]), float(row["pi_upper"])
    except Exception:
        return naive(hist_logit, h)

def main():
    gss = json.loads((RES / "gss_series.json").read_text())["variables"]
    out = {}
    for V, d in gss.items():
        series = {int(y): v for y, v in d["series"].items()}
        if 2024 not in series:
            continue
        actual = series[2024]
        entry = {"actual_2024": actual, "cutoffs": {}}
        for cutoff in (2022, 2010):
            yrs = sorted(y for y in series if y <= cutoff)
            if len(yrs) < 4:
                continue
            hl = logit([series[y] for y in yrs])
            h = sum(1 for y in series if cutoff < y <= 2024)  # real waves ahead
            methods = {}
            for name, fn in [("naive", lambda: naive(hl, h)),
                             ("linear", lambda: linear(yrs, hl, 2024)),
                             ("arima", lambda: arima(hl, h)),
                             ("ets", lambda: ets(hl, h))]:
                pt, lo, hi = fn()
                methods[name] = {"point": round(inv(pt), 2),
                                 "lo90": round(inv(lo), 2), "hi90": round(inv(hi), 2)}
            entry["cutoffs"][str(cutoff)] = {"last_year": yrs[-1], "last_value": series[yrs[-1]],
                                             "h_steps": h, "methods": methods}
        out[V] = entry
    (RES / "baselines.json").write_text(json.dumps(out, indent=2))
    print(f"Wrote {RES/'baselines.json'} ({len(out)} vars)")
    print("\nHOMOSEX 2022->2024 (actual 55.9):")
    for m, r in out["HOMOSEX"]["cutoffs"]["2022"]["methods"].items():
        print(f"  {m:7s} {r['point']:5.1f}  [{r['lo90']:.1f}, {r['hi90']:.1f}]")

if __name__ == "__main__":
    main()
