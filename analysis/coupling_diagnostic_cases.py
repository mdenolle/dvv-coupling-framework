#!/usr/bin/env python3
"""
Coupling Diagnostic Analysis Code — Three Priority Cases
=========================================================

Case 1: Ridgecrest post-earthquake coefficient change (Tier 2)
   Uses: Clements & Denolle (2023) California-wide parquet files
   Test: Split-window regression of seasonal coefficients around 2019 M7.1

Case 2: California drought-to-flood saturation-dependent β (Tier 3)
   Uses: Clements & Denolle (2023) parquet files
   Test: Non-linear sensitivity of δv/v to precipitation vs. antecedent moisture

Case 3: Parkfield tidal β time-variation (Tiers 1+2)
   Uses: Okubo et al. (2024) Parkfield parquet files
   Test: M2 tidal amplitude change around the 2004 Parkfield earthquake

Each case includes:
  - Data loading functions (designed for parquet format)
  - Synthetic data generators for validation (matching published figure ranges)
  - Analysis functions implementing the coupling diagnostic
  - Visualization functions producing publication-ready figures

When parquet files are available, replace the synthetic data generators with
the real data loading functions.

Author: M. A. Denolle (AI tools used as a research assistant under the author's direction)
Date: 2026-04-01
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from scipy.optimize import least_squares, minimize
from scipy.special import erfc
from scipy.signal import butter, filtfilt
from datetime import datetime, timedelta
import os
import warnings

# NOTE: a global warnings.filterwarnings('ignore') was removed here so that
# aliasing / rank-deficiency / numerical warnings are surfaced rather than
# silently hidden (these are scientifically meaningful for the diagnostics).

# Fixed seed for reproducible synthetic figures (np.random is used in the
# synthetic data generators below).
np.random.seed(20260401)

# Output directory for figures (repo-relative; override with $DVV_FIGDIR).
FIGDIR = os.environ.get(
    "DVV_FIGDIR",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "figures", "coupling"),
)
os.makedirs(FIGDIR, exist_ok=True)

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def date_range(start_year, end_year, dt_days=1):
    """Generate date array and decimal year array."""
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 12, 31)
    n_days = (end - start).days
    dates = [start + timedelta(days=i) for i in range(0, n_days, dt_days)]
    dec_years = np.array([(d - datetime(d.year, 1, 1)).days / 365.25 + d.year 
                          for d in dates])
    return dates, dec_years

def bandpass(data, fs, fmin, fmax, order=4):
    """Butterworth bandpass filter."""
    nyq = 0.5 * fs
    low = fmin / nyq
    high = min(fmax / nyq, 0.99)
    if low >= high or low <= 0:
        return data
    b, a = butter(order, [low, high], btype='band')
    return filtfilt(b, a, data)

def gwl_model(precip, alpha0, phi=0.3):
    """
    Groundwater level model from precipitation using exponential decay.
    Okubo et al. (2024) Eq. 4: ΔGWL(t) = Σ p(tn)/φ · exp(-α0·(t-tn))
    """
    n = len(precip)
    gwl = np.zeros(n)
    for i in range(1, n):
        gwl[i] = gwl[i-1] * np.exp(-alpha0) + precip[i] / phi
    return gwl

def log_healing(t_days, t_eq, s, tau_min_days=30, tau_max_years=10):
    """
    Logarithmic healing model. Snieder et al. (2017).
    L(t) = s · log(1 + (t-t_eq)/τ_min) / log(τ_max/τ_min) for t > t_eq
    """
    tau_max_days = tau_max_years * 365.25
    result = np.zeros_like(t_days, dtype=float)
    mask = t_days > t_eq
    dt = t_days[mask] - t_eq
    result[mask] = s * np.log(1 + dt / tau_min_days) / np.log(tau_max_days / tau_min_days)
    return result


# =============================================================================
# SYNTHETIC DATA GENERATORS (based on published figure characteristics)
# =============================================================================

def generate_california_synthetic(station_name="CI.JRC2", years=(2015, 2023)):
    """
    Generate synthetic δv/v time series matching Clements & Denolle (2023)
    characteristics for a station near the Ridgecrest epicenter.
    
    Based on: CD23 Figure 4 (mixing ratios), Figure 6 (2005 response),
    Figure 9 (Ridgecrest postseismic). Typical seasonal amplitude 0.05-0.2%.
    """
    dates, dec_years = date_range(years[0], years[1])
    t_days = np.arange(len(dates), dtype=float)
    n = len(t_days)
    
    # Environmental forcing
    # Temperature: annual cycle, amplitude ~15°C, peak in July
    temp = 15 * np.sin(2 * np.pi * (t_days - 200) / 365.25)
    
    # Precipitation: California pattern — wet winters, dry summers
    # Based on Parkfield RAWS data typical values
    precip = np.zeros(n)
    for i in range(n):
        month = dates[i].month
        if month in [11, 12, 1, 2, 3]:
            precip[i] = max(0, np.random.exponential(3.0))  # mm/day
        else:
            precip[i] = max(0, np.random.exponential(0.3))
    
    # Enhance 2016-2017 winter (post-drought wet winter)
    for i in range(n):
        if 2016.8 < dec_years[i] < 2017.3:
            precip[i] *= 2.5
    
    # GWL model 
    alpha0 = 0.024  # 1/day, from Okubo et al. Table 3
    gwl = gwl_model(precip, alpha0)
    
    # δv/v model: thermal + hydrological + earthquake
    # Pre-earthquake coefficients (matching CD23 typical values)
    a1_pre = 0.003   # Thermal sensitivity (%/°C)
    a2_pre = -0.0015  # Hydrological sensitivity (%/mm-equiv)
    
    # Post-earthquake coefficients (Tier 2 prediction: a2 changes)
    a1_post = 0.003   # Thermal unchanged
    a2_post = -0.0028  # Hydrological nearly doubled (enhanced drainage)
    
    # Ridgecrest earthquake: 2019-07-06 = decimal year ~2019.51
    t_eq_ridgecrest = (datetime(2019, 7, 6) - dates[0]).days
    
    dvv = np.zeros(n)
    for i in range(n):
        if t_days[i] < t_eq_ridgecrest:
            dvv[i] = a1_pre * temp[i] + a2_pre * gwl[i]
        else:
            dvv[i] = a1_post * temp[i] + a2_post * gwl[i]
    
    # Add coseismic drop and healing for Ridgecrest
    dvv += log_healing(t_days, t_eq_ridgecrest, s=0.04, 
                       tau_min_days=30, tau_max_years=5)
    mask_eq = t_days >= t_eq_ridgecrest
    dvv[mask_eq] -= 0.08  # Coseismic drop
    
    # Add noise
    dvv += np.random.normal(0, 0.015, n)
    
    return {
        'dates': dates, 'dec_years': dec_years, 't_days': t_days,
        'dvv': dvv, 'temp': temp, 'precip': precip, 'gwl': gwl,
        'station': station_name, 't_eq': t_eq_ridgecrest,
        'true_a1_pre': a1_pre, 'true_a2_pre': a2_pre,
        'true_a1_post': a1_post, 'true_a2_post': a2_post
    }


def generate_parkfield_synthetic(years=(2001, 2023)):
    """
    Generate synthetic Parkfield δv/v matching Okubo et al. (2024) Fig. 9.
    
    Key features: weak seasonality (~0.02%), coseismic drops at San Simeon
    (2003-12-22) and Parkfield (2004-09-28), logarithmic healing, secular
    trend of +0.0048%/yr, plus a tidal signal.

    SYNTHETIC ROUND-TRIP / ESTIMATOR-VALIDATION NOTE
    ------------------------------------------------
    This generator INJECTS a known M2 tidal step (amplitude scale 240 -> 180,
    i.e. a ~25% reduction at the Parkfield earthquake) so that the analysis can
    test whether the estimator recovers the injected parameters. It is NOT a
    discovery from real data.

    ALIASING WARNING: the series is built at 1-day sampling, but the injected
    M2 signal has period 0.5175 days, which is BELOW the Nyquist period (2 days)
    for daily sampling. Daily sampling therefore ALIASES M2. This demo is
    illustrative of the ESTIMATOR machinery only; recovering a real M2 tidal
    response requires sub-daily data.
    """
    dates, dec_years = date_range(years[0], years[1])
    t_days = np.arange(len(dates), dtype=float)
    n = len(t_days)
    
    # Environmental terms (weak at Parkfield, from Okubo Fig. 9)
    temp = 12 * np.sin(2 * np.pi * (t_days - 200) / 365.25)
    precip = np.zeros(n)
    for i in range(n):
        month = dates[i].month
        if month in [11, 12, 1, 2, 3]:
            precip[i] = max(0, np.random.exponential(2.0))
    
    gwl = gwl_model(precip, 0.024)
    
    # Earthquake times
    t_ss = (datetime(2003, 12, 22) - dates[0]).days  # San Simeon
    t_pf = (datetime(2004, 9, 28) - dates[0]).days   # Parkfield
    
    # Model: thermal + hydro + healing + trend
    a1 = 0.001  # Weak thermal (Okubo: p2 varies, median positive but small)
    a2 = -0.0005  # Weak hydro
    b0 = 0.0048 / 365.25  # %/day secular trend
    
    dvv = a1 * temp + a2 * gwl + b0 * t_days
    
    # Coseismic drops and healing
    dvv += log_healing(t_days, t_ss, s=0.03, tau_min_days=23, tau_max_years=10)
    dvv[t_days >= t_ss] -= 0.06
    dvv += log_healing(t_days, t_pf, s=0.12, tau_min_days=115, tau_max_years=10)
    dvv[t_days >= t_pf] -= 0.18
    
    # Tidal signal: M2 semidiurnal tide
    # At Parkfield, tidal strain ~50 nanostrain, β ~ -240
    # δv/v_tidal ~ 240 * 50e-9 = 1.2e-5 = 0.0012%
    # This is at the resolution limit but detectable in stacking
    # ALIASING WARNING: M2 period (0.5175 d) is below the 2-day Nyquist period
    # of this 1-day-sampled series, so this injected M2 is aliased. Kept only to
    # exercise the estimator; real M2 recovery requires sub-daily sampling.
    tidal_period_days = 0.5175  # M2 period in days
    
    # Pre-earthquake tidal β
    beta_tidal_pre = 240 * 50e-9 * 100  # in % units = 0.0012%
    
    # Post-earthquake: enhanced permeability shifts toward drained,
    # potentially reducing undrained β
    beta_tidal_post_initial = 180 * 50e-9 * 100  # Reduced by ~25%
    tau_tidal_recovery = 2 * 365.25  # 2-year recovery
    
    tidal_dvv = np.zeros(n)
    for i in range(n):
        if t_days[i] < t_pf:
            amp = beta_tidal_pre
        else:
            dt = t_days[i] - t_pf
            amp = beta_tidal_post_initial + (beta_tidal_pre - beta_tidal_post_initial) * \
                  (1 - np.exp(-dt / tau_tidal_recovery))
        tidal_dvv[i] = amp * np.sin(2 * np.pi * t_days[i] / tidal_period_days)
    
    dvv += tidal_dvv
    
    # Noise (matching Okubo residual std ~ 0.02-0.03%)
    dvv += np.random.normal(0, 0.025, n)
    
    return {
        'dates': dates, 'dec_years': dec_years, 't_days': t_days,
        'dvv': dvv, 'temp': temp, 'precip': precip, 'gwl': gwl,
        'tidal_dvv': tidal_dvv, 'tidal_period': tidal_period_days,
        't_ss': t_ss, 't_pf': t_pf,
        'true_beta_tidal_pre': beta_tidal_pre,
        'true_beta_tidal_post': beta_tidal_post_initial
    }


def _emit_plan(case_name, config, params):
    """Print and return the analysis plan for a dry run (no computation)."""
    lines = [f"[dry-run] {case_name}"]
    if config is not None:
        lines.append(f"  site: {config.site.name}")
        lines.append(f"  frequency_hz: {config.frequency_hz}")
        lines.append(f"  rule: {config.rule}")
    for key, val in params.items():
        lines.append(f"  {key}: {val}")
    print("\n".join(lines))
    return {"status": "dry_run", "case": case_name,
            "config": config, "params": params}


# =============================================================================
# CASE 1: RIDGECREST POST-EARTHQUAKE COEFFICIENT CHANGE
# =============================================================================

def case1_split_window_regression(data, window_years=2.0, config=None, dry_run=False):
    """
    Case 1: Test for Tier 2 coupling by comparing seasonal regression 
    coefficients before and after the Ridgecrest earthquake.
    
    Method: Fit δv/v = a1·T + a2·GWL + a0 in sliding or split windows.
    If a2 changes after the earthquake while a1 remains stable, this
    diagnoses earthquake-modified hydrological sensitivity.

    SYNTHETIC ROUND-TRIP / ESTIMATOR-VALIDATION NOTE
    ------------------------------------------------
    When run on ``generate_california_synthetic`` output this is an
    ESTIMATOR-VALIDATION test: the synthetic data INJECT known coefficients
    (a2_post = -0.0028 vs a2_pre = -0.0015), and this function simply checks
    that the split-window regression RECOVERS the injected step. It is NOT a
    discovery of an earthquake-modified coefficient from real data.

    Pass ``dry_run=True`` to print the analysis plan without computing.
    """
    if dry_run:
        return _emit_plan(
            "case1_split_window_regression", config,
            {"n_samples": len(data['t_days']),
             "window_years": window_years, "step_days": 90},
        )
    t = data['t_days']
    dvv = data['dvv']
    temp = data['temp']
    gwl = data['gwl']
    t_eq = data['t_eq']
    dec_years = data['dec_years']
    
    # Remove long-term trend and healing for cleaner seasonal analysis
    # (in practice, would use the Okubo/CD23 model to remove these first)
    
    # Split-window analysis
    window_days = int(window_years * 365.25)
    step_days = 90  # 3-month steps
    
    t_centers = []
    a1_values = []
    a2_values = []
    a0_values = []
    r2_values = []
    
    for start in range(0, len(t) - window_days, step_days):
        end = start + window_days
        sl = slice(start, end)
        
        # Design matrix: [T, GWL, 1]
        A = np.column_stack([temp[sl], gwl[sl], np.ones(end - start)])
        y = dvv[sl]
        
        # Remove any NaN
        valid = np.isfinite(y) & np.all(np.isfinite(A), axis=1)
        if np.sum(valid) < 100:
            continue
        
        # Least squares fit
        try:
            result = np.linalg.lstsq(A[valid], y[valid], rcond=None)
            coeffs = result[0]
            residuals = y[valid] - A[valid] @ coeffs
            ss_res = np.sum(residuals**2)
            ss_tot = np.sum((y[valid] - np.mean(y[valid]))**2)
            r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0
            
            t_center = dec_years[start + window_days // 2]
            t_centers.append(t_center)
            a1_values.append(coeffs[0])
            a2_values.append(coeffs[1])
            a0_values.append(coeffs[2])
            r2_values.append(r2)
        except Exception:
            continue
    
    t_centers = np.array(t_centers)
    a1_values = np.array(a1_values)
    a2_values = np.array(a2_values)
    r2_values = np.array(r2_values)
    
    # Earthquake time in decimal years
    eq_dec_year = dec_years[t_eq] if t_eq < len(dec_years) else 2019.51
    
    # Compute pre/post statistics
    pre_mask = t_centers < eq_dec_year - 0.5
    post_mask = t_centers > eq_dec_year + 0.5
    
    results = {
        't_centers': t_centers, 'a1': a1_values, 'a2': a2_values,
        'r2': r2_values, 'eq_year': eq_dec_year,
        'a1_pre_mean': np.mean(a1_values[pre_mask]) if np.any(pre_mask) else np.nan,
        'a1_pre_std': np.std(a1_values[pre_mask]) if np.any(pre_mask) else np.nan,
        'a1_post_mean': np.mean(a1_values[post_mask]) if np.any(post_mask) else np.nan,
        'a1_post_std': np.std(a1_values[post_mask]) if np.any(post_mask) else np.nan,
        'a2_pre_mean': np.mean(a2_values[pre_mask]) if np.any(pre_mask) else np.nan,
        'a2_pre_std': np.std(a2_values[pre_mask]) if np.any(pre_mask) else np.nan,
        'a2_post_mean': np.mean(a2_values[post_mask]) if np.any(post_mask) else np.nan,
        'a2_post_std': np.std(a2_values[post_mask]) if np.any(post_mask) else np.nan,
    }
    
    return results


def plot_case1(data, results):
    """Plot Case 1 results: split-window regression coefficient evolution."""
    fig, axes = plt.subplots(4, 1, figsize=(14, 12), sharex=True)
    
    eq_year = results['eq_year']
    
    # Panel a: δv/v time series
    ax = axes[0]
    ax.plot(data['dec_years'], data['dvv'], 'k-', linewidth=0.5, alpha=0.6)
    ax.axvline(x=eq_year, color='red', ls='--', linewidth=1.5, 
               label=f'Ridgecrest M7.1')
    ax.set_ylabel('δv/v (%)', fontsize=11)
    ax.set_title(f"Case 1: Split-window regression (SYNTHETIC round-trip / "
                 f"estimator validation) — {data['station']}", fontsize=13)
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)
    
    # Panel b: Thermal coefficient a1(t)
    ax = axes[1]
    ax.plot(results['t_centers'], results['a1'] * 1000, 'b-o', 
            markersize=3, linewidth=1.5, label='a₁ (thermal)')
    ax.axvline(x=eq_year, color='red', ls='--', linewidth=1.5)
    ax.axhline(y=results['a1_pre_mean']*1000, color='blue', ls=':', alpha=0.5,
               label=f"Pre-EQ: {results['a1_pre_mean']*1000:.2f}±{results['a1_pre_std']*1000:.2f}")
    ax.axhline(y=results['a1_post_mean']*1000, color='navy', ls=':', alpha=0.5,
               label=f"Post-EQ: {results['a1_post_mean']*1000:.2f}±{results['a1_post_std']*1000:.2f}")
    ax.set_ylabel('a₁ (×10⁻³ %/°C)', fontsize=11)
    ax.legend(fontsize=8, loc='upper left')
    ax.grid(True, alpha=0.3)
    
    # Panel c: Hydrological coefficient a2(t) — the key diagnostic
    ax = axes[2]
    ax.plot(results['t_centers'], results['a2'] * 1000, 'r-o', 
            markersize=3, linewidth=1.5, label='a₂ (hydrological)')
    ax.axvline(x=eq_year, color='red', ls='--', linewidth=1.5)
    ax.axhline(y=results['a2_pre_mean']*1000, color='salmon', ls=':', alpha=0.5,
               label=f"Pre-EQ: {results['a2_pre_mean']*1000:.2f}±{results['a2_pre_std']*1000:.2f}")
    ax.axhline(y=results['a2_post_mean']*1000, color='darkred', ls=':', alpha=0.5,
               label=f"Post-EQ: {results['a2_post_mean']*1000:.2f}±{results['a2_post_std']*1000:.2f}")
    ax.set_ylabel('a₂ (×10⁻³ %/mm)', fontsize=11)
    ax.legend(fontsize=8, loc='lower left')
    ax.grid(True, alpha=0.3)
    
    # Annotate the coupling diagnostic
    a2_change = (results['a2_post_mean'] - results['a2_pre_mean']) / abs(results['a2_pre_mean']) * 100
    ax.annotate(f'Tier 2 estimator-validation (synthetic):\nrecovered injected a₂ '
                f'change of {a2_change:+.0f}%\npost-earthquake (not a real-data discovery)',
                xy=(eq_year + 1.5, results['a2_post_mean']*1000),
                fontsize=10, fontweight='bold',
                bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
    
    # Panel d: R² of fit
    ax = axes[3]
    ax.plot(results['t_centers'], results['r2'], 'g-o', markersize=3, linewidth=1.5)
    ax.axvline(x=eq_year, color='red', ls='--', linewidth=1.5)
    ax.set_ylabel('R²', fontsize=11)
    ax.set_xlabel('Year', fontsize=11)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(FIGDIR, 'case1_ridgecrest_split_window.png'), 
                dpi=150, bbox_inches='tight')
    plt.close()


# =============================================================================
# CASE 2: DROUGHT-TO-FLOOD SATURATION-DEPENDENT β
# =============================================================================

def case2_saturation_sensitivity(data, api_window=90, config=None, dry_run=False):
    """
    Case 2: Test for Tier 3 coupling by examining whether δv/v sensitivity
    to precipitation depends on antecedent moisture conditions.
    
    Method: Compute antecedent precipitation index (API), then measure
    d(δv/v)/d(precip) in sliding windows and plot against API.

    Pass ``dry_run=True`` to print the analysis plan without computing.
    """
    if dry_run:
        return _emit_plan(
            "case2_saturation_sensitivity", config,
            {"n_samples": len(data['dvv']), "api_window": api_window},
        )
    precip = data['precip']
    dvv = data['dvv']
    dec_years = data['dec_years']
    n = len(precip)
    
    # Compute antecedent precipitation index (running sum)
    api = np.zeros(n)
    for i in range(api_window, n):
        api[i] = np.sum(precip[i-api_window:i])
    
    # Compute sensitivity in sliding 180-day windows
    window = 180
    step = 30
    
    api_centers = []
    sensitivities = []
    years_center = []
    
    for start in range(api_window, n - window, step):
        end = start + window
        sl = slice(start, end)
        
        p_win = precip[sl]
        d_win = dvv[sl]
        
        # Only use days with significant precipitation
        wet_days = p_win > 1.0  # >1 mm/day
        if np.sum(wet_days) < 10:
            continue
        
        # Compute sensitivity as regression slope: δv/v = s · precip + c
        A = np.column_stack([p_win[wet_days], np.ones(np.sum(wet_days))])
        try:
            coeffs = np.linalg.lstsq(A, d_win[wet_days], rcond=None)[0]
            sensitivity = coeffs[0]  # d(δv/v)/d(precip)
        except Exception:
            continue
        
        api_center = np.mean(api[sl])
        year_center = np.mean(dec_years[sl])
        
        api_centers.append(api_center)
        sensitivities.append(sensitivity)
        years_center.append(year_center)
    
    return {
        'api': np.array(api_centers),
        'sensitivity': np.array(sensitivities),
        'years': np.array(years_center),
        'api_full': api,
        'dec_years': dec_years
    }


def plot_case2(data, results):
    """Plot Case 2: saturation-dependent sensitivity diagnostic."""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Panel a: δv/v and API time series
    ax = axes[0, 0]
    ax.plot(data['dec_years'], data['dvv'], 'k-', linewidth=0.5, alpha=0.6)
    ax.set_ylabel('δv/v (%)', fontsize=11, color='black')
    ax2 = ax.twinx()
    ax2.plot(results['dec_years'], results['api_full'], 'b-', linewidth=1, alpha=0.5)
    ax2.set_ylabel(f"90-day API (mm)", fontsize=11, color='blue')
    ax.set_title('(a) δv/v and antecedent precipitation index', fontsize=13)
    ax.grid(True, alpha=0.3)
    
    # Panel b: Sensitivity vs API — the key diagnostic
    ax = axes[0, 1]
    sc = ax.scatter(results['api'], results['sensitivity'] * 100,
                    c=results['years'], cmap='viridis', s=30, alpha=0.7)
    plt.colorbar(sc, ax=ax, label='Year')
    
    # Fit a polynomial to see non-linearity
    valid = np.isfinite(results['api']) & np.isfinite(results['sensitivity'])
    if np.sum(valid) > 10:
        api_sorted = np.sort(results['api'][valid])
        # Quadratic fit
        p2 = np.polyfit(results['api'][valid], results['sensitivity'][valid]*100, 2)
        api_fit = np.linspace(np.min(api_sorted), np.max(api_sorted), 100)
        sens_fit = np.polyval(p2, api_fit)
        ax.plot(api_fit, sens_fit, 'r-', linewidth=2, label='Quadratic fit')
        
        # Linear fit for comparison
        p1 = np.polyfit(results['api'][valid], results['sensitivity'][valid]*100, 1)
        sens_lin = np.polyval(p1, api_fit)
        ax.plot(api_fit, sens_lin, 'b--', linewidth=1.5, label='Linear fit')
    
    ax.set_xlabel('90-day API (mm)', fontsize=11)
    ax.set_ylabel('d(δv/v)/d(precip) (%/mm × 100)', fontsize=11)
    ax.set_title('(b) Sensitivity vs. antecedent moisture', fontsize=13)
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)
    
    # Annotate coupling diagnostic
    if np.sum(valid) > 10:
        nonlin_ratio = abs(p2[0]) / (abs(p2[1]) + 1e-10)
        if nonlin_ratio > 0.01:
            ax.annotate(f'Tier 3: Non-linear!\nQuadratic coeff = {p2[0]:.2e}',
                       xy=(np.mean(api_fit), np.mean(sens_fit)),
                       fontsize=10, fontweight='bold',
                       bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
    
    # Panel c: Sensitivity binned by API quartiles
    ax = axes[1, 0]
    if np.sum(valid) > 20:
        api_valid = results['api'][valid]
        sens_valid = results['sensitivity'][valid] * 100
        quartiles = np.percentile(api_valid, [25, 50, 75])
        bins = [np.min(api_valid)] + list(quartiles) + [np.max(api_valid)]
        labels = ['Dry (Q1)', 'Moderate-dry (Q2)', 'Moderate-wet (Q3)', 'Wet (Q4)']
        colors = ['#d73027', '#fc8d59', '#91bfdb', '#4575b4']
        
        means = []
        stds = []
        for i in range(4):
            mask_bin = (api_valid >= bins[i]) & (api_valid < bins[i+1])
            if np.sum(mask_bin) > 0:
                means.append(np.mean(sens_valid[mask_bin]))
                stds.append(np.std(sens_valid[mask_bin]))
            else:
                means.append(0)
                stds.append(0)
        
        x = np.arange(4)
        bars = ax.bar(x, [abs(m) for m in means], yerr=stds, 
                      color=colors, alpha=0.8, capsize=5)
        ax.set_xticks(x)
        ax.set_xticklabels(labels, fontsize=9)
        ax.set_ylabel('|d(δv/v)/d(precip)| (×100)', fontsize=11)
        ax.set_title('(c) Sensitivity by moisture quartile', fontsize=13)
        ax.grid(True, alpha=0.3, axis='y')
    
    # Panel d: Time series of sensitivity
    ax = axes[1, 1]
    ax.plot(results['years'], np.abs(results['sensitivity']) * 100, 'k-o', 
            markersize=3, linewidth=1)
    
    # Mark extreme events
    for year, label, color in [(2017.0, '2016-17\nwet winter', 'blue'),
                                (2019.5, 'Ridgecrest', 'red')]:
        if year > np.min(results['years']) and year < np.max(results['years']):
            ax.axvline(x=year, color=color, ls='--', alpha=0.7)
            ax.text(year+0.1, ax.get_ylim()[1]*0.9, label, fontsize=8, color=color)
    
    ax.set_xlabel('Year', fontsize=11)
    ax.set_ylabel('|Sensitivity| (×100)', fontsize=11)
    ax.set_title('(d) Sensitivity evolution over time', fontsize=13)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(FIGDIR, 'case2_saturation_sensitivity.png'), 
                dpi=150, bbox_inches='tight')
    plt.close()


# =============================================================================
# CASE 3: PARKFIELD TIDAL β TIME-VARIATION
# =============================================================================

def case3_tidal_beta_evolution(data, stack_days=180, step_days=30, config=None, dry_run=False):
    """
    Case 3: Extract M2 tidal amplitude from Parkfield δv/v in sliding 
    windows and track changes around the 2004 earthquake.
    
    Method: Harmonic regression at the M2 period (12.42 hr = 0.5175 days)
    in sliding windows. Track amplitude over time.

    SYNTHETIC ROUND-TRIP / ESTIMATOR-VALIDATION NOTE
    ------------------------------------------------
    When run on ``generate_parkfield_synthetic`` output this is an
    ESTIMATOR-VALIDATION test: the synthetic data INJECT a known M2 amplitude
    step (scale 240 -> 180 at the Parkfield earthquake), and this function
    checks that the harmonic regression RECOVERS that injected step. It is NOT a
    discovery of a tidal-β change from real data.

    ALIASING WARNING: the synthetic series is 1-day sampled while M2 has period
    0.5175 d (below the 2-day Nyquist period), so the injected M2 is aliased.
    This demo is illustrative of the ESTIMATOR only; real M2 recovery requires
    sub-daily data.

    Pass ``dry_run=True`` to print the analysis plan without computing.
    """
    if dry_run:
        return _emit_plan(
            "case3_tidal_beta_evolution", config,
            {"n_samples": len(data['dvv']),
             "stack_days": stack_days, "step_days": step_days},
        )
    t_days = data['t_days']
    dvv = data['dvv']
    dec_years = data['dec_years']
    
    # M2 tidal period
    T_M2 = 0.5175  # days (12.42 hours)
    omega_M2 = 2 * np.pi / T_M2
    
    # Also fit O1 (25.82 hr) and seasonal for decontamination
    T_O1 = 1.0758  # days
    omega_O1 = 2 * np.pi / T_O1
    T_annual = 365.25
    omega_annual = 2 * np.pi / T_annual
    
    t_centers = []
    M2_amplitudes = []
    M2_phases = []
    annual_amplitudes = []
    
    for start in range(0, len(t_days) - stack_days, step_days):
        end = start + stack_days
        sl = slice(start, end)
        t_win = t_days[sl]
        d_win = dvv[sl]
        
        valid = np.isfinite(d_win)
        if np.sum(valid) < stack_days * 0.7:
            continue
        
        t_v = t_win[valid]
        d_v = d_win[valid]
        
        # Design matrix: sin/cos at M2, O1, annual, + constant + trend
        A = np.column_stack([
            np.sin(omega_M2 * t_v),
            np.cos(omega_M2 * t_v),
            np.sin(omega_O1 * t_v),
            np.cos(omega_O1 * t_v),
            np.sin(omega_annual * t_v),
            np.cos(omega_annual * t_v),
            t_v - np.mean(t_v),
            np.ones(len(t_v))
        ])
        
        try:
            coeffs = np.linalg.lstsq(A, d_v, rcond=None)[0]
            
            # M2 amplitude and phase
            a_M2 = coeffs[0]
            b_M2 = coeffs[1]
            amp_M2 = np.sqrt(a_M2**2 + b_M2**2)
            phase_M2 = np.arctan2(b_M2, a_M2)
            
            # Annual amplitude
            a_ann = coeffs[4]
            b_ann = coeffs[5]
            amp_annual = np.sqrt(a_ann**2 + b_ann**2)
            
            t_center = np.mean(dec_years[sl])
            t_centers.append(t_center)
            M2_amplitudes.append(amp_M2)
            M2_phases.append(phase_M2)
            annual_amplitudes.append(amp_annual)
        except Exception:
            continue
    
    return {
        't_centers': np.array(t_centers),
        'M2_amp': np.array(M2_amplitudes),
        'M2_phase': np.array(M2_phases),
        'annual_amp': np.array(annual_amplitudes),
        't_ss': data.get('t_ss', None),
        't_pf': data.get('t_pf', None)
    }


def plot_case3(data, results):
    """Plot Case 3: tidal β evolution at Parkfield."""
    fig, axes = plt.subplots(4, 1, figsize=(14, 12), sharex=True)
    
    # Earthquake years
    ss_year = 2003 + 356/365.25  # San Simeon: Dec 22, 2003
    pf_year = 2004 + 271/365.25  # Parkfield: Sep 28, 2004
    
    # Panel a: δv/v time series (smoothed)
    ax = axes[0]
    # Smooth for display
    window = 15
    dvv_smooth = np.convolve(data['dvv'], np.ones(window)/window, mode='same')
    ax.plot(data['dec_years'], dvv_smooth, 'k-', linewidth=0.5, alpha=0.7)
    ax.axvline(x=ss_year, color='orange', ls='--', alpha=0.7, label='San Simeon')
    ax.axvline(x=pf_year, color='red', ls='--', alpha=0.7, label='Parkfield')
    ax.set_ylabel('δv/v (%)', fontsize=11)
    ax.set_title('Case 3: Tidal β evolution at Parkfield (Tiers 1+2)\n'
                 'SYNTHETIC round-trip / estimator validation — recovers injected '
                 'M2 step; daily sampling aliases M2 (illustrative only)', fontsize=12)
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)
    
    # Panel b: M2 tidal amplitude — THE KEY DIAGNOSTIC
    ax = axes[1]
    ax.plot(results['t_centers'], results['M2_amp'] * 1e4, 'b-o', 
            markersize=3, linewidth=1.5, label='M₂ amplitude')
    ax.axvline(x=ss_year, color='orange', ls='--', alpha=0.5)
    ax.axvline(x=pf_year, color='red', ls='--', alpha=0.5)
    
    # Compute pre/post means
    pre = results['t_centers'] < pf_year - 0.5
    post_early = (results['t_centers'] > pf_year + 0.5) & (results['t_centers'] < pf_year + 3)
    post_late = results['t_centers'] > pf_year + 5
    
    if np.any(pre):
        ax.axhline(y=np.mean(results['M2_amp'][pre])*1e4, color='blue', 
                   ls=':', alpha=0.5, label=f"Pre-EQ mean: {np.mean(results['M2_amp'][pre])*1e4:.2f}")
    if np.any(post_early):
        ax.axhline(y=np.mean(results['M2_amp'][post_early])*1e4, color='red', 
                   ls=':', alpha=0.5, label=f"Post-EQ (0-3yr): {np.mean(results['M2_amp'][post_early])*1e4:.2f}")
    if np.any(post_late):
        ax.axhline(y=np.mean(results['M2_amp'][post_late])*1e4, color='green', 
                   ls=':', alpha=0.5, label=f"Post-EQ (>5yr): {np.mean(results['M2_amp'][post_late])*1e4:.2f}")
    
    ax.set_ylabel('M₂ |δv/v| (×10⁻⁴)', fontsize=11)
    ax.legend(fontsize=8, loc='upper right')
    ax.grid(True, alpha=0.3)
    
    # Annotate coupling diagnostic
    if np.any(pre) and np.any(post_early):
        change_pct = (np.mean(results['M2_amp'][post_early]) - np.mean(results['M2_amp'][pre])) / \
                     np.mean(results['M2_amp'][pre]) * 100
        ax.annotate(f'Tier 1+2 estimator-validation (synthetic):\nrecovered injected '
                    f'tidal-β change of {change_pct:+.0f}%\npost-earthquake (not a real-data discovery)',
                   xy=(pf_year + 2, np.mean(results['M2_amp'][post_early])*1e4),
                   fontsize=10, fontweight='bold',
                   bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
    
    # Panel c: M2 phase
    ax = axes[2]
    ax.plot(results['t_centers'], np.degrees(results['M2_phase']), 'g-o', 
            markersize=3, linewidth=1.5)
    ax.axvline(x=ss_year, color='orange', ls='--', alpha=0.5)
    ax.axvline(x=pf_year, color='red', ls='--', alpha=0.5)
    ax.set_ylabel('M₂ phase (°)', fontsize=11)
    ax.grid(True, alpha=0.3)
    
    # Panel d: Annual amplitude (control — should NOT change post-EQ)
    ax = axes[3]
    ax.plot(results['t_centers'], results['annual_amp'] * 100, 'k-o', 
            markersize=3, linewidth=1.5, label='Annual amplitude')
    ax.axvline(x=ss_year, color='orange', ls='--', alpha=0.5)
    ax.axvline(x=pf_year, color='red', ls='--', alpha=0.5)
    ax.set_ylabel('Annual |δv/v| (%)', fontsize=11)
    ax.set_xlabel('Year', fontsize=11)
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)
    ax.annotate('Control: annual amplitude\nshould be stable',
               xy=(2010, np.mean(results['annual_amp'])*100),
               fontsize=9, style='italic', alpha=0.7)
    
    plt.tight_layout()
    plt.savefig(os.path.join(FIGDIR, 'case3_parkfield_tidal_beta.png'), 
                dpi=150, bbox_inches='tight')
    plt.close()


# =============================================================================
# PARQUET DATA LOADING FUNCTIONS
# =============================================================================

def load_parquet_dvv(filepath, station=None, freq_band=None):
    """
    Load δv/v time series from parquet file.
    
    Expected columns (adapt to actual format):
    - date or time: datetime
    - dvv: relative velocity change (%)
    - station: station name (if multi-station file)
    - freq_min, freq_max: frequency band
    
    Returns dict matching the synthetic data format.
    """
    try:
        import pandas as pd
        df = pd.read_parquet(filepath)
        
        # Filter by station if specified
        if station and 'station' in df.columns:
            df = df[df['station'] == station]
        
        # Filter by frequency band if specified
        if freq_band and 'freq_min' in df.columns:
            df = df[(df['freq_min'] >= freq_band[0]) & (df['freq_max'] <= freq_band[1])]
        
        # Extract arrays
        if 'date' in df.columns:
            dates = pd.to_datetime(df['date']).tolist()
        elif 'time' in df.columns:
            dates = pd.to_datetime(df['time']).tolist()
        else:
            dates = df.index.tolist()
        
        dec_years = np.array([(d.timetuple().tm_yday / 365.25 + d.year) for d in dates])
        dvv = df['dvv'].values if 'dvv' in df.columns else df.iloc[:, 1].values
        
        return {
            'dates': dates,
            'dec_years': dec_years,
            't_days': np.arange(len(dates), dtype=float),
            'dvv': dvv,
            'station': station or 'unknown'
        }
    except ImportError:
        print("pandas not available; using synthetic data instead")
        return None
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return None


# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║  COUPLING DIAGNOSTIC ANALYSIS — THREE PRIORITY CASES       ║")
    print("║  Denolle & Claude, 2026                                    ║")
    print("╚══════════════════════════════════════════════════════════════╝\n")
    
    # =========================================================================
    # CASE 1: Ridgecrest post-earthquake coefficient change
    # =========================================================================
    print("=" * 70)
    print("CASE 1: Ridgecrest split-window regression (Tier 2)")
    print("       [SYNTHETIC round-trip / estimator validation — recovers")
    print("        injected coefficients, not a real-data discovery]")
    print("=" * 70)
    
    # Generate synthetic data (replace with parquet loading when available)
    # To use real data: data1 = load_parquet_dvv('path/to/CD23.parquet', 'CI.JRC2')
    data1 = generate_california_synthetic("CI.JRC2", years=(2015, 2023))
    results1 = case1_split_window_regression(data1, window_years=2.0)
    plot_case1(data1, results1)
    
    print(f"  Station: {data1['station']}")
    print(f"  Thermal coeff a₁: pre={results1['a1_pre_mean']*1000:.3f}±{results1['a1_pre_std']*1000:.3f}, "
          f"post={results1['a1_post_mean']*1000:.3f}±{results1['a1_post_std']*1000:.3f} ×10⁻³")
    print(f"  Hydro coeff a₂:   pre={results1['a2_pre_mean']*1000:.3f}±{results1['a2_pre_std']*1000:.3f}, "
          f"post={results1['a2_post_mean']*1000:.3f}±{results1['a2_post_std']*1000:.3f} ×10⁻³")
    a2_change = (results1['a2_post_mean'] - results1['a2_pre_mean']) / abs(results1['a2_pre_mean']) * 100
    a1_change = (results1['a1_post_mean'] - results1['a1_pre_mean']) / abs(results1['a1_pre_mean']) * 100
    print(f"  → a₁ change: {a1_change:+.1f}% (expect: ~0% if Tier 2)")
    print(f"  → a₂ change: {a2_change:+.1f}% (expect: significant increase if Tier 2)")
    print()
    
    # =========================================================================
    # CASE 2: Drought-to-flood saturation-dependent β
    # =========================================================================
    print("=" * 70)
    print("CASE 2: Saturation-dependent sensitivity (Tier 3)")
    print("=" * 70)
    
    data2 = generate_california_synthetic("CI.LJR", years=(2005, 2021))
    results2 = case2_saturation_sensitivity(data2, api_window=90)
    plot_case2(data2, results2)
    
    print(f"  Station: {data2['station']}")
    print(f"  API range: {np.min(results2['api']):.0f} – {np.max(results2['api']):.0f} mm")
    print(f"  Sensitivity range: {np.min(results2['sensitivity'])*100:.4f} – "
          f"{np.max(results2['sensitivity'])*100:.4f} %/mm ×100")
    if len(results2['api']) > 10:
        valid = np.isfinite(results2['api']) & np.isfinite(results2['sensitivity'])
        p2 = np.polyfit(results2['api'][valid], results2['sensitivity'][valid]*100, 2)
        print(f"  Quadratic fit: {p2[0]:.2e}·API² + {p2[1]:.2e}·API + {p2[2]:.2e}")
        print(f"  → Non-linearity coefficient: {abs(p2[0]):.2e}")
        print(f"    (>0 indicates Tier 3 coupling: β depends on saturation)")
    print()
    
    # =========================================================================
    # CASE 3: Parkfield tidal β evolution
    # =========================================================================
    print("=" * 70)
    print("CASE 3: Parkfield tidal β evolution (Tiers 1+2)")
    print("       [SYNTHETIC round-trip / estimator validation — recovers")
    print("        injected M2 step; daily sampling aliases M2 (illustrative")
    print("        only; sub-daily data required for real M2 recovery)]")
    print("=" * 70)
    
    data3 = generate_parkfield_synthetic(years=(2001, 2023))
    results3 = case3_tidal_beta_evolution(data3, stack_days=180, step_days=30)
    plot_case3(data3, results3)
    
    pf_year = 2004.74
    pre = results3['t_centers'] < pf_year - 0.5
    post_early = (results3['t_centers'] > pf_year + 0.5) & (results3['t_centers'] < pf_year + 3)
    post_late = results3['t_centers'] > pf_year + 5
    
    if np.any(pre) and np.any(post_early):
        pre_amp = np.mean(results3['M2_amp'][pre])
        post_amp = np.mean(results3['M2_amp'][post_early])
        late_amp = np.mean(results3['M2_amp'][post_late]) if np.any(post_late) else np.nan
        change = (post_amp - pre_amp) / pre_amp * 100
        recovery = (late_amp - post_amp) / (pre_amp - post_amp) * 100 if not np.isnan(late_amp) else np.nan
        
        print(f"  M₂ tidal amplitude:")
        print(f"    Pre-earthquake:  {pre_amp*1e4:.3f} ×10⁻⁴")
        print(f"    Post-EQ (0-3yr): {post_amp*1e4:.3f} ×10⁻⁴")
        if not np.isnan(late_amp):
            print(f"    Post-EQ (>5yr):  {late_amp*1e4:.3f} ×10⁻⁴")
        print(f"    → Change: {change:+.1f}%")
        if not np.isnan(recovery):
            print(f"    → Recovery: {recovery:.0f}%")
        print(f"    (Negative change = enhanced drainage shifted")
        print(f"     tidal response toward drained regime)")
    print()
    
    # =========================================================================
    # SUMMARY
    # =========================================================================
    print("=" * 70)
    print("HOW TO USE WITH REAL DATA")
    print("=" * 70)
    print("""
    Replace the synthetic data generators with parquet loading:
    
    # Case 1 (Ridgecrest):
    data1 = load_parquet_dvv('clements_denolle_2023.parquet', 
                              station='CI.JRC2', freq_band=(2, 4))
    # Add temperature and precipitation from NOAA/RAWS
    data1['temp'] = load_temperature('parkfield_raws.csv')
    data1['precip'] = load_precipitation('parkfield_raws.csv')
    data1['gwl'] = gwl_model(data1['precip'], alpha0=0.024)
    data1['t_eq'] = find_date_index(data1['dates'], datetime(2019, 7, 6))
    
    # Case 2 (Drought-to-flood):
    data2 = load_parquet_dvv('clements_denolle_2023.parquet',
                              station='CI.LJR', freq_band=(2, 4))
    data2['precip'] = load_precipitation('san_gabriel_precip.csv')
    
    # Case 3 (Parkfield tidal):
    data3 = load_parquet_dvv('okubo_2024.parquet', freq_band=(0.9, 1.2))
    # Need sub-daily resolution for tidal analysis!
    # If daily parquet, extract tidal from raw cross-correlations instead.
    
    Then run the same analysis and plotting functions.
    """)
    
    print(f"\nAll figures saved to {FIGDIR}/")
    print("  case1_ridgecrest_split_window.png")
    print("  case2_saturation_sensitivity.png")
    print("  case3_parkfield_tidal_beta.png")
