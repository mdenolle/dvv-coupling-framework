"""
poroelastic_framework.py
========================
Physical computations for Tier 1 poroelastic coupling reinterpretation of
Clements & Denolle (2023) California dv/v dataset.

All functions operate on numpy arrays or scalars.  No I/O.

References
----------
Fokker et al. (2021) Remote Sens. 13, 2684
Roeloffs (1988) Pure Appl. Geophys.
Clements & Denolle (2023) JGR Solid Earth 128, e2022JB025553
Ermert et al. (2023) Solid Earth 14, 529-549
"""

from typing import Union

import numpy as np
from scipy.special import erf, erfc

# Scalar or numpy-array numeric input.
ArrayLike = Union[float, np.ndarray]

# ─────────────────────────────────────────────────────────────────────────────
# Physical constants
# ─────────────────────────────────────────────────────────────────────────────

OMEGA_ANNUAL = 2 * np.pi / (365.25 * 86400)   # rad/s
OMEGA_DAILY  = 2 * np.pi / 86400               # rad/s
G_GRAV       = 9.81                            # m/s²
RHO_WATER    = 1000.0                          # kg/m³


# ─────────────────────────────────────────────────────────────────────────────
# 1. Sensitivity depth
# ─────────────────────────────────────────────────────────────────────────────

def sensitivity_depth(
    Vs_mps: ArrayLike,
    freq_hz: float,
    rule: str = "third_wavelength",
) -> ArrayLike:
    """
    Characteristic depth sampled by coda waves at a given frequency.

    Parameters
    ----------
    Vs_mps : float or array
        Shear-wave velocity at the surface / representative depth [m/s].
        For autocorrelation, use Vs at ~1/4 wavelength depth.
        For cross-correlation coda, use average Vs over sensitivity zone.
    freq_hz : float
        Center frequency of the measurement band [Hz].
    rule : str
        'third_wavelength'  → L = Vs / (3 f)   [default, Clements & Denolle]
        'half_wavelength'   → L = Vs / (2 f)   [surface wave half-space]
        'quarter_wavelength'→ L = Vs / (4 f)

    Returns
    -------
    L_m : float or array
        Sensitivity depth [m].
    """
    rules = {
        "third_wavelength":   1.0 / 3,
        "half_wavelength":    1.0 / 2,
        "quarter_wavelength": 1.0 / 4,
    }
    if rule not in rules:
        raise ValueError(f"rule must be one of {list(rules)}")
    return Vs_mps * rules[rule] / freq_hz


# ─────────────────────────────────────────────────────────────────────────────
# 2. Drainage timescale and regime classification
# ─────────────────────────────────────────────────────────────────────────────

def drainage_frequency(c_m2s: ArrayLike, L_m: ArrayLike) -> ArrayLike:
    """
    Characteristic drainage angular frequency ω_drain = c / L².

    Parameters
    ----------
    c_m2s : float or array
        Hydraulic diffusivity [m²/s].
    L_m : float or array
        Sensitivity depth [m].

    Returns
    -------
    omega_drain : float or array [rad/s]
    """
    return c_m2s / (L_m ** 2)


def drainage_peclet(
    c_m2s: ArrayLike,
    L_m: ArrayLike,
    omega_forcing: float | None = None,
) -> ArrayLike:
    """
    Dimensionless Péclet-like drainage number:
        Pe = ω_forcing / ω_drain = ω_forcing · L² / c

    Pe ≪ 1  → drained    (drainage fast relative to forcing)
    Pe ≈ 1  → transitional
    Pe ≫ 1  → undrained  (forcing fast relative to drainage)

    Default forcing = annual (ω_annual = 2π / (365.25 × 86400)).
    """
    if omega_forcing is None:
        omega_forcing = OMEGA_ANNUAL
    return omega_forcing * L_m**2 / c_m2s


def classify_drainage(
    c_m2s: ArrayLike,
    L_m: ArrayLike,
    omega_forcing: float | None = None,
    pe_drained: float = 0.1,
    pe_undrained: float = 10.0,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Classify each site as 'drained', 'transitional', or 'undrained'.

    Returns
    -------
    labels : array of str
    Pe     : array of float  (Péclet numbers)
    """
    Pe = drainage_peclet(c_m2s, L_m, omega_forcing)
    Pe = np.atleast_1d(np.asarray(Pe, dtype=float))
    labels = np.where(Pe < pe_drained, "drained",
              np.where(Pe > pe_undrained, "undrained", "transitional"))
    return labels, Pe


# ─────────────────────────────────────────────────────────────────────────────
# 3. Skempton & undrained Poisson ratio from Vp, Vs, density
# ─────────────────────────────────────────────────────────────────────────────

def poisson_ratio(Vp: ArrayLike, Vs: ArrayLike) -> ArrayLike:
    """Drained Poisson ratio from Vp and Vs."""
    r = (Vp / Vs) ** 2
    return (r - 2) / (2 * (r - 1))


def bulk_modulus(Vp: ArrayLike, Vs: ArrayLike, rho: ArrayLike) -> ArrayLike:
    """Undrained bulk modulus K [Pa] from seismic velocities."""
    return rho * (Vp**2 - 4.0 / 3.0 * Vs**2)


def shear_modulus(Vs: ArrayLike, rho: ArrayLike) -> ArrayLike:
    """Shear modulus μ [Pa]."""
    return rho * Vs**2


def skempton_B_from_velocities(Vp_dry, Vs_dry, rho_dry,
                                Vp_sat, Vs_sat, rho_sat):
    """
    Estimate Skempton's B coefficient from dry and saturated velocities
    using Gassmann's relations.

    B = ΔP / Δσ_mean|undrained = (K_sat - K_dry) / (K_sat + ΔK_f)

    Simplified form (after Roeloffs 1988):
        B ≈ (K_u - K_d) / (α_B · K_u)

    where α_B = 1 - K_d/K_grain (Biot coefficient).

    For a quick estimate without dry/sat pairs, use skempton_B_empirical().
    """
    K_dry = bulk_modulus(Vp_dry, Vs_dry, rho_dry)
    K_sat = bulk_modulus(Vp_sat, Vs_sat, rho_sat)
    mu_dry = shear_modulus(Vs_dry, rho_dry)
    # Gassmann: shear modulus unchanged → mu_sat ≈ mu_dry
    # Biot coefficient: α_B ≈ 1 - K_dry/K_grain
    # Assuming K_grain >> K_dry for unconsolidated sediment → α_B ≈ 1
    alpha_B = 1.0 - K_dry / K_sat   # approximate
    B = (K_sat - K_dry) / (alpha_B * K_sat)
    return np.clip(B, 0, 1), alpha_B


def skempton_B_empirical(porosity, lithology="mixed"):
    """
    Empirical Skempton B from porosity alone.

    Roeloffs (1988) Table 1 range:
      Soft sediment (φ > 0.3):     B ~ 0.8–0.99
      Consolidated rock (φ < 0.1): B ~ 0.2–0.5
      Mixed / intermediate:        B ~ 0.5–0.7

    Simple polynomial fit to Roeloffs data:
        B ≈ 1 - exp(-3.5 φ)   (approximate)
    """
    phi = np.atleast_1d(np.asarray(porosity, dtype=float))
    B = 1.0 - np.exp(-3.5 * phi)
    return np.clip(B, 0.1, 0.99)


def undrained_poisson(nu_d, B, alpha_B=1.0):
    """
    Undrained Poisson ratio ν_u from drained ν_d, Skempton B, Biot α_B.

    ν_u = (3ν_d + α_B B (1 - 2ν_d)) / (3 - α_B B (1 - 2ν_d))

    (Detournay & Cheng 1993; Roeloffs 1988)
    """
    x = alpha_B * B * (1 - 2 * nu_d)
    return (3 * nu_d + x) / (3 - x)


# ─────────────────────────────────────────────────────────────────────────────
# 4. Acoustoelastic sensitivity β and β_eff
# ─────────────────────────────────────────────────────────────────────────────

def beta_drained(mu_prime: ArrayLike, mu: ArrayLike) -> ArrayLike:
    """
    Drained stress sensitivity for isotropic effective-pressure changes [1/Pa].

    This is the stress-domain coefficient in

        δV_S / V_S = β_P · ΔP_eff,  β_P = -μ' / (2μ)

    where μ' = dμ/dP is the pressure derivative of shear modulus and μ is
    the shear modulus. It is distinct from the dimensionless strain-domain
    acoustoelastic parameter used in the manuscript,

        β_strain = -μ'κ / (2μ).

    Parameters
    ----------
    mu_prime : float
        Pressure sensitivity dμ/dP [dimensionless].
    mu : float [Pa]
        Shear modulus.

    Returns
    -------
    β_P [1/Pa]
    """
    return -mu_prime / (2 * mu)


def beta_eff(beta_d, alpha_B, B, omega, omega_drain):
    """
    Frequency-dependent effective acoustoelastic sensitivity β_eff(ω).

    In the drained limit  (ω ≪ ω_drain): κ → κ_d,  β_eff → β_d
    In the undrained limit (ω ≫ ω_drain): κ → κ_u = κ_d/(1 - α_B·B)
                                           β_eff → β_d / (1 - α_B·B)

    The transition is modeled as a smooth step (Biot characteristic frequency):

        β_eff(ω) = β_d · [(1 - f) + f / (1 - α_B·B)]
                where f(x) = x² / (1 + x²) [smooth Heaviside]

    Parameters
    ----------
    beta_d : float [1/Pa]
    alpha_B : float  Biot coefficient (0–1)
    B : float  Skempton B (0–1)
    omega : float [rad/s]  forcing angular frequency
    omega_drain : float [rad/s]  drainage angular frequency = c/L²

    Returns
    -------
    beta_eff_val : float [1/Pa]
    fraction_undrained : float (0=fully drained, 1=fully undrained)
    """
    coupling = alpha_B * B
    if np.any(np.asarray(coupling) >= 1.0):
        raise ValueError("alpha_B * B must be < 1 for a finite undrained modulus")

    x = omega / omega_drain
    # smooth logistic transition
    f = x**2 / (1 + x**2)
    beta_eff_val = beta_d * ((1.0 - f) + f / (1.0 - coupling))
    fraction_undrained = f
    return beta_eff_val, fraction_undrained


def beta_ratio_undrained_to_drained(alpha_B: ArrayLike, B: ArrayLike) -> ArrayLike:
    """
    Limiting ratio |β_u / β_d| = 1 / (1 - α_B · B).

    Range: ~1.3 (consolidated rock) to ~5 (soft sediment).
    """
    return 1.0 / (1.0 - alpha_B * B)


# ─────────────────────────────────────────────────────────────────────────────
# 5. Convert fitted model parameters to physical stress/strain
# ─────────────────────────────────────────────────────────────────────────────

def amplitude_to_stress(dvv_amplitude_pct, beta_Pa_inv):
    """
    Convert dv/v amplitude [%] to stress change [Pa] via:
        δv/v = β · Δσ_eff  →  Δσ = (δv/v) / β

    Parameters
    ----------
    dvv_amplitude_pct : float
        Peak-to-peak or RMS dv/v amplitude [%]
    beta_Pa_inv : float
        Acoustoelastic sensitivity [1/Pa]

    Returns
    -------
    delta_sigma_Pa : float [Pa]
    delta_sigma_kPa : float [kPa]
    """
    dvv_frac = dvv_amplitude_pct / 100.0
    delta_sigma_Pa = dvv_frac / beta_Pa_inv
    return delta_sigma_Pa, delta_sigma_Pa / 1e3


def fitted_c_to_physical(c_m2s, L_m, freq_center_hz):
    """
    Interpret the fitted hydraulic diffusivity c from Clements & Denolle
    in terms of drainage state and permeability.

    Parameters
    ----------
    c_m2s : float or array [m²/s]
        Fitted hydraulic diffusivity from elastic or drained model (E3/D3 column)
    L_m : float or array [m]
        Sensitivity depth
    freq_center_hz : float
        Center measurement frequency [Hz]

    Returns
    -------
    dict with:
        omega_drain   [rad/s]
        tau_drain     [days]  drainage timescale at sensitivity depth
        Pe_annual     [-]     Péclet number at annual forcing
        Pe_seasonal   [-]     Péclet number at 6-month forcing
        drainage_class ['drained'|'transitional'|'undrained']
    """
    c = np.atleast_1d(np.asarray(c_m2s, dtype=float))
    L = np.atleast_1d(np.asarray(L_m, dtype=float))

    omega_d = drainage_frequency(c, L)
    tau_drain_s = 1.0 / omega_d
    tau_drain_days = tau_drain_s / 86400.0

    Pe_annual   = drainage_peclet(c, L, OMEGA_ANNUAL)
    Pe_seasonal = drainage_peclet(c, L, 2 * OMEGA_ANNUAL)   # 6-month

    labels, _ = classify_drainage(c, L)

    return {
        "omega_drain_rad_s": omega_d,
        "tau_drain_days":    tau_drain_days,
        "Pe_annual":         Pe_annual,
        "Pe_seasonal":       Pe_seasonal,
        "drainage_class":    labels,
        "L_m":               L,
        "c_m2s":             c,
    }


# ─────────────────────────────────────────────────────────────────────────────
# 6. Infer β from fitted amplitude + elastic moduli
# ─────────────────────────────────────────────────────────────────────────────

def infer_beta_from_fit(dvv_amp_pct, delta_load_Pa, model="drained"):
    """
    Back-calculate β from a fitted dv/v amplitude and known load amplitude.

    β = (δv/v) / Δσ_eff

    Use this when you have:
      - The fitted hydro amplitude (p[2] in the Julia notation, scaled back)
      - An independent estimate of the load (e.g. from GRACE TWS or water table)

    Parameters
    ----------
    dvv_amp_pct : float  [%]
    delta_load_Pa : float  [Pa]  estimated stress/load change
    model : str  label for the coupling model (informational)

    Returns
    -------
    beta_Pa_inv : float [1/Pa]
    beta_GPa_inv : float [1/GPa]  (more convenient for reporting)
    """
    beta = (dvv_amp_pct / 100.0) / delta_load_Pa
    return beta, beta * 1e9


def infer_mu_prime(beta_Pa_inv, Vs_mps, rho_kgm3):
    """
    Infer the normalized pressure sensitivity μ' from β and elastic moduli.

    β = -μ' / (2μ)  →  μ' = -2μβ

    μ' is the dimensionless acoustoelastic constant (also written γ or ξ
    in other notations). Typical values:
        Consolidated rock:   μ' ~ 5–15
        Unconsolidated sed.: μ' ~ 20–100
        Soft soil/clay:      μ' ~ 50–200

    Returns
    -------
    mu_prime : float  [dimensionless]
    mu_Pa : float  [Pa]
    """
    mu_Pa = shear_modulus(Vs_mps, rho_kgm3)
    mu_prime = -2 * mu_Pa * beta_Pa_inv
    return mu_prime, mu_Pa


# ─────────────────────────────────────────────────────────────────────────────
# 7. Thermoelastic sensitivity
# ─────────────────────────────────────────────────────────────────────────────

def thermoelastic_sensitivity_s_T(nu, alpha_thermal, mu_prime_norm, Vs, rho):
    """
    Thermoelastic sensitivity s_T [K⁻¹], following Richter et al. (2014) / Ermert et al. (2023):

        s_T = 2b · α_th · (∂ρV²/∂σ_c)

    where b = (1+ν)/(1-ν) for S-waves. The input ``mu_prime_norm`` is the
    dimensionless derivative ∂(ρV²)/∂σ_c, not the shear modulus derivative
    multiplied by μ. Typical published values are about 50-1000.

    Parameters
    ----------
    nu : float  Poisson ratio (drained)
    alpha_thermal : float [K⁻¹]  linear thermal expansion coefficient
                                  (typical: 1e-5 to 3e-5 K⁻¹ for rock)
    mu_prime_norm : float  ∂(ρV²)/∂σ_c [dimensionless]
    Vs : float [m/s]
    rho : float [kg/m³]
        Retained for API compatibility; not used by this expression.

    Returns
    -------
    s_T : float [K⁻¹]
    """
    b = (1 + nu) / (1 - nu)
    d_rhoV2_d_sigma = mu_prime_norm
    return 2 * b * alpha_thermal * d_rhoV2_d_sigma


def thermoelastic_from_fitted_amplitude(dvv_amp_pct_per_K,
                                        nu, Vs, rho,
                                        alpha_thermal=1.5e-5):
    """
    Back-calculate ∂(ρV²)/∂σ_c from the fitted thermoelastic amplitude.

    The fitted p[4] in Clements & Denolle is in units of [% dv/v / normalized_T].
    To get s_T in K⁻¹, we need the actual temperature amplitude in K.

    This function infers the dimensionless stress sensitivity used in the
    Richter/Ermert thermoelastic formulation given s_T from fitting.

    Parameters
    ----------
    dvv_amp_pct_per_K : float  fitted s_T equivalent [%/K]
    nu, Vs, rho : elastic properties at sensitivity depth
    alpha_thermal : float [K⁻¹] (default 1.5e-5 for granite/gneiss)

    Returns
    -------
    d_rhoV2_d_sigma : float
    s_T : float [K⁻¹]
    """
    s_T = dvv_amp_pct_per_K / 100.0   # convert % to fraction
    b = (1 + nu) / (1 - nu)
    d_rhoV2_d_sigma = s_T / (2 * b * alpha_thermal)
    return d_rhoV2_d_sigma, s_T


# ─────────────────────────────────────────────────────────────────────────────
# 8. Model discrimination score
# ─────────────────────────────────────────────────────────────────────────────

def drainage_model_prediction(Pe):
    """
    Predict which Clements & Denolle model should win based on Pe.

    Returns
    -------
    predicted_winner : str
        'drained'     → Pe < 0.1    (D or FC model)
        'undrained'   → Pe > 10     (Elastic/SSW model)
        'transitional'→ 0.1 < Pe < 10 (FC or low R²)
    predicted_R2_expected : float
        Expected R² based on regime:
        - drained/undrained sites: high (>0.6) if model is correct
        - transitional sites: low (<0.4) because neither model fits
    """
    Pe = np.atleast_1d(np.asarray(Pe, dtype=float))
    winners = np.where(Pe < 0.1, "drained",
               np.where(Pe > 10.0, "undrained", "transitional"))
    # Expected R² decreases for transitional sites
    # Model: R²_expected = 0.7 - 0.3 * exp(-((log10(Pe))²)/2)
    log_Pe = np.log10(np.clip(Pe, 1e-6, 1e6))
    R2_expected = 0.7 - 0.3 * np.exp(-(log_Pe**2) / 2.0)
    return winners, R2_expected


def coupling_mismatch_score(r2_drained, r2_undrained, Pe):
    """
    Score how much of the unexplained variance is attributable to
    being in the transitional drainage regime.

    A site perfectly in transition (Pe=1) that is fit by either pure model
    will show R² ~ 0 even if the physics is perfect — the mismatch between
    the model and the actual β_eff(ω) causes systematic residuals.

    Returns
    -------
    mismatch : float (0=no mismatch, 1=maximum mismatch)
        Based on how close Pe is to 1 (transition) weighted by how much
        variance is unexplained.
    """
    Pe = np.atleast_1d(Pe)
    r2_best = np.maximum(r2_drained, r2_undrained)
    unexplained = 1.0 - r2_best
    # Transition weight: peaks at Pe=1, zero at extremes
    log_Pe = np.log10(np.clip(Pe, 1e-6, 1e6))
    transition_weight = np.exp(-(log_Pe**2) / 2.0)
    return unexplained * transition_weight


# ─────────────────────────────────────────────────────────────────────────────
# 9. Geospatial property requirements
# ─────────────────────────────────────────────────────────────────────────────

GEOSPATIAL_REQUIREMENTS = """
GEOSPATIAL PROPERTIES NEEDED PER STATION
==========================================

From seismic velocity model (you can provide Vp, Vs, density profiles):
  • Vs_surface  [m/s]   → sensitivity depth L = Vs / (3f)
  • Vp_surface  [m/s]   → drained Poisson ratio ν
  • rho_surface [kg/m³] → elastic moduli K, μ
  • Vs_gradient [m/s/m] → depth of sensitivity zone
  → Compute: μ, ν, L, β_d estimate

From geology / geospatial databases (QUERY LIST):
  1. SURFICIAL GEOLOGY
     Source: USGS Quaternary Fault database / California GEMS geology
     Variables:
       • rock_type: sediment | volcanic | metamorphic | plutonic | carbonate
       • sediment_thickness_m: basin fill thickness (key for β and B)
       • age_MY: geologic age → proxy for consolidation
     Rationale: Controls porosity φ, Biot B, drainage regime expected

  2. POROSITY / PERMEABILITY PROXIES
     Source: USGS GLHYMPS (global hydrogeology), SSURGO (soils)
     Variables:
       • permeability_log10_m2: log10 intrinsic permeability
       • porosity_frac: effective porosity
       • hydraulic_conductivity_m_s: K_h (use to cross-check fitted c)
     Rationale: c = k·K_drain/(μ_f·S_s) → allows independent estimate
     of drainage Péclet number to validate Stage 1

  3. WATER TABLE DEPTH
     Source: Fan et al. (2013) global WTD / USGS NWIS groundwater wells
     Variables:
       • wtd_mean_m: mean depth to water table [m]
       • wtd_seasonal_amplitude_m: seasonal ΔWT
     Rationale: Sites with shallow WTD (< L) are poroelastic-dominant;
     deep WTD sites may be thermoelastic-dominant → explains R_T map

  4. TOPOGRAPHIC STRESS
     Source: SRTM 30m DEM → local slope, curvature, hillshade
     Variables:
       • elevation_m: absolute elevation
       • local_relief_500m: topographic relief at 500 m radius
       • drainage_basin_area_km2: upstream catchment
       • slope_deg: local slope
     Rationale: Mountain sites have high c (fast drainage), high relief
     → drained regime. Basin sites have low c → undrained regime.
     Also controls thermoelastic amplitude (surface vs subsurface T).

  5. SEDIMENT THICKNESS / BASIN DEPTH
     Source: USGS National Crustal Model / Vs30 maps
     Variables:
       • Vs30_m_s: time-averaged Vs to 30m (USGS ShakeMap / CGS)
       • basin_depth_1km_m: depth to Vs=1 km/s interface
       • basin_depth_2p5km_m: depth to Vs=2.5 km/s (basin Z2.5)
     Rationale: Vs30 and basin depth directly encode the near-surface
     compliance that sets β magnitude and the sensitivity depth L.
     LOW Vs30 → deep sensitivity → more undrained-like behavior.

  6. FAULT PROXIMITY & TECTONIC SETTING
     Source: USGS Quaternary Faults, SCEC Community Fault Model
     Variables:
       • dist_to_fault_km: distance to nearest active fault
       • fault_style: strike-slip | thrust | normal
       • last_rupture_yr: for post-seismic masking
     Rationale: Near-fault sites have damage-related high β (Tier 2);
     masking post-seismic transients is needed before hydro interpretation.

  7. CLIMATE / SEASONALITY
     Source: PRISM (already loaded) + TerraClimate / Daymet
     Variables:
       • MAP_mm: mean annual precipitation
       • MAT_C: mean annual temperature
       • aridity_index: PET/P ratio (Budyko)
       • snow_fraction: fraction of precip as snow (delayed melt)
     Rationale: High snow fraction → spring-dominated loading → phase lag
     in fitted t_shift inconsistent with purely thermoelastic model.

  8. LAND COVER / IRRIGATION
     Source: NLCD 2019 / USDA NASS cropland data
     Variables:
       • land_cover_class: forest|shrub|grass|crop|urban|water
       • irrigation_intensity: irrigated area fraction within 10 km
     Rationale: Irrigated agriculture is a dominant anthropogenic
     hydrological signal in California. Explains anomalous SSW model
     performance in Central Valley sites (CI.RXH, CI.SAL etc.)

PRIORITY ORDER FOR ACQUISITION
================================
Tier A (essential for Stage 1):
  Vs30, basin_depth_1km, sediment_thickness, Vs_profile (you have)

Tier B (essential for Stage 2):
  porosity or permeability proxy, water table depth, rock_type

Tier C (important for Stage 3 interpretation):
  irrigation, snow fraction, fault proximity, aridity index

API SOURCES (Python-accessible):
  Vs30    → https://earthquake.usgs.gov/ws/designmaps/ (WMS)
  GLHYMPS → https://dataverse.scholarsportal.info/dataset.xhtml?persistentId=doi:10.5683/SP2/TTJNIU
  WTD     → Fan et al. 2013 netCDF (download once)
  DEM     → earthengine-api or elevation.mapzen.com
  Geology → USGS ScienceBase
"""


def print_geospatial_requirements():
    print(GEOSPATIAL_REQUIREMENTS)
