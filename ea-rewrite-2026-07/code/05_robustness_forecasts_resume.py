"""
05_robustness_forecasts_resume.py — resume 05_robustness_forecasts.py after the
first process was killed mid-run (~68 min in, during the gpt-5-mini-high point arm).

Identical protocol (same prompts, seed, decoding, arms). Differences from the
first script are purely operational:
  * skips cells already present in results/robustness_forecasts.json
  * dumps forecasts AND costs after every variable block (kill-resilient)
  * measured costs accumulate into results/robustness_costs.json under each arm;
    the killed process's untracked spend (o3 point arm + gpt-5-mini-medium point
    arm, forecasts saved but usage lost with the process) is reconstructed by
    07.. see `lost_segment_estimate` written by this script from measured
    same-arm/same-shape calls, and clearly labeled as an estimate.
"""
import json, re, subprocess, sys
from datetime import datetime
from pathlib import Path

RES = Path(__file__).resolve().parents[1] / "results"
SEED = 1930
BUDGET_CAP = 10.0
PRICES = {
    "o3": (2.00, 8.00),
    "gpt-5-mini-medium": (0.25, 2.00),
    "gpt-5-mini-high": (0.25, 2.00),
    "deepseek-v4-flash": (0.14, 0.28),
}

def secret(n):
    return subprocess.run(["/Users/maxghenis/bin/agent-secret", "get", n],
                          capture_output=True, text=True).stdout.strip()

from openai import OpenAI
OAI = OpenAI(api_key=secret("OPENAI_API_KEY"))
DS = OpenAI(api_key=secret("agent/deepseek-api-key"), base_url="https://api.deepseek.com")

ARMS = [
    {"name": "o3", "kind": "oai_reason", "model": "o3", "effort": "medium"},
    {"name": "gpt-5-mini-medium", "kind": "oai_reason", "model": "gpt-5-mini", "effort": "medium"},
    {"name": "gpt-5-mini-high", "kind": "oai_reason", "model": "gpt-5-mini", "effort": "high"},
    {"name": "deepseek-v4-flash", "kind": "deepseek", "model": "deepseek-chat", "effort": None},
]

fc = json.loads((RES / "robustness_forecasts.json").read_text())
fc.setdefault("point", {}); fc.setdefault("anon", {})
cost_path = RES / "robustness_costs.json"
cost = (json.loads(cost_path.read_text()) if cost_path.exists()
        else {m: {"in": 0, "out": 0, "usd": 0.0, "calls": 0} for m in PRICES})
for m in PRICES:
    cost.setdefault(m, {"in": 0, "out": 0, "usd": 0.0, "calls": 0})

# per-(arm, task) measured usage in THIS process, for the lost-segment estimate
meas = {}

def _track(name, task, itok, otok):
    ci, co = PRICES[name]
    cost[name]["in"] += itok; cost[name]["out"] += otok; cost[name]["calls"] += 1
    cost[name]["usd"] += itok * ci / 1e6 + otok * co / 1e6
    k = (name, task)
    meas.setdefault(k, {"in": 0, "out": 0, "calls": 0})
    meas[k]["in"] += itok; meas[k]["out"] += otok; meas[k]["calls"] += 1
    tot = sum(c["usd"] for c in cost.values())
    if tot > BUDGET_CAP:
        json.dump(cost, open(cost_path, "w"), indent=2)
        sys.exit(f"ABORT: budget cap ${BUDGET_CAP} exceeded (${tot:.2f})")

def do_call(arm, system, user):
    if arm["kind"] == "oai_reason":
        # Completion-token CEILING, not a sampling change — high-effort reasoning was
        # exhausting smaller caps (empty content + billed retries). Measured: gpt-5-mini
        # at high effort converges around ~16.6k reasoning tokens/item on this task, so
        # its cap is 24k; o3-medium and gpt-5-mini-medium fit comfortably in 12k.
        cap = 24000 if arm["name"] == "gpt-5-mini-high" else 12000
        r = OAI.chat.completions.create(
            model=arm["model"], seed=SEED, reasoning_effort=arm["effort"],
            max_completion_tokens=cap, response_format={"type": "json_object"},
            messages=[{"role": "system", "content": system}, {"role": "user", "content": user}])
        return r.choices[0].message.content, r.usage.prompt_tokens, r.usage.completion_tokens
    r = DS.chat.completions.create(
        model=arm["model"], temperature=0, max_tokens=400,
        response_format={"type": "json_object"},
        messages=[{"role": "system", "content": system}, {"role": "user", "content": user}])
    return r.choices[0].message.content, r.usage.prompt_tokens, r.usage.completion_tokens

def parse_obj(txt):
    m = re.search(r"\{.*\}", txt or "", re.S)
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

def forecast_point(arm, task, user):
    last = None
    for _ in range(2):
        try:
            txt, itok, otok = do_call(arm, SYS_PT, user)
            _track(arm["name"], task, itok, otok)
            o = parse_obj(txt)
            return {"point": float(o["point"]), "lo90": float(o["lo90"]), "hi90": float(o["hi90"])}
        except Exception as e:
            last = e
    return {"error": str(last)[:160]}

def dump():
    json.dump(fc, open(RES / "robustness_forecasts.json", "w"), indent=2)
    json.dump(cost, open(cost_path, "w"), indent=2)

def main():
    gss = json.loads((RES / "gss_series.json").read_text())
    V = gss["variables"]
    fvars = [v for v in V if 2024 in {int(y) for y in V[v]["series"]}]

    for task in ("point", "anon"):
        for arm in ARMS:
            name = arm["name"]
            # gpt-5-mini-high is rescoped to the PRIMARY aligned horizon only, point
            # task only (~16.6k reasoning tokens and ~160s PER ITEM make the full
            # 2x2 design impractical; omission recorded in meta). Same contingency
            # rule the brief specifies for o3-if-expensive.
            if name == "gpt-5-mini-high" and task == "anon":
                continue
            cutoffs = (2022,) if name == "gpt-5-mini-high" else (2022, 2010)
            slot = fc[task].setdefault(name, {})
            todo = 0
            for v in fvars:
                series = {int(y): val for y, val in V[v]["series"].items()}
                vslot = slot.setdefault(v, {})
                wrote = False
                for cutoff in cutoffs:
                    if str(cutoff) in vslot:      # already done (incl. recorded errors)
                        continue
                    hstr, yrs = hist_str(series, cutoff)
                    if len(yrs) < 4:
                        continue
                    user = point_prompt(V[v]["description"] if task == "point" else "",
                                        hstr, anon=(task == "anon"))
                    vslot[str(cutoff)] = forecast_point(arm, task, user)
                    todo += 1; wrote = True
                if wrote:
                    dump()
            print(f"[{task}] {name}: +{todo} new cells. running "
                  f"${sum(c['usd'] for c in cost.values()):.3f}", flush=True)
            dump()

    # lost-segment estimate: the killed process's o3-point + gpt-5-mini-medium-point
    # usage (80 successful calls' forecasts saved without usage records). Estimated
    # from THIS process's measured same-arm anon calls (identical series lengths;
    # identified head is ~15 tokens longer than the anon head).
    est = {}
    for name in ("o3", "gpt-5-mini-medium"):
        k = (name, "anon")
        if k in meas and meas[k]["calls"]:
            n = meas[k]["calls"]
            mean_in = meas[k]["in"] / n + 15   # identified head is slightly longer
            mean_out = meas[k]["out"] / n
            calls_lost = 40 + (3 if name == "o3" else 2)  # incl. failed calls that also billed
            ci, co = PRICES[name]
            est[name] = {
                "method": ("mean in/out tokens of this process's anon calls for the same arm "
                           "(same series, same shape; +15 input tokens for the identified head), "
                           "x lost call count incl. per-error retries"),
                "calls_lost": calls_lost,
                "est_in": round(mean_in * calls_lost),
                "est_out": round(mean_out * calls_lost),
                "est_usd": round((mean_in * ci + mean_out * co) * calls_lost / 1e6, 4),
                "estimated": True,
            }
    cost["lost_segment_estimate"] = {
        "note": ("first process was SIGKILLed ~68min in; forecasts for the o3 and "
                 "gpt-5-mini-medium point arms were saved but their usage records were "
                 "in-memory only. Measured fields above EXCLUDE that spend; this block "
                 "estimates it."),
        "arms": est,
        "est_total_usd": round(sum(a["est_usd"] for a in est.values()), 4),
    }

    fc["meta"] = {
        "generated": datetime.now().isoformat(timespec="seconds"),
        "kind": "post-registration robustness arms (NOT the pre-registered record)",
        "protocol": "identical to code/03_llm_forecasts.py (same items, prompts, cutoffs, decoding)",
        "cutoffs": fc.get("meta", {}).get("cutoffs", {}),
        "unavailable": fc.get("meta", {}).get("unavailable", {}),
        "n_vars": len(fvars),
        "resume_note": ("first process killed mid-run (host task limit); resumed by this "
                        "script skipping completed cells. See robustness_costs.json "
                        "lost_segment_estimate for the untracked spend. Resume raises "
                        "max_completion_tokens 4000->12000 (24000 for gpt-5-mini-high) for "
                        "reasoning arms (output CEILING only — prevents empty-content "
                        "truncation; sampling/decoding unchanged)."),
        "gpt5mini_high_scope": ("ALIGNED 2022 HORIZON, POINT TASK ONLY. Measured on this "
                                "task, gpt-5-mini at reasoning_effort=high uses ~16.6k "
                                "reasoning tokens and ~160s per item (vs ~30 output tokens "
                                "per item for the pre-registered minimal-effort arm), so the "
                                "full 2-horizon + anonymized design was impractical; long "
                                "horizon and anon probe omitted for this arm and the omission "
                                "reported. Same contingency principle the design allows for "
                                "o3 cost."),
        "in_progress": False,
    }
    dump()
    tot = sum(c["usd"] for c in cost.values() if isinstance(c, dict) and "usd" in c)
    print("\nRESUME COMPLETE", flush=True)
    for m in PRICES:
        c = cost[m]
        print(f"  {m:20s} {c['calls']:3d} calls  in={c['in']:6d} out={c['out']:6d}  ${c['usd']:.4f}",
              flush=True)
    print(f"  measured total ${tot:.4f}  (+ est lost segment "
          f"${cost['lost_segment_estimate']['est_total_usd']:.4f})", flush=True)

if __name__ == "__main__":
    main()
