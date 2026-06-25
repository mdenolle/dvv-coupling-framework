"""Core research APIs for reproducible dv/v measurement design.

The package starts with coda-window selection metrics because choices of
frequency band, lapse-time window, and substack length are a primary source of
method dependence in ambient-noise velocity-change studies.
"""

from .window_selection import (
    CodaWindow,
    WindowSensitivityDiagnostic,
    LapseProfile,
    WindowEstimate,
    WindowScore,
    apparent_velocity,
    window_sensitivity_diagnostic,
    characteristic_depth,
    candidate_windows,
    cycles_score,
    depth_score,
    kernel_overlap_score,
    rank_windows,
    rolling_lapse_windows,
    score_window,
    score_lapse_profile,
    substack_resolution_score,
    surface_wave_lapse_score,
)

__version__ = "0.1.0"

__all__ = [
    "CodaWindow",
    "WindowSensitivityDiagnostic",
    "LapseProfile",
    "WindowEstimate",
    "WindowScore",
    "apparent_velocity",
    "window_sensitivity_diagnostic",
    "characteristic_depth",
    "candidate_windows",
    "cycles_score",
    "depth_score",
    "kernel_overlap_score",
    "rank_windows",
    "rolling_lapse_windows",
    "score_window",
    "score_lapse_profile",
    "substack_resolution_score",
    "surface_wave_lapse_score",
    "__version__",
]
