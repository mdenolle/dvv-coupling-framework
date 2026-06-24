"""
interpret_fitted_params.py
==========================
Load the Clements & Denolle (2023) fitted parameter outputs and reinterpret
them within the Tier 1 poroelastic coupling framework.

Expected input:
  - Summary parquet:  hydro-model-90-day_L1.parquet  (one row per station)
  - Per-station parquet (optional): NET.STA.parquet with DATE, DVV, CC columns
  - Vs/Vp/density profile: CSV or parquet with columns NETSTA, depth_m, Vs, Vp, rho

Usage
-----
    from interpret_fitted_params import load_fit_summary, interpret_all_sites
    df = load_fit_summary("path/to/hydro-model-90-day_L1.parquet")
    results = interpret_all_sites(df, freq_hz=3.0)
"""

import numpy as np
import pandas as pd
from pathlib import Path

from poroelastic_framework import (
    sensitivity_depth,
    drainage_frequency,
    drainage_peclet,
    classify_drainage,
    fitted_c_to_physical,
    beta_ratio_undrained_to_drained,
    skempton_B_empirical,
    undrained_poisson,
    poisson_ratio,
    shear_modulus,
    bulk_modulus,
    infer_beta_from_fit,
    infer_mu_prime,
    thermoelastic_from_fitted_amplitude,
    coupling_mismatch_score,
    drainage_model_prediction,
    OMEGA_ANNUAL,
)


# ─────────────────────────────────────────────────────────────────────────────
# 1. Load Clements & Denolle fitted parameter table
# ─────────────────────────────────────────────────────────────────────────────

# Column name mapping: Julia output → semantic names
CD_COLUMN_MAP = {
    # Station info
    "NETSTA": "netsta",
    "LAT":    "lat",
    "LON":    "lon",
    "ELEV":   "elev_m",
    # Elastic (undrained) model: p = [offset, amp, c, thermo_amp, lag_days]
    "E1": "elastic_offset",
    "E2": "elastic_hydro_amp",
    "E3": "elastic_c_m2s",        # ← KEY: fitted hydraulic diffusivity
    "E4": "elastic_thermo_amp",
    "E5": "elastic_lag_days",
    # Drained model
    "D1": "drained_offset",
    "D2": "drained_hydro_amp",
    "D3": "drained_c_m2s",        # ← KEY: fitted hydraulic diffusivity
    "D4": "drained_thermo_amp",
    "D5": "drained_lag_days",
    # Fully coupled
    "FC1": "fc_offset",
    "FC2": "fc_hydro_amp",
    "FC3": "fc_c_m2s",
    "FC4": "fc_thermo_amp",
    "FC5": "fc_lag_days",
    # CDMk model
    "CDM1": "cdm_offset",
    "CDM2": "cdm_hydro_amp",
    "CDM3": "cdm_k_days",          # ← memory window k [days]
    "CDM4": "cdm_thermo_amp",
    "CDM5": "cdm_lag_days",
    # SSW06 (baseflow) model
    "SSW1": "ssw_offset",
    "SSW2": "ssw_hydro_amp",
    "SSW3": "ssw_decay_rate",      # ← exponential decay a [day⁻¹]
    "SSW4": "ssw_thermo_amp",
    "SSW5": "ssw_lag_days",
    # Fit quality (L1 norm correlation and R²)
    "corEL1":   "cor_elastic",
    "corDL1":   "cor_drained",
    "corFCL1":  "cor_fc",
    "corCDML1": "cor_cdm",
    "corSSWL1": "cor_ssw",
    "r2EL1":    "r2_elastic",
    "r2DL1":    "r2_drained",
    "r2FCL1":   "r2_fc",
    "r2CDML1":  "r2_cdm",
    "r2SSWL1":  "r2_ssw",
}


def load_fit_summary(path, rename=True):
    """
    Load the Clements & Denolle summary parameter parquet/arrow/csv.

    Accepts: .parquet, .arrow, .csv

    Parameters
    ----------
    path : str or Path
    rename : bool
        If True, apply CD_COLUMN_MAP to rename columns to semantic names.

    Returns
    -------
    df : pd.DataFrame  (one row per station)
    """
    path = Path(path)
    suffix = path.suffix.lower()

    if suffix == ".parquet":
        df = pd.read_parquet(path)
    elif suffix == ".arrow":
        import pyarrow as pa
        import pyarrow.ipc as ipc
        with open(path, "rb") as f:
            reader = ipc.open_file(f)
            df = reader.read_all().to_pandas()
    elif suffix in (".csv", ".tsv"):
        df = pd.read_csv(path)
    else:
        raise ValueError(f"Unsupported file format: {suffix}")

    if rename:
        df = df.rename(columns={k: v for k, v in CD_COLUMN_MAP.items()
                                 if k in df.columns})

    # Standardize column names
    df.columns = [c.lower() for c in df.columns]
    return df


def load_dvv_timeseries(path):
    """
    Load a single-station dv/v time series parquet.
    Returns DataFrame with columns: date, dvv_pct, cc
    """
    path = Path(path)
    suffix = path.suffix.lower()

    if suffix == ".parquet":
        df = pd.read_parquet(path)
    elif suffix == ".arrow":
        import pyarrow.ipc as ipc
        with open(path, "rb") as f:
            reader = ipc.open_file(f)
            df = reader.read_all().to_pandas()
    else:
        df = pd.read_csv(path, parse_dates=["DATE"])

    col_map = {"DATE": "date", "DVV": "dvv_pct", "CC": "cc"}
    df = df.rename(columns={k: v for k, v in col_map.items() if k in df.columns})
    df.columns = [c.lower() for c in df.columns]
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"])
        df = df.sort_values("date").reset_index(drop=True)
    return df


# ─────────────────────────────────────────────────────────────────────────────
# 2. Attach seismic velocity profiles
# ─────────────────────────────────────────────────────────────────────────────

def attach_velocity_profiles(df_stations, df_profiles,
                              depth_layer_m=50.0):
    """
    Merge Vs, Vp, density at a target depth into the station summary table.

    Parameters
    ----------
    df_stations : pd.DataFrame  (one row per station, must have 'netsta')
    df_profiles : pd.DataFrame
        Columns: netsta, depth_m, Vs_mps, Vp_mps, rho_kgm3
        One row per (station, depth) layer.
    depth_layer_m : float
        Target depth to extract [m]. Uses nearest layer.

    Returns
    -------
    df_stations with new columns: Vs_sens, Vp_sens, rho_sens
    """
    # Extract nearest depth layer per station
    selected = []
    for netsta, grp in df_profiles.groupby("netsta"):
        idx = (grp["depth_m"] - depth_layer_m).abs().idxmin()
        row = grp.loc[idx, ["netsta", "Vs_mps", "Vp_mps", "rho_kgm3"]].copy()
        row["depth_extracted_m"] = grp.loc[idx, "depth_m"]
        selected.append(row)

    df_vel = pd.DataFrame(selected).rename(columns={
        "Vs_mps": "Vs_sens",
        "Vp_mps": "Vp_sens",
        "rho_kgm3": "rho_sens",
    })
    return df_stations.merge(df_vel, on="netsta", how="left")


def attach_vs30_fallback(df, vs30_default=600.0):
    """
    If Vs_sens is missing, use Vs30 as a fallback for sensitivity depth.
    Vs30 can be sourced from USGS or CGS (to be queried separately).
    """
    if "vs30" in df.columns:
        df["Vs_sens"] = df["Vs_sens"].fillna(df["vs30"])
    else:
        df["Vs_sens"] = df.get("Vs_sens", pd.Series(vs30_default, index=df.index))
        df["Vs_sens"] = df["Vs_sens"].fillna(vs30_default)
    return df


# ─────────────────────────────────────────────────────────────────────────────
# 3. Main interpretation pipeline
# ─────────────────────────────────────────────────────────────────────────────

def interpret_all_sites(df, freq_hz=3.0,
                        depth_rule="third_wavelength",
                        Vs_default=700.0,
                        alpha_B_default=0.8,
                        B_default=0.6,
                        porosity_default=0.15):
    """
    Full Tier 1 interpretation pipeline applied to all stations.

    Adds the following columns to the DataFrame:
      Physical:
        L_m               : sensitivity depth [m]
        nu_d              : drained Poisson ratio (from Vp/Vs if available)
        mu_Pa             : shear modulus [Pa]
        B_skempton        : Skempton B (empirical or from velocity)
        nu_u              : undrained Poisson ratio
        beta_ratio        : |β_u/β_d| = 1/(1-α_B·B)

      Drainage regime (from fitted elastic c = E3):
        c_elastic         : = elastic_c_m2s (already in df)
        omega_drain       : drainage frequency [rad/s]
        tau_drain_days    : drainage timescale [days]
        Pe_annual         : Péclet number at annual forcing
        drainage_class    : 'drained' | 'transitional' | 'undrained'

      Model interpretation:
        best_model        : model with highest R²
        best_r2           : R² of best model
        predicted_winner  : drainage-theory prediction of best model
        theory_match      : bool — does predicted_winner == best_model?
        mismatch_score    : coupling mismatch diagnostic [0–1]
        R2_gap            : R²(best) - R²(predicted model)

      Amplitude/stress:
        dvv_seasonal_amp_pct  : estimated seasonal dv/v amplitude [%]
        beta_est_Pa_inv       : estimated β [Pa⁻¹] (if load_Pa provided)
        mu_prime_est          : estimated μ' [dimensionless]

      Thermoelastic:
        thermo_dominance     : fraction of variance from thermoelastic term
        s_T_est_K_inv        : estimated thermoelastic sensitivity [K⁻¹]

    Parameters
    ----------
    df : pd.DataFrame  output of load_fit_summary()
    freq_hz : float  center measurement frequency [Hz]
    depth_rule : str  for sensitivity_depth()
    Vs_default : float [m/s]  fallback Vs if velocity profiles unavailable
    alpha_B_default : float  Biot coefficient default
    B_default : float  Skempton B default
    porosity_default : float  default porosity
    """
    df = df.copy()
    N = len(df)

    # ── Shear velocity at sensitivity depth ──────────────────────────────────
    if "vs_sens" not in df.columns:
        df["vs_sens"] = Vs_default
    Vs = df["vs_sens"].fillna(Vs_default).values

    if "vp_sens" not in df.columns:
        df["vp_sens"] = np.nan
    Vp = df["vp_sens"].values

    if "rho_sens" not in df.columns:
        df["rho_sens"] = np.nan
    rho = df["rho_sens"].values

    # ── Sensitivity depth ─────────────────────────────────────────────────────
    df["L_m"] = sensitivity_depth(Vs, freq_hz, rule=depth_rule)

    # ── Elastic moduli ────────────────────────────────────────────────────────
    rho_use = np.where(np.isnan(rho), 2200.0, rho)   # fallback density
    df["mu_Pa"] = shear_modulus(Vs, rho_use)

    has_vp = ~np.isnan(Vp)
    nu = np.full(N, 0.27)   # Clements & Denolle default
    nu[has_vp] = poisson_ratio(Vp[has_vp], Vs[has_vp])
    nu = np.clip(nu, 0.05, 0.49)
    df["nu_d"] = nu

    # ── Skempton B and undrained Poisson ratio ───────────────────────────────
    # Prefer porosity-based if available; else use default
    if "porosity" in df.columns:
        B = skempton_B_empirical(df["porosity"].fillna(porosity_default).values)
    else:
        B = np.full(N, B_default)
        # Heuristic: low Vs30 / basin sites get higher B
        if "vs30" in df.columns:
            vs30 = df["vs30"].fillna(Vs_default).values
            # Map Vs30 600→B=0.4, Vs30 200→B=0.85
            B = np.clip(0.85 - 0.45 * (vs30 - 200) / 400, 0.2, 0.95)
        elif "elev_m" in df.columns:
            elev = df["elev_m"].fillna(0).values
            # Low elevation (basin) → higher B
            B = np.clip(0.8 - 0.4 * np.minimum(elev, 1000) / 1000, 0.2, 0.9)

    df["B_skempton"] = B
    df["nu_u"] = undrained_poisson(nu, B, alpha_B=alpha_B_default)
    df["beta_ratio"] = beta_ratio_undrained_to_drained(alpha_B_default, B)

    # ── Drainage regime (Stage 1) ─────────────────────────────────────────────
    # Use elastic model c as the primary estimate of hydraulic diffusivity
    c_col = None
    for candidate in ["elastic_c_m2s", "c_elastic", "e3"]:
        if candidate in df.columns:
            c_col = candidate
            break
    if c_col is None:
        raise ValueError("Cannot find hydraulic diffusivity column. "
                         "Expected 'elastic_c_m2s' or 'E3' in fit summary.")

    c = df[c_col].values
    L = df["L_m"].values

    df["omega_drain_rad_s"] = drainage_frequency(c, L)
    df["tau_drain_days"]    = 1.0 / df["omega_drain_rad_s"] / 86400.0
    df["Pe_annual"]         = drainage_peclet(c, L, OMEGA_ANNUAL)
    drainage_labels, _ = classify_drainage(c, L)
    df["drainage_class"] = drainage_labels

    # ── Best model identification ─────────────────────────────────────────────
    r2_cols = {
        "elastic":    "r2_elastic",
        "drained":    "r2_drained",
        "fc":         "r2_fc",
        "cdm":        "r2_cdm",
        "ssw":        "r2_ssw",
    }
    # Keep only models that exist in df
    r2_cols = {k: v for k, v in r2_cols.items() if v in df.columns}

    if r2_cols:
        r2_matrix = df[[v for v in r2_cols.values()]].values
        best_idx = np.argmax(r2_matrix, axis=1)
        model_names = list(r2_cols.keys())
        df["best_model"] = [model_names[i] for i in best_idx]
        df["best_r2"]    = r2_matrix[np.arange(N), best_idx]

        # R² gap: best vs second-best
        r2_sorted = np.sort(r2_matrix, axis=1)[:, ::-1]
        df["r2_gap"] = r2_sorted[:, 0] - r2_sorted[:, 1]
    else:
        df["best_model"] = "unknown"
        df["best_r2"]    = np.nan
        df["r2_gap"]     = np.nan

    # ── Theory prediction vs observation ────────────────────────────────────
    predicted, R2_theory = drainage_model_prediction(df["Pe_annual"].values)
    df["predicted_winner"] = predicted
    df["R2_theory_expected"] = R2_theory

    def matches(best, predicted):
        # 'drained' prediction matches 'drained' or 'fc' model win
        # 'undrained' prediction matches 'elastic' or 'ssw' model win
        mapping = {
            "drained":     {"drained", "fc"},
            "undrained":   {"elastic", "ssw"},
            "transitional": set(),  # no clear prediction
        }
        return best in mapping.get(predicted, set())

    df["theory_match"] = [
        matches(b, p) for b, p in zip(df["best_model"], df["predicted_winner"])
    ]

    # ── Mismatch score (coupling diagnostic) ──────────────────────────────────
    r2_d = df.get("r2_drained", pd.Series(0.0, index=df.index)).fillna(0).values
    r2_e = df.get("r2_elastic", pd.Series(0.0, index=df.index)).fillna(0).values
    df["mismatch_score"] = coupling_mismatch_score(r2_d, r2_e, df["Pe_annual"].values)

    # ── Thermoelastic dominance ───────────────────────────────────────────────
    # R_T = thermo_amp² × var(T) / var(ypred) — not directly available from
    # parameters alone; approximate from relative amplitudes
    thermo_cols = {
        "elastic": ("elastic_hydro_amp", "elastic_thermo_amp"),
        "drained": ("drained_hydro_amp", "drained_thermo_amp"),
        "fc":      ("fc_hydro_amp",      "fc_thermo_amp"),
    }
    for model, (hcol, tcol) in thermo_cols.items():
        if hcol in df.columns and tcol in df.columns:
            h = df[hcol].fillna(0).abs().values
            t = df[tcol].fillna(0).abs().values
            total = h + t
            total = np.where(total == 0, 1, total)
            df[f"thermo_fraction_{model}"] = t / total

    # Use elastic model as primary
    if "thermo_fraction_elastic" in df.columns:
        df["thermo_dominance"] = df["thermo_fraction_elastic"]
    elif "thermo_fraction_drained" in df.columns:
        df["thermo_dominance"] = df["thermo_fraction_drained"]
    else:
        df["thermo_dominance"] = np.nan

    # ── SSW decay rate → equivalent c interpretation ──────────────────────────
    # SSW decay rate a [day⁻¹] → groundwater memory τ = 1/a days
    if "ssw_decay_rate" in df.columns:
        a = df["ssw_decay_rate"].values
        df["ssw_memory_days"] = np.where(a > 0, 1.0 / (a * 86400), np.nan)
        # Effective c from SSW: c_eff ≈ L² × a (matching SSW to drainage frequency)
        df["ssw_c_equivalent"] = L**2 * a / 86400   # m²/s

    # ── CDMk memory window interpretation ────────────────────────────────────
    if "cdm_k_days" in df.columns:
        k = df["cdm_k_days"].values
        # CDMk k maps loosely to a linear trend timescale → equivalent drainage
        # c_equiv from CDMk: c ~ L²/tau where tau = k/2 (half-memory)
        df["cdm_c_equivalent"] = 2 * L**2 / (np.maximum(k, 1) * 86400)

    return df


# ─────────────────────────────────────────────────────────────────────────────
# 4. Compute β from fitted amplitudes + load estimates
# ─────────────────────────────────────────────────────────────────────────────

def estimate_beta_per_site(df, precip_seasonal_mm=400.0,
                            rho_water=1000.0, g=9.81):
    """
    Estimate β [Pa⁻¹] per site from fitted hydrological amplitude.

    The fitted hydro_amp (p[2] in Julia, elastic_hydro_amp here) gives
    dv/v [%] per unit of normalized precipitation forcing.

    To convert to physical units we need the actual load in Pa:
        Δσ = ρ_w · g · Δh_water  where Δh = seasonal precip column [m]

    This is approximate — for a proper β you need the actual precipitation
    amplitude at each site, not a single California-wide mean.

    Parameters
    ----------
    df : pd.DataFrame  output of interpret_all_sites()
    precip_seasonal_mm : float
        Approximate seasonal precipitation amplitude [mm].
        Use per-site PRISM values if available.
    """
    df = df.copy()

    # Load in Pa from water column
    delta_load_Pa = rho_water * g * (precip_seasonal_mm / 1000.0)

    for model in ["elastic", "drained", "fc"]:
        amp_col = f"{model}_hydro_amp"
        if amp_col not in df.columns:
            continue
        # The amplitude is fitted against normalized (zero-mean, unit-std) forcing
        # So the actual dv/v amplitude ≈ amp × std(precip)
        # Without per-site std(precip) we use the load amplitude directly
        dvv_amp = df[amp_col].abs() * 100   # assume already in % / normalized unit
        beta_Pa, beta_GPa = zip(*[
            infer_beta_from_fit(a, delta_load_Pa)
            for a in dvv_amp.values
        ])
        df[f"beta_{model}_Pa_inv"] = beta_Pa
        df[f"beta_{model}_GPa_inv"] = beta_GPa

        # μ' from β
        if "mu_pa" in df.columns:
            mu = df["mu_pa"].values
            df[f"mu_prime_{model}"] = -2 * mu * np.array(beta_Pa)

    return df


# ─────────────────────────────────────────────────────────────────────────────
# 5. Summary statistics
# ─────────────────────────────────────────────────────────────────────────────

def drainage_regime_summary(df):
    """
    Print a summary table of drainage regime classification.
    """
    if "drainage_class" not in df.columns:
        raise ValueError("Run interpret_all_sites() first.")

    summary = df.groupby("drainage_class").agg(
        n_sites=("netsta", "count"),
        median_Pe=("Pe_annual", "median"),
        median_c=("elastic_c_m2s", "median"),
        median_tau_days=("tau_drain_days", "median"),
        mean_best_r2=("best_r2", "mean"),
        theory_match_frac=("theory_match", "mean"),
    ).round(3)

    print("\n=== Drainage Regime Summary ===")
    print(summary.to_string())
    return summary


def model_selection_table(df):
    """
    Cross-tabulation of drainage_class × best_model.
    """
    if "drainage_class" not in df.columns or "best_model" not in df.columns:
        raise ValueError("Run interpret_all_sites() first.")
    ct = pd.crosstab(df["drainage_class"], df["best_model"],
                     margins=True, margins_name="Total")
    print("\n=== Model Selection vs Drainage Regime ===")
    print(ct.to_string())
    return ct


def variance_decomposition(df):
    """
    Decompose unexplained variance into:
      (a) transitional-regime mismatch
      (b) thermoelastic dominance
      (c) true residual (noise / tectonic)
    """
    if "best_r2" not in df.columns:
        raise ValueError("Run interpret_all_sites() first.")

    df = df.copy()
    df["unexplained"] = 1.0 - df["best_r2"].clip(0, 1)

    # Fraction of unexplained variance at transitional sites
    is_trans = df["drainage_class"] == "transitional"
    frac_transitional = df.loc[is_trans, "unexplained"].mean()
    frac_drained      = df.loc[df["drainage_class"] == "drained",    "unexplained"].mean()
    frac_undrained    = df.loc[df["drainage_class"] == "undrained",  "unexplained"].mean()

    print("\n=== Variance Decomposition by Drainage Regime ===")
    print(f"  Drained sites:      mean unexplained R² = {frac_drained:.3f}")
    print(f"  Undrained sites:    mean unexplained R² = {frac_undrained:.3f}")
    print(f"  Transitional sites: mean unexplained R² = {frac_transitional:.3f}")
    print(f"\n  Transitional excess = {frac_transitional - frac_drained:.3f}")
    print(f"  (expected ~0 if pure drained/undrained only)")

    # Correlation of Pe with unexplained variance
    log_Pe = np.log10(df["Pe_annual"].clip(1e-4, 1e4))
    corr = df["unexplained"].corr(np.abs(log_Pe - 0))
    print(f"\n  Corr(|log Pe|, unexplained): {corr:.3f}")
    print("  (near-zero Pe=1 → high unexplained if coupling hypothesis is correct)")

    return {
        "mean_unexplained_drained":      frac_drained,
        "mean_unexplained_undrained":    frac_undrained,
        "mean_unexplained_transitional": frac_transitional,
        "cor_logPe_unexplained":         corr,
    }
