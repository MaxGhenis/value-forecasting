"""
Run value forecasting experiments with LLMs.
Uses trajectories extracted from GSS microdata.
"""

import json
import re
from pathlib import Path
from openai import OpenAI

# Model cutoffs for clean temporal tests
MODEL_CUTOFFS = {
    "gpt-3.5-turbo-instruct": "2021-09",  # September 2021
    "gpt-4o": "2023-10",  # October 2023
    "gpt-4-turbo": "2023-12",  # December 2023
}


def load_trajectories(path: str = "data/trajectories.json") -> dict:
    """Load trajectories from JSON file."""
    with open(path) as f:
        data = json.load(f)
    return data["variables"]


def get_historical_context(var_data: dict, cutoff_year: int) -> tuple[str, dict]:
    """Build historical context string up to cutoff year."""
    traj = var_data["trajectory"]

    # Convert all keys to int, filter to years <= cutoff
    pre_cutoff = {int(y): round(v) for y, v in traj.items() if int(y) <= cutoff_year}

    if len(pre_cutoff) < 2:
        return None, None

    history = "\n".join([f"  {y}: {v}%" for y, v in sorted(pre_cutoff.items())])
    return history, pre_cutoff


def forecast_instruct(client, var: str, desc: str, history: str,
                      cutoff_year: int, target_year: int) -> int | None:
    """Get forecast from gpt-3.5-turbo-instruct."""
    prompt = f"""Historical GSS data for "{desc}":
{history}

Predicted percentage for {target_year}:"""

    try:
        response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=20,
            temperature=0
        )
        text = response.choices[0].text.strip()
        # Extract first number
        match = re.search(r'(\d+)', text)
        if match:
            val = int(match.group(1))
            if 0 <= val <= 100:
                return val
    except Exception as e:
        print(f"  Error for {var}: {e}")
    return None


def forecast_chat(client, var: str, desc: str, history: str,
                  cutoff_year: int, target_year: int, model: str = "gpt-4o") -> int | None:
    """Get forecast from chat model."""
    system = f"You are a social scientist in {cutoff_year}. You predict survey trends based on historical data."
    user = f"""Based on historical General Social Survey data, predict the percentage of Americans who will say "{desc}" in {target_year}.

Historical data (% giving this response):
{history}

Predict only a single number between 0 and 100."""

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user}
            ],
            max_tokens=10,
            temperature=0
        )
        text = response.choices[0].message.content.strip()
        match = re.search(r'\d+', text)
        if match:
            return int(match.group())
    except Exception as e:
        print(f"  Error for {var}: {e}")
    return None


def run_experiment(trajectories: dict, model: str, cutoff_year: int,
                   target_year: int, client: OpenAI) -> list[dict]:
    """Run forecasting experiment across all variables."""
    results = []

    for var, data in trajectories.items():
        history, pre_cutoff = get_historical_context(data, cutoff_year)
        if history is None:
            continue

        # Check if we have actual target year data
        traj = {int(y): v for y, v in data["trajectory"].items()}
        if target_year not in traj:
            continue
        actual = round(traj[target_year])

        # Get baseline (last known value)
        baseline_year = max(y for y in pre_cutoff.keys())
        baseline = pre_cutoff[baseline_year]

        # Get prediction
        if model == "gpt-3.5-turbo-instruct":
            predicted = forecast_instruct(
                client, var, data["description"], history, cutoff_year, target_year
            )
        else:
            predicted = forecast_chat(
                client, var, data["description"], history, cutoff_year, target_year, model
            )

        if predicted is not None:
            results.append({
                "variable": var,
                "description": data["description"],
                "cutoff_year": cutoff_year,
                "target_year": target_year,
                "baseline_year": baseline_year,
                "baseline": baseline,
                "actual": actual,
                "predicted": predicted,
                "error": predicted - actual,
                "abs_error": abs(predicted - actual),
                "actual_change": actual - baseline,
                "naive_error": abs(baseline - actual),
            })

    return results


def print_results(results: list[dict], model: str):
    """Print formatted results."""
    print(f"\n{'=' * 75}")
    print(f"Model: {model}")
    print(f"Cutoff: {results[0]['cutoff_year']} → Target: {results[0]['target_year']}")
    print(f"{'=' * 75}")

    # Sort by absolute error
    for r in sorted(results, key=lambda x: x["abs_error"]):
        direction = "✓" if (r["predicted"] > r["baseline"]) == (r["actual"] > r["baseline"]) else "✗"
        print(f"{r['variable']:12} {r['baseline']:2}%→{r['actual']:2}%  "
              f"Pred:{r['predicted']:2}%  Err:{r['error']:+3}  {direction}")

    # Summary stats
    mae = sum(r["abs_error"] for r in results) / len(results)
    naive_mae = sum(r["naive_error"] for r in results) / len(results)
    bias = sum(r["error"] for r in results) / len(results)
    direction_correct = sum(
        1 for r in results
        if (r["predicted"] > r["baseline"]) == (r["actual"] > r["baseline"])
        or r["actual_change"] == 0
    )

    print(f"\n{'─' * 40}")
    print(f"MAE:           {mae:.1f} pts")
    print(f"Naive MAE:     {naive_mae:.1f} pts")
    print(f"Improvement:   {naive_mae/mae:.2f}x")
    print(f"Bias:          {bias:+.1f} pts")
    print(f"Direction:     {direction_correct}/{len(results)} correct")

    return {"mae": mae, "naive_mae": naive_mae, "bias": bias,
            "direction_correct": direction_correct, "n": len(results)}


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="gpt-3.5-turbo-instruct")
    parser.add_argument("--cutoff", type=int, default=2010)
    parser.add_argument("--target", type=int, default=2024)
    parser.add_argument("--data", default="data/trajectories.json")
    args = parser.parse_args()

    client = OpenAI()
    trajectories = load_trajectories(args.data)

    print(f"Loaded {len(trajectories)} variables")
    print(f"Running: {args.model} predicting {args.target} from {args.cutoff} baseline")

    results = run_experiment(trajectories, args.model, args.cutoff, args.target, client)

    if results:
        stats = print_results(results, args.model)

        # Save results
        output = {
            "model": args.model,
            "cutoff_year": args.cutoff,
            "target_year": args.target,
            "results": results,
            "summary": stats,
        }

        output_path = f"data/experiment_{args.model}_{args.cutoff}_{args.target}.json"
        with open(output_path, "w") as f:
            json.dump(output, f, indent=2)
        print(f"\nSaved to {output_path}")
    else:
        print("No results generated")
