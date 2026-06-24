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
    validate_and_summarize,
)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _valid_site_kwargs(**overrides):
    base = dict(
        name="test",
        Vs=2500.0,
        rho=2500.0,
        nu=0.25,
        mu_prime=251.0,
        beta=-240.0,
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
    assert site.kappa > site.mu  # for nu = 0.25, kappa > mu


@pytest.mark.parametrize(
    "overrides",
    [
        {"Vs": -1.0},
        {"rho": 0.0},
        {"alpha_B": 1.5},
        {"alpha_B": -0.1},
        {"B_skemp": 2.0},
        {"phi": 1.5},
        {"nu": 0.5},
        {"perm": 0.0},
        {"depth": -10.0},
        {"name": ""},
    ],
)
def test_siteconfig_rejects_invalid(overrides):
    with pytest.raises(ValidationError):
        SiteConfig(**_valid_site_kwargs(**overrides))


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


def test_yaml_presets_load():
    files = glob.glob(os.path.join(ROOT, "presets", "*.yaml"))
    assert files, "no preset YAML files found"
    for path in files:
        cfg = load_analysis_config(path)
        assert isinstance(cfg, AnalysisConfig)
        assert cfg.site.Vs > 0
