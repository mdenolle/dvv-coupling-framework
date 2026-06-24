# Changelog

All notable changes to this project are documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

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
