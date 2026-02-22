"""
Extract GSS variable trajectories from microdata.
Generates the data used for value forecasting experiments.
"""

import pandas as pd
import json
from pathlib import Path

# Variable definitions with their "liberal" response coding
VARIABLE_CONFIGS = {
    # Social values
    "homosex": {
        "liberal_values": [4],  # "Not wrong at all"
        "description": "Same-sex relations not wrong",
    },
    "grass": {
        "liberal_values": [1],  # "Legal"
        "description": "Marijuana should be legal",
    },
    "premarsx": {
        "liberal_values": [4],  # "Not wrong at all"
        "description": "Premarital sex not wrong",
    },
    "abany": {
        "liberal_values": [1],  # "Yes"
        "description": "Abortion for any reason",
    },
    "fepol": {
        "liberal_values": [2],  # "Disagree" women unsuited
        "description": "Women suited for politics",
    },
    "cappun": {
        "liberal_values": [2],  # "Oppose"
        "description": "Oppose death penalty",
    },
    "gunlaw": {
        "liberal_values": [1],  # "Favor"
        "description": "Favor gun permits",
    },
    # Economic/spending
    "natrace": {
        "liberal_values": [1],  # "Too little"
        "description": "More spending on race issues",
    },
    "nateduc": {
        "liberal_values": [1],  # "Too little"
        "description": "More spending on education",
    },
    "natenvir": {
        "liberal_values": [1],  # "Too little"
        "description": "More spending on environment",
    },
    "natheal": {
        "liberal_values": [1],  # "Too little"
        "description": "More spending on health",
    },
    "eqwlth": {
        "liberal_values": [1, 2, 3],  # Top 3 on 1-7 scale
        "description": "Government reduce inequality",
    },
    "helppoor": {
        "liberal_values": [1, 2],  # Top 2 on 1-5 scale
        "description": "Government help poor",
    },
    # Trust/social capital
    "trust": {
        "liberal_values": [1],  # "Can trust"
        "description": "Most people can be trusted",
    },
    "fair": {
        "liberal_values": [1],  # "Try to be fair"
        "description": "People try to be fair",
    },
    # Political
    "polviews": {
        "liberal_values": [1, 2, 3],  # Liberal on 1-7 scale
        "description": "Self-identified liberal",
    },
    "prayer": {
        "liberal_values": [1],  # "Approve" of ban
        "description": "Approve school prayer ban",
    },
}

# Years to extract
TARGET_YEARS = [1972, 1974, 1976, 1978, 1980, 1982, 1984, 1985, 1986, 1987, 1988, 1989,
                1990, 1991, 1993, 1994, 1996, 1998, 2000, 2002, 2004, 2006, 2008,
                2010, 2012, 2014, 2016, 2018, 2021, 2022, 2024]

# Key years for experiments (subset with good coverage)
KEY_YEARS = [1972, 1980, 1990, 2000, 2010, 2018, 2021, 2022, 2024]


def extract_trajectories(data_path: str, min_n: int = 50) -> dict:
    """
    Extract value trajectories from GSS microdata.

    Args:
        data_path: Path to GSS .dta file
        min_n: Minimum sample size to include a year

    Returns:
        Dictionary mapping variable names to year->percentage trajectories
    """
    print(f"Loading GSS data from {data_path}...")
    df = pd.read_stata(data_path, convert_categoricals=False)
    print(f"Loaded {len(df):,} respondents across {df['year'].nunique()} years")

    results = {}

    for var, config in VARIABLE_CONFIGS.items():
        if var not in df.columns:
            print(f"Warning: {var} not found in dataset")
            continue

        trajectory = {}
        liberal_vals = config["liberal_values"]

        for year in TARGET_YEARS:
            subset = df[df["year"] == year]
            if var not in subset.columns:
                continue

            col = subset[var]
            # Exclude missing, DK, NA (typically coded as negative or very high)
            valid = col[col.notna() & (col > 0) & (col < 90)]

            if len(valid) >= min_n:
                liberal_pct = (valid.isin(liberal_vals).sum() / len(valid)) * 100
                trajectory[int(year)] = round(liberal_pct, 1)

        if len(trajectory) >= 3:  # At least 3 data points
            results[var.upper()] = {
                "description": config["description"],
                "trajectory": trajectory,
            }

    return results


def calculate_summary_stats(results: dict) -> dict:
    """Calculate summary statistics for each variable."""
    summary = {}

    for var, data in results.items():
        traj = data["trajectory"]
        years = sorted(traj.keys())

        if len(years) < 2:
            continue

        first_year, last_year = years[0], years[-1]
        first_val, last_val = traj[first_year], traj[last_year]
        total_change = last_val - first_val

        # Calculate recent change (2018-2024 if available)
        recent_change = None
        if 2018 in traj and 2024 in traj:
            recent_change = traj[2024] - traj[2018]

        summary[var] = {
            "first_year": first_year,
            "last_year": last_year,
            "first_value": first_val,
            "last_value": last_val,
            "total_change": round(total_change, 1),
            "years_span": last_year - first_year,
            "recent_change_2018_2024": round(recent_change, 1) if recent_change else None,
            "n_observations": len(years),
        }

    return summary


def generate_python_code(results: dict) -> str:
    """Generate Python code for HISTORICAL_TRAJECTORIES dict."""
    lines = ["HISTORICAL_TRAJECTORIES = {"]

    for var, data in sorted(results.items()):
        traj = data["trajectory"]
        desc = data["description"]

        # Format trajectory on one line for key years, or multiple lines if many
        key_years_traj = {y: v for y, v in traj.items() if y in KEY_YEARS}

        lines.append(f'    "{var}": {{')
        lines.append(f'        # {desc}')

        # Split into chunks of 4-5 years per line
        items = list(key_years_traj.items())
        for i in range(0, len(items), 5):
            chunk = items[i:i+5]
            line = ", ".join(f"{y}: {v}" for y, v in chunk)
            lines.append(f"        {line},")

        lines.append("    },")

    lines.append("}")
    return "\n".join(lines)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Extract GSS trajectories from microdata")
    parser.add_argument("--data", default="data/gss7224_r2.dta", help="Path to GSS .dta file")
    parser.add_argument("--output", default="data/trajectories.json", help="Output JSON file")
    parser.add_argument("--min-n", type=int, default=50, help="Minimum sample size")
    args = parser.parse_args()

    # Extract trajectories
    results = extract_trajectories(args.data, min_n=args.min_n)

    # Calculate summary
    summary = calculate_summary_stats(results)

    # Print summary
    print("\n" + "=" * 70)
    print("VARIABLE TRAJECTORIES SUMMARY")
    print("=" * 70)

    for var, stats in sorted(summary.items(), key=lambda x: -abs(x[1]["total_change"])):
        data = results[var]
        print(f"\n{var}: {data['description']}")
        print(f"  {stats['first_year']}-{stats['last_year']}: {stats['first_value']:.0f}% → {stats['last_value']:.0f}% ({stats['total_change']:+.1f} pts)")
        if stats["recent_change_2018_2024"]:
            print(f"  Recent (2018-2024): {stats['recent_change_2018_2024']:+.1f} pts")

    # Save to JSON
    output = {
        "variables": results,
        "summary": summary,
        "extraction_params": {"min_n": args.min_n, "data_file": args.data},
    }

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nSaved to {args.output}")

    # Also generate Python code
    print("\n" + "=" * 70)
    print("PYTHON CODE (copy to gss_variables.py):")
    print("=" * 70)
    print(generate_python_code(results))
