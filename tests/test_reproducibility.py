"""Reproducibility and smoke tests for the diagnostic-case workflows."""

import numpy as np

from analysis import (
    PARKFIELD,
    AnalysisConfig,
    case1_split_window_regression,
    case3_tidal_beta_evolution,
)
from analysis.coupling_diagnostic_cases import (
    generate_california_synthetic,
    generate_parkfield_synthetic,
)


def test_california_synthetic_is_deterministic():
    np.random.seed(42)
    a = generate_california_synthetic(years=(2015, 2018))
    np.random.seed(42)
    b = generate_california_synthetic(years=(2015, 2018))
    assert np.allclose(a["dvv"], b["dvv"])
    assert len(a["dvv"]) == len(a["t_days"])


def test_parkfield_synthetic_has_signal():
    np.random.seed(0)
    data = generate_parkfield_synthetic(years=(2001, 2006))
    assert np.nanstd(data["dvv"]) > 0


def test_case1_dry_run_does_not_compute():
    np.random.seed(1)
    data = generate_california_synthetic(years=(2015, 2018))
    cfg = AnalysisConfig(site=PARKFIELD)
    result = case1_split_window_regression(data, config=cfg, dry_run=True)
    assert result["status"] == "dry_run"
    assert result["params"]["n_samples"] == len(data["t_days"])


def test_case3_dry_run_reports_params():
    np.random.seed(2)
    data = generate_parkfield_synthetic(years=(2001, 2006))
    result = case3_tidal_beta_evolution(data, stack_days=180, dry_run=True)
    assert result["status"] == "dry_run"
    assert result["params"]["stack_days"] == 180
