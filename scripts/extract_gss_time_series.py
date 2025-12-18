"""Extract full GSS time series for all variables."""

import pandas as pd
import numpy as np
from pathlib import Path

# Variable definitions with liberal response values (as strings from GSS Stata file)
VARIABLES = {
    "HOMOSEX": {"liberal": ["not wrong at all"], "description": "Not wrong at all"},
    "GRASS": {"liberal": ["should be legal"], "description": "Legal"},
    "PREMARSX": {"liberal": ["not wrong at all"], "description": "Not wrong at all"},
    "ABANY": {"liberal": ["yes"], "description": "Yes"},
    "FEPOL": {"liberal": ["disagree"], "description": "Disagree (women suited)"},
    "NATRACE": {"liberal": ["too little"], "description": "Too little"},
    "NATEDUC": {"liberal": ["too little"], "description": "Too little"},
    "NATENVIR": {"liberal": ["too little"], "description": "Too little"},
    "NATHEAL": {"liberal": ["too little"], "description": "Too little"},
    "EQWLTH": {"liberal": ["the government should reduce income differences", "2.0", "3.0"], "description": "Gov reduce (1-3)"},  # 7-point scale
    "HELPPOOR": {"liberal": ["government should help", "2.0"], "description": "Gov action (1-2)"},  # 5-point scale
    "CAPPUN": {"liberal": ["oppose"], "description": "Oppose"},
    "GUNLAW": {"liberal": ["favor"], "description": "Favor"},
    "TRUST": {"liberal": ["can trust", "most people can be trusted"], "description": "Can trust"},
    "FAIR": {"liberal": ["fair", "would try to be fair"], "description": "Fair"},
    "POLVIEWS": {"liberal": ["extremely liberal", "liberal", "slightly liberal"], "description": "Liberal"},
    "PRAYER": {"liberal": ["approve"], "description": "Approve"},
}


def main():
    data_path = Path(__file__).parent.parent / "data" / "gss7224_r2.dta"

    # Read relevant columns
    cols = ["year"] + [v.lower() for v in VARIABLES.keys()]
    print(f"Loading GSS data from {data_path}...")

    try:
        df = pd.read_stata(data_path, columns=cols)
    except ValueError as e:
        # Some columns might not exist, try loading all and filter
        print(f"Warning: {e}")
        df = pd.read_stata(data_path)
        available_cols = [c for c in cols if c in df.columns]
        df = df[available_cols]

    print(f"Loaded {len(df)} observations, years {df['year'].min()}-{df['year'].max()}")

    results = {}

    for var_upper, config in VARIABLES.items():
        var = var_upper.lower()
        if var not in df.columns:
            print(f"  Skipping {var_upper} (not in dataset)")
            continue

        var_df = df[["year", var]].dropna()

        # Convert to string for comparison (handles categorical)
        var_series = var_df[var].astype(str).str.lower().str.strip()
        liberal_vals = [str(v).lower().strip() for v in config["liberal"]]

        def calc_pct(group):
            vals = group[var].astype(str).str.lower().str.strip()
            n_liberal = vals.isin(liberal_vals).sum()
            return 100 * n_liberal / len(vals) if len(vals) > 0 else np.nan

        # Calculate % liberal by year
        yearly = var_df.groupby("year", observed=True).apply(
            calc_pct, include_groups=False
        ).dropna().round(0).astype(int)

        results[var_upper] = dict(yearly)
        print(f"  {var_upper}: {len(yearly)} years, range {yearly.min():.0f}%-{yearly.max():.0f}%")

    # Print as Python dict for copy-paste
    print("\n\n# Copy this to gss_variables.py:\n")
    print("HISTORICAL_TRAJECTORIES = {")
    for var, data in sorted(results.items()):
        print(f'    "{var}": {{')
        items = sorted(data.items())
        # Format in rows of ~5 items
        for i in range(0, len(items), 5):
            row = items[i:i+5]
            line = ", ".join(f"{y}: {v}" for y, v in row)
            if i + 5 < len(items):
                line += ","
            print(f"        {line}")
        print("    },")
    print("}")


if __name__ == "__main__":
    main()
