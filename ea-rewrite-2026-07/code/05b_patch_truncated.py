"""
05b_patch_truncated.py — re-run robustness forecasts that failed ONLY because the
reasoning model exhausted max_completion_tokens on reasoning (empty content ->
JSON parse failure). Mechanical harness fix, run once after 05_robustness_forecasts.py;
each patched cell is re-called with a 24k completion cap and flagged in meta.
Cells that still fail after one retry stay missing. Appends cost to robustness_costs.json.
"""
import json, re, subprocess, sys
from pathlib import Path

RES = Path(__file__).resolve().parents[1] / "results"
SEED = 1930
PRICES = {"o3": (2.00, 8.00), "gpt-5-mini-medium": (0.25, 2.00),
          "gpt-5-mini-high": (0.25, 2.00), "deepseek-v4-flash": (0.14, 0.28)}
EFFORT = {"o3": ("o3", "medium"), "gpt-5-mini-medium": ("gpt-5-mini", "medium"),
          "gpt-5-mini-high": ("gpt-5-mini", "high")}

def secret(n):
    return subprocess.run(["/Users/maxghenis/bin/agent-secret", "get", n],
                          capture_output=True, text=True).stdout.strip()
from openai import OpenAI
OAI = OpenAI(api_key=secret("OPENAI_API_KEY"))
DS = OpenAI(api_key=secret("agent/deepseek-api-key"), base_url="https://api.deepseek.com")

fc = json.loads((RES / "robustness_forecasts.json").read_text())
cost = json.loads((RES / "robustness_costs.json").read_text())
gss = json.loads((RES / "gss_series.json").read_text())
V = gss["variables"]

SYS_PT = ("You are an expert forecaster of US public opinion. You reason only from the "
          "historical series you are given. Respond with ONLY a JSON object, no prose.")

def hist_str(series, cutoff):
    yrs = sorted(y for y in series if y <= cutoff)
    return "\n".join(f"  {y}: {series[y]:.1f}%" for y in yrs)

def point_prompt(desc, hstr, anon=False):
    head = ("An anonymized US national survey attitude item measured periodically "
            "(higher % = more agreement)." if anon else
            f"General Social Survey item: percent who say {desc}.")
    return (f"{head}\nPercent by year:\n{hstr}\n\n"
            "Forecast the percentage for 2024. Give a point estimate and a 90% interval "
            "(only a 10% chance the true value falls outside it).\n"
            'Respond with ONLY: {"point": <0-100>, "lo90": <0-100>, "hi90": <0-100>}')

def parse_obj(txt):
    m = re.search(r"\{.*\}", txt or "", re.S)
    return json.loads(m.group(0)) if m else None

def call_big(arm_name, user):
    if arm_name in EFFORT:
        model, eff = EFFORT[arm_name]
        r = OAI.chat.completions.create(
            model=model, seed=SEED, reasoning_effort=eff,
            max_completion_tokens=24000, response_format={"type": "json_object"},
            messages=[{"role": "system", "content": SYS_PT}, {"role": "user", "content": user}])
        return r.choices[0].message.content, r.usage.prompt_tokens, r.usage.completion_tokens
    r = DS.chat.completions.create(
        model="deepseek-chat", temperature=0, max_tokens=2000,
        response_format={"type": "json_object"},
        messages=[{"role": "system", "content": SYS_PT}, {"role": "user", "content": user}])
    return r.choices[0].message.content, r.usage.prompt_tokens, r.usage.completion_tokens

patched, still_failed = [], []
for task in ("point", "anon"):
    for arm_name, vars_ in fc.get(task, {}).items():
        for v, cuts in vars_.items():
            for cut, m in list(cuts.items()):
                if "error" not in m:
                    continue
                series = {int(y): val for y, val in V[v]["series"].items()}
                hstr = hist_str(series, int(cut))
                user = point_prompt(V[v]["description"] if task == "point" else "",
                                    hstr, anon=(task == "anon"))
                ok = False
                last = m["error"]
                for _ in range(2):
                    try:
                        txt, itok, otok = call_big(arm_name, user)
                        ci, co = PRICES[arm_name]
                        cost[arm_name]["in"] += itok; cost[arm_name]["out"] += otok
                        cost[arm_name]["calls"] += 1
                        cost[arm_name]["usd"] += itok * ci / 1e6 + otok * co / 1e6
                        o = parse_obj(txt)
                        cuts[cut] = {"point": float(o["point"]), "lo90": float(o["lo90"]),
                                     "hi90": float(o["hi90"]), "patched_bigcap": True}
                        ok = True
                        break
                    except Exception as e:
                        last = str(e)[:160]
                if ok:
                    patched.append(f"{task}/{arm_name}/{v}/{cut}")
                else:
                    cuts[cut] = {"error": last}
                    still_failed.append(f"{task}/{arm_name}/{v}/{cut}")
                print(("PATCHED " if ok else "STILL-FAILED ") + f"{task}/{arm_name}/{v}/{cut}")

fc.setdefault("meta", {})["truncation_patch"] = {
    "reason": ("initial run capped reasoning models at max_completion_tokens=4000; on a few "
               "items the model spent the whole cap on reasoning tokens leaving empty content. "
               "Those cells re-called once with a 24000 cap (same prompt/seed/effort)."),
    "patched": patched, "still_failed": still_failed}
json.dump(fc, open(RES / "robustness_forecasts.json", "w"), indent=2)
json.dump(cost, open(RES / "robustness_costs.json", "w"), indent=2)
tot = sum(c["usd"] for c in cost.values() if isinstance(c, dict) and "usd" in c)
print(f"\npatched={len(patched)} still_failed={len(still_failed)} running total ${tot:.4f}")
