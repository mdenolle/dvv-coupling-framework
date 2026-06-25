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

from pydantic import BaseModel, ConfigDict, Field, computed_field, model_validator

try:  # package import
    from .poroelastic_framework import (
        OMEGA_ANNUAL,
        OMEGA_DAILY,
        bridge_beta,
        bulk_modulus,
        classify_drainage,
        drainage_peclet,
        drained_bulk_modulus,
        mu_prime_from_bridge,
        sensitivity_depth,
    )
except ImportError:  # flat import (run from within analysis/)
    from poroelastic_framework import (
        OMEGA_ANNUAL,
        OMEGA_DAILY,
        bridge_beta,
        bulk_modulus,
        classify_drainage,
        drainage_peclet,
        drained_bulk_modulus,
        mu_prime_from_bridge,
        sensitivity_depth,
    )

DepthRule = Literal["third_wavelength", "half_wavelength", "quarter_wavelength"]
Regime = Literal["drained", "undrained"]
BetaSource = Literal["bridge", "published"]

#: Relative tolerance for the bridge-consistency check (β vs -μ'κ/2μ).
_BRIDGE_RTOL = 0.03


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
                    "Vp": 4500.0,
                    "rho": 2500.0,
                    "mu_prime": 251.0,
                    "beta": -240.0,
                    "alpha_B": 0.7,
                    "B_skemp": 0.4,
                    "perm": 1e-15,
                    "phi": 0.05,
                    "depth": 800.0,
                    "regime": "undrained",
                    "beta_source": "bridge",
                    "kappa_T": 1.0e-6,
                    "alpha_T": 8e-6,
                }
            ]
        },
    )

    name: str = Field(..., min_length=1, description="Site label")
    Vs: float = Field(..., gt=0, description="Shear-wave velocity [m/s]")
    Vp: float = Field(..., gt=0, description="Compressional-wave velocity [m/s]")
    rho: float = Field(..., gt=0, description="Bulk density [kg/m^3]")
    mu_prime: float = Field(..., description="dmu/dP, normalized shear-pressure sensitivity")
    beta: float = Field(..., description="Strain-domain acoustoelastic parameter (typ. < 0)")
    alpha_B: float = Field(..., ge=0.0, le=1.0, description="Biot coefficient")
    B_skemp: float = Field(..., ge=0.0, le=1.0, description="Skempton B coefficient")
    perm: float = Field(..., gt=0, description="Permeability [m^2]")
    phi: float = Field(..., ge=0.0, le=1.0, description="Porosity")
    depth: float = Field(..., gt=0, description="Sensitivity depth [m]")
    regime: Regime = Field(
        "undrained",
        description="Loading regime selecting which kappa enters the bridge "
        "(set from the data-driven Peclet number; see provenance_tables.md)",
    )
    beta_source: BetaSource = Field(
        "bridge",
        description="'bridge' = beta derived from -mu'*kappa/(2mu); "
        "'published' = beta calibrated in the source (e.g. Cascadia/Kidiwela)",
    )
    kappa_T: float = Field(1.0e-6, gt=0, description="Thermal diffusivity [m^2/s]")
    alpha_T: float = Field(8.0e-6, gt=0, description="Thermal expansion [1/K]")

    @computed_field  # type: ignore[prop-decorator]
    @property
    def mu(self) -> float:
        """Shear modulus mu = rho * Vs**2 [Pa] (regime-independent)."""
        return self.rho * self.Vs**2

    @computed_field  # type: ignore[prop-decorator]
    @property
    def kappa_u(self) -> float:
        """Undrained (seismic-band) bulk modulus rho(Vp^2 - 4/3 Vs^2) [Pa]."""
        return float(bulk_modulus(self.Vp, self.Vs, self.rho))

    @computed_field  # type: ignore[prop-decorator]
    @property
    def kappa_d(self) -> float:
        """Drained bulk modulus kappa_u * (1 - alpha_B * B) [Pa]."""
        return float(drained_bulk_modulus(self.kappa_u, self.alpha_B, self.B_skemp))

    @computed_field  # type: ignore[prop-decorator]
    @property
    def kappa(self) -> float:
        """Regime-appropriate bulk modulus that enters the bridge relation."""
        return self.kappa_u if self.regime == "undrained" else self.kappa_d

    @computed_field  # type: ignore[prop-decorator]
    @property
    def nu(self) -> float:
        """Poisson ratio implied by mu and the regime kappa (k>mu => nu>0.2)."""
        k, m = self.kappa, self.mu
        return (3 * k - 2 * m) / (2 * (3 * k + m))

    @computed_field  # type: ignore[prop-decorator]
    @property
    def beta_bridge(self) -> float:
        """Strain-domain beta predicted by the bridge at the regime kappa."""
        return float(bridge_beta(self.mu_prime, self.kappa, self.mu))

    @model_validator(mode="after")
    def _check_bridge_consistency(self) -> "SiteConfig":
        """Enforce claim 1: a 'bridge'-sourced beta must satisfy -mu'*kappa/(2mu).

        'published' betas (e.g. the borehole-calibrated Cascadia value) are
        exempt from the equality but their implied mu' is still available via
        :attr:`mu_prime` for the consistency check.
        """
        if self.beta_source == "bridge":
            predicted = self.beta_bridge
            if predicted == 0 or abs(self.beta - predicted) > _BRIDGE_RTOL * abs(predicted):
                raise ValueError(
                    f"{self.name}: stored beta={self.beta:.1f} violates the bridge "
                    f"relation (-mu'*kappa/2mu={predicted:.1f}, rtol={_BRIDGE_RTOL}). "
                    "Set beta to the bridge value or mark beta_source='published'."
                )
        return self


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

# All numerical values are grounded in docs/site_analyses/provenance_tables.md.
# beta_source='bridge' => beta == -mu'*kappa/(2mu) (enforced); 'published' =>
# beta is calibrated in the cited source and the bridge is a consistency check.

#: Parkfield: fractured Salinian granite at ~0.8 km depth (SAFOD; Okubo 2024).
#: Regime drained->transitional (Pe<1); we report the seismic kappa_u endpoint.
PARKFIELD = SiteConfig(
    name="Parkfield (granite)",
    Vs=2500.0,     # SAFOD, 0.8 km weathered granite
    Vp=4500.0,     # -> kappa_u = 29.8 GPa, mu = 15.6 GPa
    rho=2500.0,
    mu_prime=251.0,
    beta=-240.0,   # directional (axial); bridge-consistent w/ kappa_u
    beta_source="bridge",
    regime="undrained",
    alpha_B=0.7,
    B_skemp=0.4,
    perm=1e-15,
    phi=0.05,
    depth=800.0,
    kappa_T=1.0e-6,
    alpha_T=8e-6,
)

#: Cascadia: marine sediment ~0.2 km below the seafloor (Kidiwela 2026).
#: Pe ~= 2.5 (transitional->undrained) => seismic kappa_u justified.
CASCADIA = SiteConfig(
    name="Cascadia (sediment)",
    Vs=500.0,      # paper 9.2.2 (Han 2017; USGS CVM)
    Vp=1700.0,     # -> kappa_u = 4.86 GPa, mu = 0.475 GPa
    rho=1900.0,
    mu_prime=618.0,        # consistency-check output: -2mu*beta/kappa_u
    beta=-3160.0,          # PUBLISHED: borehole-calibrated (Kidiwela 2026)
    beta_source="published",
    regime="undrained",
    alpha_B=0.95,
    B_skemp=0.75,
    perm=1e-13,
    phi=0.40,
    depth=200.0,
    kappa_T=0.5e-6,
    alpha_T=5e-6,
)

#: Nepal Himalayas: post-Gorkha earthquake crust (Illien et al. 2022).
#: ILLUSTRATIVE preset (not part of the §9 three-site application): the moduli
#: and beta are bridge-consistent example values, not a calibrated fit.
NEPAL = SiteConfig(
    name="Nepal (post-earthquake)",
    Vs=1500.0,
    Vp=2600.0,     # Vp/Vs ~ 1.73 crust -> kappa_u = 9.02 GPa
    rho=2400.0,
    mu_prime=150.0,
    beta=-125.3,   # bridge value at kappa_u
    beta_source="bridge",
    regime="undrained",
    alpha_B=0.8,
    B_skemp=0.5,
    perm=1e-14,
    phi=0.10,
    depth=300.0,
    kappa_T=0.8e-6,
    alpha_T=7e-6,
)

#: Agricultural soil: vadose zone, partially saturated (Shi et al. 2026).
#: ILLUSTRATIVE preset (not part of the §9 three-site application): the moduli
#: and beta are bridge-consistent example values, not a calibrated fit.
AGRICULTURAL = SiteConfig(
    name="Agricultural soil",
    Vs=200.0,
    Vp=450.0,      # low Vp (air in pores) -> kappa_u = 0.239 GPa
    rho=1600.0,
    mu_prime=2000.0,
    beta=-3730.0,  # bridge value at kappa_u
    beta_source="bridge",
    regime="undrained",
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


def mu_prime_consistency(site: SiteConfig) -> float:
    """mu' implied by the site's beta and regime kappa, via the inverse bridge.

    For a 'published' beta (e.g. Cascadia/Kidiwela) this is the consistency
    check: it should match the stored ``site.mu_prime``.
    """
    return float(mu_prime_from_bridge(site.beta, site.kappa, site.mu))


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

