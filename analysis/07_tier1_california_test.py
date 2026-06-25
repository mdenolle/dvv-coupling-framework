"""
07_tier1_california_test.py
============================
Driver script for Tier 1 poroelastic coupling reinterpretation of
Clements & Denolle (2023) California dv/v data.

Run this file directly, or copy cells into a Jupyter notebook.

Usage:
    cd dvv_tier1
    python src/07_tier1_california_test.py \
        --fit_summary  data/hydro-model-90-day_L1.parquet \
        --vs_profiles  data/velocity_profiles.csv \
        --freq         3.0 \
        --output_dir   figures

OR import as a module and call run_all() directly.
"""

import sys
import argparse
import numpy as np
import pandas as pd
from pathlib import Path

# Add src to path if running as script
sys.path.insert(0, str(Path(__file__).parent))

from poroelastic_framework import (
    sensitivity_depth, drainage_peclet, classify_drainage,
    beta_ratio_undrained_to_drained, OMEGA_ANNUAL
)
from interpret_fitted_params import (
    load_fit_summary, attach_velocity_profiles, attach_vs30_fallback,
    interpret_all_sites, estimate_beta_per_site,
    drainage_regime_summary, model_selection_table, variance_decomposition
)
from fetch_geospatial import fetch_all_geospatial
from plot_tier1 import run_all_figures


# ─────────────────────────────────────────────────────────────────────────────
# STEP 0: Load and inspect the fitted parameter table
# ─────────────────────────────────────────────────────────────────────────────

def step0_inspect(fit_summary_path):
    """
    Load and print the schema of the fit summary file.
    Call this first with your actual data to verify column names.
    """
    df = load_fit_summary(fit_summary_path)
    print("=== Fit Summary Schema ===")
    print(f"Shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    print("\nFirst 3 rows:")
    print(df.head(3).to_string())
    print("\nNumerical summary:")
    # Show key columns if present
    key_cols = [c for c in ["elastic_c_m2s", "drained_c_m2s", "r2_elastic",
                             "r2_drained", "r2_fc", "r2_cdm", "r2_ssw",
                             "lat", "lon", "elev_m"]
                if c in df.columns]
    if key_cols:
        print(df[key_cols].describe().round(4).to_string())
    return df


# ─────────────────────────────────────────────────────────────────────────────
# STEP 1: Attach velocity profiles and geospatial priors
# ─────────────────────────────────────────────────────────────────────────────

def step1_enrich(df, vs_profiles_path=None,
                  geospatial_cache_dir="data/geospatial_cache",
                  freq_hz=3.0,
                  fan_wtd_path=None,
                  fetch_network=True):
    """
    Attach Vs profiles and geospatial data to the fit summary.

    Parameters
    ----------
    df : fit summary DataFrame
    vs_profiles_path : str or None
        CSV/parquet with columns: netsta, depth_m, Vs_mps, Vp_mps, rho_kgm3
        If None, uses Vs30 fallback.
    geospatial_cache_dir : str
        Where to cache API responses (Vs30, porosity, etc.)
    freq_hz : float
        Measurement center frequency.
    fan_wtd_path : str or None
        Path to Fan et al. (2013) global water table depth NetCDF.
    fetch_network : bool
        If False, skip all network API calls (use cached data only).
    """
    print("\n─── Step 1: Enriching with velocity profiles and geospatial data ───")

    # ── Velocity profiles ──────────────────────────────────────────────────────
    if vs_profiles_path and Path(vs_profiles_path).exists():
        print(f"Loading velocity profiles from {vs_profiles_path}")
        if str(vs_profiles_path).endswith(".parquet"):
            df_vel = pd.read_parquet(vs_profiles_path)
        else:
            df_vel = pd.read_csv(vs_profiles_path)

        # Target depth = sensitivity depth L at center frequency
        # Use a rough estimate for the first pass, then iterate
        L_approx = sensitivity_depth(700.0, freq_hz)   # ~78 m at 3 Hz, Vs=700
        df = attach_velocity_profiles(df, df_vel, depth_layer_m=L_approx)
        print(f"  → Velocity profiles attached. Vs range: "
              f"{df['vs_sens'].min():.0f}–{df['vs_sens'].max():.0f} m/s")
    else:
        df = attach_vs30_fallback(df, vs30_default=700.0)
        print("  → No velocity profiles; using Vs30/default fallback.")

    # ── Geospatial data ────────────────────────────────────────────────────────
    if fetch_network:
        df_geo = fetch_all_geospatial(
            df[["netsta", "lat", "lon"]],
            cache_dir=geospatial_cache_dir,
            fan_wtd_path=fan_wtd_path,
            fetch_vs30=True,
            fetch_porosity=True,
            fetch_wells=False,   # slow; enable for validation
        )
        df = df.merge(df_geo.drop(columns=["lat","lon"], errors="ignore"),
                      on="netsta", how="left")
        print(f"  → Geospatial data attached. New columns: "
              f"{[c for c in df_geo.columns if c not in ['netsta','lat','lon']]}")
    else:
        print("  → Skipping network fetch (fetch_network=False)")

    return df


# ─────────────────────────────────────────────────────────────────────────────
# STEP 2: Stage 1 — Drainage regime classification
# ─────────────────────────────────────────────────────────────────────────────

def step2_drainage_classification(df, freq_hz=3.0, depth_rule="third_wavelength"):
    """
    Compute drainage Péclet number, timescale, and classify sites.
    """
    print("\n─── Step 2: Stage 1 — Drainage Regime Classification ───")

    # Store metadata for plot titles
    df.attrs["freq_hz"]    = freq_hz
    df.attrs["depth_rule"] = depth_rule

    df = interpret_all_sites(
        df,
        freq_hz=freq_hz,
        depth_rule=depth_rule,
        Vs_default=700.0,
        alpha_B_default=0.8,
        B_default=0.6,
        porosity_default=0.15,
    )

    # Print regime summary
    summary = drainage_regime_summary(df)

    # Cross-tab
    ct = model_selection_table(df)

    # Variance decomposition
    vd = variance_decomposition(df)

    # Quick theory-match assessment
    n_match    = df["theory_match"].sum()
    n_total    = (df["drainage_class"] != "transitional").sum()
    match_rate = 100 * n_match / max(n_total, 1)
    print(f"\n  Theory match rate (drained + undrained sites): "
          f"{n_match}/{n_total} = {match_rate:.1f}%")

    return df, {"regime_summary": summary, "model_crosstab": ct, "variance": vd}


# ─────────────────────────────────────────────────────────────────────────────
# STEP 3: Stage 2 — Stress/strain amplitude interpretation
# ─────────────────────────────────────────────────────────────────────────────

def step3_amplitude_interpretation(df, precip_seasonal_mm=400.0):
    """
    Back-calculate β, μ' from fitted amplitudes.

    NOTE: precip_seasonal_mm should ideally be the per-site PRISM amplitude.
    Here we use a California-wide annual cycle approximation.
    """
    print("\n─── Step 3: Amplitude → β, μ' interpretation ───")

    df = estimate_beta_per_site(df, precip_seasonal_mm=precip_seasonal_mm)

    # Print per-regime β statistics
    for model in ["elastic", "drained"]:
        beta_col = f"beta_{model}_GPa_inv"
        if beta_col not in df.columns:
            continue
        print(f"\n  β_{model} [GPa⁻¹] by drainage class:")
        for regime, grp in df.groupby("drainage_class"):
            b = grp[beta_col].dropna()
            if len(b) > 0:
                print(f"    {regime:12s}: median={b.median():.3f}, "
                      f"IQR=[{b.quantile(0.25):.3f}, {b.quantile(0.75):.3f}]")

    # Print β_ratio (undrained enhancement factor)
    print(f"\n  β_u/β_d ratio by drainage class:")
    for regime, grp in df.groupby("drainage_class"):
        r = grp["beta_ratio"].dropna()
        if len(r) > 0:
            print(f"    {regime:12s}: median={r.median():.2f}, "
                  f"range=[{r.min():.2f}, {r.max():.2f}]")

    return df


# ─────────────────────────────────────────────────────────────────────────────
# STEP 4: Stage 3 — Coupling diagnostic and unexplained variance
# ─────────────────────────────────────────────────────────────────────────────

def step4_coupling_diagnostic(df):
    """
    Quantify how much unexplained variance comes from transitional sites.
    """
    print("\n─── Step 4: Stage 3 — Coupling Mismatch Diagnostic ───")

    vd = variance_decomposition(df)

    # Correlation of log|Pe - 1| with unexplained variance.
    # Convert both to numpy arrays and apply a single combined finite mask so the
    # two pearsonr/spearmanr arguments stay aligned (previously a dropna'd Series
    # was paired with a boolean-masked array, which could misalign / mismatch).
    from scipy.stats import pearsonr, spearmanr
    log_Pe_dist = np.abs(np.log10(df["Pe_annual"].clip(1e-4, 1e4)).values)
    unexplained = (1 - df["best_r2"].clip(0, 1)).values

    finite = np.isfinite(log_Pe_dist) & np.isfinite(unexplained)
    log_Pe_dist_f = log_Pe_dist[finite]
    unexplained_f = unexplained[finite]

    r_pearson,  p_pearson  = pearsonr(log_Pe_dist_f, unexplained_f)
    r_spearman, p_spearman = spearmanr(log_Pe_dist_f, unexplained_f)

    print(f"\n  Pearson  corr(|log Pe|, unexplained): r={r_pearson:.3f}, p={p_pearson:.3e}")
    print(f"  Spearman corr(|log Pe|, unexplained): r={r_spearman:.3f}, p={p_spearman:.3e}")
    print("\n  Interpretation: Large r (>0.3) at p<0.01 supports hypothesis that")
    print("  transitional-regime sites drive unexplained variance (coupling effect).")

    # How much of total unexplained variance is from transitional sites?
    is_trans = df["drainage_class"] == "transitional"
    frac_trans_stations = is_trans.mean()
    frac_trans_unexplained = (
        unexplained[is_trans].sum() / np.nansum(unexplained)
        if np.nansum(unexplained) > 0 else 0
    )
    print(f"\n  Transitional sites: {100*frac_trans_stations:.0f}% of stations, "
          f"{100*frac_trans_unexplained:.0f}% of total unexplained variance")

    return {**vd,
            "r_pearson_logPe_unexplained":  r_pearson,
            "r_spearman_logPe_unexplained": r_spearman,
            "frac_trans_stations":          frac_trans_stations,
            "frac_trans_unexplained":       frac_trans_unexplained}


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

def run_all(fit_summary_path,
            vs_profiles_path=None,
            freq_hz=3.0,
            output_dir="figures",
            geospatial_cache_dir="data/geospatial_cache",
            fan_wtd_path=None,
            fetch_network=True,
            precip_seasonal_mm=400.0):
    """
    Full pipeline: load → enrich → classify → interpret → plot.

    Parameters
    ----------
    fit_summary_path : str
        Path to hydro-model-90-day_L1.parquet (or .arrow or .csv)
    vs_profiles_path : str or None
        Path to velocity profile CSV/parquet (columns: netsta, depth_m, Vs_mps, Vp_mps, rho_kgm3)
        If None, uses Vs30 from USGS API or default.
    freq_hz : float
        Center measurement frequency [Hz]. Default 3.0 (C&D 2-4 Hz band).
    output_dir : str
        Directory for output figures and tables.
    geospatial_cache_dir : str
        Cache directory for API responses.
    fan_wtd_path : str or None
        Path to Fan et al. (2013) global WTD NetCDF.
    fetch_network : bool
        If False, skip all network API calls.
    precip_seasonal_mm : float
        Approximate seasonal precipitation amplitude for β estimation.

    Returns
    -------
    df : enriched and interpreted DataFrame
    stats : dict of statistical outputs
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # ── Load ────────────────────────────────────────────────────────────────
    print(f"\n{'='*60}")
    print("Tier 1 California Poroelastic Coupling Test")
    print(f"{'='*60}")
    print(f"Input: {fit_summary_path}")
    print(f"Frequency: {freq_hz} Hz")

    df = step0_inspect(fit_summary_path)

    # ── Enrich ──────────────────────────────────────────────────────────────
    df = step1_enrich(df, vs_profiles_path=vs_profiles_path,
                       geospatial_cache_dir=geospatial_cache_dir,
                       freq_hz=freq_hz,
                       fan_wtd_path=fan_wtd_path,
                       fetch_network=fetch_network)

    # ── Stage 1: drainage classification ────────────────────────────────────
    df, stats1 = step2_drainage_classification(df, freq_hz=freq_hz)

    # ── Stage 2: amplitude interpretation ────────────────────────────────────
    df = step3_amplitude_interpretation(df, precip_seasonal_mm=precip_seasonal_mm)

    # ── Stage 3: coupling diagnostic ─────────────────────────────────────────
    stats3 = step4_coupling_diagnostic(df)

    # ── Save intermediate results ─────────────────────────────────────────────
    out_csv = Path(output_dir) / "tier1_interpreted_stations.csv"
    df.to_csv(out_csv, index=False)
    print(f"\nInterpreted table saved to: {out_csv}")

    # ── Generate figures ──────────────────────────────────────────────────────
    print("\nGenerating figures...")
    run_all_figures(df, fig_dir=output_dir)

    return df, {**stats1, **stats3}


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Tier 1 poroelastic coupling test for C&D California dv/v data"
    )
    parser.add_argument("--fit_summary",   required=True,
                        help="Path to hydro-model-90-day_L1.parquet")
    parser.add_argument("--vs_profiles",   default=None,
                        help="Path to velocity profiles CSV")
    parser.add_argument("--freq",          type=float, default=3.0,
                        help="Center frequency [Hz] (default: 3.0)")
    parser.add_argument("--output_dir",    default="figures",
                        help="Output directory for figures and tables")
    parser.add_argument("--cache_dir",     default="data/geospatial_cache",
                        help="Cache directory for API results")
    parser.add_argument("--wtd_path",      default=None,
                        help="Path to Fan et al. (2013) WTD NetCDF")
    parser.add_argument("--no_network",    action="store_true",
                        help="Skip all network API calls")
    parser.add_argument("--precip_mm",     type=float, default=400.0,
                        help="Seasonal precipitation amplitude [mm] for β")

    args = parser.parse_args()

    df, stats = run_all(
        fit_summary_path=args.fit_summary,
        vs_profiles_path=args.vs_profiles,
        freq_hz=args.freq,
        output_dir=args.output_dir,
        geospatial_cache_dir=args.cache_dir,
        fan_wtd_path=args.wtd_path,
        fetch_network=not args.no_network,
        precip_seasonal_mm=args.precip_mm,
    )
