"""
05_robustness_forecasts.py — POST-REGISTRATION robustness arms.

NOT part of the pre-registered record. Reuses the EXACT protocol of
03_llm_forecasts.py (same 20 GSS items, same SYS_PT/point_prompt prompts, same
aligned 2022->2024 and long 2010->2024 designs, same anonymized-series probe,
same temperature/decoding) but adds new model arms and writes to SEPARATE files
so the pre-registered llm_forecasts.json / costs.json are never touched.

Arms (candidate clean reasoning + effort sweep + open-weights):
  o3                cutoff 2024-06 (OpenAI docs)  CLEAN   reasoning_effort=medium, seed=1930
  gpt-5-mini-medium cutoff 2024-05 (OpenAI docs)  CLEAN   reasoning_effort=medium, seed=1930
  gpt-5-mini-high   cutoff 2024-05 (OpenAI docs)  CLEAN   reasoning_effort=high,   seed=1930
  deepseek-v4-flash (deepseek-chat alias)         CONTAMINATED/UNVERIFIED  temperature=0
  claude-3-5-sonnet-20241022  requested CLEAN (~Apr 2024) but RETIRED 2025-10-28 -> UNAVAILABLE

Tasks: point (2022 aligned + 2010 long) and anon (identity-stripped, both cutoffs),
for every available arm. Distribution arm omitted (not in the robustness deliverable).

Outputs: results/robustness_forecasts.json, results/robustness_costs.json
Budget cap: $10 total (expected ~$1.5). One retry per failed call, then record missing.
"""
import json, re, subprocess, sys
from datetime import datetime
from pathlib import Path

RES = Path(__file__).resolve().parents[1] / "results"
SEED = 1930
BUDGET_CAP = 10.0

# published prices (input, output) $/1M tokens, from each vendor's own docs (URLs in meta)
PRICES = {
    "o3": (2.00, 8.00),
    "gpt-5-mini-medium": (0.25, 2.00),
    "gpt-5-mini-high": (0.25, 2.00),
    "deepseek-v4-flash": (0.14, 0.28),  # deepseek-chat = non-thinking deepseek-v4-flash
}
cost = {m: {"in": 0, "out": 0, "usd": 0.0, "calls": 0} for m in PRICES}

# cutoff verification (vendor-stated, fetched from vendor docs today 2026-07-10)
CUTOFFS = {
    "o3": {"provider": "openai", "vendor_cutoff": "2024-06-01",
           "url": "https://developers.openai.com/api/docs/models/o3",
           "stated": "Jun 01, 2024 knowledge cutoff",
           "clean_rule": "stated cutoff <= 2024-12 (end of GSS 2024 fieldwork)",
           "label": "clean"},
    "gpt-5-mini-medium": {"provider": "openai", "vendor_cutoff": "2024-05-31",
           "url": "https://developers.openai.com/api/docs/models/gpt-5-mini",
           "stated": "May 31, 2024 knowledge cutoff",
           "clean_rule": "stated cutoff <= 2024-12", "label": "clean"},
    "gpt-5-mini-high": {"provider": "openai", "vendor_cutoff": "2024-05-31",
           "url": "https://developers.openai.com/api/docs/models/gpt-5-mini",
           "stated": "May 31, 2024 knowledge cutoff",
           "clean_rule": "stated cutoff <= 2024-12", "label": "clean"},
    "deepseek-v4-flash": {"provider": "deepseek",
           "vendor_cutoff": "not documented",
           "url": "https://api-docs.deepseek.com/quick_start/pricing",
           "stated": "deepseek-chat = non-thinking mode of deepseek-v4-flash (per DeepSeek docs); "
                     "no vendor-stated training cutoff published; V4 line is a 2025+ model",
           "clean_rule": "stated cutoff <= 2024-12 (UNVERIFIABLE)",
           "label": "contaminated/unverified"},
}

def secret(n):
    return subprocess.run(["/Users/maxghenis/bin/agent-secret", "get", n],
                          capture_output=True, text=True).stdout.strip()

from openai import OpenAI
import anthropic
OAI = OpenAI(api_key=secret("OPENAI_API_KEY"))
DS = OpenAI(api_key=secret("agent/deepseek-api-key"), base_url="https://api.deepseek.com")
ANT = anthropic.Anthropic(api_key=secret("ANTHROPIC_API_KEY"))

ARMS = [
    {"name": "o3", "kind": "oai_reason", "model": "o3", "effort": "medium"},
    {"name": "gpt-5-mini-medium", "kind": "oai_reason", "model": "gpt-5-mini", "effort": "medium"},
    {"name": "gpt-5-mini-high", "kind": "oai_reason", "model": "gpt-5-mini", "effort": "high"},
    {"name": "deepseek-v4-flash", "kind": "deepseek", "model": "deepseek-chat", "effort": None},
]

def _track(name, itok, otok):
    ci, co = PRICES[name]
    cost[name]["in"] += itok; cost[name]["out"] += otok; cost[name]["calls"] += 1
    cost[name]["usd"] += itok * ci / 1e6 + otok * co / 1e6
    tot = sum(c["usd"] for c in cost.values())
    if tot > BUDGET_CAP:
        json.dump(cost, open(RES / "robustness_costs.json", "w"), indent=2)
        sys.exit(f"ABORT: budget cap ${BUDGET_CAP} exceeded (${tot:.2f})")

def do_call(arm, system, user):
    """One raw API call. Returns (text, itok, otok). Reasoning arms use
    max_completion_tokens + reasoning_effort + seed + json_object (matching the
    committed gpt-5 path); deepseek uses temperature=0 (matching the committed
    deterministic gpt-4o path)."""
    if arm["kind"] == "oai_reason":
        r = OAI.chat.completions.create(
            model=arm["model"], seed=SEED, reasoning_effort=arm["effort"],
            max_completion_tokens=4000, response_format={"type": "json_object"},
            messages=[{"role": "system", "content": system}, {"role": "user", "content": user}])
        return r.choices[0].message.content, r.usage.prompt_tokens, r.usage.completion_tokens
    if arm["kind"] == "deepseek":
        r = DS.chat.completions.create(
            model=arm["model"], temperature=0, max_tokens=400,
            response_format={"type": "json_object"},
            messages=[{"role": "system", "content": system}, {"role": "user", "content": user}])
        return r.choices[0].message.content, r.usage.prompt_tokens, r.usage.completion_tokens
    raise ValueError(arm["kind"])

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

def forecast_point(arm, system, user):
    """One retry, then record missing. Cost is tracked for every call that reaches
    the server (honest), including a call whose JSON later fails to parse."""
    last = None
    for _ in range(2):
        try:
            txt, itok, otok = do_call(arm, system, user)
            _track(arm["name"], itok, otok)
            o = parse_obj(txt)
            return {"point": float(o["point"]), "lo90": float(o["lo90"]), "hi90": float(o["hi90"])}
        except Exception as e:
            last = e
    return {"error": str(last)[:160]}

def main():
    gss = json.loads((RES / "gss_series.json").read_text())
    V = gss["variables"]
    fvars = [v for v in V if 2024 in {int(y) for y in V[v]["series"]}]

    fc = {"meta": {}, "point": {}, "anon": {}}

    # ---- record the retired / unavailable candidate clean Anthropic arm (live attempt) ----
    unavailable = {}
    try:
        ANT.messages.create(model="claude-3-5-sonnet-20241022", max_tokens=16,
                            messages=[{"role": "user", "content": "ping"}])
        unavailable["claude-3-5-sonnet-20241022"] = {"status": "available_unexpected"}
    except Exception as e:
        unavailable["claude-3-5-sonnet-20241022"] = {
            "status": "unavailable",
            "requested_label": "clean (candidate Anthropic arm; vendor-stated cutoff ~Apr 2024)",
            "error": str(e)[:200],
            "note": ("Retired 2025-10-28 per Anthropic model lifecycle; 404 not_found_error. "
                     "All Claude snapshots with a training cutoff <= Dec 2024 are now retired, "
                     "so no CLEAN Anthropic arm is runnable via the API. The pre-registered "
                     "claude-opus-4-8 remains the contaminated Anthropic ceiling.")}

    # ---- point forecasts: every available arm x both cutoffs ----
    for arm in ARMS:
        name = arm["name"]
        fc["point"][name] = {}
        for v in fvars:
            series = {int(y): val for y, val in V[v]["series"].items()}
            fc["point"][name][v] = {}
            for cutoff in (2022, 2010):
                hstr, yrs = hist_str(series, cutoff)
                if len(yrs) < 4:
                    continue
                fc["point"][name][v][str(cutoff)] = forecast_point(
                    arm, SYS_PT, point_prompt(V[v]["description"], hstr))
        json.dump({**fc, "meta": {"unavailable": unavailable, "cutoffs": CUTOFFS,
                   "in_progress": True}}, open(RES / "robustness_forecasts.json", "w"), indent=2)
        print(f"[point] {name} done. running ${sum(c['usd'] for c in cost.values()):.3f}")

    # ---- anonymized probe: every available arm x both cutoffs ----
    for arm in ARMS:
        name = arm["name"]
        fc["anon"][name] = {}
        for v in fvars:
            series = {int(y): val for y, val in V[v]["series"].items()}
            fc["anon"][name][v] = {}
            for cutoff in (2022, 2010):
                hstr, yrs = hist_str(series, cutoff)
                if len(yrs) < 4:
                    continue
                fc["anon"][name][v][str(cutoff)] = forecast_point(
                    arm, SYS_PT, point_prompt("", hstr, anon=True))
        json.dump({**fc, "meta": {"unavailable": unavailable, "cutoffs": CUTOFFS,
                   "in_progress": True}}, open(RES / "robustness_forecasts.json", "w"), indent=2)
        print(f"[anon] {name} done. running ${sum(c['usd'] for c in cost.values()):.3f}")

    fc["meta"] = {
        "generated": datetime.now().isoformat(timespec="seconds"),
        "kind": "post-registration robustness arms (NOT the pre-registered record)",
        "protocol": "identical to code/03_llm_forecasts.py (same items, prompts, cutoffs, decoding)",
        "cutoffs": CUTOFFS,
        "unavailable": unavailable,
        "n_vars": len(fvars),
        "in_progress": False,
    }
    json.dump(fc, open(RES / "robustness_forecasts.json", "w"), indent=2)
    json.dump(cost, open(RES / "robustness_costs.json", "w"), indent=2)

    tot = sum(c["usd"] for c in cost.values())
    print(f"\nWrote robustness_forecasts.json + robustness_costs.json")
    for m, c in cost.items():
        print(f"  {m:20s} {c['calls']:3d} calls  in={c['in']:6d} out={c['out']:6d}  ${c['usd']:.4f}")
    print(f"  TOTAL ${tot:.4f}")

if __name__ == "__main__":
    main()
