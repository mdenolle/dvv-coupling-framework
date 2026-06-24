"""
Generate the streamlined JGR Solid Earth main-display figure set.

These figures summarize the manuscript's central argument. Detailed tutorial
and sensitivity plots remain in the notebook-generated supporting figures.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


OUTDIR = Path(__file__).resolve().parents[1] / "figures" / "main"
OUTDIR.mkdir(parents=True, exist_ok=True)


def setup_style() -> None:
    plt.rcParams.update(
        {
            "figure.dpi": 160,
            "savefig.dpi": 220,
            "font.size": 10,
            "axes.labelsize": 10,
            "axes.titlesize": 11,
            "legend.fontsize": 9,
            "xtick.labelsize": 9,
            "ytick.labelsize": 9,
            "font.family": "DejaVu Sans",
            "axes.spines.top": False,
            "axes.spines.right": False,
        }
    )


def add_box(ax, xy, wh, text, fc, ec="#30343b", fontsize=10):
    box = FancyBboxPatch(
        xy,
        wh[0],
        wh[1],
        boxstyle="round,pad=0.02,rounding_size=0.025",
        facecolor=fc,
        edgecolor=ec,
        linewidth=1.2,
    )
    ax.add_patch(box)
    ax.text(
        xy[0] + wh[0] / 2,
        xy[1] + wh[1] / 2,
        text,
        ha="center",
        va="center",
        fontsize=fontsize,
        color="#111827",
        linespacing=1.2,
    )


def add_arrow(ax, start, end, color="#4b5563"):
    ax.add_patch(
        FancyArrowPatch(
            start,
            end,
            arrowstyle="-|>",
            mutation_scale=14,
            linewidth=1.4,
            color=color,
            shrinkA=4,
            shrinkB=4,
        )
    )


def figure_01_workflow():
    fig, ax = plt.subplots(figsize=(11, 6.2))
    ax.set_axis_off()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    cols = {
        "forcing": "#dbeafe",
        "stress": "#fee2e2",
        "material": "#ecfccb",
        "observable": "#ede9fe",
        "diagnostic": "#fef3c7",
    }

    add_box(ax, (0.04, 0.67), (0.18, 0.18), "Forcing\nT, rain, GWL,\nice, tectonics,\nmagmatic pressure", cols["forcing"])
    add_box(ax, (0.29, 0.67), (0.18, 0.18), "Stress / strain\nisotropic pressure,\ndeviatoric stress,\npore pressure", cols["stress"])
    add_box(ax, (0.54, 0.67), (0.18, 0.18), "Material response\nbeta, mu prime,\ncracks, saturation,\nrheology", cols["material"])
    add_box(ax, (0.78, 0.67), (0.18, 0.18), "Observable\nfrequency-dependent\n$\\delta v/v(f,t)$", cols["observable"])

    for x0, x1 in [(0.22, 0.29), (0.47, 0.54), (0.72, 0.78)]:
        add_arrow(ax, (x0, 0.76), (x1, 0.76))

    add_box(ax, (0.08, 0.35), (0.18, 0.15), "Forward models\nthermoelastic\nporoelastic\ncapillary", "#e0f2fe")
    add_box(ax, (0.32, 0.35), (0.18, 0.15), "Sensitivity kernels\n$K(z,f)$\nRayleigh / Love", "#f0fdf4")
    add_box(ax, (0.56, 0.35), (0.18, 0.15), "Mechanism tests\nsign, phase,\nfrequency, azimuth", "#fff7ed")
    add_box(ax, (0.78, 0.35), (0.18, 0.15), "Stress / rheology\nestimate with\nuncertainty", cols["diagnostic"])

    add_arrow(ax, (0.87, 0.67), (0.87, 0.50))
    add_arrow(ax, (0.78, 0.43), (0.74, 0.43))
    add_arrow(ax, (0.56, 0.43), (0.50, 0.43))
    add_arrow(ax, (0.32, 0.43), (0.26, 0.43))

    ax.text(0.5, 0.18, "codameter implementation target", ha="center", fontsize=12, weight="bold")
    add_box(
        ax,
        (0.13, 0.06),
        (0.74, 0.09),
        "ingest data  ->  kernels  ->  forward models  ->  mechanism diagnostics  ->  stress/rheology report",
        "#f8fafc",
        fontsize=9,
    )

    ax.set_title("Unified workflow for interpreting ambient-noise velocity changes", fontsize=14, weight="bold", pad=12)
    fig.savefig(OUTDIR / "fig01_unified_workflow.png", bbox_inches="tight")
    plt.close(fig)


def figure_02_depth_kernels():
    fig, axes = plt.subplots(1, 3, figsize=(12, 4.1), constrained_layout=True)
    freqs = np.array([0.1, 0.3, 0.5, 1.0, 2.0, 4.0])
    vs = 1800.0
    depths = np.linspace(0, 8000, 600)
    colors = plt.cm.viridis(np.linspace(0.1, 0.9, len(freqs)))

    for f, c in zip(freqs, colors):
        z_peak = vs / (3 * f)
        sigma = 0.8 * z_peak + 80
        kernel = np.exp(-0.5 * ((depths - z_peak) / sigma) ** 2)
        kernel /= np.trapezoid(kernel, depths)
        axes[0].plot(kernel / kernel.max(), depths / 1000, color=c, label=f"{f:g} Hz")
    axes[0].invert_yaxis()
    axes[0].set_xlabel("Normalized sensitivity")
    axes[0].set_ylabel("Depth (km)")
    axes[0].set_title("(a) Broad frequency kernels")
    axes[0].legend(frameon=False, ncol=2)

    for vs_val, label, color in [(500, "soft sediment", "#2563eb"), (1800, "weathered rock", "#16a34a"), (3200, "crystalline rock", "#dc2626")]:
        axes[1].loglog(freqs, vs_val / (3 * freqs) / 1000, "o-", color=color, label=label)
    axes[1].set_xlabel("Frequency (Hz)")
    axes[1].set_ylabel("Peak depth (km)")
    axes[1].set_title("(b) $z_{peak} \\approx V_S / 3f$")
    axes[1].grid(True, which="both", alpha=0.25)
    axes[1].legend(frameon=False)

    nfreq = np.arange(2, 11)
    nominal = 1 / np.sqrt(nfreq)
    effective = 1 / np.sqrt(1 + 0.35 * (nfreq - 1))
    axes[2].plot(nfreq, nominal, "o-", label="independent bands", color="#2563eb")
    axes[2].plot(nfreq, effective, "s-", label="correlated kernels", color="#dc2626")
    axes[2].set_xlabel("Number of frequency bands")
    axes[2].set_ylabel("Relative uncertainty")
    axes[2].set_ylim(0.25, 0.8)
    axes[2].set_title("(c) Depth inversion is ill-conditioned")
    axes[2].grid(True, alpha=0.25)
    axes[2].legend(frameon=False)

    fig.suptitle("Frequency-dependent depth sensitivity and inversion limits", fontsize=14, weight="bold")
    fig.savefig(OUTDIR / "fig02_depth_kernels.png", bbox_inches="tight")
    plt.close(fig)


def figure_03_hydrological_competition():
    fig, axes = plt.subplots(1, 3, figsize=(12, 4.0), constrained_layout=True)
    mu = 5e8
    mu_prime = 80
    g = 9.81

    def dvv_load(T33, u0):
        pore = -mu_prime / (2 * mu) * u0
        load = (mu_prime + 1) / (12 * mu) * T33
        return pore + load, pore, load

    scenarios = [
        ("Ice thickness (m)", np.linspace(0, 3000, 180), 917 * g, 0.6 / 3, "(a) Ice / snow loading"),
        ("Rain load (mm)", np.linspace(0, 500, 180), 1000 * g / 1000, 0.8, "(b) Seasonal rainfall"),
        ("Reservoir depth (m)", np.linspace(0, 100, 180), 1000 * g, 0.5, "(c) Reservoir impoundment"),
    ]
    for ax, (xlabel, x, load_scale, b_eff, title) in zip(axes, scenarios):
        t33 = load_scale * x
        u0 = load_scale * x * b_eff
        total, pore, load = dvv_load(t33, u0)
        ax.plot(x, total * 100, color="black", lw=2.2, label="total")
        ax.plot(x, pore * 100, "--", color="#2563eb", lw=1.8, label="pore pressure")
        ax.plot(x, load * 100, "--", color="#dc2626", lw=1.8, label="surface load")
        ax.axhline(0, color="0.5", lw=0.8)
        ax.set_xlabel(xlabel)
        ax.set_title(title)
        ax.grid(True, alpha=0.25)
    axes[0].set_ylabel("$\\delta v/v$ (%)")
    axes[1].legend(frameon=False, loc="best")
    fig.suptitle("Hydrological signals are a sign competition between loading and pore pressure", fontsize=13, weight="bold")
    fig.savefig(OUTDIR / "fig03_hydrological_competition.png", bbox_inches="tight")
    plt.close(fig)


def figure_04_material_sensitivity():
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.2), constrained_layout=True)
    materials = ["Steel", "Granite\n(intact)", "Fractured\ncrystalline", "Soft\nsediment"]
    beta = np.array([10, 40, 300, 3160])
    colors = ["#64748b", "#16a34a", "#f97316", "#2563eb"]
    axes[0].bar(materials, beta, color=colors)
    axes[0].set_yscale("log")
    axes[0].set_ylabel(r"$|\beta|$")
    axes[0].set_title("(a) Material sensitivity spans orders of magnitude")
    axes[0].grid(True, axis="y", which="both", alpha=0.25)

    sites = ["Parkfield", "N. Cascadia", "Kilauea"]
    dvv = np.array([0.005, 0.038, 0.5])
    stress = np.array([12.0, 0.58, 170.0])
    x = np.arange(len(sites))
    width = 0.35
    ax2 = axes[1]
    ax2.bar(x - width / 2, dvv / dvv[0], width, label=r"$\delta v/v$ amplitude", color="#8b5cf6")
    ax2.bar(x + width / 2, stress / stress[0], width, label="stress perturbation", color="#14b8a6")
    ax2.set_yscale("log")
    ax2.set_xticks(x)
    ax2.set_xticklabels(sites)
    ax2.set_ylabel("Ratio relative to Parkfield")
    ax2.set_title("(b) Amplitude ratios are not stress ratios")
    ax2.grid(True, axis="y", which="both", alpha=0.25)
    ax2.legend(frameon=False)

    fig.suptitle("Material sensitivity controls stress conversion from velocity change", fontsize=13, weight="bold")
    fig.savefig(OUTDIR / "fig04_material_sensitivity.png", bbox_inches="tight")
    plt.close(fig)


def figure_05_anisotropy():
    fig = plt.figure(figsize=(11.5, 6.0), constrained_layout=True)
    gs = fig.add_gridspec(2, 3)
    ax0 = fig.add_subplot(gs[:, 0], projection="polar")
    ax1 = fig.add_subplot(gs[0, 1])
    ax2 = fig.add_subplot(gs[0, 2])
    ax3 = fig.add_subplot(gs[1, 1])
    ax4 = fig.add_subplot(gs[1, 2])

    theta = np.linspace(0, 2 * np.pi, 400)
    for amp, color, label in [(0.15, "#94a3b8", "weak fabric"), (0.35, "#2563eb", "strong fabric")]:
        r = 1 + amp * np.cos(2 * theta)
        ax0.plot(theta, r, color=color, lw=2, label=label)
    ax0.set_theta_zero_location("N")
    ax0.set_theta_direction(-1)
    ax0.set_title("(a) Directional sensitivity")
    ax0.legend(loc="upper right", bbox_to_anchor=(1.20, 1.04), frameon=False)

    def schematic(ax, title, cracks, arrows, sign):
        ax.set_axis_off()
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_title(title)
        for x0, y0, x1, y1 in cracks:
            ax.plot([x0, x1], [y0, y1], color="#111827", lw=2)
        for start, end in arrows:
            add_arrow(ax, start, end, "#dc2626")
        ax.text(0.5, 0.08, sign, ha="center", va="center", fontsize=10, weight="bold")

    schematic(
        ax1,
        "(b) Parkfield",
        [(0.25, 0.2, 0.75, 0.8), (0.18, 0.35, 0.65, 0.88), (0.35, 0.1, 0.85, 0.6)],
        [((0.9, 0.5), (0.65, 0.5)), ((0.1, 0.5), (0.35, 0.5))],
        "fault-normal contraction -> +dv/v",
    )
    schematic(
        ax2,
        "(c) Cascadia",
        [(0.2, 0.2, 0.8, 0.25), (0.18, 0.45, 0.82, 0.48), (0.25, 0.68, 0.78, 0.74)],
        [((0.15, 0.75), (0.35, 0.6)), ((0.85, 0.75), (0.65, 0.6)), ((0.5, 0.95), (0.5, 0.75))],
        "volumetric compaction -> scalar works",
    )
    schematic(
        ax3,
        "(d) Kilauea",
        [(0.5 + 0.26 * np.cos(t), 0.5 + 0.26 * np.sin(t), 0.5 + 0.34 * np.cos(t), 0.5 + 0.34 * np.sin(t)) for t in np.linspace(0, 2 * np.pi, 16, endpoint=False)],
        [((0.5, 0.94), (0.5, 0.72)), ((0.06, 0.5), (0.28, 0.5)), ((0.94, 0.5), (0.72, 0.5))],
        "ring-fracture compression -> +dv/v",
    )

    ax4.set_title("(e) Isotropic model failure")
    labels = ["Parkfield", "Cascadia", "Kilauea"]
    vals = [-1, 1, -1]
    ax4.bar(labels, vals, color=["#ef4444", "#22c55e", "#ef4444"])
    ax4.axhline(0, color="0.3", lw=0.8)
    ax4.set_ylim(-1.4, 1.4)
    ax4.set_ylabel("Scalar sign test")
    ax4.set_yticks([-1, 1])
    ax4.set_yticklabels(["fails", "succeeds"])
    ax4.grid(True, axis="y", alpha=0.2)

    fig.suptitle("Deviatoric stress and fracture fabric determine the observed velocity sign", fontsize=14, weight="bold")
    fig.savefig(OUTDIR / "fig05_anisotropy_fabric.png", bbox_inches="tight")
    plt.close(fig)


def figure_06_rheology():
    fig, axes = plt.subplots(2, 2, figsize=(10.5, 7.0), constrained_layout=True)
    t = np.linspace(0, 5, 500)
    step = np.ones_like(t)
    maxwell = np.exp(-t / 1.2)
    kelvin = 1 - np.exp(-t / 1.2)
    slow = np.log1p(t / 0.05) / np.log1p(5 / 0.05)
    axes[0, 0].plot(t, step, label="elastic", lw=2)
    axes[0, 0].plot(t, maxwell, label="Maxwell", lw=2)
    axes[0, 0].plot(t, kelvin, label="Kelvin-Voigt", lw=2)
    axes[0, 0].plot(t, slow, label="slow dynamics", lw=2)
    axes[0, 0].set_xlabel("Time after forcing")
    axes[0, 0].set_ylabel("Normalized response")
    axes[0, 0].set_title("(a) Step response")
    axes[0, 0].legend(frameon=False)
    axes[0, 0].grid(True, alpha=0.25)

    strain = np.sin(np.linspace(0, 2 * np.pi, 400))
    axes[0, 1].plot(strain, strain, lw=2, label="elastic")
    axes[0, 1].plot(strain, 0.75 * strain + 0.25 * strain**2, lw=2, label="higher-order")
    axes[0, 1].plot(strain, np.sin(np.linspace(0, 2 * np.pi, 400) - 0.6), lw=2, label="viscoelastic lag")
    axes[0, 1].set_xlabel("Strain")
    axes[0, 1].set_ylabel(r"$\delta v/v$")
    axes[0, 1].set_title("(b) Crossplot diagnostic")
    axes[0, 1].legend(frameon=False)
    axes[0, 1].grid(True, alpha=0.25)

    years = np.linspace(2001, 2021, 600)
    trend = 0.0048 * (years - 2001)
    healing = -0.08 * np.log1p(np.maximum(years - 2004.75, 0) / 0.15) / np.log1p((2021 - 2004.75) / 0.15)
    seasonal = 0.015 * np.sin(2 * np.pi * years)
    axes[1, 0].plot(years, trend + healing + seasonal, color="#111827", lw=1.6)
    axes[1, 0].plot(years, trend, "--", color="#dc2626", label="tectonic trend")
    axes[1, 0].plot(years, healing, "--", color="#2563eb", label="postseismic healing")
    axes[1, 0].set_xlabel("Year")
    axes[1, 0].set_ylabel(r"$\delta v/v$ (%)")
    axes[1, 0].set_title("(c) Parkfield-like dual population")
    axes[1, 0].legend(frameon=False)
    axes[1, 0].grid(True, alpha=0.25)

    amp = np.array([1, 10, 50, 100, 300])
    distortion = (amp / 100) ** 2
    axes[1, 1].loglog(amp, distortion, "o-", lw=2, color="#7c3aed")
    axes[1, 1].axvline(50, color="0.4", ls="--", lw=1)
    axes[1, 1].text(52, 0.02, "Earth tides", va="bottom", fontsize=9)
    axes[1, 1].set_xlabel("Strain amplitude (nanostrain)")
    axes[1, 1].set_ylabel("Harmonic distortion")
    axes[1, 1].set_title("(d) Tidal nonlinearity test")
    axes[1, 1].grid(True, which="both", alpha=0.25)

    fig.suptitle("Rheology is diagnosed from phase, hysteresis, and recovery shape", fontsize=14, weight="bold")
    fig.savefig(OUTDIR / "fig06_rheology_diagnostics.png", bbox_inches="tight")
    plt.close(fig)


def figure_07_three_site():
    fig, axes = plt.subplots(2, 2, figsize=(11.5, 7.0), constrained_layout=True)
    sites = ["Parkfield", "N. Cascadia", "Kilauea"]
    beta = np.array([240, 3160, 300])
    mu_prime = np.array([251, 618, 360])
    stress = np.array([12, 0.58, 170])
    colors = ["#f97316", "#2563eb", "#dc2626"]

    axes[0, 0].bar(sites, beta, color=colors)
    axes[0, 0].set_yscale("log")
    axes[0, 0].set_ylabel(r"$|\beta|$")
    axes[0, 0].set_title("(a) Effective velocity-strain sensitivity")
    axes[0, 0].grid(True, axis="y", which="both", alpha=0.25)

    axes[0, 1].bar(sites, mu_prime, color=colors)
    axes[0, 1].set_ylabel(r"$\mu'$")
    axes[0, 1].set_title("(b) Inferred shear-modulus pressure derivative")
    axes[0, 1].grid(True, axis="y", alpha=0.25)

    axes[1, 0].bar(sites, stress, color=colors)
    axes[1, 0].set_yscale("log")
    axes[1, 0].set_ylabel("Stress perturbation\n(kPa/yr or kPa/event)")
    axes[1, 0].set_title("(c) Stress after material normalization")
    axes[1, 0].grid(True, axis="y", which="both", alpha=0.25)

    ax = axes[1, 1]
    ax.set_axis_off()
    ax.set_title("(d) Mechanism branch selected by geometry")
    rows = [
        ("Parkfield", "deviatoric", "fault-normal\ncontraction", "fails"),
        ("N. Cascadia", "isotropic", "volumetric\ncompression", "works"),
        ("Kilauea", "deviatoric", "radial ring-fracture\ncompression", "fails"),
    ]
    y0 = 0.82
    for i, (site, branch, strain, check) in enumerate(rows):
        y = y0 - i * 0.27
        add_box(ax, (0.02, y - 0.08), (0.22, 0.13), site, "#f8fafc", fontsize=9)
        add_box(ax, (0.30, y - 0.08), (0.22, 0.13), branch, "#ecfccb" if branch == "isotropic" else "#fee2e2", fontsize=9)
        add_box(ax, (0.58, y - 0.08), (0.25, 0.13), strain, "#e0f2fe", fontsize=8)
        add_box(ax, (0.88, y - 0.08), (0.10, 0.13), check, "#dcfce7" if check == "works" else "#fee2e2", fontsize=8)
        add_arrow(ax, (0.24, y - 0.015), (0.30, y - 0.015))
        add_arrow(ax, (0.52, y - 0.015), (0.58, y - 0.015))

    fig.suptitle("Three-site synthesis: the same dv/v framework selects different stress branches", fontsize=14, weight="bold")
    fig.savefig(OUTDIR / "fig07_three_site_synthesis.png", bbox_inches="tight")
    plt.close(fig)


def main():
    setup_style()
    figure_01_workflow()
    figure_02_depth_kernels()
    figure_03_hydrological_competition()
    figure_04_material_sensitivity()
    figure_05_anisotropy()
    figure_06_rheology()
    figure_07_three_site()
    print(f"Wrote figures to {OUTDIR}")


if __name__ == "__main__":
    main()
