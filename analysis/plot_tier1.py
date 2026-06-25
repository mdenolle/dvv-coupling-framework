"""
plot_tier1.py
=============
Figures for the Tier 1 poroelastic coupling reinterpretation.

Stage 1: California drainage regime map (Pe_annual per site)
Stage 2: Model selection vs. drainage regime confusion matrix + map
Stage 3: Transitional-site variance diagnostic

All figures saved to figures/fig07_tier1_california_*.png
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.patches as mpatches
from matplotlib.ticker import LogLocator, LogFormatter
from pathlib import Path
import warnings

# Colorblind-friendly regime colors
REGIME_COLORS = {
    "drained":      "#2196F3",   # blue
    "transitional": "#FF9800",   # orange
    "undrained":    "#9C27B0",   # purple
    "unknown":      "#BDBDBD",   # grey
}

MODEL_MARKERS = {
    "drained":  "s",    # square
    "elastic":  "^",    # triangle up (undrained/elastic)
    "ssw":      "v",    # triangle down
    "fc":       "D",    # diamond
    "cdm":      "o",    # circle
    "unknown":  "x",
}

# California bounding box
CA_EXTENT = [-124.5, -114.0, 32.3, 42.2]


def _ca_background(ax, extent=CA_EXTENT):
    """Set up a California map axis."""
    ax.set_xlim(extent[0], extent[1])
    ax.set_ylim(extent[2], extent[3])
    ax.set_aspect("equal")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.grid(True, linestyle="--", alpha=0.3)


def fig_drainage_regime_map(df, savepath="figures/fig07_tier1_california_drainage_regime.png"):
    """
    Stage 1: California map colored by Pe_annual (drainage Péclet number).

    Left panel:  Pe_annual color scale (log10)
    Right panel: Discrete drainage classification
    """
    Path(savepath).parent.mkdir(parents=True, exist_ok=True)

    fig, axes = plt.subplots(1, 2, figsize=(14, 7))

    # ── Left: continuous Pe map ───────────────────────────────────────────────
    ax = axes[0]
    Pe = df["Pe_annual"].clip(1e-3, 1e3).values
    sc = ax.scatter(
        df["lon"], df["lat"],
        c=np.log10(Pe),
        cmap="RdBu_r",
        vmin=-2, vmax=2,
        s=25, linewidths=0.3, edgecolors="k", alpha=0.85,
    )
    cbar = fig.colorbar(sc, ax=ax, shrink=0.7, label="log₁₀(Pe_annual)")
    cbar.set_ticks([-2, -1, 0, 1, 2])
    cbar.set_ticklabels(["0.01", "0.1", "1", "10", "100"])
    ax.axhline(0, color="k", linewidth=0)
    _ca_background(ax)
    ax.set_title(r"Drainage Péclet number  $Pe = \omega_{annual} L^2 / c$",
                 fontsize=11)

    # Dashed contour lines at Pe = 0.1 and Pe = 10 (transition boundaries)
    ax.annotate("← drained  |  undrained →", xy=(0.5, 0.02),
                xycoords="axes fraction", ha="center", fontsize=9, color="gray")

    # ── Right: discrete classification ────────────────────────────────────────
    ax = axes[1]
    for regime, grp in df.groupby("drainage_class"):
        color = REGIME_COLORS.get(regime, "#999999")
        ax.scatter(grp["lon"], grp["lat"],
                   c=color, s=25, linewidths=0.3, edgecolors="k", alpha=0.85,
                   label=f"{regime} (n={len(grp)})")
    _ca_background(ax)
    ax.legend(loc="lower right", fontsize=9, framealpha=0.9)
    ax.set_title("Drainage regime classification\n"
                 r"(drained: Pe<0.1 | trans: 0.1<Pe<10 | undrained: Pe>10)",
                 fontsize=10)

    fig.suptitle(
        "Tier 1 Poroelastic Coupling — Stage 1: Drainage Regime\n"
        f"(f = {df.attrs.get('freq_hz', 3.0)} Hz, depth rule: {df.attrs.get('depth_rule', 'λ/3')})",
        fontsize=12, y=1.01
    )
    plt.tight_layout()
    fig.savefig(savepath, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {savepath}")
    return fig


def fig_drainage_vs_tau(df, savepath="figures/fig07_tier1_california_drainage_timescale.png"):
    """
    Supplementary: histogram of drainage timescales and Pe values.
    """
    Path(savepath).parent.mkdir(parents=True, exist_ok=True)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    ax = axes[0]
    bins = np.logspace(-1, 5, 30)  # 0.1 to 100,000 days
    for regime, grp in df.groupby("drainage_class"):
        ax.hist(grp["tau_drain_days"].clip(0.1, 1e5),
                bins=bins, alpha=0.5, label=regime,
                color=REGIME_COLORS.get(regime))
    ax.set_xscale("log")
    ax.set_xlabel("Drainage timescale τ [days]")
    ax.set_ylabel("N stations")
    ax.axvline(365, color="k", linestyle="--", label="1 year")
    ax.legend()
    ax.set_title("Distribution of drainage timescales")

    ax = axes[1]
    bins_Pe = np.logspace(-3, 3, 30)
    ax.hist(df["Pe_annual"].clip(1e-3, 1e3),
            bins=bins_Pe, color="#607D8B", edgecolor="k", linewidth=0.3)
    ax.set_xscale("log")
    ax.axvline(0.1, color=REGIME_COLORS["drained"],   linestyle="--", label="drained threshold")
    ax.axvline(10,  color=REGIME_COLORS["undrained"],  linestyle="--", label="undrained threshold")
    ax.set_xlabel(r"Annual Péclet number $Pe$")
    ax.set_ylabel("N stations")
    ax.legend()
    ax.set_title("Drainage Péclet number distribution")

    plt.tight_layout()
    fig.savefig(savepath, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {savepath}")


def fig_model_selection_map(df, savepath="figures/fig07_tier1_california_model_selection.png"):
    """
    Stage 2: California map where color = drainage regime, marker = winning model.
    Annotates theory_match sites differently.
    """
    Path(savepath).parent.mkdir(parents=True, exist_ok=True)

    if "best_model" not in df.columns:
        warnings.warn("No 'best_model' column — run interpret_all_sites() first.")
        return

    fig, axes = plt.subplots(1, 2, figsize=(14, 7))

    # ── Left: model selection map ─────────────────────────────────────────────
    ax = axes[0]
    for (regime, model), grp in df.groupby(["drainage_class", "best_model"]):
        color  = REGIME_COLORS.get(regime,  "#999")
        marker = MODEL_MARKERS.get(model, "x")
        ax.scatter(grp["lon"], grp["lat"],
                   c=color, marker=marker, s=30,
                   linewidths=0.4, edgecolors="k", alpha=0.8,
                   zorder=3)

    # Legend for drainage regime (color)
    regime_patches = [
        mpatches.Patch(color=REGIME_COLORS[r], label=r)
        for r in ["drained", "transitional", "undrained"]
    ]
    model_markers = [
        plt.Line2D([0], [0], marker=MODEL_MARKERS.get(m, "x"), color="w",
                   markerfacecolor="gray", markersize=7, label=m)
        for m in ["drained", "elastic", "ssw", "fc", "cdm"]
        if m in df["best_model"].unique()
    ]
    leg1 = ax.legend(handles=regime_patches, loc="upper right",
                     title="Drainage regime", fontsize=8, framealpha=0.9)
    ax.add_artist(leg1)
    ax.legend(handles=model_markers, loc="lower right",
              title="Best model (marker)", fontsize=8, framealpha=0.9)
    _ca_background(ax)
    ax.set_title("Drainage regime (color) × winning model (marker)", fontsize=10)

    # ── Right: theory match map ────────────────────────────────────────────────
    ax = axes[1]
    match    = df[df["theory_match"] == True]
    no_match = df[df["theory_match"] == False]
    trans    = df[df["drainage_class"] == "transitional"]

    ax.scatter(no_match["lon"], no_match["lat"], c="#EF5350", s=20,
               edgecolors="k", linewidths=0.3, alpha=0.7, label="Theory mismatch")
    ax.scatter(match["lon"],    match["lat"],    c="#66BB6A", s=20,
               edgecolors="k", linewidths=0.3, alpha=0.8, label="Theory match")
    ax.scatter(trans["lon"],    trans["lat"],    c=REGIME_COLORS["transitional"],
               s=15, marker="D", edgecolors="k", linewidths=0.3,
               alpha=0.6, label=f"Transitional (n={len(trans)})")
    _ca_background(ax)
    n_match = match["theory_match"].sum()
    n_total = len(df[df["drainage_class"] != "transitional"])
    ax.set_title(f"Theory prediction vs. best model\n"
                 f"Match rate: {n_match}/{n_total} = "
                 f"{100*n_match/max(n_total,1):.0f}%", fontsize=10)
    ax.legend(loc="lower right", fontsize=8, framealpha=0.9)

    fig.suptitle("Tier 1 Coupling — Stage 2: Model Selection vs. Drainage Theory",
                 fontsize=12, y=1.01)
    plt.tight_layout()
    fig.savefig(savepath, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {savepath}")


def fig_rt_comparison(df,
                       savepath="figures/fig07_tier1_california_RT_drainage.png"):
    """
    Compare C&D R_T (thermoelastic dominance) with Pe drainage regime.
    Tests whether the R_T spatial pattern is partly a drainage-regime signature.
    """
    Path(savepath).parent.mkdir(parents=True, exist_ok=True)

    if "thermo_dominance" not in df.columns:
        warnings.warn("No 'thermo_dominance' column.")
        return

    fig, axes = plt.subplots(1, 2, figsize=(14, 7))

    # ── Left: R_T map ─────────────────────────────────────────────────────────
    ax = axes[0]
    sc = ax.scatter(df["lon"], df["lat"],
                    c=df["thermo_dominance"].clip(0, 1),
                    cmap="coolwarm_r", vmin=0, vmax=1,
                    s=25, edgecolors="k", linewidths=0.3, alpha=0.85)
    fig.colorbar(sc, ax=ax, shrink=0.7, label="Thermoelastic fraction R_T")
    _ca_background(ax)
    ax.set_title("Thermoelastic fraction R_T\n(1 = thermo dominated, 0 = hydro dominated)",
                 fontsize=10)

    # ── Right: R_T vs Pe scatter ───────────────────────────────────────────────
    ax = axes[1]
    Pe = df["Pe_annual"].clip(1e-3, 1e3)
    RT = df["thermo_dominance"].clip(0, 1)
    for regime, grp in df.groupby("drainage_class"):
        ax.scatter(grp["Pe_annual"].clip(1e-3, 1e3),
                   grp["thermo_dominance"].clip(0, 1),
                   c=REGIME_COLORS.get(regime), s=15, alpha=0.5,
                   edgecolors="none", label=regime)

    # Moving average of R_T vs Pe (uniform_filter1d is a moving average,
    # not a median — labelled accordingly).
    Pe_sorted = np.sort(Pe.values)
    from scipy.ndimage import uniform_filter1d
    idx = np.argsort(Pe.values)
    RT_smooth = uniform_filter1d(RT.values[idx], size=30)
    ax.semilogx(Pe_sorted, RT_smooth, "k-", lw=2, label="Moving average")

    ax.axvline(0.1, color=REGIME_COLORS["drained"],    linestyle="--", alpha=0.7)
    ax.axvline(10,  color=REGIME_COLORS["undrained"],   linestyle="--", alpha=0.7)
    ax.set_xlabel(r"Drainage Péclet number $Pe$")
    ax.set_ylabel("Thermoelastic fraction R_T")
    ax.legend(fontsize=9)
    ax.set_title("R_T vs Pe: is thermoelastic dominance a drainage-regime artifact?",
                 fontsize=10)

    fig.suptitle("Tier 1 Coupling — Stage 2: Thermoelastic Map vs. Drainage Regime",
                 fontsize=12, y=1.01)
    plt.tight_layout()
    fig.savefig(savepath, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {savepath}")


def fig_transitional_diagnostic(df,
                                  savepath="figures/fig07_tier1_california_transitional_diag.png"):
    """
    Stage 3: Transitional-site diagnostic.

    Top: Pe vs best_r2 scatter (expect low R² near Pe=1)
    Bottom: Mismatch score map
    """
    Path(savepath).parent.mkdir(parents=True, exist_ok=True)

    fig, axes = plt.subplots(1, 3, figsize=(18, 6))

    # ── Panel A: Pe vs best R² ────────────────────────────────────────────────
    ax = axes[0]
    Pe = df["Pe_annual"].clip(1e-3, 1e3)
    r2 = df["best_r2"].clip(0, 1)

    for regime, grp in df.groupby("drainage_class"):
        ax.scatter(grp["Pe_annual"].clip(1e-3, 1e3),
                   grp["best_r2"].clip(0, 1),
                   c=REGIME_COLORS.get(regime), s=15, alpha=0.6,
                   edgecolors="none", label=regime)

    # Diagnostic prior curve. NOTE: this is the SAME functional form used to
    # construct the coupling mismatch score, so data agreeing with it is
    # CIRCULAR and is NOT an independent validation. Plotted only to show the
    # prior that defines the score.
    Pe_theory = np.logspace(-3, 3, 200)
    log_Pe = np.log10(Pe_theory)
    R2_pred = 0.7 - 0.3 * np.exp(-(log_Pe**2) / 2.0)
    ax.semilogx(Pe_theory, R2_pred, "k--", lw=1.5,
                label="Diagnostic prior (defines the score; not an independent validation)")

    ax.axvline(0.1, color=REGIME_COLORS["drained"],   linestyle=":", alpha=0.7)
    ax.axvline(10,  color=REGIME_COLORS["undrained"],  linestyle=":", alpha=0.7)
    ax.set_xlabel(r"$Pe_{annual} = \omega_{annual} L^2 / c$")
    ax.set_ylabel("Best-model R²")
    ax.set_title("Stage 3: Transitional sites\nhave systematically low R²", fontsize=10)
    ax.legend(fontsize=8)
    ax.set_ylim(0, 1)

    # ── Panel B: R² gap (drained - undrained) vs Pe ───────────────────────────
    ax = axes[1]
    if "r2_drained" in df.columns and "r2_elastic" in df.columns:
        r2_diff = df["r2_drained"].fillna(0) - df["r2_elastic"].fillna(0)
        sc = ax.scatter(Pe, r2_diff.clip(-0.5, 0.5),
                        c=np.log10(Pe.clip(1e-3, 1e3)),
                        cmap="RdBu_r", vmin=-2, vmax=2,
                        s=15, alpha=0.7, edgecolors="none")
        fig.colorbar(sc, ax=ax, shrink=0.7, label="log₁₀(Pe)")
        ax.axhline(0, color="k", linewidth=1)
        ax.axvline(1, color="gray", linestyle="--", alpha=0.5)
        ax.set_xscale("log")
        ax.set_xlabel(r"$Pe_{annual}$")
        ax.set_ylabel("R²(drained) − R²(undrained)")
        ax.set_title("Model preference:\n+ve = drained wins, −ve = undrained wins", fontsize=10)

    # ── Panel C: Mismatch score map ────────────────────────────────────────────
    ax = axes[2]
    sc = ax.scatter(df["lon"], df["lat"],
                    c=df["mismatch_score"].clip(0, 0.8),
                    cmap="YlOrRd", vmin=0, vmax=0.8,
                    s=20, edgecolors="k", linewidths=0.2, alpha=0.9)
    fig.colorbar(sc, ax=ax, shrink=0.7,
                 label="Coupling mismatch score\n(high = transitional + unexplained)")
    _ca_background(ax)
    ax.set_title("Sites requiring β_eff(ω) model\n(high score = coupling model needed)",
                 fontsize=10)

    fig.suptitle("Tier 1 Coupling — Stage 3: Transitional-Site Diagnostic",
                 fontsize=12, y=1.01)
    plt.tight_layout()
    fig.savefig(savepath, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {savepath}")


def fig_beta_map(df, savepath="figures/fig07_tier1_california_beta_eff.png"):
    """
    Map of effective β (stress sensitivity) per site,
    showing the spatial pattern of coupling strength.
    """
    Path(savepath).parent.mkdir(parents=True, exist_ok=True)

    beta_col = None
    for c in ["beta_elastic_GPa_inv", "beta_drained_GPa_inv"]:
        if c in df.columns:
            beta_col = c
            break

    if beta_col is None:
        warnings.warn("No beta column found — run estimate_beta_per_site() first.")
        return

    fig, axes = plt.subplots(1, 2, figsize=(14, 7))

    # ── β map ──────────────────────────────────────────────────────────────────
    ax = axes[0]
    beta = df[beta_col].clip(0, 5).values
    sc = ax.scatter(df["lon"], df["lat"],
                    c=np.log10(np.clip(beta, 1e-4, 5)),
                    cmap="plasma", vmin=-2, vmax=0.7,
                    s=25, edgecolors="k", linewidths=0.3, alpha=0.9)
    fig.colorbar(sc, ax=ax, shrink=0.7, label="log₁₀(β [GPa⁻¹])")
    _ca_background(ax)
    ax.set_title(r"Acoustoelastic sensitivity $\beta$ [GPa$^{-1}$]", fontsize=11)

    # ── β vs Vs30 scatter ─────────────────────────────────────────────────────
    ax = axes[1]
    if "vs30" in df.columns:
        for regime, grp in df.groupby("drainage_class"):
            ax.scatter(grp["vs30"].clip(100, 2000),
                       grp[beta_col].clip(0, 5),
                       c=REGIME_COLORS.get(regime), s=15, alpha=0.5,
                       edgecolors="none", label=regime)
        ax.set_xlabel("Vs30 [m/s]")
        ax.set_ylabel(f"β [{beta_col.split('_')[2]}]")
        ax.set_title("β vs Vs30: softer rock → higher sensitivity")
        ax.legend(fontsize=8)
    elif "elev_m" in df.columns:
        ax.scatter(df["elev_m"], df[beta_col].clip(0, 5),
                   c=[REGIME_COLORS.get(r, "#999") for r in df["drainage_class"]],
                   s=15, alpha=0.5, edgecolors="none")
        ax.set_xlabel("Elevation [m]")
        ax.set_ylabel("β [GPa⁻¹]")
        ax.set_title("β vs elevation proxy")

    fig.suptitle("Acoustoelastic Sensitivity β per Station", fontsize=12, y=1.01)
    plt.tight_layout()
    fig.savefig(savepath, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {savepath}")


def run_all_figures(df, fig_dir="figures"):
    """
    Generate all Stage 1–3 figures from an interpreted DataFrame.
    """
    Path(fig_dir).mkdir(parents=True, exist_ok=True)
    fig_drainage_regime_map(df, f"{fig_dir}/fig07_tier1_california_drainage_regime.png")
    fig_drainage_vs_tau(df,    f"{fig_dir}/fig07_tier1_california_drainage_timescale.png")
    fig_model_selection_map(df, f"{fig_dir}/fig07_tier1_california_model_selection.png")
    fig_rt_comparison(df,      f"{fig_dir}/fig07_tier1_california_RT_drainage.png")
    fig_transitional_diagnostic(df, f"{fig_dir}/fig07_tier1_california_transitional_diag.png")
    fig_beta_map(df,           f"{fig_dir}/fig07_tier1_california_beta_eff.png")
    print(f"\nAll figures saved to {fig_dir}/")
