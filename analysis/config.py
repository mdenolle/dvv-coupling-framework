"""
config.py
=========
Unified, validated input schema for the DVV coupling framework.

This module provides a single, discoverable source of truth for site
material properties (:class:`SiteConfig`) and analysis parameters
(:class:`AnalysisConfig`), replacing the ad-hoc ``Site`` container and the
defaults that were previously scattered across the analysis scripts.

The configs are `pydantic <https://docs.pydantic.dev>`_ models, so they are
programmatically introspectable (``SiteConfig.model_json_schema()``),
self-validating (out-of-range values raise a clear error), and importable as
named presets (``PARKFIELD``, ``CASCADIA``, ``NEPAL``, ``AGRICULTURAL``).

Examples
--------
>>> from analysis.config import PARKFIELD, AnalysisConfig, validate_and_summarize
>>> cfg = AnalysisConfig(site=PARKFIELD, frequency_hz=3.0)
>>> print(validate_and_summarize(cfg))  # doctest: +ELLIPSIS
Site: Parkfield (granite)
...
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, computed_field

try:  # package import
    from .poroelastic_framework import (
        OMEGA_ANNUAL,
        OMEGA_DAILY,
        classify_drainage,
        drainage_peclet,
        sensitivity_depth,
    )
except ImportError:  # flat import (run from within analysis/)
    from poroelastic_framework import (
        OMEGA_ANNUAL,
        OMEGA_DAILY,
        classify_drainage,
        drainage_peclet,
        sensitivity_depth,
    )

DepthRule = Literal["third_wavelength", "half_wavelength", "quarter_wavelength"]


class SiteConfig(BaseModel):
    """Physical properties of a monitoring site.

    All fields are validated on construction. The derived elastic moduli
    ``mu`` and ``kappa`` are computed from ``Vs``, ``rho`` and ``nu`` so they
    can never become inconsistent with the primary inputs.

    Parameters
    ----------
    name : str
        Human-readable site label.
    Vs : float
        Shear-wave velocity [m/s], must be > 0.
    rho : float
        Bulk density [kg/m^3], must be > 0.
    nu : float
        Drained Poisson ratio, in [0, 0.5).
    mu_prime : float
        Normalized pressure sensitivity of the shear modulus (dimensionless).
    beta : float
        Acoustoelastic stress sensitivity (typically negative).
    alpha_B : float
        Biot coefficient, in [0, 1].
    B_skemp : float
        Skempton's B coefficient, in [0, 1].
    perm : float
        Intrinsic permeability [m^2], must be > 0.
    phi : float
        Porosity, in [0, 1].
    depth : float
        Coda sensitivity depth [m], must be > 0.
    kappa_T : float
        Thermal diffusivity [m^2/s], must be > 0.
    alpha_T : float
        Linear thermal expansion coefficient [1/K], must be > 0.
    """

    model_config = ConfigDict(
        frozen=True,
        json_schema_extra={
            "examples": [
                {
                    "name": "Parkfield (granite)",
                    "Vs": 2500.0,
                    "rho": 2500.0,
                    "nu": 0.25,
                    "mu_prime": 251.0,
                    "beta": -240.0,
                    "alpha_B": 0.7,
                    "B_skemp": 0.4,
                    "perm": 1e-15,
                    "phi": 0.05,
                    "depth": 800.0,
                    "kappa_T": 1.0e-6,
                    "alpha_T": 8e-6,
                }
            ]
        },
    )

    name: str = Field(..., min_length=1, description="Site label")
    Vs: float = Field(..., gt=0, description="Shear-wave velocity [m/s]")
    rho: float = Field(..., gt=0, description="Bulk density [kg/m^3]")
    nu: float = Field(..., ge=0.0, lt=0.5, description="Drained Poisson ratio")
    mu_prime: float = Field(..., description="Normalized shear-pressure sensitivity")
    beta: float = Field(..., description="Acoustoelastic stress sensitivity")
    alpha_B: float = Field(..., ge=0.0, le=1.0, description="Biot coefficient")
    B_skemp: float = Field(..., ge=0.0, le=1.0, description="Skempton B coefficient")
    perm: float = Field(..., gt=0, description="Permeability [m^2]")
    phi: float = Field(..., ge=0.0, le=1.0, description="Porosity")
    depth: float = Field(..., gt=0, description="Sensitivity depth [m]")
    kappa_T: float = Field(1.0e-6, gt=0, description="Thermal diffusivity [m^2/s]")
    alpha_T: float = Field(8.0e-6, gt=0, description="Thermal expansion [1/K]")

    @computed_field  # type: ignore[prop-decorator]
    @property
    def mu(self) -> float:
        """Shear modulus mu = rho * Vs**2 [Pa]."""
        return self.rho * self.Vs**2

    @computed_field  # type: ignore[prop-decorator]
    @property
    def kappa(self) -> float:
        """Drained bulk modulus kappa = 2 mu (1 + nu) / (3 (1 - 2 nu)) [Pa]."""
        return 2 * self.mu * (1 + self.nu) / (3 * (1 - 2 * self.nu))


class AnalysisConfig(BaseModel):
    """Parameters controlling a single sensitivity / coupling analysis.

    Parameters
    ----------
    site : SiteConfig
        The site whose properties drive the analysis.
    frequency_hz : float
        Coda center frequency [Hz], must be > 0.
    rule : DepthRule
        Mapping from velocity and frequency to sensitivity depth.
    omega_forcing : float
        Angular frequency of the environmental forcing [rad/s]. Defaults to
        the annual cycle.
    pe_drained_threshold : float
        Peclet number below which the site is classified as drained.
    pe_undrained_threshold : float
        Peclet number above which the site is classified as undrained.
    """

    model_config = ConfigDict(frozen=True)

    site: SiteConfig
    frequency_hz: float = Field(3.0, gt=0, description="Coda center frequency [Hz]")
    rule: DepthRule = "third_wavelength"
    omega_forcing: float = Field(
        OMEGA_ANNUAL, gt=0, description="Forcing angular frequency [rad/s]"
    )
    pe_drained_threshold: float = Field(0.1, gt=0, description="Drained Pe cutoff")
    pe_undrained_threshold: float = Field(
        10.0, gt=0, description="Undrained Pe cutoff"
    )


# ─────────────────────────────────────────────────────────────────────────────
# Named site presets (literature-sourced; see coupling_tier_tests.py header)
# ─────────────────────────────────────────────────────────────────────────────

#: Parkfield: fractured Salinian granite at ~0.8 km depth (SAFOD).
PARKFIELD = SiteConfig(
    name="Parkfield (granite)",
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
    kappa_T=1.0e-6,
    alpha_T=8e-6,
)

#: Cascadia: marine sediment ~0.2 km below the seafloor.
CASCADIA = SiteConfig(
    name="Cascadia (sediment)",
    Vs=500.0,
    rho=1900.0,
    nu=0.40,
    mu_prime=618.0,
    beta=-3160.0,
    alpha_B=0.95,
    B_skemp=0.75,
    perm=1e-13,
    phi=0.40,
    depth=200.0,
    kappa_T=0.5e-6,
    alpha_T=5e-6,
)

#: Nepal Himalayas: post-Gorkha earthquake crust (Illien et al. 2022).
NEPAL = SiteConfig(
    name="Nepal (post-earthquake)",
    Vs=1500.0,
    rho=2400.0,
    nu=0.28,
    mu_prime=150.0,
    # Preserve the original derived value: -150 * kappa / (2 mu).
    beta=-150.0 * (2 * (2400.0 * 1500.0**2) * (1 + 0.28) / (3 * (1 - 2 * 0.28)))
    / (2 * (2400.0 * 1500.0**2)),
    alpha_B=0.8,
    B_skemp=0.5,
    perm=1e-14,
    phi=0.10,
    depth=300.0,
    kappa_T=0.8e-6,
    alpha_T=7e-6,
)

#: Agricultural soil: vadose zone (Shi et al. 2026).
AGRICULTURAL = SiteConfig(
    name="Agricultural soil",
    Vs=200.0,
    rho=1600.0,
    nu=0.35,
    mu_prime=2000.0,
    beta=-2000.0 * (2 * (1600.0 * 200.0**2) * (1 + 0.35) / (3 * (1 - 2 * 0.35)))
    / (2 * (1600.0 * 200.0**2)),
    alpha_B=0.99,
    B_skemp=0.90,
    perm=1e-11,
    phi=0.45,
    depth=5.0,
    kappa_T=0.3e-6,
    alpha_T=10e-6,
)

#: Registry of all named presets, keyed by a short identifier.
PRESETS: dict[str, SiteConfig] = {
    "parkfield": PARKFIELD,
    "cascadia": CASCADIA,
    "nepal": NEPAL,
    "agricultural": AGRICULTURAL,
}


def get_defaults() -> dict[str, object]:
    """Return every analysis default value from a single place.

    Returns
    -------
    dict
        Mapping of parameter name to default value. Mirrors the defaults
        declared on :class:`AnalysisConfig`.
    """
    return {
        "frequency_hz": 3.0,
        "rule": "third_wavelength",
        "omega_forcing": OMEGA_ANNUAL,
        "omega_daily": OMEGA_DAILY,
        "pe_drained_threshold": 0.1,
        "pe_undrained_threshold": 10.0,
        "kappa_T": 1.0e-6,
        "alpha_T": 8.0e-6,
    }


def validate_and_summarize(config: AnalysisConfig) -> str:
    """Validate a config and return a human-readable diagnostic summary.

    The summary reports the site properties, the sensitivity depth implied by
    the chosen frequency and rule, and the drainage regime at the forcing
    frequency. No figures are produced and no expensive computation is run, so
    this is safe to call as a dry-run before launching a full analysis.

    Parameters
    ----------
    config : AnalysisConfig
        A validated analysis configuration.

    Returns
    -------
    str
        Multi-line diagnostic summary.
    """
    site = config.site
    L = sensitivity_depth(site.Vs, config.frequency_hz, rule=config.rule)

    # Hydraulic diffusivity from permeability (water): c = k / (Ss * eta).
    eta = 1e-3  # Pa s, dynamic viscosity of water
    Ss = 1e-5  # 1/m, specific storage
    c = site.perm / (Ss * eta)

    labels, pe = classify_drainage(
        c,
        L,
        omega_forcing=config.omega_forcing,
        pe_drained=config.pe_drained_threshold,
        pe_undrained=config.pe_undrained_threshold,
    )
    pe_annual = float(drainage_peclet(c, L, omega_forcing=OMEGA_ANNUAL))

    lines = [
        f"Site: {site.name}",
        f"  Vs = {site.Vs:.0f} m/s, rho = {site.rho:.0f} kg/m^3, nu = {site.nu:.2f}",
        f"  mu = {site.mu / 1e9:.2f} GPa, kappa = {site.kappa / 1e9:.2f} GPa",
        f"  beta = {site.beta:.1f}, mu' = {site.mu_prime:.0f}",
        f"  alpha_B = {site.alpha_B:.2f}, B = {site.B_skemp:.2f}, "
        f"alpha_B*B = {site.alpha_B * site.B_skemp:.2f}",
        f"Analysis @ {config.frequency_hz:.2f} Hz (rule={config.rule}):",
        f"  sensitivity depth = {float(L):.1f} m",
        f"  hydraulic diffusivity c = {c:.2e} m^2/s",
        f"  drainage regime = {labels[0].upper()} (Pe = {float(pe[0]):.3g})",
        f"  Pe @ annual forcing = {pe_annual:.3g}",
    ]
    return "\n".join(lines)


def load_analysis_config(path: str | object) -> AnalysisConfig:
    """Build an :class:`AnalysisConfig` from a YAML preset file.

    The YAML file must contain a top-level ``site`` mapping (whose keys match
    :class:`SiteConfig` fields) and may contain an ``analysis`` mapping with
    any :class:`AnalysisConfig` overrides. Extra keys such as ``description``
    and ``reference`` are ignored.

    Parameters
    ----------
    path : str or path-like
        Path to a ``*.yaml`` preset file.

    Returns
    -------
    AnalysisConfig
        A fully validated configuration.
    """
    import yaml

    with open(path, "r", encoding="utf-8") as fh:
        spec = yaml.safe_load(fh)

    site = SiteConfig(**spec["site"])
    analysis_kwargs = spec.get("analysis", {}) or {}
    return AnalysisConfig(site=site, **analysis_kwargs)

