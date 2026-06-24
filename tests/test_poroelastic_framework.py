"""Unit tests for the pure physics functions in ``poroelastic_framework``."""

import numpy as np
import pytest

from analysis.poroelastic_framework import (
    OMEGA_ANNUAL,
    beta_drained,
    beta_eff,
    beta_ratio_undrained_to_drained,
    classify_drainage,
    drainage_frequency,
    drainage_peclet,
    sensitivity_depth,
    thermoelastic_from_fitted_amplitude,
    thermoelastic_sensitivity_s_T,
)


def test_sensitivity_depth_third_wavelength():
    L = sensitivity_depth(2500.0, 2.0, rule="third_wavelength")
    assert L == pytest.approx(2500.0 / (3 * 2.0), rel=1e-9)


def test_sensitivity_depth_rules_ordering():
    quarter = sensitivity_depth(2500.0, 2.0, rule="quarter_wavelength")
    third = sensitivity_depth(2500.0, 2.0, rule="third_wavelength")
    half = sensitivity_depth(2500.0, 2.0, rule="half_wavelength")
    assert quarter < third < half


def test_sensitivity_depth_invalid_rule():
    with pytest.raises(ValueError):
        sensitivity_depth(2500.0, 2.0, rule="not_a_rule")


def test_sensitivity_depth_vectorized():
    Vs = np.array([500.0, 2500.0])
    L = sensitivity_depth(Vs, 2.0)
    assert L.shape == (2,)
    assert np.all(L > 0)


def test_drainage_frequency_and_peclet_consistent():
    c, L = 1e-5, 100.0
    omega_d = drainage_frequency(c, L)
    pe = drainage_peclet(c, L, omega_forcing=omega_d)
    # Pe = omega_forcing / omega_drain, so this must equal 1.
    assert pe == pytest.approx(1.0, rel=1e-9)


def test_drainage_peclet_default_is_annual():
    c, L = 1e-5, 100.0
    assert drainage_peclet(c, L) == pytest.approx(
        drainage_peclet(c, L, omega_forcing=OMEGA_ANNUAL), rel=1e-12
    )


def test_classify_drainage_labels():
    # Small Pe -> drained; large Pe -> undrained.
    labels, pe = classify_drainage(
        np.array([1e-2, 1e-9]), np.array([10.0, 1000.0])
    )
    assert labels[0] == "drained"
    assert labels[1] == "undrained"
    assert np.all(pe > 0)


def test_beta_eff_limits_match_documented_amplification():
    beta_d = -1.0e-9
    alpha_B, B = 0.8, 0.5
    omega_drain = 1.0

    beta_low, frac_low = beta_eff(beta_d, alpha_B, B, 1.0e-6, omega_drain)
    assert beta_low == pytest.approx(beta_d, rel=1e-6)
    assert frac_low == pytest.approx(0.0, abs=1e-12)

    beta_high, frac_high = beta_eff(beta_d, alpha_B, B, 1.0e6, omega_drain)
    expected = beta_d * beta_ratio_undrained_to_drained(alpha_B, B)
    assert beta_high == pytest.approx(expected, rel=1e-6)
    assert frac_high == pytest.approx(1.0, rel=1e-12)


def test_beta_eff_rejects_singular_coupling():
    with pytest.raises(ValueError):
        beta_eff(-1.0e-9, alpha_B=1.0, B=1.0, omega=1.0, omega_drain=1.0)


def test_beta_drained_is_stress_sensitivity():
    assert beta_drained(100.0, 5.0e8) == pytest.approx(-1.0e-7)


def test_thermoelastic_sensitivity_uses_dimensionless_derivative():
    s_t = thermoelastic_sensitivity_s_T(
        nu=0.25,
        alpha_thermal=1.0e-5,
        mu_prime_norm=100.0,
        Vs=2500.0,
        rho=2500.0,
    )
    assert s_t == pytest.approx(2 * (1.25 / 0.75) * 1.0e-5 * 100.0)

    inferred, s_t_back = thermoelastic_from_fitted_amplitude(
        dvv_amp_pct_per_K=s_t * 100.0,
        nu=0.25,
        Vs=2500.0,
        rho=2500.0,
        alpha_thermal=1.0e-5,
    )
    assert s_t_back == pytest.approx(s_t)
    assert inferred == pytest.approx(100.0)
