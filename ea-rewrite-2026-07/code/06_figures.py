"""
06_figures.py — paper figures, drawn only from the committed result JSONs.

Reads results/gss_series.json, results/analysis.json, results/llm_forecasts.json,
results/robustness_analysis.json. Every plotted number therefore traces to the
committed record; headline values are re-asserted here so the figures cannot
silently drift from the tables.

Outputs to ../figures/: fig1_reversals, fig2_accuracy_calibration,
fig3_anonymization, fig4_effort — each as .pdf (paper), .png (300 dpi), .svg.
"""
import json
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np


def r1(x):
    """Round half away from zero to 1 dp (matches the tables, unlike float .1f)."""
    d = Decimal(str(x)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
    return f"{d:+}"

RES = Path(__file__).resolve().parents[1] / "results"
FIG = Path(__file__).resolve().parents[1] / "figures"
FIG.mkdir(exist_ok=True)

gss = json.loads((RES / "gss_series.json").read_text())
ana = json.loads((RES / "analysis.json").read_text())
llm = json.loads((RES / "llm_forecasts.json").read_text())
rob = json.loads((RES / "robustness_analysis.json").read_text())
etsc = json.loads((RES / "ets_corrected.json").read_text())

# ---- sanity gates: the committed record says what the paper says ----
assert ana["actual_2024"]["HOMOSEX"] == 55.94
assert ana["strata"]["HOMOSEX"]["pre"] == 62.72
assert ana["metrics"]["2022"]["naive"]["mae"] == 3.15
assert ana["metrics"]["2022"]["gpt-5-mini"]["mae"] == 4.07
assert rob["metrics"]["2022"]["o3"]["mae"] == 3.93
assert rob["metrics"]["2022"]["gpt-5-mini-high"]["n"] == 11
assert etsc["cutoffs"]["2022"]["mae"] == 4.33 and etsc["cutoffs"]["2022"]["n_covered"] == 12
assert llm["point"]["gpt-5-mini"]["HOMOSEX"]["2010"]["point"] == 78.0
assert llm["anon"]["gpt-5-mini"]["HOMOSEX"]["2010"]["point"] == 47.5

# ---- shared style (dataviz skill: validated palette, hairline chrome) ----
BLUE, RED, AQUA = "#2a78d6", "#e34948", "#1baf7a"
INK, INK2, MUTED = "#0b0b0b", "#52514e", "#898781"
GRID, AXIS = "#e1e0d9", "#c3c2b7"
mpl.rcParams.update({
    "font.family": ["Helvetica Neue", "Helvetica", "Arial", "DejaVu Sans"],
    "svg.fonttype": "none", "pdf.fonttype": 42,
    "axes.edgecolor": AXIS, "axes.linewidth": 0.6,
    "xtick.color": MUTED, "ytick.color": MUTED,
    "xtick.labelcolor": INK2, "ytick.labelcolor": INK2,
    "axes.labelcolor": INK2,
    "figure.facecolor": "white", "axes.facecolor": "white",
})


def save(fig, stem):
    for ext in ("pdf", "png", "svg"):
        fig.savefig(FIG / f"{stem}.{ext}", dpi=300, bbox_inches="tight",
                    facecolor="white")
    plt.close(fig)
    print("wrote", FIG / stem)


def despine(ax, keep=("left", "bottom")):
    for side in ("top", "right", "left", "bottom"):
        ax.spines[side].set_visible(side in keep)


# ================= fig 1 — 20 series, 8 reversals =================
strata = ana["strata"]
LARGEST_EVER = {"PRAYER", "HOMOSEX", "FEFAM", "GRASS"}  # RESULTS.md, per-series max checked in 04
order = (sorted([v for v in strata if strata[v]["class"] == "reversal"],
                key=lambda v: strata[v]["change24"])
         + sorted([v for v in strata if strata[v]["class"] == "continuation"],
                  key=lambda v: -abs(strata[v]["change24"]))
         + sorted([v for v in strata if strata[v]["class"] == "stable"],
                  key=lambda v: -abs(strata[v]["change24"])))
assert len(order) == 20

fig, axes = plt.subplots(4, 5, figsize=(9.2, 5.9))
for ax, var in zip(axes.flat, order):
    s = gss["variables"][var]["series"]
    yrs = np.array(sorted(int(y) for y in s))
    vals = np.array([s[str(y)] for y in yrs])
    rev = strata[var]["class"] == "reversal"
    c_end = RED if rev else BLUE
    pre = yrs <= 2022
    ax.plot(yrs[pre], vals[pre], color=BLUE, lw=1.1, solid_joinstyle="round")
    ax.plot(yrs[yrs >= 2022], vals[yrs >= 2022], color=c_end, lw=1.4)
    ax.plot([2024], [s["2024"]], "o", ms=3.6, color=c_end,
            markeredgecolor="white", markeredgewidth=0.7, zorder=5)
    star = "*" if var in LARGEST_EVER else ""
    ax.text(0.03, 1.04, f"{var}{star}", transform=ax.transAxes, fontsize=7,
            fontweight="bold", color=INK, va="bottom")
    ax.text(0.97, 1.04, r1(strata[var]["change24"]), transform=ax.transAxes,
            fontsize=6.5, color=INK2 if not rev else INK, ha="right", va="bottom")
    ax.set_xlim(1971, 2027)
    lo, hi = vals.min(), vals.max()
    pad = max(3, 0.12 * (hi - lo))
    ax.set_ylim(lo - pad, hi + pad)
    ax.set_yticks([round(lo), round(hi)])
    ax.set_xticks([1980, 2010])
    ax.tick_params(length=2, width=0.5, labelsize=6)
    if ax not in axes[-1]:
        ax.set_xticklabels([])
    despine(ax)
fig.subplots_adjust(hspace=0.55, wspace=0.32)
save(fig, "fig1_reversals")

# ============ fig 2 — MAE vs 90% coverage, aligned horizon ============
m22, r22 = ana["metrics"]["2022"], rob["metrics"]["2022"]
pts = [  # (label, mae, cov, n, family)
    ("naive", m22["naive"]["mae"], m22["naive"]["cov90"], 20, "base"),
    ("ETS (corrected)", etsc["cutoffs"]["2022"]["mae"], etsc["cutoffs"]["2022"]["cov90"], 20, "base"),
    ("linear", m22["linear"]["mae"], m22["linear"]["cov90"], 20, "base"),
    ("ARIMA(1,1,0)", m22["arima"]["mae"], m22["arima"]["cov90"], 20, "base"),
    ("gpt-5-mini (minimal)", m22["gpt-5-mini"]["mae"], m22["gpt-5-mini"]["cov90"], 20, "clean"),
    ("gpt-4o", m22["gpt-4o"]["mae"], m22["gpt-4o"]["cov90"], 20, "clean"),
    ("o3", r22["o3"]["mae"], r22["o3"]["cov90"], 20, "clean"),
    ("gpt-5-mini (medium)", r22["gpt-5-mini-medium"]["mae"], r22["gpt-5-mini-medium"]["cov90"], 20, "clean"),
    ("gpt-5-mini (high)†", r22["gpt-5-mini-high"]["mae"], r22["gpt-5-mini-high"]["cov90"], 10, "clean"),
    ("claude-opus-4-8", m22["claude-opus-4-8"]["mae"], m22["claude-opus-4-8"]["cov90"], 20, "contam"),
]
ORANGE = "#eb6834"
fig, ax = plt.subplots(figsize=(5.6, 3.9))
ax.axhline(0.90, color=AXIS, lw=0.9, zorder=1)
ax.text(4.62, 0.907, "nominal 90%", fontsize=7, color=MUTED, ha="right", va="bottom")
for label, mae, cov, n, fam in pts:
    if fam == "contam":  # open diamond, so the coincident ARIMA point stays visible
        ax.scatter([mae], [cov], s=150, marker="D", facecolors="none",
                   edgecolors=ORANGE, linewidths=1.6, zorder=3)
    else:
        ax.scatter([mae], [cov], s=58, marker="o",
                   color=INK2 if fam == "base" else BLUE,
                   edgecolors="white", linewidths=1.2, zorder=4)
offsets = {  # nudge labels off their markers; leader-free, collision-checked by eye
    "naive": (-0.04, 0.022, "right"), "linear": (0.05, 0.022, "left"),
    "ETS (corrected)": (0.045, -0.026, "left"),
    "ARIMA(1,1,0)": (-0.09, 0.0, "right"), "claude-opus-4-8": (0.0, -0.042, "center"),
    "gpt-5-mini (minimal)": (0.05, -0.005, "left"), "gpt-4o": (-0.05, -0.008, "right"),
    "o3": (-0.05, 0.005, "right"), "gpt-5-mini (medium)": (0.05, 0.008, "left"),
    "gpt-5-mini (high)†": (-0.03, 0.034, "center"),
}
for label, mae, cov, n, fam in pts:
    dx, dy, ha = offsets[label]
    ax.text(mae + dx, cov + dy, label, fontsize=7, color=INK, ha=ha, va="center")
ax.set_xlabel("mean absolute error, percentage points (lower = more accurate)", fontsize=8)
ax.set_ylabel("empirical 90% interval coverage", fontsize=8)
ax.set_xlim(2.85, 4.75)
ax.set_ylim(0.42, 1.0)
ax.set_yticks([0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
ax.set_yticklabels(["50%", "60%", "70%", "80%", "90%", "100%"], fontsize=7)
ax.set_xticks([3.0, 3.5, 4.0, 4.5])
ax.set_xticklabels(["3.0", "3.5", "4.0", "4.5"], fontsize=7)
ax.tick_params(axis="x", length=3, width=0.5)
ax.tick_params(axis="y", length=3, width=0.5)
from matplotlib.lines import Line2D
fam_handles = [
    Line2D([], [], marker="o", ls="", color=INK2, markeredgecolor="white",
           ms=7, label="classical baseline"),
    Line2D([], [], marker="o", ls="", color=BLUE, markeredgecolor="white",
           ms=7, label="clean LLM"),
    Line2D([], [], marker="D", ls="", markerfacecolor="none",
           markeredgecolor=ORANGE, markeredgewidth=1.5, ms=8,
           label="contaminated LLM"),
]
ax.legend(handles=fam_handles, loc="lower left", fontsize=7, frameon=False,
          handletextpad=0.4, borderaxespad=0.2)
despine(ax)
save(fig, "fig2_accuracy_calibration")

# ========= fig 3 — identified vs anonymized, 2010 cutoff =========
ident = {v: llm["point"]["gpt-5-mini"][v]["2010"]["point"] for v in ana["actual_2024"]}
anon = {v: llm["anon"]["gpt-5-mini"][v]["2010"]["point"] for v in ana["actual_2024"]}
swing = {v: ident[v] - anon[v] for v in ident}
rows = sorted(swing, key=lambda v: -abs(swing[v]))
assert round(swing["HOMOSEX"], 1) == 30.5 and round(swing["GRASS"], 1) == 17.0

fig, ax = plt.subplots(figsize=(5.6, 5.4))
ys = np.arange(len(rows))[::-1]
for y, v in zip(ys, rows):
    a, i, act = anon[v], ident[v], ana["actual_2024"][v]
    ax.plot([min(a, i), max(a, i)], [y, y], color=GRID, lw=1.6, zorder=1)
    ax.plot([act, act], [y - 0.32, y + 0.32], color=INK, lw=1.0, zorder=2)
    # anonymized = open ring, identified = filled dot: both stay visible when
    # the two coincide (which is itself the aligned-horizon finding)
    ax.plot([a], [y], "o", ms=8.2, markerfacecolor="white", markeredgecolor=AQUA,
            markeredgewidth=1.5, zorder=3)
    ax.plot([i], [y], "o", ms=4.6, color=BLUE, zorder=4)
    if abs(swing[v]) >= 5:
        ax.text(max(a, i) + 2.2, y, f"{swing[v]:+.1f}", fontsize=6.5, color=INK,
                va="center")
ax.set_yticks(ys)
ax.set_yticklabels(rows, fontsize=7, color=INK)
ax.set_xlabel("gpt-5-mini forecast of the 2024 share, shown history ≤ 2010 "
              "(percentage points)", fontsize=8)
ax.tick_params(axis="x", labelsize=7, length=3, width=0.5)
ax.tick_params(axis="y", length=0)
ax.set_xlim(0, 100)
from matplotlib.lines import Line2D
handles = [
    Line2D([], [], marker="o", ls="", color=BLUE, ms=5, label="item identified"),
    Line2D([], [], marker="o", ls="", markerfacecolor="white",
           markeredgecolor=AQUA, markeredgewidth=1.5, ms=8, label="item anonymized"),
    Line2D([], [], marker="|", ls="", color=INK, ms=9, markeredgewidth=1.2,
           label="2024 actual"),
]
ax.legend(handles=handles, loc="upper left", fontsize=7, frameon=False,
          borderaxespad=0.4)
despine(ax, keep=("bottom",))
save(fig, "fig3_anonymization")

# ================= fig 4 — reasoning-effort sweep =================
sweep = [("minimal\nn = 20", m22["gpt-5-mini"]["mae"], 20),
         ("medium\nn = 20", r22["gpt-5-mini-medium"]["mae"], 20),
         ("high\nn = 11 of 20", r22["gpt-5-mini-high"]["mae"], 11)]
assert [s[1] for s in sweep] == [4.07, 4.16, 4.21]
fig, ax = plt.subplots(figsize=(3.4, 2.9))
xs = np.arange(3)
bars = ax.bar(xs, [s[1] for s in sweep], width=0.38, color=BLUE, zorder=3)
for b in bars:
    b.set_linewidth(0)
for x, (lab, mae, n) in zip(xs, sweep):
    ax.text(x, mae + 0.08, f"{mae:.2f}", ha="center", fontsize=7.5, color=INK)
ax.axhline(m22["naive"]["mae"], color=INK2, lw=0.9, zorder=4)
ax.set_xlim(-0.55, 2.85)
ax.text(2.8, m22["naive"]["mae"] + 0.07, "naive 3.15", fontsize=7, color=INK2,
        ha="right")
ax.set_xticks(xs)
ax.set_xticklabels([s[0] for s in sweep], fontsize=7.5, color=INK)
ax.set_ylabel("MAE, percentage points", fontsize=8)
ax.set_ylim(0, 4.85)
ax.set_yticks([0, 1, 2, 3, 4])
ax.tick_params(length=3, width=0.5, labelsize=7)
ax.set_xlabel("gpt-5-mini reasoning effort", fontsize=8)
despine(ax)
save(fig, "fig4_effort")

print("all figures written to", FIG)
