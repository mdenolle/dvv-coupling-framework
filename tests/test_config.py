"""Tests for the validated configuration schema and presets."""

import glob
import os

import pytest
from pydantic import ValidationError

from analysis.config import (
    AGRICULTURAL,
    CASCADIA,
    NEPAL,
    PARKFIELD,
    PRESETS,
    AnalysisConfig,
    SiteConfig,
    get_defaults,
    load_analysis_config,
    mu_prime_consistency,
    validate_and_summarize,
)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _valid_site_kwargs(**overrides):
    base = dict(
        name="test",
        Vs=2500.0,
        Vp=4500.0,
        rho=2500.0,
        mu_prime=251.0,
        beta=-240.0,
        beta_source="bridge",
        regime="undrained",
        alpha_B=0.7,
        B_skemp=0.4,
        perm=1e-15,
        phi=0.05,
        depth=800.0,
    )
    base.update(overrides)
    return base


def test_siteconfig_computes_moduli():
    site = SiteConfig(**_valid_site_kwargs())
    assert site.mu == pytest.approx(2500.0 * 2500.0**2)
    assert site.kappa_u > site.mu  # seismic kappa_u from Vp,Vs
    assert site.kappa_d < site.kappa_u  # drained < undrained
    assert 0.0 < site.nu < 0.5


@pytest.mark.parametrize(
    "overrides",
    [
        {"Vs": -1.0},
        {"Vp": 0.0},
        {"rho": 0.0},
        {"alpha_B": 1.5},
        {"alpha_B": -0.1},
        {"B_skemp": 2.0},
        {"phi": 1.5},
        {"perm": 0.0},
        {"depth": -10.0},
        {"name": ""},
    ],
)
def test_siteconfig_rejects_invalid(overrides):
    with pytest.raises(ValidationError):
        SiteConfig(**_valid_site_kwargs(**overrides))


def test_siteconfig_rejects_bridge_violating_beta():
    # beta that does not satisfy -mu'*kappa/(2mu) must be rejected unless
    # explicitly flagged as published.
    with pytest.raises(ValidationError):
        SiteConfig(**_valid_site_kwargs(beta=-50.0))
    # published source is exempt from the equality
    site = SiteConfig(**_valid_site_kwargs(beta=-50.0, beta_source="published"))
    assert site.beta == -50.0


def test_presets_satisfy_bridge_relation():
    from analysis.config import mu_prime_consistency
    for site in (PARKFIELD, NEPAL, AGRICULTURAL):
        # bridge-sourced presets: stored beta == bridge beta
        assert site.beta == pytest.approx(site.beta_bridge, rel=0.03)
    # Cascadia: published beta, but the implied mu' must match the stored mu'
    assert mu_prime_consistency(CASCADIA) == pytest.approx(CASCADIA.mu_prime, rel=0.03)


def test_siteconfig_is_frozen():
    site = SiteConfig(**_valid_site_kwargs())
    with pytest.raises(ValidationError):
        site.Vs = 100.0


def test_analysisconfig_defaults_match_get_defaults():
    cfg = AnalysisConfig(site=PARKFIELD)
    defaults = get_defaults()
    assert cfg.frequency_hz == defaults["frequency_hz"]
    assert cfg.rule == defaults["rule"]
    assert cfg.pe_drained_threshold == defaults["pe_drained_threshold"]


def test_analysisconfig_rejects_bad_frequency():
    with pytest.raises(ValidationError):
        AnalysisConfig(site=PARKFIELD, frequency_hz=0.0)


def test_presets_registry_complete():
    assert set(PRESETS) == {"parkfield", "cascadia", "nepal", "agricultural"}
    assert PRESETS["parkfield"] is PARKFIELD
    for site in (PARKFIELD, CASCADIA, NEPAL, AGRICULTURAL):
        assert isinstance(site, SiteConfig)


def test_validate_and_summarize_returns_text():
    summary = validate_and_summarize(AnalysisConfig(site=CASCADIA))
    assert "Cascadia" in summary
    assert "drainage regime" in summary


def test_golden_site_values():
    """Lock the grounded numbers from provenance_tables.md so they cannot drift."""
    # Parkfield: mu ~ 15.6 GPa, kappa_u ~ 29.8 GPa, mu' = 251, beta ~ -240.
    assert PARKFIELD.mu == pytest.approx(15.62e9, rel=0.01)
    assert PARKFIELD.kappa_u == pytest.approx(29.79e9, rel=0.01)
    assert PARKFIELD.beta == pytest.approx(-240.0, rel=0.01)

    # Cascadia: mu = 0.475 GPa, kappa_u = 4.86 GPa, published beta -3160,
    # implied mu' = 618 (NOT the superseded 1290).
    assert CASCADIA.mu == pytest.approx(0.475e9, rel=0.01)
    assert CASCADIA.kappa_u == pytest.approx(4.86e9, rel=0.01)
    assert mu_prime_consistency(CASCADIA) == pytest.approx(618.0, rel=0.02)
    # Stress rate 2 mu (dv/v) / mu' for dv/v=3.8e-4/yr -> ~0.58 kPa/yr.
    stress_rate = 2 * CASCADIA.mu * 3.8e-4 / mu_prime_consistency(CASCADIA)
    assert stress_rate == pytest.approx(584.0, rel=0.05)  # Pa/yr


def test_undrained_regime_uses_seismic_kappa():
    # In the undrained regime the bridge kappa is the seismic kappa_u.
    assert CASCADIA.regime == "undrained"
    assert CASCADIA.kappa == CASCADIA.kappa_u


def test_yaml_presets_match_python_presets():
    """Each YAML preset must construct and agree with its Python twin."""
    import os
    name_to_preset = {p.name: p for p in (PARKFIELD, CASCADIA, NEPAL, AGRICULTURAL)}
    for path in glob.glob(os.path.join(ROOT, "presets", "*.yaml")):
        cfg = load_analysis_config(path)
        twin = name_to_preset.get(cfg.site.name)
        if twin is None:
            continue
        assert cfg.site.Vp == pytest.approx(twin.Vp)
        assert cfg.site.beta == pytest.approx(twin.beta, rel=0.01)
        assert cfg.site.beta_source == twin.beta_source


def test_yaml_presets_load():
    files = glob.glob(os.path.join(ROOT, "presets", "*.yaml"))
    assert files, "no preset YAML files found"
    for path in files:
        cfg = load_analysis_config(path)
        assert isinstance(cfg, AnalysisConfig)
        assert cfg.site.Vs > 0
