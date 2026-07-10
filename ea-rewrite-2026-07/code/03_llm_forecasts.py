"""
03_llm_forecasts.py — LLM forecasts of GSS 2024 attitude shares.

Arms:
  gpt-5-mini      cutoff 2024-05  CLEAN for GSS 2024 (released 2025)   [headline]
  gpt-4o          cutoff 2023-10  CLEAN                                 [robustness]
  claude-opus-4-8 cutoff 2026-01  CONTAMINATED                          [ceiling]

Tasks:
  point       point + 90% interval, cutoffs 2022 (aligned) and 2010 (long), all arms
  distribution full response distribution for HOMOSEX/PREMARSX/POLVIEWS, gpt-5-mini + claude
  anon        anonymized-series probe (identity stripped), gpt-5-mini, both cutoffs

Outputs: results/llm_forecasts.json, results/costs.json
Budget cap: $25 (expected << $2). Aborts if projected spend exceeds cap.
"""
import json, re, subprocess, sys
from pathlib import Path

RES = Path(__file__).resolve().parents[1] / "results"
SEED = 1930
BUDGET_CAP = 25.0
PRICES = {  # (input, output) $/1M tokens
    "gpt-5-mini": (0.25, 2.00), "gpt-4o": (2.50, 10.00), "claude-opus-4-8": (5.00, 25.00),
}
cost = {m: {"in": 0, "out": 0, "usd": 0.0, "calls": 0} for m in PRICES}

def secret(n):
    return subprocess.run(["/Users/maxghenis/bin/agent-secret", "get", n],
                          capture_output=True, text=True).stdout.strip()

from openai import OpenAI
import anthropic
OAI = OpenAI(api_key=secret("OPENAI_API_KEY"))
ANT = anthropic.Anthropic(api_key=secret("ANTHROPIC_API_KEY"))

def _track(model, itok, otok):
    ci, co = PRICES[model]
    cost[model]["in"] += itok; cost[model]["out"] += otok; cost[model]["calls"] += 1
    cost[model]["usd"] += itok * ci / 1e6 + otok * co / 1e6
    tot = sum(c["usd"] for c in cost.values())
    if tot > BUDGET_CAP:
        json.dump(cost, open(RES / "costs.json", "w"), indent=2)
        sys.exit(f"ABORT: budget cap ${BUDGET_CAP} exceeded (${tot:.2f})")

def call(model, system, user, max_out=2000):
    if model.startswith("gpt-5"):
        r = OAI.chat.completions.create(
            model=model, seed=SEED, reasoning_effort="minimal",
            max_completion_tokens=max_out, response_format={"type": "json_object"},
            messages=[{"role": "system", "content": system}, {"role": "user", "content": user}])
        _track(model, r.usage.prompt_tokens, r.usage.completion_tokens)
        return r.choices[0].message.content
    if model.startswith("gpt-4"):
        r = OAI.chat.completions.create(
            model=model, seed=SEED, temperature=0, max_tokens=400,
            response_format={"type": "json_object"},
            messages=[{"role": "system", "content": system}, {"role": "user", "content": user}])
        _track(model, r.usage.prompt_tokens, r.usage.completion_tokens)
        return r.choices[0].message.content
    # anthropic
    r = ANT.messages.create(model=model, max_tokens=500,
                            system=system, messages=[{"role": "user", "content": user}])
    _track(model, r.usage.input_tokens, r.usage.output_tokens)
    return "".join(b.text for b in r.content if b.type == "text")

def parse_obj(txt):
    m = re.search(r"\{.*\}", txt, re.S)
    return json.loads(m.group(0)) if m else None

SYS_PT = ("You are an expert forecaster of US public opinion. You reason only from the "
          "historical series you are given. Respond with ONLY a JSON object, no prose.")

def hist_str(series, cutoff):
    yrs = sorted(y for y in series if y <= cutoff)
    return "\n".join(f"  {y}: {series[y]:.1f}%" for y in yrs), yrs

def point_prompt(desc, hstr, anon=False):
    head = ("An anonymized US national survey attitude item measured periodically "
            "(higher % = more agreement)." if anon else
            f"General Social Survey item: percent who say {desc}.")
    return (f"{head}\nPercent by year:\n{hstr}\n\n"
            "Forecast the percentage for 2024. Give a point estimate and a 90% interval "
            "(only a 10% chance the true value falls outside it).\n"
            'Respond with ONLY: {"point": <0-100>, "lo90": <0-100>, "hi90": <0-100>}')

def main():
    gss = json.loads((RES / "gss_series.json").read_text())
    V = gss["variables"]; DIST = gss["distributions"]
    fc = {"point": {}, "distribution": {}, "anon": {}}
    fvars = [v for v in V if 2024 in {int(y) for y in V[v]["series"]}]

    # ---- point forecasts: all arms x both cutoffs ----
    for model in ["gpt-5-mini", "gpt-4o", "claude-opus-4-8"]:
        fc["point"][model] = {}
        for v in fvars:
            series = {int(y): val for y, val in V[v]["series"].items()}
            fc["point"][model][v] = {}
            for cutoff in (2022, 2010):
                hstr, yrs = hist_str(series, cutoff)
                if len(yrs) < 4:
                    continue
                try:
                    o = parse_obj(call(model, SYS_PT,
                                       point_prompt(V[v]["description"], hstr)))
                    fc["point"][model][v][str(cutoff)] = {
                        "point": float(o["point"]), "lo90": float(o["lo90"]),
                        "hi90": float(o["hi90"])}
                except Exception as e:
                    fc["point"][model][v][str(cutoff)] = {"error": str(e)[:120]}
        print(f"[point] {model} done. running ${sum(c['usd'] for c in cost.values()):.3f}")
        json.dump(fc, open(RES / "llm_forecasts.json", "w"), indent=2)

    # ---- distribution arm ----
    for model in ["gpt-5-mini", "claude-opus-4-8"]:
        fc["distribution"][model] = {}
        for v in ["HOMOSEX", "PREMARSX", "POLVIEWS"]:
            by = {int(y): d for y, d in DIST[v]["by_year"].items()}
            labels = DIST[v]["labels"]
            waves = [y for y in sorted(by) if y <= 2022][-3:]
            block = "\n".join(f"  {y}: " + ", ".join(f"{k} {by[y][k]:.0f}%" for k in labels)
                              for y in waves)
            user = (f"General Social Survey item: {V[v]['description'].split(' (')[0]}.\n"
                    f"Response categories: {', '.join(labels)}.\n"
                    f"Recent distributions (%):\n{block}\n\n"
                    "Forecast the full 2024 distribution (percentages summing to ~100).\n"
                    "Respond with ONLY a JSON object mapping each category label to its percent.")
            try:
                o = parse_obj(call(model, SYS_PT, user))
                s = sum(float(x) for x in o.values()) or 1.0
                fc["distribution"][model][v] = {k: round(float(o.get(k, 0)) * 100 / s, 2)
                                                for k in labels}
            except Exception as e:
                fc["distribution"][model][v] = {"error": str(e)[:120]}
        json.dump(fc, open(RES / "llm_forecasts.json", "w"), indent=2)
    print(f"[distribution] done. running ${sum(c['usd'] for c in cost.values()):.3f}")

    # ---- anonymized probe: gpt-5-mini, both cutoffs ----
    fc["anon"]["gpt-5-mini"] = {}
    for v in fvars:
        series = {int(y): val for y, val in V[v]["series"].items()}
        fc["anon"]["gpt-5-mini"][v] = {}
        for cutoff in (2022, 2010):
            hstr, yrs = hist_str(series, cutoff)
            if len(yrs) < 4:
                continue
            try:
                o = parse_obj(call("gpt-5-mini", SYS_PT, point_prompt("", hstr, anon=True)))
                fc["anon"]["gpt-5-mini"][v][str(cutoff)] = {
                    "point": float(o["point"]), "lo90": float(o["lo90"]), "hi90": float(o["hi90"])}
            except Exception as e:
                fc["anon"]["gpt-5-mini"][v][str(cutoff)] = {"error": str(e)[:120]}
    json.dump(fc, open(RES / "llm_forecasts.json", "w"), indent=2)

    json.dump(cost, open(RES / "costs.json", "w"), indent=2)
    tot = sum(c["usd"] for c in cost.values())
    print(f"\nWrote llm_forecasts.json + costs.json")
    for m, c in cost.items():
        print(f"  {m:16s} {c['calls']:3d} calls  in={c['in']:6d} out={c['out']:6d}  ${c['usd']:.4f}")
    print(f"  TOTAL ${tot:.4f}")

if __name__ == "__main__":
    main()
