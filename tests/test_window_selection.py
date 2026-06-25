"""Tests for codameter coda-window selection metrics."""

import pytest

from codameter import (
    CodaWindow,
    WindowEstimate,
    window_sensitivity_diagnostic,
    candidate_windows,
    characteristic_depth,
    cycles_score,
    depth_score,
    rank_windows,
    rolling_lapse_windows,
    score_lapse_profile,
    score_window,
    surface_wave_lapse_score,
)


def test_window_validates_bounds():
    with pytest.raises(ValueError):
        CodaWindow(start_s=10, end_s=5, fmin_hz=1, fmax_hz=2)
    with pytest.raises(ValueError):
        CodaWindow(start_s=0, end_s=5, fmin_hz=2, fmax_hz=1)


def test_cycles_score_penalizes_too_short_window():
    short = CodaWindow(start_s=0, end_s=2, fmin_hz=1, fmax_hz=2)
    long = CodaWindow(start_s=0, end_s=12, fmin_hz=1, fmax_hz=2)
    assert cycles_score(short) < 1.0
    assert cycles_score(long) == pytest.approx(1.0)


def test_surface_wave_lapse_score_prefers_rayleigh_consistent_lapse():
    early = CodaWindow(start_s=4, end_s=6, fmin_hz=2, fmax_hz=4)
    late = CodaWindow(start_s=18, end_s=22, fmin_hz=2, fmax_hz=4)
    distance_m = 5000.0
    rayleigh_velocity_mps = 1000.0
    assert surface_wave_lapse_score(early, distance_m, rayleigh_velocity_mps) > 0.95
    assert surface_wave_lapse_score(late, distance_m, rayleigh_velocity_mps) < 0.1


def test_depth_score_prefers_frequency_targeting_depth():
    high_freq = CodaWindow(start_s=4, end_s=16, fmin_hz=2, fmax_hz=4)
    low_freq = CodaWindow(start_s=4, end_s=16, fmin_hz=0.25, fmax_hz=0.5)
    assert characteristic_depth(high_freq, vs_mps=1500.0) < characteristic_depth(
        low_freq, vs_mps=1500.0
    )
    assert depth_score(high_freq, vs_mps=1500.0, target_depth_range_m=(100, 250)) > 0.9
    assert depth_score(low_freq, vs_mps=1500.0, target_depth_range_m=(100, 250)) < 0.1


def test_rank_windows_combines_observation_and_physics_scores():
    good = CodaWindow(start_s=4, end_s=16, fmin_hz=2, fmax_hz=4, label="good")
    bad = CodaWindow(start_s=20, end_s=32, fmin_hz=2, fmax_hz=4, label="bad")
    ranked = rank_windows(
        [bad, good],
        observations={
            "good": {"coherence": 0.9, "snr": 10.0, "dvv_sigma": 2e-5},
            "bad": {"coherence": 0.4, "snr": 2.0, "dvv_sigma": 2e-4},
        },
        distance_m=10000.0,
        rayleigh_group_velocity_mps=1000.0,
        vs_mps=1500.0,
        target_depth_range_m=(100, 250),
    )
    assert ranked[0].window is good
    assert ranked[0].score > ranked[1].score
    assert "low_wave_type" in ranked[1].flags


def test_candidate_window_grid_size():
    windows = candidate_windows(
        starts_s=[2, 4],
        durations_s=[8, 12],
        bands_hz=[(1, 2), (2, 4)],
        substacks_days=[7, 14],
    )
    assert len(windows) == 16
    assert all(window.duration_s in {8, 12} for window in windows)


def test_rolling_lapse_windows_walk_from_early_to_late():
    windows = rolling_lapse_windows(
        start_s=2,
        stop_s=10,
        window_duration_s=4,
        step_s=2,
        fmin_hz=2,
        fmax_hz=4,
    )
    assert [(w.start_s, w.end_s) for w in windows] == [(2, 6), (4, 8), (6, 10)]
    assert [w.label for w in windows] == ["lapse_000", "lapse_001", "lapse_002"]


def test_score_lapse_profile_preserves_early_to_late_order():
    windows = rolling_lapse_windows(
        start_s=2,
        stop_s=14,
        window_duration_s=4,
        step_s=4,
        fmin_hz=2,
        fmax_hz=4,
    )
    profile = score_lapse_profile(
        windows,
        observations={
            "lapse_000": {"coherence": 0.9, "snr": 10.0},
            "lapse_001": {"coherence": 0.8, "snr": 8.0},
            "lapse_002": {"coherence": 0.4, "snr": 2.0},
        },
        distance_m=4000.0,
        rayleigh_group_velocity_mps=1000.0,
        vs_mps=1500.0,
        target_depth_range_m=(100, 250),
    )
    assert list(profile.centers_s) == [4.0, 8.0, 12.0]
    assert profile.scores[0].window.label == "lapse_000"
    assert profile.ranked()[0].score >= profile.ranked()[-1].score


def test_window_sensitivity_diagnostic_decomposes_method_uncertainty():
    windows = rolling_lapse_windows(
        start_s=2,
        stop_s=14,
        window_duration_s=4,
        step_s=4,
        fmin_hz=2,
        fmax_hz=4,
    )
    profile = score_lapse_profile(
        windows,
        observations={
            "lapse_000": {"coherence": 0.9, "snr": 10.0},
            "lapse_001": {"coherence": 0.9, "snr": 10.0},
            "lapse_002": {"coherence": 0.9, "snr": 10.0},
        },
    )
    posterior = window_sensitivity_diagnostic(
        profile,
        estimates={
            "lapse_000": WindowEstimate(mean=1.0e-4, sigma=1.0e-5),
            "lapse_001": WindowEstimate(mean=1.1e-4, sigma=1.0e-5),
            "lapse_002": WindowEstimate(mean=4.0e-4, sigma=1.0e-5),
        },
    )
    assert posterior.mean > 1.0e-4
    assert posterior.epistemic_sigma > posterior.aleatoric_sigma
    assert posterior.total_variance == pytest.approx(
        posterior.aleatoric_variance + posterior.epistemic_variance
    )
    assert sum(posterior.weights.values()) == pytest.approx(1.0)


def test_score_window_works_with_partial_context():
    window = CodaWindow(start_s=4, end_s=16, fmin_hz=1, fmax_hz=2)
    score = score_window(window, coherence=0.8, snr=8)
    assert score.metrics["coherence"] == pytest.approx(0.8)
    assert score.metrics["snr"] > 0.7
    assert 0 <= score.score <= 1
