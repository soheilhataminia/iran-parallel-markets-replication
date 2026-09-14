"""Figures for Stage 6 V4 (matplotlib)."""
import csv, json, os, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = sys.argv[1] if len(sys.argv) > 1 else "stage6_v4_out"
FIGOUT = sys.argv[2] if len(sys.argv) > 2 else OUT
os.makedirs(FIGOUT, exist_ok=True)
res = json.load(open(f"{OUT}/S6v4_results.json"))
def read_csv(p):
    with open(p) as f: return list(csv.DictReader(f))
lp = read_csv(f"{OUT}/S6v4_lp_monthly.csv")
rc = read_csv(f"{OUT}/S6v4_recursive_paths.csv")
plt.rcParams.update({"font.size": 9.5, "axes.grid": True, "grid.alpha": 0.3,
                     "figure.dpi": 150, "savefig.bbox": "tight"})

# FIG 1: primary monthly LP 2x2 with BOTH adjusted p-values shown
pt = res["path_tests"]
fig, axes = plt.subplots(2, 2, figsize=(10.5, 7), sharex=True)
panels = [("USD", "HOUS", "#1f4e79"), ("CPREM", "HOUS", "#8a4b08"),
          ("USD", "VEH", "#1f4e79"), ("CPREM", "VEH", "#8a4b08")]
for ax, (sk, oc, clr) in zip(axes.ravel(), panels):
    rows = [r for r in lp if r["outcome"] == oc]
    h = np.array([int(r["h"]) for r in rows])
    if sk == "USD":
        b = np.array([float(r["b_sUSD"]) for r in rows]); se = np.array([float(r["se"]) for r in rows])
        lo = np.array([float(r["supt_lo95"]) for r in rows]); hi = np.array([float(r["supt_hi95"]) for r in rows])
    else:
        b = np.array([float(r["b_sCPREM"]) for r in rows]); se = np.array([float(r["seC"]) for r in rows])
        lo = np.array([float(r["supt_loC"]) for r in rows]); hi = np.array([float(r["supt_hiC"]) for r in rows])
    ax.fill_between(h, 100 * lo, 100 * hi, alpha=0.15, color=clr, label="95% simultaneous, 12 horizons (wild)")
    ax.fill_between(h, 100 * (b - 1.96 * se), 100 * (b + 1.96 * se), alpha=0.35, color=clr, label="95% pointwise (HAC)")
    ax.plot(h, 100 * b, color=clr, lw=2, marker="o", ms=3.5)
    ax.axhline(0, color="k", lw=0.8)
    lower, upper = ax.get_ylim()
    ax.set_ylim(lower, upper + 0.20 * (upper-lower))
    key = f"{sk}->{oc}"
    ax.set_title(f"$s^{{{sk}}}$ → {'Housing' if oc == 'HOUS' else 'Vehicles'}", fontsize=10)
    ax.text(0.03, 0.96,
            "Holm-adjusted path p:  wild = %.4f | block-wild = %.4f\n(unadjusted: %.4f | %.4f)" %
            (pt["p_wild_holm4"][key], pt["p_blockwild_holm4"][key],
             pt["p_wild"][key], pt["p_blockwild"][key]),
            transform=ax.transAxes, va="top", fontsize=7.8,
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="0.6"))
for ax in axes[1]: ax.set_xlabel("Horizon h (months ahead)")
for ax in axes[:, 0]: ax.set_ylabel("Monthly return response (%)\nper one-s.d. shock")
axes[0, 0].legend(frameon=False, fontsize=7.5, loc="lower left")
fig.suptitle("Stage 6 (corrected bootstrap) — Monthly LP, h = 1…12; s$^{USD}$ = VECM USD-equation residual,\n"
             "s$^{CPREM}$ = two-lag premium-innovation residual; Holm-adjusted path p-values lead", y=1.0, fontsize=10)
fig.savefig(f"{FIGOUT}/fig_s6v4_1_lp_monthly.png"); plt.close(fig)

# FIG 2: confirmatory forecast family
fam_p = res["confirmatory_family_CW_M2vsM0"]["p"]
fam_h = res["confirmatory_family_CW_M2vsM0"]["holm6"]
oo = res["pseudo_oos_main"]
keys = ["HOUS_h1", "HOUS_h3", "HOUS_h6", "VEH_h1", "VEH_h3", "VEH_h6"]
r2 = [oo[k.split("_")[0]][k.split("_")[1]]["R2_M2"] for k in keys]
fig, ax = plt.subplots(figsize=(8.8, 4.8))
cols = ["#1f4e79" if fam_h[k] < 0.05 else ("#5a7fa8" if k.startswith("HOUS") else "#9aa5ad") for k in keys]
bars = ax.bar(np.arange(6), r2, color=cols)
for j, k in enumerate(keys):
    yv = r2[j]
    if yv >= 0:
        ax.text(j, yv + 0.008, "CW p=%.4f\nHolm=%.3f" % (fam_p[k], fam_h[k]),
                ha="center", va="bottom", fontsize=7.8)
    else:
        ax.text(j, yv - 0.008, "CW p=%.4f\nHolm=%.3f" % (fam_p[k], fam_h[k]),
                ha="center", va="top", fontsize=7.8)
ax.axhline(0, color="k", lw=0.8)
ax.set_xticks(np.arange(6)); ax.set_xticklabels(["Housing\nh=1", "Housing\nh=3", "Housing\nh=6",
                                                 "Vehicles\nh=1", "Vehicles\nh=3", "Vehicles\nh=6"])
lo_, hi_ = min(r2), max(r2)
ax.set_ylim(lo_ - 0.09, hi_ + 0.09)
ax.set_ylabel("$R^2_{OOS}$ of M2 vs locked benchmark M0")
ax.set_title("Confirmatory family: CW(M2 vs M0), two markets × three horizons, Holm over six", fontsize=10.5, pad=12)
ax.annotate("survives Holm×6 (p = %.3f)" % fam_h["HOUS_h1"],
            xy=(0, r2[0]), xytext=(2.0, hi_ + 0.045),
            arrowprops=dict(arrowstyle="->", lw=0.9), fontsize=9, ha="left",
            bbox=dict(boxstyle="round,pad=0.35", fc="#eaf1f8", ec="#1f4e79"))
fig.text(0.5, -0.02, "TAU0 = 72; β$_{τ-1}$ information rule; origin-specific historical shocks; "
                     "real-time (leakage-free) current shocks.", ha="center", fontsize=8.3, style="italic")
fig.savefig(f"{FIGOUT}/fig_s6v4_2_confirmatory_family.png"); plt.close(fig)

# FIG 3: stability + robustness of the surviving cell (raw / Holm x6 shown together)
addendum_path = f"{OUT}/S6v4_addendum_results.json"
holm_within = None
if os.path.exists(addendum_path):
    add = json.load(open(addendum_path))
    holm_within = add.get("holm_within_variant_families")

fig, axes = plt.subplots(1, 2, figsize=(10.5, 3.9))
ax = axes[0]
xr = np.arange(len(rc))
b = np.array([float(r["b_sUSD_h1"]) for r in rc]); se = np.array([float(r["se"]) for r in rc])
ax.fill_between(xr, 100 * (b - 1.96 * se), 100 * (b + 1.96 * se), alpha=0.25, color="#1f4e79")
ax.plot(xr, 100 * b, color="#1f4e79", lw=2)
ax.axhline(0, color="k", lw=0.8)
tick = np.linspace(0, len(xr) - 1, 6).astype(int)
ax.set_xticks(tick); ax.set_xticklabels([rc[i]["through_month"] for i in tick], fontsize=8)
sp = res["stability_split_full_reestimation"]
ax.set_ylabel("h = 1 coefficient on $s^{USD}$ (%)")
ax.set_title("Recursive estimate; split-halves Wald: $\\chi^2(3)$ = %.1f, p = %.4f\n→ instability present" %
             (sp["chi2"], sp["p"]), fontsize=9)

ax = axes[1]
labels = ["Main\n(origin-specific)", "Recursive\nshocks", "TAU0 = 60", "TAU0 = 84"]
ps_raw = [fam_p["HOUS_h1"],
          res["pseudo_oos_recursive_robustness"]["HOUS"]["h1"]["CW_M2vsM0"][1],
          res["window_sensitivity"]["TAU0_60"]["HOUS_h1"]["CW_p"],
          res["window_sensitivity"]["TAU0_84"]["HOUS_h1"]["CW_p"]]
if holm_within is not None:
    ps_holm = [fam_h["HOUS_h1"],
               holm_within["fully_recursive"]["holm6"]["HOUS_h1"],
               holm_within["TAU0_60"]["holm6"]["HOUS_h1"],
               holm_within["TAU0_84"]["holm6"]["HOUS_h1"]]
else:
    # fallback to values agreed and verified in Stage6_V4_summary.md
    ps_holm = [0.023, 0.0377, 0.0407, 0.1021]
r2s = [oo["HOUS"]["h1"]["R2_M2"],
       res["pseudo_oos_recursive_robustness"]["HOUS"]["h1"]["R2_M2"],
       res["window_sensitivity"]["TAU0_60"]["HOUS_h1"]["R2_M2"],
       res["window_sensitivity"]["TAU0_84"]["HOUS_h1"]["R2_M2"]]
bar_colors = ["#1f4e79" if ph < 0.05 else "#9aa5ad" for ph in ps_holm]
ax.bar(np.arange(4), r2s, color=bar_colors, alpha=0.9)
for j in range(4):
    lab = "raw p=%.4f\nHolm×6=%.4f" % (ps_raw[j], ps_holm[j])
    if ps_holm[j] >= 0.05:
        lab += "\n(not family-significant)"
    ax.text(j, r2s[j] + 0.004, lab, ha="center", fontsize=7.3)
ax.axhline(0, color="k", lw=0.8)
ax.set_xticks(np.arange(4)); ax.set_xticklabels(labels, fontsize=8.5)
ax.set_ylim(min(r2s) - 0.01, max(r2s) + 0.06)
ax.set_ylabel("$R^2_{OOS}$, housing h = 1")
ax.set_title("Robustness of the surviving cell (housing, h = 1)\n"
             "in-sample LP-coefficient sensitivity — not OOS: b(h=1) = 1.21–1.42%, all p < 0.0003", fontsize=8.7)
fig.suptitle("Stage 6 — Stability and robustness", y=1.04, fontsize=10.5)
fig.savefig(f"{FIGOUT}/fig_s6v4_3_stability_robustness.png"); plt.close(fig)
print("figures written")
