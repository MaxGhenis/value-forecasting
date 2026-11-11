"""
01_extract_gss.py — survey-weighted GSS attitude series (1972-2024) for the
2026-07 value-forecasting rewrite.

Reads the cumulative GSS 1972-2024 R2 file, computes weighted shares of a
verified target response per variable-year, and full response distributions for
ordinal items. Target/denominator codes are verified against the file's value
labels (see PREANALYSIS_PLAN.md). Output: results/gss_series.json.

Weights (NORC guidance for the cumulative file):
  year <= 2018 -> wtssall   ;   year >= 2021 -> wtssnrps
with documented fallbacks. Denominator = substantive responses only
(DK/NA/IAP/refused/skipped are Stata extended-missing -> NaN -> dropped).
"""
import json
from pathlib import Path
import numpy as np
import pandas as pd
import pyreadstat

DTA = Path("/Users/maxghenis/value-forecasting/data/gss7224_r2.dta")
OUT = Path(__file__).resolve().parents[1] / "results" / "gss_series.json"
MIN_N = 50  # minimum unweighted valid responses per wave

# Verified codings (codes confirmed against value labels 2026-07-10).
# target = codes counted in the numerator; denom = substantive codes counted in
# the denominator (excludes 'other'=5 on the sex-morality items).
VARS = {
    "HOMOSEX":  dict(target=[4], denom=[1,2,3,4], label="not wrong at all",
                     desc="same-sex sexual relations are not wrong at all"),
    "GRASS":    dict(target=[1], denom=[1,2], label="should be legal",
                     desc="marijuana should be made legal"),
    "PREMARSX": dict(target=[4], denom=[1,2,3,4], label="not wrong at all",
                     desc="premarital sex is not wrong at all"),
    "FEFAM":    dict(target=[3,4], denom=[1,2,3,4], label="disagree",
                     desc="disagree that women should tend home, men achieve outside"),
    "FEPOL":    dict(target=[2], denom=[1,2], label="disagree",
                     desc="disagree that men are better suited emotionally for politics"),
    "SPKHOMO":  dict(target=[1], denom=[1,2], label="allowed to speak",
                     desc="a homosexual should be allowed to give a public speech"),
    "SPKATH":   dict(target=[1], denom=[1,2], label="allowed to speak",
                     desc="an anti-religionist should be allowed to give a public speech"),
    "ABANY":    dict(target=[1], denom=[1,2], label="yes",
                     desc="abortion should be legal for any reason"),
    "CAPPUN":   dict(target=[2], denom=[1,2], label="oppose",
                     desc="oppose the death penalty for murder"),
    "POLVIEWS": dict(target=[1,2,3], denom=[1,2,3,4,5,6,7], label="liberal side (1-3)",
                     desc="self-identify on the liberal side of the 7-point ideology scale"),
    "EQWLTH":   dict(target=[1,2,3], denom=[1,2,3,4,5,6,7], label="govt reduce differences (1-3)",
                     desc="government should reduce income differences (1-3 of 7)"),
    "HELPPOOR": dict(target=[1,2], denom=[1,2,3,4,5], label="govt should help (1-2)",
                     desc="government should help the poor (1-2 of 5)"),
    "GUNLAW":   dict(target=[1], denom=[1,2], label="favor permit",
                     desc="favor requiring a police permit to buy a gun"),
    "NATRACE":  dict(target=[1], denom=[1,2,3], label="too little",
                     desc="too little is spent improving conditions of Black Americans"),
    "NATENVIR": dict(target=[1], denom=[1,2,3], label="too little",
                     desc="too little is spent on the environment"),
    "NATFARE":  dict(target=[1], denom=[1,2,3], label="too little",
                     desc="too little is spent on welfare"),
    "NATHEAL":  dict(target=[1], denom=[1,2,3], label="too little",
                     desc="too little is spent on health"),
    "NATEDUC":  dict(target=[1], denom=[1,2,3], label="too little",
                     desc="too little is spent on education"),
    "TRUST":    dict(target=[1], denom=[1,2,3], label="can be trusted",
                     desc="most people can be trusted"),
    "FAIR":     dict(target=[2], denom=[1,2,3], label="try to be fair",
                     desc="people try to be fair"),
    "PRAYER":   dict(target=[1], denom=[1,2], label="approve ban",
                     desc="approve the Supreme Court ban on required school prayer"),
}
# Ordinal items for the full-distribution arm (code -> short label).
DIST = {
    "HOMOSEX":  {1:"always wrong",2:"almost always wrong",3:"sometimes wrong",4:"not wrong at all"},
    "PREMARSX": {1:"always wrong",2:"almost always wrong",3:"sometimes wrong",4:"not wrong at all"},
    "POLVIEWS": {1:"extremely liberal",2:"liberal",3:"slightly liberal",4:"moderate",
                 5:"slightly conservative",6:"conservative",7:"extremely conservative"},
}

def main():
    cols = ["year","wtssall","wtssnrps","wtssps","wtss"] + [v.lower() for v in VARS]
    print(f"Reading {DTA} ({len(cols)} cols)...")
    df, _ = pyreadstat.read_dta(str(DTA), usecols=cols, encoding="latin1")
    df["year"] = df["year"].astype(int)
    print(f"Loaded {len(df):,} rows, {df.year.min()}-{df.year.max()}")

    # Resolve one weight per row (explicit, year-based).
    w_pre  = df["wtssall"].fillna(df["wtss"]).fillna(1.0)
    w_post = df["wtssnrps"].fillna(df["wtssps"]).fillna(df["wtssall"]).fillna(df["wtss"]).fillna(1.0)
    df["w"] = np.where(df["year"] >= 2021, w_post, w_pre)
    # record dominant weight source per year for transparency
    wsrc = {}
    for y, g in df.groupby("year"):
        if y >= 2021:
            wsrc[int(y)] = "wtssnrps" if g["wtssnrps"].notna().mean() > 0.5 else "wtssps/other"
        else:
            wsrc[int(y)] = "wtssall" if g["wtssall"].notna().mean() > 0.5 else "wtss/other"

    out = {"source": DTA.name, "min_n": MIN_N,
           "weight_rule": "year<=2018:wtssall ; year>=2021:wtssnrps (fallbacks documented)",
           "weight_source_by_year": wsrc, "variables": {}}

    for V, spec in VARS.items():
        v = V.lower()
        s = pd.to_numeric(df[v], errors="coerce")
        denom = df[s.isin(spec["denom"])].copy()
        series, ns = {}, {}
        for y, g in denom.groupby("year"):
            n = len(g)
            if n < MIN_N:
                continue
            num = g.loc[pd.to_numeric(g[v]).isin(spec["target"]), "w"].sum()
            den = g["w"].sum()
            series[int(y)] = round(100 * num / den, 2)
            ns[int(y)] = int(n)
        out["variables"][V] = {
            "description": spec["desc"], "target_label": spec["label"],
            "target_codes": spec["target"], "denom_codes": spec["denom"],
            "series": series, "n": ns, "n_waves": len(series),
        }
        yrs = sorted(series)
        tail = {y: series[y] for y in yrs if y >= 2016}
        print(f"  {V:9s} {len(series):2d} waves  {yrs[0]}-{yrs[-1]}  recent={tail}")

    # distribution arm
    out["distributions"] = {}
    for V, codemap in DIST.items():
        v = V.lower(); s = pd.to_numeric(df[v], errors="coerce")
        allcodes = list(codemap)
        sub = df[s.isin(allcodes)]
        dist = {}
        for y, g in sub.groupby("year"):
            if len(g) < MIN_N:
                continue
            den = g["w"].sum()
            dist[int(y)] = {codemap[c]: round(100*g.loc[pd.to_numeric(g[v])==c,"w"].sum()/den,2)
                            for c in allcodes}
        out["distributions"][V] = {"labels": list(codemap.values()), "by_year": dist}

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2))
    print(f"\nWrote {OUT}")
    # sanity gate
    h = out["variables"]["HOMOSEX"]["series"]
    print(f"SANITY HOMOSEX: 2018={h.get(2018)} 2021={h.get(2021)} 2022={h.get(2022)} 2024={h.get(2024)}")
    print(f"        GRASS 2024={out['variables']['GRASS']['series'].get(2024)}  "
          f"ABANY 2024={out['variables']['ABANY']['series'].get(2024)}")

if __name__ == "__main__":
    main()
