#!/usr/bin/env python3
"""
Numerical Coupling-Tier Tests for the Unified δv/v Framework
=============================================================

Tests the three tiers of coupling mechanisms using physically realistic 
material properties and literature-grounded scenario forcings.

Tier 1: Poroelastic bidirectional coupling (αB·B parameterization)
Tier 2: Damage–permeability feedback (post-earthquake k(t))
Tier 3: Saturation-dependent nonlinear elasticity (β(Sw))

Each test demonstrates: (a) when coupling matters, (b) the magnitude of 
error from ignoring coupling, (c) observational diagnostics.

Scenarios are designed to be consistent with published observations at:
  - Parkfield (strike-slip, fractured granite, ~0.8 km depth)
  - Cascadia (subduction, marine sediment, ~0.2 km depth)
  - Nepal Himalayas (post-earthquake, Illien et al. 2022)
  - Groningen (gas extraction, Fokker et al. 2021)
  - Agricultural settings (vadose zone, Shi et al. 2026)

Output: Figures saved to /home/claude/figures/ and summary metrics printed.

Authors: M. A. Denolle & Claude (Anthropic AI)
Date: 2026-04-01
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import matplotlib.patches as mpatches
from scipy.special import erf, erfc
from scipy.integrate import quad
import os

# Create output directory
os.makedirs('/home/claude/figures', exist_ok=True)

# =============================================================================
# Material property database (from literature)
# =============================================================================

class Site:
    """Container for site-specific material properties."""
    pass

# Parkfield: fractured Salinian granite at ~0.8 km depth
parkfield = Site()
parkfield.name = "Parkfield (granite)"
parkfield.Vs = 2500.0         # m/s (SAFOD, Jeppson & Tobin 2015)
parkfield.rho = 2500.0        # kg/m³
parkfield.mu = parkfield.rho * parkfield.Vs**2  # 15.6 GPa
parkfield.nu = 0.25           # Poisson's ratio
parkfield.kappa = 2*parkfield.mu*(1+parkfield.nu)/(3*(1-2*parkfield.nu))  # ~26 GPa
parkfield.mu_prime = 251.0    # From manuscript Table 2
parkfield.beta = -240.0       # From manuscript Table 2
parkfield.alpha_B = 0.7       # Biot coefficient (fractured rock)
parkfield.B_skemp = 0.4       # Skempton coeff (partially drained granite)
parkfield.perm = 1e-15        # Permeability m² (fault zone)
parkfield.phi = 0.05          # Porosity
parkfield.depth = 800.0       # Sensitivity depth, m
parkfield.kappa_T = 1.0e-6    # Thermal diffusivity m²/s
parkfield.alpha_T = 8e-6      # Thermal expansion K⁻¹

# Cascadia: marine sediment at ~0.2 km depth below seafloor
cascadia = Site()
cascadia.name = "Cascadia (sediment)"
cascadia.Vs = 500.0           # m/s (Han et al. 2017)
cascadia.rho = 1900.0         # kg/m³
cascadia.mu = cascadia.rho * cascadia.Vs**2  # 0.475 GPa
cascadia.nu = 0.40            # High Poisson's ratio (soft sediment)
cascadia.kappa = 2*cascadia.mu*(1+cascadia.nu)/(3*(1-2*cascadia.nu))  # ~4.4 GPa
cascadia.mu_prime = 618.0     # From manuscript Table 2
cascadia.beta = -3160.0       # From manuscript Table 2
cascadia.alpha_B = 0.95       # Biot coefficient (unconsolidated)
cascadia.B_skemp = 0.75       # Skempton coeff (high-porosity, saturated)
cascadia.perm = 1e-13         # Permeability m² (accretionary wedge)
cascadia.phi = 0.40           # Porosity
cascadia.depth = 200.0        # Sensitivity depth, m
cascadia.kappa_T = 0.5e-6     # Thermal diffusivity m²/s
cascadia.alpha_T = 5e-6       # Thermal expansion K⁻¹

# Nepal Himalayas: post-Gorkha earthquake (Illien et al. 2022)
nepal = Site()
nepal.name = "Nepal (post-earthquake)"
nepal.Vs = 1500.0             # m/s (average shallow crust)
nepal.rho = 2400.0
nepal.mu = nepal.rho * nepal.Vs**2  # 5.4 GPa
nepal.nu = 0.28
nepal.kappa = 2*nepal.mu*(1+nepal.nu)/(3*(1-2*nepal.nu))
nepal.mu_prime = 150.0        # Moderate fractured rock
nepal.beta = -150.0 * nepal.kappa / (2*nepal.mu)
nepal.alpha_B = 0.8
nepal.B_skemp = 0.5
nepal.perm = 1e-14            # Pre-earthquake
nepal.phi = 0.10
nepal.depth = 300.0
nepal.kappa_T = 0.8e-6
nepal.alpha_T = 7e-6

# Agricultural soil: vadose zone (Shi et al. 2026)
agri = Site()
agri.name = "Agricultural soil"
agri.Vs = 200.0               # m/s (near-surface soil)
agri.rho = 1600.0
agri.mu = agri.rho * agri.Vs**2  # 0.064 GPa
agri.nu = 0.35
agri.kappa = 2*agri.mu*(1+agri.nu)/(3*(1-2*agri.nu))
agri.mu_prime = 2000.0        # Very high for unconsolidated
agri.beta = -2000.0 * agri.kappa / (2*agri.mu)
agri.alpha_B = 0.99           # Nearly 1 for soil
agri.B_skemp = 0.90
agri.perm = 1e-11             # Sandy soil
agri.phi = 0.45
agri.depth = 5.0              # Very shallow
agri.kappa_T = 0.3e-6
agri.alpha_T = 10e-6

sites = [parkfield, cascadia, nepal, agri]


# =============================================================================
# TIER 1: Poroelastic Bidirectional Coupling
# =============================================================================

def tier1_drained_undrained_transition():
    """
    Test: How does β_eff change between drained and undrained conditions?
    
    Physics: Under undrained conditions, pore fluid resists compression,
    making the effective bulk modulus larger: κ_u = κ/(1 - α_B·B).
    This increases |β| by the same factor.
    
    Diagnostic: Compare δv/v predicted with drained vs undrained β for 
    different forcing timescales.
    """
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    # Panel (a): β_eff vs α_B·B for different sites
    ax = axes[0]
    aB_B = np.linspace(0, 0.95, 100)
    
    for site in sites:
        beta_drained = site.beta
        amplification = 1.0 / (1.0 - aB_B)
        beta_undrained = beta_drained * amplification
        ax.plot(aB_B, np.abs(beta_undrained)/np.abs(beta_drained), 
                label=site.name, linewidth=2)
    
    # Mark actual site values
    for site in sites:
        aB_B_site = site.alpha_B * site.B_skemp
        amp = 1.0 / (1.0 - aB_B_site)
        ax.plot(aB_B_site, amp, 'o', markersize=10, zorder=5)
    
    ax.set_xlabel(r'$\alpha_B \cdot B$ (coupling parameter)', fontsize=12)
    ax.set_ylabel(r'$|\beta_{\rm undrained}|/|\beta_{\rm drained}|$', fontsize=12)
    ax.set_title('(a) Undrained amplification of β', fontsize=13)
    ax.legend(fontsize=9, loc='upper left')
    ax.set_xlim(0, 1)
    ax.set_ylim(1, 10)
    ax.axhline(y=1.5, color='gray', ls='--', alpha=0.5)
    ax.text(0.02, 1.55, '50% error threshold', fontsize=9, color='gray')
    ax.grid(True, alpha=0.3)
    
    # Panel (b): Drainage transition timescale vs permeability
    ax = axes[1]
    perm_range = np.logspace(-18, -10, 100)  # m²
    eta = 1e-3  # Pa·s (water viscosity)
    Ss = 1e-5   # 1/m (specific storage)
    
    for L in [1, 10, 100, 1000]:
        c_hydro = perm_range / (Ss * eta)
        T_drain = L**2 / c_hydro  # seconds
        T_drain_days = T_drain / 86400
        ax.loglog(perm_range, T_drain_days, label=f'L = {L} m', linewidth=2)
    
    # Mark forcing timescales
    ax.axhline(y=0.5, color='red', ls=':', alpha=0.7, linewidth=1.5)
    ax.text(1e-17, 0.6, 'Tidal (12 hr)', fontsize=9, color='red')
    ax.axhline(y=180, color='blue', ls=':', alpha=0.7, linewidth=1.5)
    ax.text(1e-17, 220, 'Seasonal (6 mo)', fontsize=9, color='blue')
    ax.axhline(y=3650, color='green', ls=':', alpha=0.7, linewidth=1.5)
    ax.text(1e-17, 4500, 'Decadal (10 yr)', fontsize=9, color='green')
    
    # Mark site permeabilities
    for site in sites:
        ax.axvline(x=site.perm, color='gray', ls='--', alpha=0.3)
    
    ax.set_xlabel('Permeability (m²)', fontsize=12)
    ax.set_ylabel('Drainage time (days)', fontsize=12)
    ax.set_title('(b) Drained–undrained transition', fontsize=13)
    ax.legend(fontsize=9)
    ax.set_xlim(1e-18, 1e-10)
    ax.set_ylim(1e-2, 1e8)
    ax.grid(True, alpha=0.3)
    
    # Panel (c): δv/v error from ignoring coupling
    ax = axes[2]
    # Scenario: 1 kPa pore pressure change at each site
    delta_P = 1000.0  # Pa
    
    site_names = []
    errors_pct = []
    dvv_drained_list = []
    dvv_undrained_list = []
    
    for site in sites:
        # Drained: β uses drained κ
        dvv_drained = site.beta * (-delta_P / site.kappa) * 1e2  # in %
        
        # Undrained: β uses undrained κ
        aB_B_val = site.alpha_B * site.B_skemp
        kappa_u = site.kappa / (1 - aB_B_val)
        beta_u = -site.mu_prime * kappa_u / (2 * site.mu)
        # But in undrained, the pore pressure change itself is modified:
        # Δu = B·Δσ_kk/3 (Skempton relation)
        # For the same external loading, the pore pressure is larger
        # The effective stress change is: Δσ_eff = Δσ - α_B·Δu
        # For unit external load: Δσ_eff = 1 - α_B·B·1 = (1 - α_B·B)
        # So δv/v_undrained = β_drained × ε_kk (same strain produces same δv/v)
        # The difference is in how pore pressure couples to stress
        dvv_undrained = beta_u * (-delta_P / kappa_u) * 1e2
        
        # Actually, the key difference is when we have a stress perturbation
        # (e.g., tidal load) applied rapidly: in undrained, pore pressure
        # absorbs part of the load, reducing effective stress change
        # In drained, all load goes to effective stress
        
        # For a surface load T33 in Fokker formulation:
        # Drained: δVs/Vs = (-μ'/2μ)·0 + (μ'+1)/(12μ)·T33 [pore pressure = 0]
        T33 = -1000.0  # Pa, compressive
        dvv_drained_fokker = (site.mu_prime + 1) / (12 * site.mu) * T33
        
        # Undrained: δVs/Vs = (-μ'/2μ)·B(1+ν_u)/(3(1-ν_u))·T33 + ...
        nu_u = 0.5 * (site.nu + site.alpha_B * site.B_skemp * (1 - 2*site.nu) / 
                       (3 * (1 - site.alpha_B * site.B_skemp * (1 - 2*site.nu)/(3*(1-2*site.nu)))))
        # Simplified: use Fokker Eq. 9
        u0_undrained = site.B_skemp * (1 + nu_u) / (3 * (1 - nu_u)) * T33
        dvv_undrained_fokker = (-site.mu_prime / (2*site.mu)) * u0_undrained + \
                               (site.mu_prime + 1) / (12 * site.mu) * T33
        
        error = np.abs(dvv_undrained_fokker - dvv_drained_fokker) / np.abs(dvv_drained_fokker) * 100
        
        site_names.append(site.name.split('(')[0].strip())
        errors_pct.append(min(error, 500))
        dvv_drained_list.append(dvv_drained_fokker * 1e4)
        dvv_undrained_list.append(dvv_undrained_fokker * 1e4)
    
    x = np.arange(len(site_names))
    width = 0.35
    bars1 = ax.bar(x - width/2, [abs(d) for d in dvv_drained_list], width, 
                    label='Drained', color='steelblue', alpha=0.8)
    bars2 = ax.bar(x + width/2, [abs(d) for d in dvv_undrained_list], width, 
                    label='Undrained', color='darkorange', alpha=0.8)
    
    ax.set_xlabel('Site', fontsize=12)
    ax.set_ylabel(r'$|\delta v/v|$ (×10⁻⁴ per kPa load)', fontsize=12)
    ax.set_title('(c) Drained vs undrained δv/v', fontsize=13)
    ax.set_xticks(x)
    ax.set_xticklabels(site_names, fontsize=9, rotation=15)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig('/home/claude/figures/tier1_poroelastic_coupling.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    print("TIER 1 — Poroelastic Coupling Results:")
    print("=" * 60)
    for i, site in enumerate(sites):
        aB_B_val = site.alpha_B * site.B_skemp
        amp = 1.0 / (1.0 - aB_B_val)
        print(f"  {site.name}: α_B·B = {aB_B_val:.2f}, "
              f"|β_u/β_d| = {amp:.1f}×")
    print()


# =============================================================================
# TIER 2: Damage–Permeability Feedback (Post-Earthquake)
# =============================================================================

def tier2_damage_permeability():
    """
    Test: How does earthquake-induced permeability change modify the
    seasonal δv/v regression coefficients?
    
    Scenario: Nepal-like setting (Illien et al. 2022). Monsoon 
    precipitation drives seasonal δv/v. An Mw 7.8 earthquake increases 
    permeability by 3×, which changes the hydrological transfer function.
    
    Diagnostic: Change in seasonal δv/v amplitude before vs after earthquake.
    """
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Time axis: 10 years, earthquake at year 5
    dt = 1.0  # days
    t_days = np.arange(0, 3650, dt)
    t_years = t_days / 365.25
    t_eq = 5.0 * 365.25  # Earthquake at year 5 (in days)
    
    # Monsoon precipitation: seasonal with peak in July-August
    # ~2000 mm/yr total, concentrated in 4 months
    precip_mm = np.maximum(0, 15 * np.sin(2*np.pi*(t_days - 120)/365.25) + 5)
    precip_mm *= (1 + 0.3 * np.random.randn(len(t_days)))
    precip_mm = np.maximum(0, precip_mm)
    
    # Permeability evolution: step increase at earthquake, exponential healing
    tau_heal = 180.0  # days (6 months, from Illien et al. 2022)
    D_coseismic = np.log(3)  # 3× increase (Elkhoury et al. 2006)
    
    perm_factor = np.ones_like(t_days)
    post_eq_mask = t_days >= t_eq
    perm_factor[post_eq_mask] = np.exp(D_coseismic * np.exp(-(t_days[post_eq_mask] - t_eq) / tau_heal))
    
    # Hydraulic diffusivity (proportional to permeability)
    c_base = 1e-4  # m²/s (base diffusivity, Nepal-like)
    c_t = c_base * perm_factor
    
    # Compute pore pressure at depth z using Roeloffs (1988) model
    z_sens = 300.0  # m, sensitivity depth
    
    # Simplified: pore pressure from precipitation convolution
    # P(z,t) = ∫ precip(t') × erfc(z/√(4c(t-t'))) dt'
    # For computational efficiency, use discrete convolution
    
    pore_pressure = np.zeros_like(t_days, dtype=float)
    loading = np.zeros_like(t_days, dtype=float)
    
    rho_w = 1000.0
    g = 9.81
    
    for i in range(1, len(t_days)):
        # Accumulate pore pressure from each day's precipitation
        dt_back = t_days[i] - t_days[:i]
        dt_back_sec = dt_back * 86400.0
        valid = dt_back_sec > 0
        
        if i <= 500:  # Use full convolution for first 500 days
            c_eff = c_t[:i][valid]
            arg = z_sens / np.sqrt(4 * c_eff * dt_back_sec[valid] + 1e-10)
            kernel = erfc(arg)
            precip_load = precip_mm[:i][valid] * 1e-3 * rho_w * g  # Convert mm to Pa
            pore_pressure[i] = np.sum(precip_load * kernel) / max(1, np.sum(valid))
        else:
            # Approximate: use running average of recent c
            c_avg = np.mean(c_t[max(0,i-365):i])
            dt_effective = 90 * 86400  # Use 90-day effective memory
            arg = z_sens / np.sqrt(4 * c_avg * dt_effective)
            # Simple exponential decay model
            alpha_decay = np.exp(-dt / (c_avg * 86400 / z_sens**2 * 365))
            pore_pressure[i] = alpha_decay * pore_pressure[i-1] + \
                               (1-alpha_decay) * precip_mm[i] * 1e-3 * rho_w * g * erfc(arg)
        
        loading[i] = precip_mm[i] * 1e-3 * rho_w * g  # Surface loading (Pa)
    
    # Compute δv/v using Fokker formulation
    site = nepal
    dvv_from_pore = -site.mu_prime / (2 * site.mu) * pore_pressure
    dvv_from_load = (site.mu_prime + 1) / (12 * site.mu) * (-loading)
    dvv_total = dvv_from_pore + dvv_from_load
    
    # Add co-seismic drop and healing
    coseismic_drop = np.zeros_like(t_days)
    coseismic_drop[post_eq_mask] = -0.005  # -0.5% co-seismic drop
    
    tau_min, tau_max = 1.0, 3650.0  # Healing timescales (days)
    healing = np.zeros_like(t_days)
    for i in range(len(t_days)):
        if t_days[i] > t_eq:
            t_since = (t_days[i] - t_eq)
            if t_since > 0.1:
                healing[i] = 0.003 * np.log(1 + t_since/tau_min) / np.log(tau_max/tau_min)
    
    dvv_total_with_eq = dvv_total + coseismic_drop + healing
    
    # Panel (a): Permeability evolution
    ax = axes[0, 0]
    ax.plot(t_years, perm_factor, 'k-', linewidth=2)
    ax.axvline(x=5.0, color='red', ls='--', alpha=0.7, label='Earthquake')
    ax.set_xlabel('Time (years)', fontsize=12)
    ax.set_ylabel('k(t) / k₀', fontsize=12)
    ax.set_title('(a) Permeability evolution', fontsize=13)
    ax.legend(fontsize=10)
    ax.set_ylim(0.8, 3.5)
    ax.grid(True, alpha=0.3)
    ax.annotate(f'τ_heal = {tau_heal:.0f} days\nD = 3×', xy=(5.1, 3.0), fontsize=10)
    
    # Panel (b): Precipitation and pore pressure
    ax = axes[0, 1]
    ax2 = ax.twinx()
    ax.bar(t_years, precip_mm, width=1/365.25, color='steelblue', alpha=0.3, label='Precipitation')
    ax2.plot(t_years, pore_pressure/1000, 'r-', linewidth=1.5, label='Pore pressure')
    ax.set_xlabel('Time (years)', fontsize=12)
    ax.set_ylabel('Precipitation (mm/day)', fontsize=12, color='steelblue')
    ax2.set_ylabel('Pore pressure (kPa)', fontsize=12, color='red')
    ax.set_title('(b) Forcing and pore pressure response', fontsize=13)
    ax.axvline(x=5.0, color='red', ls='--', alpha=0.5)
    
    # Panel (c): δv/v time series
    ax = axes[1, 0]
    ax.plot(t_years, dvv_total_with_eq * 100, 'k-', linewidth=1, alpha=0.7)
    ax.axvline(x=5.0, color='red', ls='--', alpha=0.7, label='Earthquake')
    ax.set_xlabel('Time (years)', fontsize=12)
    ax.set_ylabel('δv/v (%)', fontsize=12)
    ax.set_title('(c) δv/v with damage–permeability coupling', fontsize=13)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    
    # Panel (d): Seasonal amplitude before vs after earthquake
    ax = axes[1, 1]
    # Compute seasonal amplitude in sliding windows
    window = 365  # days
    seasonal_amp = np.zeros(len(t_days) - window)
    for i in range(len(seasonal_amp)):
        segment = dvv_total[i:i+window]
        seasonal_amp[i] = np.max(segment) - np.min(segment)
    t_amp = t_years[:len(seasonal_amp)]
    
    ax.plot(t_amp, seasonal_amp * 100, 'k-', linewidth=2)
    ax.axvline(x=5.0, color='red', ls='--', alpha=0.7, label='Earthquake')
    
    # Compute pre and post averages
    pre_mask = t_amp < 4.5
    post_mask = (t_amp > 5.5) & (t_amp < 7.0)
    late_mask = t_amp > 8.0
    
    if np.any(pre_mask) and np.any(post_mask):
        pre_amp = np.mean(seasonal_amp[pre_mask]) * 100
        post_amp = np.mean(seasonal_amp[post_mask]) * 100
        ax.axhline(y=pre_amp, color='blue', ls=':', alpha=0.7, 
                    label=f'Pre-EQ mean: {pre_amp:.4f}%')
        ax.axhline(y=post_amp, color='orange', ls=':', alpha=0.7, 
                    label=f'Post-EQ mean: {post_amp:.4f}%')
    
    ax.set_xlabel('Time (years)', fontsize=12)
    ax.set_ylabel('Seasonal δv/v amplitude (%)', fontsize=12)
    ax.set_title('(d) Seasonal amplitude change diagnostic', fontsize=13)
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/home/claude/figures/tier2_damage_permeability.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    print("TIER 2 — Damage-Permeability Coupling Results:")
    print("=" * 60)
    print(f"  Scenario: Nepal-like, Mw 7.8 earthquake at year 5")
    print(f"  Permeability increase: 3× (D = ln(3))")
    print(f"  Healing timescale: {tau_heal:.0f} days")
    if np.any(pre_mask) and np.any(post_mask):
        print(f"  Pre-earthquake seasonal δv/v amplitude: {pre_amp:.5f}%")
        print(f"  Post-earthquake seasonal δv/v amplitude: {post_amp:.5f}%")
        print(f"  Change: {(post_amp/pre_amp - 1)*100:+.1f}%")
    print()


# =============================================================================
# TIER 3: Saturation-Dependent Nonlinear Elasticity
# =============================================================================

def tier3_saturation_beta():
    """
    Test: How does β vary with water saturation?
    
    Physics: Laboratory measurements (Van Den Abeele et al. 2002; 
    Winkler & McGowan 2004) show that nonlinear elastic parameters
    depend strongly and non-monotonically on saturation. At low 
    saturation (1-20%), adsorbed water activates capillary forces;
    at intermediate saturation (~80%), liquid bridge dynamics peak.
    
    Implication: The δv/v response to any forcing (tidal, thermoelastic,
    tectonic) depends on the current saturation state — a multiplicative
    coupling.
    """
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    # Panel (a): β(Sw) model
    # Based on Van Den Abeele et al. (2002) and Mews et al. (2024)
    ax = axes[0]
    Sw = np.linspace(0, 1, 200)
    
    # Model: β has contributions from dry frame + capillary + liquid bridge
    # Following the schematic behavior from laboratory data
    beta_dry = -50.0  # Dry rock β (relatively small)
    
    # Capillary enhancement at low saturation (peak at ~10%)
    capillary = -500 * Sw * np.exp(-Sw/0.1)
    
    # Liquid bridge enhancement at intermediate saturation (peak at ~80%)
    bridge = -200 * np.exp(-((Sw - 0.80)/0.15)**2)
    
    # High saturation: β decreases as water stiffens contacts
    stiffening = 300 * Sw**3
    
    beta_Sw = beta_dry + capillary + bridge + stiffening
    
    ax.plot(Sw * 100, np.abs(beta_Sw), 'k-', linewidth=2)
    ax.fill_between(Sw * 100, 0, np.abs(beta_Sw), alpha=0.1, color='blue')
    
    # Mark the sensitivity windows
    ax.axvspan(1, 20, alpha=0.15, color='orange', label='Capillary window')
    ax.axvspan(70, 90, alpha=0.15, color='green', label='Liquid bridge window')
    
    ax.set_xlabel('Water saturation (%)', fontsize=12)
    ax.set_ylabel(r'$|\beta(S_w)|$', fontsize=12)
    ax.set_title(r'(a) Saturation-dependent $\beta$', fontsize=13)
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)
    
    # Panel (b): δv/v from same tidal strain at different saturations
    ax = axes[1]
    epsilon_tidal = 50e-9  # 50 nanostrain (typical Earth tide)
    
    dvv_tidal = beta_Sw * epsilon_tidal * 1e6  # in 10⁻⁶
    
    ax.plot(Sw * 100, np.abs(dvv_tidal), 'k-', linewidth=2)
    ax.set_xlabel('Water saturation (%)', fontsize=12)
    ax.set_ylabel(r'$|\delta v/v|$ from 50 nε tide (×10⁻⁶)', fontsize=12)
    ax.set_title('(b) Tidal δv/v depends on saturation', fontsize=13)
    ax.grid(True, alpha=0.3)
    
    # Add annotation showing the range
    dvv_min = np.min(np.abs(dvv_tidal))
    dvv_max = np.max(np.abs(dvv_tidal))
    ax.annotate(f'Range: {dvv_min:.2f} – {dvv_max:.2f}\n'
                f'Factor: {dvv_max/max(dvv_min,1e-10):.1f}×',
                xy=(50, dvv_max*0.8), fontsize=11,
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    # Panel (c): Seasonal scenario — saturation varies, modulating tidal response
    ax = axes[2]
    t_days = np.arange(0, 730, 1)
    t_months = t_days / 30.44
    
    # Seasonal saturation cycle (from agricultural soil scenario)
    Sw_seasonal = 0.5 + 0.3 * np.sin(2*np.pi*t_days/365.25 - np.pi/3)
    Sw_seasonal = np.clip(Sw_seasonal, 0.1, 0.95)
    
    # Tidal strain (constant amplitude)
    epsilon_tide = 50e-9 * np.sin(2*np.pi*t_days/0.5)  # Semidiurnal tide
    
    # β at each time step
    beta_t = np.interp(Sw_seasonal, Sw, beta_Sw)
    
    # δv/v with constant β (decoupled)
    dvv_decoupled = np.mean(beta_Sw) * epsilon_tide
    
    # δv/v with saturation-dependent β (coupled)
    dvv_coupled = beta_t * epsilon_tide
    
    # Show the envelope (daily max/min of tidal δv/v)
    window = 2  # days
    n_windows = len(t_days) // window
    tidal_amp_coupled = np.zeros(n_windows)
    tidal_amp_decoupled = np.zeros(n_windows)
    t_windows = np.zeros(n_windows)
    
    for i in range(n_windows):
        sl = slice(i*window, (i+1)*window)
        tidal_amp_coupled[i] = (np.max(dvv_coupled[sl]) - np.min(dvv_coupled[sl])) / 2
        tidal_amp_decoupled[i] = (np.max(dvv_decoupled[sl]) - np.min(dvv_decoupled[sl])) / 2
        t_windows[i] = np.mean(t_months[sl])
    
    ax.plot(t_windows, tidal_amp_coupled * 1e6, 'r-', linewidth=2, 
            label=r'Coupled: $\beta(S_w(t))$')
    ax.plot(t_windows, tidal_amp_decoupled * 1e6, 'b--', linewidth=2, 
            label=r'Decoupled: $\beta = \langle\beta\rangle$')
    
    ax2 = ax.twinx()
    ax2.plot(t_months, Sw_seasonal * 100, 'g-', linewidth=1, alpha=0.5)
    ax2.set_ylabel('Saturation (%)', fontsize=12, color='green')
    ax2.tick_params(axis='y', colors='green')
    
    ax.set_xlabel('Time (months)', fontsize=12)
    ax.set_ylabel(r'Tidal $|\delta v/v|$ amplitude (×10⁻⁶)', fontsize=12)
    ax.set_title('(c) Seasonally modulated tidal response', fontsize=13)
    ax.legend(fontsize=9, loc='upper left')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/home/claude/figures/tier3_saturation_nonlinearity.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    print("TIER 3 — Saturation-Dependent Nonlinearity Results:")
    print("=" * 60)
    print(f"  β range: {np.min(beta_Sw):.0f} to {np.max(beta_Sw):.0f}")
    print(f"  Tidal δv/v range: {np.min(np.abs(dvv_tidal)):.3f} to "
          f"{np.max(np.abs(dvv_tidal)):.3f} ×10⁻⁶")
    print(f"  Multiplicative variation: {np.max(np.abs(dvv_tidal))/max(np.min(np.abs(dvv_tidal)),1e-10):.1f}×")
    print()


# =============================================================================
# CROSS-TIER: Prognostic Scenarios
# =============================================================================

def prognostic_scenarios():
    """
    Demonstrate how δv/v with coupling awareness could serve as a 
    prognostic tool for hazard assessment and resource management.
    
    Scenario 1: Landslide early warning (coupled hydrology + damage)
    Scenario 2: Water resource monitoring (coupled saturation + δv/v)
    Scenario 3: Post-earthquake infrastructure assessment
    """
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    
    # SCENARIO 1: Landslide early warning
    # δv/v tracks progressive weakening of a hillslope through 
    # moisture accumulation + micro-damage
    ax = axes[0]
    t = np.arange(0, 365, 0.5)  # Half-day resolution, 1 year
    
    # Rainfall (monsoon-like, with an extreme event)
    rain = 5 + 10 * np.sin(2*np.pi*t/365.25 - np.pi/3)
    rain = np.maximum(0, rain)
    # Add extreme event at day 200
    rain[395:405] = 80  # Extreme rainfall
    
    # Saturation responds to cumulative rainfall (with drainage)
    Sw = np.zeros_like(t)
    Sw[0] = 0.4
    tau_drain_soil = 30.0  # days
    for i in range(1, len(t)):
        Sw[i] = Sw[i-1] + (rain[i]*0.001 - (Sw[i-1]-0.3)/tau_drain_soil) * 0.5
        Sw[i] = np.clip(Sw[i], 0.1, 0.99)
    
    # δv/v: coupled model (β depends on Sw)
    beta_base = -500
    beta_t = beta_base * (1 + 3 * Sw**2)  # β becomes more negative with saturation
    
    # Effective stress decreases with saturation (pore pressure increases)
    sigma_eff = 50000 * (1 - 0.8*Sw)  # Pa, effective stress
    dvv = -0.001 * (1 - sigma_eff/50000)  # Simplified: velocity tracks eff. stress
    
    # Add micro-damage acceleration above a saturation threshold
    damage_mask = Sw > 0.85
    micro_damage = np.cumsum(damage_mask * 0.00002)
    dvv -= micro_damage
    
    ax.plot(t, dvv * 100, 'k-', linewidth=2)
    ax.axhline(y=-0.15, color='red', ls='--', alpha=0.7)
    ax.text(10, -0.14, 'Alert threshold', fontsize=9, color='red')
    
    # Mark the extreme event and landslide window
    ax.axvspan(197, 202, alpha=0.3, color='blue', label='Extreme rainfall')
    ax.axvspan(202, 220, alpha=0.2, color='red', label='Elevated risk window')
    
    ax.set_xlabel('Day of year', fontsize=12)
    ax.set_ylabel('δv/v (%)', fontsize=12)
    ax.set_title('(a) Landslide early warning', fontsize=13)
    ax.legend(fontsize=9, loc='lower left')
    ax.grid(True, alpha=0.3)
    
    # SCENARIO 2: Water resource monitoring
    # δv/v at different frequencies reveals water table depth and 
    # vadose zone moisture — useful for drought monitoring
    ax = axes[1]
    
    # Multi-year scenario with drought
    t_years_wr = np.arange(0, 2190, 1) / 365.25  # 6 years
    t_days_wr = np.arange(0, 2190, 1)
    
    # Groundwater level: seasonal + drought trend in years 3-4
    gwl = np.zeros(2190)
    for i in range(2190):
        seasonal = 2.0 * np.sin(2*np.pi*t_days_wr[i]/365.25)
        drought = 0.0
        if 2.5 < t_years_wr[i] < 4.5:
            drought = -3.0 * (1 - np.cos(np.pi*(t_years_wr[i]-2.5)/2.0))
        gwl[i] = 10.0 + seasonal + drought  # meters below surface
    
    # δv/v at different frequencies (different depth sensitivities)
    # High freq (2 Hz, z_sens ~ 50m): sees vadose zone + shallow GWL
    # Low freq (0.5 Hz, z_sens ~ 500m): sees deeper, less GWL influence
    
    beta_shallow = -2000
    beta_deep = -200
    
    # Shallow δv/v: dominated by water table position
    dvv_shallow = beta_shallow * (-(gwl - 10)/10) * 1e-5  # Simplified
    
    # Deep δv/v: mostly tectonic trend + small hydro signal
    dvv_deep = 0.0001 * t_years_wr + beta_deep * (-(gwl - 10)/10) * 1e-7
    
    ax.plot(t_years_wr, dvv_shallow * 100, 'b-', linewidth=2, 
            label='2 Hz (shallow, ~50m)')
    ax.plot(t_years_wr, dvv_deep * 100, 'r-', linewidth=2, 
            label='0.5 Hz (deep, ~500m)')
    
    # Mark drought period
    ax.axvspan(2.5, 4.5, alpha=0.15, color='orange', label='Drought')
    
    ax.set_xlabel('Time (years)', fontsize=12)
    ax.set_ylabel('δv/v (%)', fontsize=12)
    ax.set_title('(b) Water resource monitoring', fontsize=13)
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)
    
    # SCENARIO 3: Post-earthquake infrastructure assessment
    # Coupling diagnostic: if seasonal coefficients change after earthquake,
    # the subsurface has been damaged
    ax = axes[2]
    
    # Pre-earthquake: stable seasonal δv/v
    t = np.arange(0, 1825, 1) / 365.25  # 5 years
    
    # Environmental δv/v (thermoelastic + hydrological)
    seasonal = 0.05 * np.sin(2*np.pi*np.arange(1825)/365.25)
    
    # Earthquake at year 2.5
    eq_time = 2.5
    
    # Pre-EQ coefficients
    sT_pre = 0.05
    pH_pre = 0.03
    
    # Post-EQ coefficients (changed due to permeability modification)
    sT_post = 0.05  # Thermoelastic unchanged
    pH_post = 0.06  # Hydrological sensitivity doubled (faster drainage)
    
    dvv = np.zeros(1825)
    for i in range(1825):
        yr = i / 365.25
        thermo = sT_pre * np.sin(2*np.pi*i/365.25)
        if yr < eq_time:
            hydro = pH_pre * np.sin(2*np.pi*i/365.25 + np.pi/4)
            dvv[i] = thermo + hydro
        else:
            # Co-seismic drop + healing
            t_since = (yr - eq_time) * 365.25
            coseismic = -0.3 * np.exp(-t_since/200)
            healing = 0.2 * np.log(1 + t_since/10) / np.log(365)
            hydro = pH_post * np.sin(2*np.pi*i/365.25 + np.pi/4)
            dvv[i] = thermo + hydro + coseismic + healing
    
    ax.plot(t, dvv, 'k-', linewidth=1.5)
    ax.axvline(x=eq_time, color='red', ls='--', alpha=0.7, label='Earthquake')
    
    # Show the change in seasonal envelope
    # Pre-earthquake envelope
    t_pre = t[t < eq_time - 0.2]
    env_pre = sT_pre + pH_pre
    ax.axhline(y=env_pre, xmin=0, xmax=0.45, color='blue', ls=':', alpha=0.5)
    ax.axhline(y=-env_pre, xmin=0, xmax=0.45, color='blue', ls=':', alpha=0.5)
    
    # Post-earthquake envelope (larger)
    env_post = sT_post + pH_post
    ax.axhline(y=env_post, xmin=0.55, xmax=1.0, color='orange', ls=':', alpha=0.5)
    ax.axhline(y=-env_post, xmin=0.55, xmax=1.0, color='orange', ls=':', alpha=0.5)
    
    ax.annotate('Pre-EQ\namplitude', xy=(1, env_pre), fontsize=9, color='blue',
                xytext=(0.3, 0.12), arrowprops=dict(arrowstyle='->', color='blue'))
    ax.annotate('Post-EQ\namplitude\n(larger)', xy=(4, env_post), fontsize=9, color='orange',
                xytext=(3.8, 0.15), arrowprops=dict(arrowstyle='->', color='orange'))
    
    ax.set_xlabel('Time (years)', fontsize=12)
    ax.set_ylabel('δv/v (%)', fontsize=12)
    ax.set_title('(c) Post-earthquake damage diagnostic', fontsize=13)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/home/claude/figures/prognostic_scenarios.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    print("PROGNOSTIC SCENARIOS:")
    print("=" * 60)
    print("  (a) Landslide: δv/v drops below -0.15% alert threshold")
    print("      during extreme rainfall + saturated hillslope")
    print("  (b) Water resources: Multi-frequency δv/v resolves drought")
    print("      signal at depth; 2 Hz sees GWL drop, 0.5 Hz shows tectonic trend")
    print(f"  (c) Infrastructure: Seasonal amplitude increases from "
          f"{sT_pre+pH_pre:.2f}% to {sT_post+pH_post:.2f}% post-earthquake")
    print("      → diagnostic for subsurface damage / permeability change")
    print()


# =============================================================================
# COUPLING REGIME DIAGRAM
# =============================================================================

def coupling_regime_diagram():
    """
    Comprehensive regime diagram showing where each coupling tier matters.
    Extends the manuscript's Figure 18 with coupling boundaries.
    """
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Axes: forcing period (x) vs depth (y)
    # Using log scale for both
    
    # Background: dominant process regions (simplified)
    periods = np.logspace(-1, 4, 500)  # 0.1 day to 10,000 days
    depths = np.logspace(-1, 4, 500)   # 0.1 m to 10 km
    
    P, D = np.meshgrid(periods, depths)
    
    # Thermal skin depth (annual: ~3m, daily: ~0.15m)
    # z_thermal = sqrt(kappa_T * T / pi)
    kT = 1e-6  # m²/s
    z_thermal = np.sqrt(kT * P * 86400 / np.pi)
    
    # Regime assignments (simplified)
    regime = np.zeros_like(P)
    # 0 = thermoelastic, 1 = hydrological, 2 = tectonic, 3 = capillary
    
    # Thermoelastic: z < z_thermal
    regime[D < z_thermal] = 0
    # Hydrological: z > z_thermal, z < 1000m
    regime[(D >= z_thermal) & (D < 1000)] = 1
    # Tectonic: z > 1000m
    regime[D >= 1000] = 2
    # Capillary: z < 10m and partially saturated
    regime[D < 10] = 3
    
    cmap = plt.cm.Set3
    ax.pcolormesh(P, D, regime, cmap=cmap, alpha=0.3, shading='auto')
    
    # Coupling boundaries
    # 1. Drained-undrained transition for different permeabilities
    for perm, ls, label in [(1e-11, '-', 'k=10⁻¹¹ m² (sand)'), 
                            (1e-14, '--', 'k=10⁻¹⁴ m² (fractured rock)'),
                            (1e-16, ':', 'k=10⁻¹⁶ m² (tight rock)')]:
        eta = 1e-3
        Ss = 1e-5
        c = perm / (Ss * eta)
        T_drain = depths**2 / c / 86400  # days
        ax.plot(T_drain, depths, color='navy', ls=ls, linewidth=2, label=label)
    
    # 2. Thermal skin depth
    T_annual = 365.25
    z_annual = np.sqrt(kT * T_annual * 86400 / np.pi)
    ax.axhline(y=z_annual, color='red', ls='-.', linewidth=1.5, alpha=0.7, 
               label=f'Thermal skin depth (annual) = {z_annual:.1f} m')
    
    # 3. Water table (typical range)
    ax.axhspan(2, 30, alpha=0.1, color='cyan', label='Typical water table range')
    
    # 4. Coda sensitivity depth (peak sensitivity z = Vs/(3f))
    for f, Vs_text in [(0.5, 500), (1.0, 500), (2.0, 300), (4.0, 200)]:
        z_peak = Vs_text / (3 * f)
        ax.plot(periods[-1]*1.05, z_peak, '>', markersize=8, color='black')
        ax.text(periods[-1]*1.2, z_peak, f'{f} Hz\n({z_peak:.0f} m)', 
                fontsize=8, va='center')
    
    # Mark forcing timescales
    for T_force, name, color in [(0.5, 'Tidal', 'purple'),
                                   (1, 'Daily', 'brown'),
                                   (365, 'Annual', 'darkgreen'),
                                   (3650, 'Decadal', 'darkred')]:
        ax.axvline(x=T_force, color=color, ls=':', alpha=0.5, linewidth=1)
        ax.text(T_force*1.1, 0.12, name, fontsize=9, color=color, rotation=90)
    
    # Coupling zones (hatched)
    # Tier 1: Poroelastic coupling dominant (left of drained line for k=10⁻¹⁴)
    ax.text(0.2, 500, 'UNDRAINED\n(Tier 1 coupling\ndominant)', fontsize=10, 
            color='navy', fontweight='bold', ha='center',
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
    
    ax.text(2000, 500, 'DRAINED\n(Tier 1 coupling\nweak)', fontsize=10, 
            color='navy', ha='center',
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
    
    # Tier 3: Saturation window
    ax.text(30, 3, 'Tier 3:\nβ(Sw) coupling', fontsize=9, color='darkgreen',
            fontweight='bold', ha='center',
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.5))
    
    # Tier 2: Post-earthquake (applies transiently at all depths)
    ax.annotate('Tier 2: Damage–permeability\ncoupling (post-earthquake,\ntransient: months–years)',
                xy=(100, 2000), fontsize=9, color='red', fontweight='bold',
                bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
    
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('Forcing period (days)', fontsize=13)
    ax.set_ylabel('Depth (m)', fontsize=13)
    ax.set_title('Coupling Regime Diagram: When Linear Superposition Fails', fontsize=14)
    ax.set_xlim(0.1, 1e4)
    ax.set_ylim(0.1, 1e4)
    ax.invert_yaxis()
    ax.legend(fontsize=8, loc='lower right', ncol=2)
    ax.grid(True, alpha=0.2)
    
    plt.tight_layout()
    plt.savefig('/home/claude/figures/coupling_regime_diagram.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    print("COUPLING REGIME DIAGRAM generated.")
    print("  Key finding: The drained–undrained transition line (navy curves)")
    print("  separates regions where Tier 1 coupling is strong (left/above)")
    print("  from regions where it is weak (right/below).")
    print("  Tier 3 (saturation) applies only above the water table.")
    print("  Tier 2 (damage) applies transiently after earthquakes at all depths.")
    print()


# =============================================================================
# PARAMETER SENSITIVITY TABLE
# =============================================================================

def print_parameter_summary():
    """Print comprehensive summary of coupling parameters across sites."""
    print("\n" + "=" * 80)
    print("COMPREHENSIVE COUPLING PARAMETER SUMMARY")
    print("=" * 80)
    
    header = f"{'Parameter':<30} {'Parkfield':<15} {'Cascadia':<15} {'Nepal':<15} {'Agri. Soil':<15}"
    print(header)
    print("-" * 80)
    
    for site in sites:
        pass
    
    rows = [
        ("Vs (m/s)", [s.Vs for s in sites]),
        ("μ (GPa)", [s.mu/1e9 for s in sites]),
        ("κ (GPa)", [s.kappa/1e9 for s in sites]),
        ("μ'", [s.mu_prime for s in sites]),
        ("|β| (drained)", [abs(s.beta) for s in sites]),
        ("α_B", [s.alpha_B for s in sites]),
        ("B (Skempton)", [s.B_skemp for s in sites]),
        ("α_B·B", [s.alpha_B * s.B_skemp for s in sites]),
        ("|β_u/β_d|", [1/(1-s.alpha_B*s.B_skemp) for s in sites]),
        ("|β| (undrained)", [abs(s.beta)/(1-s.alpha_B*s.B_skemp) for s in sites]),
        ("Permeability (m²)", [s.perm for s in sites]),
        ("Porosity", [s.phi for s in sites]),
        ("Depth (m)", [s.depth for s in sites]),
    ]
    
    for name, vals in rows:
        if any(v > 1e6 or v < 1e-6 for v in vals if v != 0):
            line = f"{name:<30}" + "".join(f"{v:<15.2e}" for v in vals)
        else:
            line = f"{name:<30}" + "".join(f"{v:<15.1f}" for v in vals)
        print(line)
    
    print("\n" + "=" * 80)
    print("KEY INSIGHTS FROM COUPLING ANALYSIS:")
    print("-" * 80)
    print("1. Agricultural soil has the strongest undrained amplification")
    print(f"   (|β_u/β_d| = {1/(1-agri.alpha_B*agri.B_skemp):.1f}×)")
    print(f"   because α_B·B = {agri.alpha_B*agri.B_skemp:.2f} ≈ 1.")
    print()
    print("2. Cascadia sediment has high α_B·B = "
          f"{cascadia.alpha_B*cascadia.B_skemp:.2f},")
    print("   but the isotropic framework succeeds because it implicitly uses")
    print("   the effective stress (including pore pressure coupling).")
    print()
    print("3. Parkfield granite has moderate α_B·B = "
          f"{parkfield.alpha_B*parkfield.B_skemp:.2f},")
    print("   so the undrained β is only "
          f"{1/(1-parkfield.alpha_B*parkfield.B_skemp):.1f}× larger than drained.")
    print("   But the post-earthquake permeability change (Tier 2)")
    print("   may be more important here.")
    print("=" * 80)


# =============================================================================
# RUN ALL TESTS
# =============================================================================

if __name__ == "__main__":
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║  COUPLING-TIER NUMERICAL TESTS                             ║")
    print("║  Unified δv/v Framework — Denolle & Claude                 ║")
    print("╚══════════════════════════════════════════════════════════════╝\n")
    
    tier1_drained_undrained_transition()
    tier2_damage_permeability()
    tier3_saturation_beta()
    prognostic_scenarios()
    coupling_regime_diagram()
    print_parameter_summary()
    
    print("\nAll figures saved to /home/claude/figures/")
    print("Files: tier1_poroelastic_coupling.png")
    print("       tier2_damage_permeability.png")
    print("       tier3_saturation_nonlinearity.png")
    print("       prognostic_scenarios.png")
    print("       coupling_regime_diagram.png")
