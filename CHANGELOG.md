# Changelog

All notable changes to this project are documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [0.3.0] - 2026-06-25

Audit remediation grounding the bridge relation (β = −μ′κ/2μ) and the
drainage regime in published / data-driven values. See
`docs/ai_documentation/08_full_research_audit_2026-06-25.md` and
`docs/site_analyses/provenance_tables.md`.

### Added
- **Provenance tables** (`docs/site_analyses/provenance_tables.md`): single
  source of truth tagging every site input as published `[P]` or
  framework-derived `[D]`, with the data-driven Péclet drainage regime.
- **Bridge machinery** in `poroelastic_framework.py`: `bridge_beta`,
  `mu_prime_from_bridge`, `drained_bulk_modulus`; `bulk_modulus` documented as
  the undrained (seismic-band) modulus.
- **`SiteConfig`**: `Vp` field; computed `kappa_u`/`kappa_d`/`kappa`(regime)/
  `nu`/`beta_bridge`; `regime` and `beta_source` fields; a model-validator that
  **enforces the bridge relation** for `beta_source="bridge"` presets.
- **Kīlauea site analysis** (`docs/site_analyses/kilauea_stress_analysis.md`).
- Tests: bridge consistency, ν_u ≥ ν_d invariant, golden site values,
  YAML↔Python preset agreement (53 tests total).

### Changed
- **Data-driven drainage regime**: regime now set by Pe = ωL²/c; Cascadia’s
  undrained κ_u (4.86 GPa) is justified by Pe ≈ 2.5 (not assumed). Manuscript
  §2.5/§9.2 and Table 1 updated.
- **Cascadia reconciled** to the grounded set: μ′ = 618, stress 0.58 kPa/yr
  (the site doc’s 1290 / 1.24 kPa/yr used the wrong velocity layer); β = −3160
  flagged as **published** (Kidiwela 2026) → bridge is a consistency check.
- **Tier-1 coupling figure** replaced (was an algebraic-cancellation artifact
  with a wrong undrained-Poisson formula) by an emergent β_eff(ω) frequency
  sweep grounded in each site’s drainage frequency.
- **Tier-2 pore pressure**: single dimensionally-consistent exponential-memory
  convolution (removed the two-branch hack with the undocumented ×365 factor).
- Notebooks: split μ′ (=dμ/dP) from S_σ (=∂(ρv²)/∂σ_c); removed NB1 ad-hoc
  Berger components; replaced NB6 fabricated error map with a real disba-kernel
  computation; corrected nonlinearity-demo coefficients and prose constants.

### Fixed
- Biot coefficient in `skempton_B_from_velocities` (uses grain modulus, not K_sat).
- Reproducibility: seeded RNG in coupling scripts.

## [0.2.0] - 2026-06-06

### Added
- **Validated input contract** (`analysis/config.py`): immutable `SiteConfig`
  and `AnalysisConfig` pydantic models with physical-bound validation,
  computed `mu`/`kappa` properties, and `validate_and_summarize()`.
- **Literature-sourced presets**: `PARKFIELD`, `CASCADIA`, `NEPAL`,
  `AGRICULTURAL`, plus matching YAML recipes under `presets/`.
- **Test suite** (`tests/`): 28 tests covering the poroelastic framework,
  config validation, and synthetic-data reproducibility.
- **Packaging**: `pyproject.toml` (editable install, `[test]` and
  `[notebooks]` extras) and an importable `analysis` package with `__all__`.
- **Agent affordances**: `docs/tutorials.yaml` machine-readable example index,
  `dry_run` mode for diagnostic cases, `docs/data_sources.md`,
  `docs/troubleshooting.md`, and a `00_quickstart.ipynb` notebook.
- **Continuous integration**: GitHub Actions workflow running `pytest`.
- **`pixi run test`** task.

### Changed
- Type hints added across `analysis/poroelastic_framework.py`.
- `coupling_tier_tests.py` now imports presets from `analysis.config` instead
  of an inline `Site` class.
- Figure output directory is now repo-relative and configurable via
  `DVV_FIGDIR` (replaces the hardcoded `/home/claude/figures` path).

## [0.1.0] - Initial release

### Added
- Six analysis notebooks (thermoelastic, hydrological, nonlinear elasticity,
  stress anisotropy, rheological models, sensitivity/validity).
- Poroelastic coupling framework and tier/diagnostic case scripts.
- Manuscript draft and AI-traceability documentation.
