"""Generate TypeScript variableData from HISTORICAL_TRAJECTORIES."""

import sys
sys.path.insert(0, 'src')

from value_forecasting.gss_variables import HISTORICAL_TRAJECTORIES, GSS_VARIABLES

# LLM forecasts (keep these as they are calibrated)
llm_forecasts = {
    "HOMOSEX": {
        "description": "Same-sex relations not wrong",
        "forecasts": [
            {"year": 2024, "predicted": 63, "predLow": 56, "predHigh": 70},
            {"year": 2030, "predicted": 66, "predLow": 57, "predHigh": 75},
            {"year": 2050, "predicted": 75, "predLow": 64, "predHigh": 86},
            {"year": 2100, "predicted": 80, "predLow": 69, "predHigh": 91}
        ],
        "predicted2024": 63
    },
    "GRASS": {
        "description": "Marijuana should be legal",
        "forecasts": [
            {"year": 2024, "predicted": 70, "predLow": 61, "predHigh": 79},
            {"year": 2030, "predicted": 72, "predLow": 57, "predHigh": 87},
            {"year": 2050, "predicted": 80, "predLow": 57, "predHigh": 100},
            {"year": 2100, "predicted": 80, "predLow": 57, "predHigh": 100}
        ],
        "predicted2024": 70
    },
    "PREMARSX": {
        "description": "Premarital sex not wrong",
        "forecasts": [
            {"year": 2024, "predicted": 66, "predLow": 59, "predHigh": 73},
            {"year": 2030, "predicted": 70, "predLow": 59, "predHigh": 81},
            {"year": 2050, "predicted": 80, "predLow": 69, "predHigh": 91},
            {"year": 2100, "predicted": 80, "predLow": 69, "predHigh": 91}
        ],
        "predicted2024": 66
    },
    "ABANY": {
        "description": "Abortion for any reason",
        "forecasts": [
            {"year": 2024, "predicted": 50, "predLow": 42, "predHigh": 58},
            {"year": 2030, "predicted": 60, "predLow": 51, "predHigh": 69},
            {"year": 2050, "predicted": 60, "predLow": 42, "predHigh": 78},
            {"year": 2100, "predicted": 60, "predLow": 37, "predHigh": 83}
        ],
        "predicted2024": 50
    },
    "FEPOL": {
        "description": "Women suited for politics",
        "forecasts": [
            {"year": 2024, "predicted": 82, "predLow": 77, "predHigh": 87},
            {"year": 2030, "predicted": 84, "predLow": 77, "predHigh": 91},
            {"year": 2050, "predicted": 86, "predLow": 77, "predHigh": 95},
            {"year": 2100, "predicted": 85, "predLow": 69, "predHigh": 100}
        ],
        "predicted2024": 82
    },
    "CAPPUN": {
        "description": "Oppose death penalty",
        "forecasts": [
            {"year": 2024, "predicted": 39, "predLow": 33, "predHigh": 45},
            {"year": 2030, "predicted": 42, "predLow": 33, "predHigh": 51},
            {"year": 2050, "predicted": 45, "predLow": 34, "predHigh": 56},
            {"year": 2100, "predicted": 55, "predLow": 32, "predHigh": 78}
        ],
        "predicted2024": 39
    },
    "GUNLAW": {
        "description": "Favor gun permits",
        "forecasts": [
            {"year": 2024, "predicted": 72, "predLow": 65, "predHigh": 79},
            {"year": 2030, "predicted": 71, "predLow": 64, "predHigh": 78},
            {"year": 2050, "predicted": 70, "predLow": 59, "predHigh": 81},
            {"year": 2100, "predicted": 70, "predLow": 59, "predHigh": 81}
        ],
        "predicted2024": 72
    },
    "NATRACE": {
        "description": "More spending on race issues",
        "forecasts": [
            {"year": 2024, "predicted": 45, "predLow": 31, "predHigh": 59},
            {"year": 2030, "predicted": 52, "predLow": 37, "predHigh": 67},
            {"year": 2050, "predicted": 55, "predLow": 32, "predHigh": 78},
            {"year": 2100, "predicted": 55, "predLow": 32, "predHigh": 78}
        ],
        "predicted2024": 45
    },
    "NATEDUC": {
        "description": "More spending on education",
        "forecasts": [
            {"year": 2024, "predicted": 73, "predLow": 69, "predHigh": 77},
            {"year": 2030, "predicted": 74, "predLow": 69, "predHigh": 79},
            {"year": 2050, "predicted": 75, "predLow": 68, "predHigh": 82},
            {"year": 2100, "predicted": 75, "predLow": 68, "predHigh": 82}
        ],
        "predicted2024": 73
    },
    "NATENVIR": {
        "description": "More spending on environment",
        "forecasts": [
            {"year": 2024, "predicted": 63, "predLow": 55, "predHigh": 71},
            {"year": 2030, "predicted": 65, "predLow": 56, "predHigh": 74},
            {"year": 2050, "predicted": 65, "predLow": 54, "predHigh": 76},
            {"year": 2100, "predicted": 65, "predLow": 54, "predHigh": 76}
        ],
        "predicted2024": 63
    },
    "NATHEAL": {
        "description": "More spending on health",
        "forecasts": [
            {"year": 2024, "predicted": 68, "predLow": 59, "predHigh": 77},
            {"year": 2030, "predicted": 70, "predLow": 59, "predHigh": 81},
            {"year": 2050, "predicted": 70, "predLow": 59, "predHigh": 81},
            {"year": 2100, "predicted": 70, "predLow": 59, "predHigh": 81}
        ],
        "predicted2024": 68
    },
    "EQWLTH": {
        "description": "Government reduce inequality",
        "forecasts": [
            {"year": 2024, "predicted": 49, "predLow": 43, "predHigh": 55},
            {"year": 2030, "predicted": 52, "predLow": 44, "predHigh": 60},
            {"year": 2050, "predicted": 51, "predLow": 42, "predHigh": 60},
            {"year": 2100, "predicted": 50, "predLow": 39, "predHigh": 61}
        ],
        "predicted2024": 49
    },
    "HELPPOOR": {
        "description": "Government help poor",
        "forecasts": [
            {"year": 2024, "predicted": 31, "predLow": 25, "predHigh": 37},
            {"year": 2030, "predicted": 35, "predLow": 27, "predHigh": 43},
            {"year": 2050, "predicted": 36, "predLow": 27, "predHigh": 45},
            {"year": 2100, "predicted": 35, "predLow": 24, "predHigh": 46}
        ],
        "predicted2024": 31
    },
    "TRUST": {
        "description": "Most people can be trusted",
        "forecasts": [
            {"year": 2024, "predicted": 33, "predLow": 29, "predHigh": 37},
            {"year": 2030, "predicted": 28, "predLow": 21, "predHigh": 35},
            {"year": 2050, "predicted": 27, "predLow": 18, "predHigh": 36},
            {"year": 2100, "predicted": 27, "predLow": 18, "predHigh": 36}
        ],
        "predicted2024": 33
    },
    "FAIR": {
        "description": "People try to be fair",
        "forecasts": [
            {"year": 2024, "predicted": 40, "predLow": 36, "predHigh": 44},
            {"year": 2030, "predicted": 42, "predLow": 35, "predHigh": 49},
            {"year": 2050, "predicted": 43, "predLow": 34, "predHigh": 52},
            {"year": 2100, "predicted": 45, "predLow": 34, "predHigh": 56}
        ],
        "predicted2024": 40
    },
    "POLVIEWS": {
        "description": "Self-identified liberal",
        "forecasts": [
            {"year": 2024, "predicted": 28, "predLow": 24, "predHigh": 32},
            {"year": 2030, "predicted": 30, "predLow": 25, "predHigh": 35},
            {"year": 2050, "predicted": 30, "predLow": 23, "predHigh": 37},
            {"year": 2100, "predicted": 31, "predLow": 24, "predHigh": 38}
        ],
        "predicted2024": 28
    },
    "PRAYER": {
        "description": "Approve school prayer ban",
        "forecasts": [
            {"year": 2024, "predicted": 42, "predLow": 38, "predHigh": 46},
            {"year": 2030, "predicted": 48, "predLow": 39, "predHigh": 57},
            {"year": 2050, "predicted": 50, "predLow": 39, "predHigh": 61},
            {"year": 2100, "predicted": 45, "predLow": 34, "predHigh": 56}
        ],
        "predicted2024": 42
    }
}

def main():
    print("const variableData: Record<string, {")
    print("  description: string;")
    print("  historical: { year: number; actual: number }[];")
    print("  forecasts: { year: number; predicted: number; predLow: number; predHigh: number }[];")
    print("  actual2024: number;")
    print("  predicted2024: number;")
    print("}> = {")

    for var_name in llm_forecasts.keys():
        if var_name not in HISTORICAL_TRAJECTORIES:
            continue

        trajectory = HISTORICAL_TRAJECTORIES[var_name]
        forecast_data = llm_forecasts[var_name]

        # Build historical array (excluding 2024 which is holdout)
        historical = [{"year": y, "actual": v} for y, v in sorted(trajectory.items()) if y < 2024]
        actual2024 = trajectory.get(2024, 0)

        print(f"  {var_name}: {{")
        print(f'    description: "{forecast_data["description"]}",')

        # Historical data
        print("    historical: [")
        for i, h in enumerate(historical):
            comma = "," if i < len(historical) - 1 else ""
            print(f"      {{ year: {h['year']}, actual: {h['actual']} }}{comma}")
        print("    ],")

        # Forecasts
        print("    forecasts: [")
        for i, f in enumerate(forecast_data["forecasts"]):
            comma = "," if i < len(forecast_data["forecasts"]) - 1 else ""
            print(f"      {{ year: {f['year']}, predicted: {f['predicted']}, predLow: {f['predLow']}, predHigh: {f['predHigh']} }}{comma}")
        print("    ],")

        print(f"    actual2024: {actual2024},")
        print(f"    predicted2024: {forecast_data['predicted2024']}")
        print("  },")

    print("}")

if __name__ == "__main__":
    main()
