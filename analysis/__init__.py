"""DVV Coupling Framework — unified treatment of seismic velocity changes.

This package exposes the physical computations, the validated input schema,
and the diagnostic case workflows behind the manuscript *"Seismic Velocity
Changes as Stress and Strain Meters."*

Public API
----------
Configuration
    :class:`SiteConfig`, :class:`AnalysisConfig`, :func:`get_defaults`,
    :func:`validate_and_summarize`, and the named presets ``PARKFIELD``,
    ``CASCADIA``, ``NEPAL``, ``AGRICULTURAL``.
Physics
    :func:`sensitivity_depth`, :func:`drainage_frequency`,
    :func:`drainage_peclet`, :func:`classify_drainage`, and the elastic /
    poroelastic helpers.
Diagnostic cases
    :func:`case1_split_window_regression`, :func:`case2_saturation_sensitivity`,
    :func:`case3_tidal_beta_evolution`.

Examples
--------
>>> import analysis
>>> analysis.sensitivity_depth(2500, 2.0)
416.6...
"""

from .config import (
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
from .coupling_diagnostic_cases import (
    case1_split_window_regression,
    case2_saturation_sensitivity,
    case3_tidal_beta_evolution,
)
from .poroelastic_framework import (
    OMEGA_ANNUAL,
    OMEGA_DAILY,
    beta_drained,
    beta_eff,
    beta_ratio_undrained_to_drained,
    bulk_modulus,
    classify_drainage,
    drainage_frequency,
    drainage_peclet,
    poisson_ratio,
    sensitivity_depth,
    shear_modulus,
    skempton_B_empirical,
    undrained_poisson,
)

__version__ = "0.2.0"

__all__ = [
    # config
    "SiteConfig",
    "AnalysisConfig",
    "get_defaults",
    "validate_and_summarize",
    "load_analysis_config",
    "PARKFIELD",
    "CASCADIA",
    "NEPAL",
    "AGRICULTURAL",
    "PRESETS",
    # physics
    "sensitivity_depth",
    "drainage_frequency",
    "drainage_peclet",
    "classify_drainage",
    "poisson_ratio",
    "bulk_modulus",
    "shear_modulus",
    "skempton_B_empirical",
    "undrained_poisson",
    "beta_drained",
    "beta_eff",
    "beta_ratio_undrained_to_drained",
    "OMEGA_ANNUAL",
    "OMEGA_DAILY",
    # diagnostic cases
    "case1_split_window_regression",
    "case2_saturation_sensitivity",
    "case3_tidal_beta_evolution",
    "__version__",
]
