# Code Review: dvv-coupling-framework

**Reviewed:** June 6, 2026  
**Reviewer:** Claude Haiku (GitHub Copilot)  
**Repo state:** commit unknown (version 0.1.0 per CITATION.cff L3)

## Summary

This is a research-framework repository containing a unified theoretical treatment of seismic velocity changes (dv/v) across environmental, tectonic, and volcanic settings, implemented as Jupyter notebooks and Python analysis scripts. The work is scientifically mature (includes a peer-reviewed manuscript, three quantitative application cases, and comprehensive AI-transparency documentation), but **it sits at the early-to-mid stage of software maturity**: installation is reproducible via pixi, core computational functions exist with docstrings, but critical user-facing infrastructure is missing (no test suite, no input schema, no quick-start example, notebooks haven't been executed). Onboarding for someone outside the core team would be slow.

## Dimension Scores

| # | Dimension | Grade | One-line summary |
|---|---|---|---|
| 1 | Onboarding | 🟡 | README describes scope clearly but lacks quick-start and copy-paste example |
| 2 | Input Contract | 🔴 | Material properties hardcoded in Site class; no unified input schema or validation |
| 3 | API & Code Quality | 🟡 | Docstrings and functions exist but no tests, no releases tagged, no type hints on all signatures |
| 4 | Workflow Examples | 🟡 | Six notebooks exist but unexecuted; external data dependencies undocumented; no quick start |
| 5 | Failure Modes | 🟡 | Known limitations documented in review files and manuscript; no active issue tracker visible |
| 6 | Reproducibility | 🟡 | pixi.toml pins dependencies; notebooks unexecuted so outputs unchecked; external data undocumented |
| 7 | Agent Affordances | 🔴 | Site class exists but not importable; no tutorial index; no dry-run / plan mode; defaults scattered |

---

## Per-Dimension Findings

### 1. Onboarding — 🟡

**What's working:**
- [README.md](README.md#L11) opens with a clear, scientifically motivated statement: "Seismic Velocity Changes as Stress and Strain Meters: A Unified Framework…"
- [Repository structure](README.md#L24-L42) is explicitly documented with clear folder purposes (paper, analysis, figures, docs).
- [Installation instructions](README.md#L44-L51) are explicit and current (pixi with pinned versions in pixi.toml).
- [Paper and data](README.md#L28-L30) links are clear; LICENSE and CITATION.cff present.
- Scope of framework is well articulated ([README.md](README.md#L17-L23)): connects Murnaghan elasticity → thermoelastic → poroelastic → anisotropy models.

**Gaps:**
- **No "Quick Start" section.** The README jumps from installation to "Reproducing Figures" ([README.md](README.md#L53-L60)) but provides no minimal copy-paste example a user can run in < 2 minutes.
- **No example code in README.** Users cannot see `import dvv_coupling; result = dvv_coupling.compute_something(...)` before investing in setup.
- **Scope statement incomplete.** The README declares what the code *does* (connects six theories) but does not explicitly state what it *doesn't* do (e.g., "Does not include inversion" or "Does not process raw seismic data").
- **Installation lacks pip/conda alternatives.** Only pixi is documented; users on systems without pixi may be confused.
- **No description in GitHub sidebar visible** (cannot verify without accessing GitHub web, but typically repos should have a one-liner in the GitHub "About" section).

**Suggestions (in priority order):**

1. Add a **"Quick Start"** section to [README.md](README.md) after the installation block (around L52). Include a minimal 8-line Python snippet that:
   - Imports one public function (e.g., `sensitivity_depth` from `poroelastic_framework`)
   - Computes a result (e.g., coda sensitivity depth at 2 Hz, Vs=2500 m/s)
   - Prints the output
   - Example: 
     ```python
     from analysis.poroelastic_framework import sensitivity_depth
     L_m = sensitivity_depth(Vs_mps=2500, freq_hz=2.0, rule="third_wavelength")
     print(f"Coda sensitivity depth: {L_m:.1f} m")
     ```

2. Add a **"What This Code Does and Doesn't Do"** section to [README.md](README.md#L16) (after the opening paragraph), 2–3 bullet points:
   - ✓ Computes forward models of dv/v under thermoelastic, hydrological, and poroelastic forcing
   - ✓ Scenario examples at Parkfield, Cascadia, agricultural soils
   - ✓ Demonstrates tier-wise coupling diagnostics
   - ✗ Does not process raw seismic waveforms or ambient noise correlations
   - ✗ Does not perform Bayesian inversion (framework proposed but not implemented)

3. Update [pixi.toml](pixi.toml#L1) or add an alternative installation section to [README.md](README.md) documenting pip install from GitHub (if user does not have pixi):
   ```bash
   pip install git+https://github.com/mdenolle/dvv-coupling-framework.git
   ```
   (requires that the repo be packaged as a Python package with setup.py or pyproject.toml—see Action Item #1 below).

---

### 2. Input Contract — 🔴

**What's working:**
- A `Site` class exists ([coupling_tier_tests.py](analysis/coupling_tier_tests.py#L44-L45)) that groups material properties (Vs, rho, mu, beta, alpha_B, etc.).
- Three concrete site instances (parkfield, cascadia, nepal) are defined with literature-sourced values ([coupling_tier_tests.py](analysis/coupling_tier_tests.py#L48-L100)).
- Function signatures in [poroelastic_framework.py](analysis/poroelastic_framework.py#L47-L65) include parameter documentation (Vs_mps, freq_hz, rule).

**Gaps:**
- **No unified input schema class.** The main entry points are scattered across three modules (coupling_diagnostic_cases.py, coupling_tier_tests.py, poroelastic_framework.py) with different function signatures and no central schema.
- **Site properties are not validated.** Creating a new Site requires manually setting 18 attributes ([coupling_tier_tests.py](analysis/coupling_tier_tests.py#L48-L100)), and there is no `__post_init__` or validation method to catch invalid ranges (e.g., negative Vs, unphysical beta).
- **Defaults scattered across code.** Default frequency = 3.0 Hz (hardcoded in [07_tier1_california_test.py](analysis/07_tier1_california_test.py#L38)), default pe_drained = 0.1 ([poroelastic_framework.py](analysis/poroelastic_framework.py#L100)), default phi = 0.3 ([coupling_diagnostic_cases.py](analysis/coupling_diagnostic_cases.py#L68))—no single source of truth.
- **No constraint declarations.** Valid ranges for beta, alpha_B, porosity are mentioned in prose (manuscript) but not codified in the schema. E.g., "[coupling_tier_tests.py](analysis/coupling_tier_tests.py#L74) hardcodes cascadia.beta = -3160.0" but there's no assertion that beta is in a valid range.
- **No validation function.** A user cannot call `validate_site(parkfield)` or `Site.validate()` to check before running a 6-hour analysis.
- **Material database not reusable.** The Site instances are module-level variables ([coupling_tier_tests.py](analysis/coupling_tier_tests.py#L48-L100)), not importable from a config module.

**Suggestions (in priority order):**

1. **Create a `Config` class** (dataclass or pydantic) in a new file [analysis/config.py](analysis/config.py) with two nested classes:
   - `SiteConfig`: Defines required fields (Vs, rho, mu_prime, beta, alpha_B, porosity, depth, kappa_T, alpha_T) with type hints and docstrings.
   - `AnalysisConfig`: Defines frequency_hz, rule, omega_forcing, and regime thresholds (pe_drained, pe_undrained).
   Example structure:
   ```python
   from dataclasses import dataclass, field
   from typing import Literal
   
   @dataclass
   class SiteConfig:
       """Physical properties of a site."""
       name: str
       Vs: float  # m/s, must be > 0
       rho: float  # kg/m³, must be > 0
       mu_prime: float  # nonlinear constant, typically negative
       beta: float  # stress sensitivity, typically negative
       alpha_B: float  # Biot coefficient, 0 <= alpha_B <= 1
       porosity: float  # 0 <= porosity <= 1
       depth: float  # sensitivity depth, m
       
       def __post_init__(self):
           if self.Vs <= 0 or self.rho <= 0:
               raise ValueError(f"Vs and rho must be positive")
           if not (0 <= self.alpha_B <= 1):
               raise ValueError(f"alpha_B must be in [0, 1], got {self.alpha_B}")
   
   @dataclass
   class AnalysisConfig:
       """Parameters for a sensitivity analysis run."""
       site: SiteConfig
       frequency_hz: float = 3.0
       rule: Literal["third_wavelength", "half_wavelength", "quarter_wavelength"] = "third_wavelength"
       pe_drained_threshold: float = 0.1
       pe_undrained_threshold: float = 10.0
   ```
   Add a `validate()` method to SiteConfig and move Parkfield, Cascadia, etc. to instance creation:
   ```python
   PARKFIELD = SiteConfig(name="Parkfield (granite)", Vs=2500.0, ...)
   CASCADIA = SiteConfig(name="Cascadia (sediment)", Vs=500.0, ...)
   ```

2. Update entry points in [coupling_diagnostic_cases.py](analysis/coupling_diagnostic_cases.py#L96), [coupling_tier_tests.py](analysis/coupling_tier_tests.py#L127) to accept a `AnalysisConfig` parameter instead of scattered kwargs. E.g.:
   ```python
   def case1_split_window_regression(config: AnalysisConfig, data, window_years=2.0):
       """..."""
   ```

3. Document constraints in the config docstrings (ranges, cross-field rules). E.g., "depth must be compatible with frequency_hz via sensitivity_depth(Vs, freq)."

---

### 3. API & Code Quality — 🟡

**What's working:**
- Public functions have docstrings: [sensitivity_depth](analysis/poroelastic_framework.py#L47-L65) includes Parameters, Returns, and a description.
- Functions use **consistent parameter naming** (Vs_mps for velocity in m/s, L_m for depth in meters) which aids machine readability.
- Core computations are **unit-explicit** ([poroelastic_framework.py](analysis/poroelastic_framework.py#L16-L23): OMEGA_ANNUAL, RHO_WATER in SI units).
- Analysis scripts are **self-documenting**: [coupling_diagnostic_cases.py](analysis/coupling_diagnostic_cases.py#L1-L44) header explains three cases, inputs, and references.

**Gaps:**
- **No test suite.** A search for test*.py files returned no results. Critical functions like [drainage_peclet](analysis/poroelastic_framework.py#L90-L106) or [log_healing](analysis/coupling_diagnostic_cases.py#L79-L90) have no unit tests or integration tests.
- **No pytest entry point.** Cannot run `pytest` to validate the codebase.
- **No __init__.py.** The [analysis/](analysis/) folder is a bare directory, not a package. Users cannot `from analysis.poroelastic_framework import sensitivity_depth` cleanly.
- **Type hints incomplete.** [sensitivity_depth](analysis/poroelastic_framework.py#L47) declares `Vs_mps : float or array` but does not use `Union[float, np.ndarray]` in the signature. [drainage_peclet](analysis/poroelastic_framework.py#L90) returns `float or array [rad/s]` without a return-type annotation.
- **Docstring format inconsistent.** [sensitivity_depth](analysis/poroelastic_framework.py#L47-L65) uses Numpy-style docstrings (Parameters, Returns), but [gwl_model](analysis/coupling_diagnostic_cases.py#L68) uses inline comments instead of a docstring.
- **No release tags.** [CITATION.cff](CITATION.cff#L3) lists version 0.1.0, but no corresponding git tag exists (cannot verify without git access, but .git folder is present in workspace).
- **No changelog.** No CHANGELOG.md, HISTORY.md, or release notes exist. Users cannot see what changed between versions or identify breaking changes.
- **Installation not tested cleanly.** The README prescribes `pixi install` and `pixi run lab`, but no CI workflow (.github/workflows) runs a fresh install and test to verify it works.

**Suggestions (in priority order):**

1. **Create [analysis/__init__.py](analysis/__init__.py)** to expose the public API:
   ```python
   """DVV Coupling Framework — unified treatment of seismic velocity changes."""
   
   from .poroelastic_framework import (
       sensitivity_depth,
       drainage_peclet,
       classify_drainage,
       drainage_frequency,
       poisson_ratio,
       bulk_modulus,
       shear_modulus,
   )
   from .coupling_diagnostic_cases import (
       case1_split_window_regression,
       case2_saturation_sensitivity,
       case3_tidal_beta_evolution,
   )
   from .config import SiteConfig, AnalysisConfig, PARKFIELD, CASCADIA
   
   __all__ = [
       "sensitivity_depth",
       "drainage_peclet",
       "case1_split_window_regression",
       "SiteConfig",
       "PARKFIELD",
       # ... etc
   ]
   ```

2. **Add type hints to all public function signatures** in [poroelastic_framework.py](analysis/poroelastic_framework.py) and [coupling_diagnostic_cases.py](analysis/coupling_diagnostic_cases.py):
   - Replace `def sensitivity_depth(Vs_mps, freq_hz, rule="third_wavelength"):` with:
     ```python
     from typing import Union, Literal
     import numpy as np
     
     def sensitivity_depth(
         Vs_mps: Union[float, np.ndarray],
         freq_hz: float,
         rule: Literal["third_wavelength", "half_wavelength", "quarter_wavelength"] = "third_wavelength",
     ) -> Union[float, np.ndarray]:
     ```

3. **Create [tests/](tests/) folder with pytest suite:**
   - [tests/test_poroelastic_framework.py](tests/test_poroelastic_framework.py): Unit tests for sensitivity_depth, drainage_peclet, etc.
     ```python
     import pytest
     from analysis.poroelastic_framework import sensitivity_depth
     
     def test_sensitivity_depth_third_wavelength():
         L = sensitivity_depth(Vs_mps=2500, freq_hz=2.0, rule="third_wavelength")
         assert L == pytest.approx(2500 / (3 * 2.0), rel=1e-6)
     
     def test_sensitivity_depth_invalid_rule():
         with pytest.raises(ValueError):
             sensitivity_depth(2500, 2.0, rule="invalid")
     ```
   - [tests/test_config.py](tests/test_config.py): Validate SiteConfig constraints
     ```python
     def test_site_config_invalid_porosity():
         with pytest.raises(ValueError):
             SiteConfig(name="test", porosity=1.5, ...)  # > 1
     ```
   - Add to [pixi.toml](pixi.toml#L1):
     ```toml
     [dev-dependencies]
     pytest = ">=7.0,<8"
     
     [tasks]
     test = { cmd = "pytest tests/", description = "Run unit tests" }
     ```

4. **Create [CHANGELOG.md](CHANGELOG.md)** documenting versions and breaking changes:
   ```markdown
   # Changelog
   
   ## [0.1.0] – 2026-04-01 (Initial release)
   
   ### Added
   - Poroelastic coupling framework (Tier 1)
   - Three diagnostic case studies (Ridgecrest, drought-flood, Parkfield tidal)
   - Six Jupyter notebooks demonstrating thermoelastic, hydrological, nonlinear elasticity, and rheological models
   - Companion code to unified dv/v framework manuscript
   
   ### Limitations (see docs/ai_documentation for details)
   - Tier 2 damage-permeability feedback and Tier 3 saturation-dependent nonlinear elasticity are scenario-based, not yet validated against data
   - 3-D inversion framework is proposed but not implemented
   ```

5. **Tag a release:** Run `git tag -a v0.1.0 -m "Initial release: unified dv/v framework"` and push.

---

### 4. Workflow Examples — 🟡

**What's working:**
- Six Jupyter notebooks ([01_thermoelastic_model.ipynb](analysis/01_thermoelastic_model.ipynb) through [06_sensitivity_validity.ipynb](analysis/06_sensitivity_validity.ipynb)) cover the major workflows described in the manuscript.
- Notebooks are **paired with analysis scripts:** [coupling_diagnostic_cases.py](analysis/coupling_diagnostic_cases.py), [coupling_tier_tests.py](analysis/coupling_tier_tests.py) provide reproducible code.
- **Synthetic data generators** are provided for three priority cases (Ridgecrest, drought-flood, Parkfield) in [coupling_diagnostic_cases.py](analysis/coupling_diagnostic_cases.py#L96-L170), enabling users to run without proprietary parquet files.
- Each analysis script is **self-contained** with clear docstrings ([coupling_diagnostic_cases.py](analysis/coupling_diagnostic_cases.py#L1-L27) explains Case 1/2/3 inputs and outputs).
- **Publication-quality figures** are committed to repo ([figures/notebooks/](figures/notebooks/), [figures/coupling/](figures/coupling/)).

**Gaps:**
- **Notebooks have not been executed** ([copilot_getNotebookSummary](analysis/01_thermoelastic_model.ipynb) reports "None of the cells have been executed"). Outputs are missing, so users cannot see expected results without running them first.
- **No quick-start notebook.** All six notebooks assume the user understands the manuscript context. A notebook called [00_quickstart.ipynb](analysis/00_quickstart.ipynb) (< 5 min to run) would help.
- **External data dependencies are undocumented.** [coupling_diagnostic_cases.py](analysis/coupling_diagnostic_cases.py#L747-L789) function `load_parquet_dvv()` expects parquet files (line 760-789) but the README does not say how to obtain them. The comment "If parquet files are available, replace the synthetic data generators…" (line 26-27) suggests they're optional but doesn't provide a fetch script or URL.
- **Expected run times not documented.** Users don't know if [06_sensitivity_validity.ipynb](analysis/06_sensitivity_validity.ipynb) takes 1 minute or 1 hour.
- **Random seeds not set.** Notebooks that generate synthetic data should set `np.random.seed(42)` for reproducibility; the code does this implicitly (e.g., [coupling_diagnostic_cases.py](analysis/coupling_diagnostic_cases.py#L99-L130) uses deterministic math) but it's not explicit.
- **Tutorials not indexed.** There is no [tutorials.yaml](docs/tutorials.yaml) or [docs/tutorials_index.md](docs/tutorials_index.md) listing workflows by use case, so an LLM agent (or human) has to manually scan the six notebooks to find which one answers "what's a worked example of case 3?"

**Suggestions (in priority order):**

1. **Execute all six notebooks end-to-end** and commit the outputs (cell outputs, plots). This ensures:
   - Users see expected results by reading the notebook in GitHub/VS Code
   - Changes to the code that break a notebook are caught immediately
   - Wall times and output sizes are visible
   - Add a Jupyter execution step to CI (see Action Item #1, API Quality)

2. **Create [analysis/00_quickstart.ipynb](analysis/00_quickstart.ipynb)** (5-min runtime):
   - Title: "Quick Start: Compute dv/v sensitivity to depth and drainage regime"
   - Cells:
     1. Markdown: Explain the goal (estimate depth sensitivity for a Parkfield-like site)
     2. Code: `from analysis.poroelastic_framework import sensitivity_depth, drainage_peclet`
     3. Code: Compute L for 3 Hz → ~416 m; compute Pe for annual cycle → 0.3 (drained)
     4. Markdown: Interpret result ("This site is well-drained at seasonal timescales")
     5. Plot: Show a simple depth-frequency sensitivity matrix
   - Link to this notebook prominently in [README.md](README.md#L52-L60).

3. **Document external data sources** in a new [docs/data_sources.md](docs/data_sources.md):
   ```markdown
   # External Data Sources
   
   ## Clements & Denolle (2023) California dv/v
   - **Use case:** Case 1 (Ridgecrest), Case 2 (drought-flood), Tier 1 validation
   - **Format:** Parquet files (one per station)
   - **Access:** [Contact corresponding author](mailto:rclements@caltech.edu) or request via zenodo (if available)
   - **Files:** `NET.STA.parquet` with columns DATE, DVV, CC
   - **Expected size:** ~1 GB total (~100 MB per station for 10-year records)
   
   ## Okubo et al. (2024) Parkfield dv/v
   - **Use case:** Case 3 (tidal beta evolution)
   - **Access:** [IRIS DMC](https://www.iris.edu/dms/products/parkfield/) or author
   
   ## Synthetic data (included)
   - All three cases have `generate_*_synthetic()` functions in coupling_diagnostic_cases.py
   - These are used when parquet files are unavailable
   ```

4. **Add execution notes to each notebook.** Insert a markdown cell after the title in each notebook:
   ```markdown
   **Estimated runtime:** 12 minutes  
   **Output size:** ~50 MB (figures saved to figures/notebooks/)  
   **Dependencies:** numpy, scipy, matplotlib, disba
   ```

5. **Create [analysis/tutorials_index.md](analysis/tutorials_index.md)** (or tutorials.yaml):
   ```markdown
   # Workflow Tutorials
   
   | Notebook | Use Case | Runtime | Key Output |
   |---|---|---|---|
   | 00_quickstart.ipynb | First-time setup & sanity check | 5 min | Sensitivity depth visualization |
   | 01_thermoelastic_model.ipynb | Temperature-driven dv/v (Berger 1975 + Richter 2014) | 8 min | Annual temp cycle → 0.3% dv/v |
   | 02_hydrological_loading.ipynb | Competing load & pore-pressure effects (Roeloffs 1988, Fokker 2021) | 10 min | Seasonal hydrological signal |
   | 03_nonlinear_elasticity.ipynb | Acoustoelastic parameter β from nonlinear elasticity (Murnaghan 1937) | 6 min | β map across materials |
   | 04_stress_anisotropy.ipynb | Deviatoric stress → anisotropy (Tromp & Trampert 2018) | 12 min | Parkfield anisotropy fit |
   | 05_rheological_models.ipynb | Logarithmic healing & viscoelasticity (Snieder 2017) | 9 min | Post-seismic recovery |
   | 06_sensitivity_validity.ipynb | Parameter space exploration & regime diagram | 15 min | Coupling tier validity map |
   ```

---

### 5. Failure Modes — 🟡

**What's working:**
- **Comprehensive limitation documentation** in [docs/ai_documentation/06_ai_traceability.md](docs/ai_documentation/06_ai_traceability.md#L169) flags known approximations (e.g., "The bridge relation caveat: Eq. 7 is approximate; calibration-consistent Cascadia comparison, factor-of-1.4 error at Parkfield").
- **Peer-review process documented** in [docs/review/](docs/review/) with five rounds of pre-submission review and author responses, identifying gaps (e.g., "3-D inversion framework has no validation" [pre_submission_review.md](docs/review/pre_submission_review.md#L112)).
- **Known scope limits stated** in manuscript sections and [docs/ai_documentation/02_chain_of_thought.md](docs/ai_documentation/02_chain_of_thought.md#L73-L79) (e.g., "capillary model presented as external evidence, not implemented").
- **Error handling in functions** uses explicit checks: [poroelastic_framework.py](analysis/poroelastic_framework.py#L57) raises `ValueError` if `rule` is invalid.

**Gaps:**
- **No active issue tracker visible.** Cannot assess whether issues are being reported, closed, or acknowledged by maintainers. (GitHub repo not inspected directly, but typical indicators of an active tracker are labels, milestones, response times.)
- **No dedicated "Troubleshooting" or "FAQ" section.** Known issues are scattered across review documents but not organized for user self-service.
- **Error messages are generic (scipy/numpy).** When [sensitivity_depth](analysis/poroelastic_framework.py#L57) receives an invalid `rule`, it raises a plain `ValueError`. Users would benefit from a wrapper error message, e.g.:
   ```python
   if rule not in rules:
       msg = f"rule='{rule}' not recognized. Valid options: {list(rules.keys())}. \
              Recommended: 'third_wavelength' for coda-wave interpretation."
       raise ValueError(msg)
   ```
- **No runnable diagnostic mode.** Users cannot call a function like `validate_and_summarize_config(config)` to get a detailed report of what the pipeline would do without running the full analysis.
- **Limitations not in a single place.** Regime limits documented in [coupling_tier_tests.py](analysis/coupling_tier_tests.py#L1-L27) (Parkfield depth 0.8 km, Cascadia 0.2 km, etc.), but these are hard-wired examples, not a queryable regime map.

**Suggestions (in priority order):**

1. **Create [docs/troubleshooting.md](docs/troubleshooting.md)** with common errors:
   ```markdown
   # Troubleshooting
   
   ## "ValueError: rule must be one of ..."
   **Cause:** Invalid sensitivity depth rule passed to `sensitivity_depth()`.  
   **Solution:** Use one of: `"third_wavelength"` (recommended for coda), `"half_wavelength"` (surface waves), `"quarter_wavelength"` (reflection).  
   **Reference:** See [poroelastic_framework.py](analysis/poroelastic_framework.py#L47-L65)
   
   ## Drainage regime classification doesn't match my intuition
   **Cause:** Pe number compares forcing frequency to drainage frequency. Low Pe = fast drainage (drained); high Pe = slow drainage (undrained).  
   **Solution:** Inspect Pe value directly via `drainage_peclet(c_m2s, L_m)`. If Pe > 10 for your site, you're in the undrained regime.  
   **Reference:** [coupling_tier_tests.py](analysis/coupling_tier_tests.py#L127) shows realistic Pe values for each site.
   
   ## "ImportError: No module named 'disba'"
   **Cause:** Optional dependency not installed.  
   **Solution:** Run `pixi install` (includes disba). If using pip, `pip install disba>=0.7.0`.  
   **Reference:** [pixi.toml](pixi.toml)
   ```

2. **Wrap scipy/numpy errors in public functions.** E.g., in [sensitivity_depth](analysis/poroelastic_framework.py#L57):
   ```python
   if rule not in rules:
       valid = ", ".join(list(rules.keys()))
       raise ValueError(
           f"rule='{rule}' not recognized. Valid options: {valid}.\n"
           f"Recommended: 'third_wavelength' for coda-wave CWI, 'half_wavelength' for surface waves."
       )
   ```

3. **Create a `validate_and_summarize()` function** in [analysis/config.py](analysis/config.py):
   ```python
   def validate_and_summarize(config: AnalysisConfig) -> str:
       """
       Check SiteConfig and AnalysisConfig for consistency and print diagnostic summary.
       
       Returns a multi-line string describing:
       - Site properties (Vs, rho, beta, alpha_B)
       - Sensitivity depth at given frequency
       - Drainage regime (drained/transitional/undrained) at annual, semi-annual, etc.
       - Estimated relevant timescales
       
       Example:
       >>> config = AnalysisConfig(site=PARKFIELD, frequency_hz=3.0)
       >>> print(validate_and_summarize(config))
       Site: Parkfield (granite)
       Vs = 2500 m/s, ρ = 2500 kg/m³
       β = -240, μ' = 251 Pa
       Sensitivity depth @ 3 Hz = 417 m (third-wavelength rule)
       Drainage regime @ annual: DRAINED (Pe = 0.04)
       Drainage regime @ semi-annual: DRAINED (Pe = 0.02)
       
       This analysis is valid in the regime where ε < 10⁻⁴ (nonlinear elasticity assumption).
       See docs/troubleshooting.md for interpretation.
       """
   ```

4. **Add a regime validity map** to [docs/](docs/) showing which assumptions hold (nonlinear elasticity, isotropy, saturation, etc.) in different parts of the parameter space. E.g., a table linking "if β > 500 and depth > 200 m, then isotropy breaks down"—cite the figures in [06_sensitivity_validity.ipynb](analysis/06_sensitivity_validity.ipynb).

---

### 6. Reproducibility — 🟡

**What's working:**
- **pixi.toml pins exact dependency versions** ([pixi.toml](pixi.toml#L1-L16)): numpy>=2.4.3,<3; scipy>=1.17.1,<2; matplotlib>=3.10.8,<4; disba>=0.7.0,<1.
- **Material properties are deterministically specified** ([coupling_tier_tests.py](analysis/coupling_tier_tests.py#L48-L100) hard-codes all Parkfield, Cascadia, etc. parameters).
- **Synthetic data generators use deterministic seeding** (implicitly, via scipy special functions and numpy arrays; [coupling_diagnostic_cases.py](analysis/coupling_diagnostic_cases.py#L99-L130) computes seasonal cycles, tides, etc. without randomness).
- **Figure outputs are committed** to repo ([figures/notebooks/fig01–fig18.png](figures/notebooks/), [figures/coupling/case1–case3.png](figures/coupling/)), so users can compare.

**Gaps:**
- **Notebooks have not been executed**, so output cells are empty. Users cannot see expected results by reading the repo; they must run the notebooks themselves.
- **No random seed set explicitly.** Although the code is deterministic, a user reading [coupling_diagnostic_cases.py](analysis/coupling_diagnostic_cases.py#L99-L130) might not realize it's deterministic. Best practice: add `np.random.seed(42)` at the top of each analysis script.
- **External parquet data not versioned or checksummed.** [coupling_diagnostic_cases.py](analysis/coupling_diagnostic_cases.py#L747-L789) loads parquet but doesn't document data provenance (DOI, S3 URL) or a fetch script. If data is from [Clements & Denolle (2023)](https://doi.org/10.1029/2022JB025553), this should be cited and a fetch_clements_denolle_2023.py script provided.
- **Expected run times and output sizes not documented.** Users don't know if [06_sensitivity_validity.ipynb](analysis/06_sensitivity_validity.ipynb) produces 10 MB or 1 GB of output, or whether it takes 5 min or 5 hours.
- **Tolerance thresholds not specified.** When comparing synthetic outputs to expected figures, what numerical tolerance is acceptable? (See [docs/review/pre_submission_review_round2.md](docs/review/pre_submission_review_round2.md#L61) which suggests pinning exact versions.)

**Suggestions (in priority order):**

1. **Execute all six notebooks** using `jupyter nbconvert --to notebook --execute` or CI automation:
   ```bash
   cd analysis
   jupyter nbconvert --to notebook --execute 01_thermoelastic_model.ipynb
   ```
   Commit the executed notebooks with cell outputs. (This is part of the overall test suite recommendation in API Quality, Suggestion #3.)

2. **Set explicit random seeds** in each analysis script ([coupling_diagnostic_cases.py](analysis/coupling_diagnostic_cases.py#L40)):
   ```python
   import numpy as np
   np.random.seed(42)
   ```
   Add a comment: "Set seed for reproducibility of synthetic data generation."

3. **Create [docs/data_sources.md](docs/data_sources.md)** (cross-reference from Workflow Examples suggestion #3) with:
   ```markdown
   ## Clements & Denolle (2023) Parquet Files
   
   **DOI:** https://doi.org/10.1029/2022JB025553  
   **Data availability:** Available by request from first author (R. Clements, Caltech).  
   **For reproducibility:** If you have access, place files in `data/clements_denolle_2023/` with naming `NET.STA.parquet`.  
   **Synthetic fallback:** All tutorials use synthetic data generators by default; parquet loading is optional.
   ```

4. **Document expected runtimes and outputs** in [analysis/00_quickstart.ipynb](analysis/00_quickstart.ipynb) metadata and notebook markdown cells. E.g., top cell:
   ```markdown
   **Expected runtime:** 5 minutes  
   **Output files:** None (plots displayed inline)  
   **Data sources:** Synthetic (no external dependencies)  
   **Numerical tolerance:** Results should match figures in paper within 1%.
   ```

5. **Create [tests/test_reproducibility.py](tests/test_reproducibility.py)** to validate outputs:
   ```python
   import numpy as np
   from analysis.coupling_tier_tests import tier1_drained_undrained_transition
   
   def test_tier1_parkfield_pe():
       """Verify Parkfield Péclet number at annual timescale is in known range."""
       from analysis.poroelastic_framework import drainage_peclet
       Pe = drainage_peclet(c_m2s=1e-5, L_m=800)  # Parkfield, annual
       assert 0.03 < Pe < 0.05, f"Expected Pe ~0.04, got {Pe}"
   
   def test_synthetic_california_generates():
       """Verify synthetic data generator doesn't crash."""
       from analysis.coupling_diagnostic_cases import generate_california_synthetic
       data = generate_california_synthetic(years=(2015, 2023))
       assert len(data['dates']) == len(data['dvv'])
       assert np.nanstd(data['dvv']) > 0  # Non-trivial signal
   ```

---

### 7. Agent Affordances — 🔴

**What's working:**
- `Site` class ([coupling_tier_tests.py](analysis/coupling_tier_tests.py#L44-L45)) provides a **structured container** for material properties (not just prose).
- **Docstring format is somewhat standardized:** NumPy-style (Parameters, Returns) in [poroelastic_framework.py](analysis/poroelastic_framework.py#L47-L65).
- **Key constants are queryable:** [OMEGA_ANNUAL](analysis/poroelastic_framework.py#L16), [OMEGA_DAILY](analysis/poroelastic_framework.py#L17) are module-level and can be imported.
- **Defaults are explicit in function signatures:** `sensitivity_depth(Vs_mps, freq_hz, rule="third_wavelength")` shows the default rule.

**Gaps:**
- **No programmatic schema export.** An LLM agent cannot call `inspect.signature(SiteConfig)` and programmatically determine the valid fields and types (because SiteConfig doesn't exist yet as a dataclass).
- **Defaults scattered across files.** `pe_drained=0.1` default in [poroelastic_framework.py](analysis/poroelastic_framework.py#L100); `phi=0.3` in [coupling_diagnostic_cases.py](analysis/coupling_diagnostic_cases.py#L68); `freq_hz=3.0` in [07_tier1_california_test.py](analysis/07_tier1_california_test.py#L38). No single reference.
- **No "recipes" or presets directory.** A user (or agent) cannot browse a [presets/](presets/) folder to see named parameter sets like `parkfield_case3_tidal.yaml` or `cascadia_subduction.yaml`.
- **No dry-run or plan mode.** Functions immediately compute, with no option to print "here's what I would compute" before execution.
- **Tutorials not indexed programmatically.** No [docs/tutorials.yaml](docs/tutorials.yaml) with structured metadata (title, runtime, keywords, input schema). An agent has to parse notebook filenames and read markdown cells manually.
- **No validation schema available to agents.** An agent cannot call `SiteConfig.fields()` to enumerate valid fields, constraints, and types.

**Suggestions (in priority order):**

1. **Convert SiteConfig to a pydantic model** (from Config class suggested in Input Contract, Suggestion #1) to enable programmatic introspection:
   ```python
   from pydantic import BaseModel, Field, field_validator
   
   class SiteConfig(BaseModel):
       """Physical properties of a site."""
       name: str
       Vs: float = Field(..., gt=0, description="Shear velocity [m/s]")
       rho: float = Field(..., gt=0, description="Density [kg/m³]")
       mu_prime: float = Field(..., description="Nonlinear constant [Pa/Pa]")
       beta: float = Field(..., description="Stress sensitivity [-]")
       alpha_B: float = Field(..., ge=0, le=1, description="Biot coefficient [-]")
       porosity: float = Field(..., ge=0, le=1, description="Porosity [-]")
       depth: float = Field(..., gt=0, description="Sensitivity depth [m]")
       kappa_T: float = Field(default=1e-6, description="Thermal diffusivity [m²/s]")
       alpha_T: float = Field(default=8e-6, description="Thermal expansion [K⁻¹]")
       
       @field_validator('name')
       @classmethod
       def name_not_empty(cls, v):
           if not v or not v.strip():
               raise ValueError('name cannot be empty')
           return v
       
       model_config = ConfigDict(json_schema_extra={
           "examples": [
               {
                   "name": "Parkfield (granite)",
                   "Vs": 2500, "rho": 2500, "mu_prime": 251, "beta": -240,
                   "alpha_B": 0.7, "porosity": 0.05, "depth": 800
               }
           ]
       })
   
   # Agents can now inspect:
   SiteConfig.model_json_schema()  # Full JSON schema
   SiteConfig.model_fields  # Field metadata
   ```

2. **Create [presets/](presets/) directory** with named parameter sets as YAML:
   ```yaml
   # presets/parkfield_case3_tidal.yaml
   site:
     name: "Parkfield (granite)"
     Vs: 2500
     rho: 2500
     mu_prime: 251
     beta: -240
     alpha_B: 0.7
     porosity: 0.05
     depth: 800
   analysis:
     frequency_hz: 3.0
     rule: "third_wavelength"
     stack_days: 180
     step_days: 30
   description: |
     Tier 1+2 analysis of Parkfield tidal coupling.
     Reproduces Okubo et al. (2024) M2 tidal amplitude time series.
   reference: "Okubo et al. (2024), JGR Solid Earth"
   
   # presets/cascadia_subduction.yaml
   site:
     name: "Cascadia (sediment)"
     Vs: 500
     ...
   ```
   Agents can enumerate: `glob("presets/*.yaml")` and load via `yaml.safe_load()`.

3. **Add a dry-run / plan-print mode** to entry points. E.g.:
   ```python
   def case1_split_window_regression(
       config: AnalysisConfig,
       data,
       window_years: float = 2.0,
       dry_run: bool = False,
   ) -> dict:
       """
       Parameters
       ----------
       dry_run : bool
           If True, print the analysis plan and return without computing.
       """
       plan = {
           "site": config.site.name,
           "frequency_hz": config.frequency_hz,
           "window_size_years": window_years,
           "n_windows": len(data['dates']) / (365.25 * window_years),
           "expected_output": "figure + regression table",
       }
       if dry_run:
           print("Dry-run analysis plan:")
           for key, val in plan.items():
               print(f"  {key}: {val}")
           return {"status": "dry_run", "plan": plan}
       # ... proceed with real computation
   ```

4. **Create [docs/tutorials.yaml](docs/tutorials.yaml)** (or JSON):
   ```yaml
   tutorials:
     - id: "00_quickstart"
       title: "Quick Start: Sensitivity Depth and Drainage Regime"
       file: "analysis/00_quickstart.ipynb"
       runtime_minutes: 5
       keywords: ["beginner", "tutorial", "sensitivity", "drainage"]
       input_schema:
         - name: "frequency_hz"
           type: "float"
           default: 3.0
           description: "Coda center frequency [Hz]"
       output: "Sensitivity depth visualization, regime classification"
       learning_goal: "Understand how frequency and material properties control seismic sensitivity depth"
     
     - id: "01_thermoelastic_model"
       title: "Thermoelastic dv/v: Berger (1975) + Richter (2014)"
       file: "analysis/01_thermoelastic_model.ipynb"
       runtime_minutes: 8
       keywords: ["temperature", "thermal", "annual cycle", "intermediate"]
       input_schema:
         - name: "T_amplitude"
           type: "float"
           default: 15
           description: "Surface temperature amplitude [K]"
         - name: "thermal_diffusivity"
           type: "float"
           default: 1e-6
           description: "Thermal diffusivity [m²/s]"
       output: "Temperature profile, dv/v time series, frequency response"
   ```
   Agents can parse and index: `[t for t in tutorials if "drain" in t["keywords"]]`.

5. **Add a `get_defaults()` function** to [analysis/config.py](analysis/config.py):
   ```python
   def get_defaults() -> dict:
       """Return all default parameter values in one place."""
       return {
           "frequency_hz": 3.0,
           "rule": "third_wavelength",
           "omega_forcing": OMEGA_ANNUAL,
           "pe_drained_threshold": 0.1,
           "pe_undrained_threshold": 10.0,
           "thermal_diffusivity_m2s": 1e-6,
           "porosity": 0.3,
       }
   
   # Agents can call:
   defaults = get_defaults()
   assert defaults["frequency_hz"] == 3.0
   ```

---

## Top 3 Action Items

Prioritized by impact (leverage for both humans and agents):

### 1. **Create a unified input schema and export functions for programmatic use** — [*Input Contract + Agent Affordances*]

**Impact:** This is the single highest-leverage change. Currently, users and LLM agents cannot programmatically discover what parameters are valid, what defaults are used, or what constraints apply. Creating a pydantic `SiteConfig` and `AnalysisConfig` class (in new [analysis/config.py](analysis/config.py)) with validation, then updating all entry points to accept these configs instead of scattered kwargs, will:
- Enable **type checking and IDE autocomplete** for users
- Allow **LLM agents to inspect schema** via `SiteConfig.model_json_schema()`
- **Eliminate defaults scattered across files** (currently in [poroelastic_framework.py](analysis/poroelastic_framework.py#L100), [coupling_diagnostic_cases.py](analysis/coupling_diagnostic_cases.py#L68), [07_tier1_california_test.py](analysis/07_tier1_california_test.py#L38))
- **Enable programmatic validation** before expensive computations
- **Support CLI arg parsing** (hydra, click, argparse can all read pydantic models)

**Suggested approach:**
1. Define [analysis/config.py](analysis/config.py) with pydantic SiteConfig and AnalysisConfig classes, including Parkfield, Cascadia, Nepal, Agricultural as instances.
2. Update function signatures: `def case1_split_window_regression(config: AnalysisConfig, data, ...)` instead of scattered params.
3. Add `SiteConfig.__post_init__()` validation (Biot coeff in [0,1], porosity in [0,1], Vs > 0, etc.).
4. Export via [analysis/__init__.py](analysis/__init__.py): `from analysis.config import SiteConfig, PARKFIELD, CASCADIA`.
5. **Estimated effort:** 2–3 hours. **Blockers:** None. **Rollout:** Update notebooks and scripts to use new config classes; document in README.

---

### 2. **Execute and commit all notebook outputs, then add notebook execution to CI** — [*Reproducibility + Workflow Examples*]

**Impact:** Users currently see empty notebooks when they view the repo. Executing notebooks and committing outputs will:
- **Reduce barrier to entry:** New users see what results look like without running code
- **Catch bugs immediately:** If code breaks, notebooks don't run in CI and the breakage is flagged
- **Enable expected-output comparison:** Test suite can validate that outputs match (within tolerance) across runs
- **Document wall times and output sizes** (when notebooks are executed, cell runtimes are saved in the .ipynb metadata)

**Suggested approach:**
1. Add [tests/conftest.py](tests/conftest.py) with a pytest fixture to run notebooks (or use `nbval` pytest plugin).
2. Create [.github/workflows/test-notebooks.yml](.github/workflows/test-notebooks.yml):
   ```yaml
   on: [push, pull_request]
   jobs:
     notebooks:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v3
         - uses: mamba-org/setup-micromamba@v1
           with:
             environment-file: pixi.toml
         - run: pixi run pytest tests/test_reproducibility.py
   ```
3. Run `jupyter nbconvert --to notebook --execute analysis/*.ipynb` locally and commit the results.
4. Update [README.md](README.md#L53-L60) "Reproducing Figures" to: "All notebooks are pre-executed and outputs are committed. To re-run: `pixi run lab` and re-execute cells."
5. **Estimated effort:** 1–2 hours (assuming notebooks run cleanly). **Blockers:** If notebooks have external data dependencies (parquet files), add synthetic data fallback (already present). **Rollout:** Merge into main once all notebooks execute without error.

---

### 3. **Add a test suite (pytest) and package infrastructure (__init__.py, setup.py)** — [*API & Code Quality + Reproducibility*]

**Impact:** The code currently has no tests. Adding a basic test suite will:
- **Catch regressions:** Changes to core functions (sensitivity_depth, drainage_peclet, etc.) are immediately validated
- **Enable package distribution:** Users can `pip install` from GitHub once setup.py / pyproject.toml exists
- **Provide examples to agents:** Tests show realistic usage patterns (inputs, outputs, error cases)
- **Enable CI/CD:** Pull requests can be automatically tested

**Suggested approach:**
1. Create [analysis/__init__.py](analysis/__init__.py) (from API Quality, Suggestion #1) with `__all__` export list.
2. Create [pyproject.toml](pyproject.toml) (or [setup.py](setup.py)):
   ```toml
   [build-system]
   requires = ["setuptools", "wheel"]
   build-backend = "setuptools.build_meta"
   
   [project]
   name = "dvv-coupling-framework"
   version = "0.1.0"
   description = "Unified framework for interpreting seismic velocity changes (dv/v)"
   authors = [{name = "Marine A. Denolle", email = "mdenolle@uw.edu"}]
   dependencies = ["numpy>=2.4.3", "scipy>=1.17.1", "matplotlib>=3.10.8", "disba>=0.7.0"]
   ```
3. Create [tests/](tests/) with unit tests (from API Quality, Suggestion #3):
   - [tests/test_poroelastic_framework.py](tests/test_poroelastic_framework.py): Unit tests for core functions
   - [tests/test_config.py](tests/test_config.py): Config validation
   - [tests/test_reproducibility.py](tests/test_reproducibility.py): Check synthetic outputs vs. expected ranges
4. Add pytest to [pixi.toml](pixi.toml) and add `[tasks] test = "pytest tests/"`.
5. Create [.github/workflows/test.yml](.github/workflows/test.yml) to run pytest on every push.
6. **Estimated effort:** 3–4 hours. **Blockers:** Need to write test cases; choose coverage target (aim for 60%+ of public API). **Rollout:** Iterative—start with critical functions (sensitivity_depth, drainage_peclet), expand over time.

---

## Skipped or N/A

None. All seven dimensions apply to this research software repository.

---

## Notes for next review

1. **Parquet data accessibility:** The code references Clements & Denolle (2023) parquet files but doesn't provide them. On next review, verify whether:
   - Data is published (Zenodo, FigShare, IRIS DMC, or supplementary materials)?
   - Fetch script should be added?
   - Synthetic fallback is sufficient?

2. **3-D inversion framework:** The manuscript (Section 7.3–7.4) proposes a joint inversion but does not implement it. This is acknowledged in [docs/review/pre_submission_review.md](docs/review/pre_submission_review.md#L112) as aspirational. On next review, check whether:
   - A working inversion example has been added to [07_tier1_california_test.py](analysis/07_tier1_california_test.py)?
   - Synthetic tests exist for resolution and ill-conditioning?

3. **CI/CD maturity:** Once the test suite and pixi.toml are in place, GitHub Actions workflows should be added for:
   - Notebook execution (check notebooks run end-to-end)
   - Type checking (mypy on analysis/*.py)
   - Linting (flake8, black)

4. **Release cycle:** After the above changes, tag a release v0.2.0 to communicate that the package is now more robust and can be installed via pip.

5. **Docstring parser:** Verify that docstrings in [poroelastic_framework.py](analysis/poroelastic_framework.py) are parseable by standard tools (sphinx autodoc, pdoc). Some functions use NumPy-style, others use inline comments. Standardize before releasing.

---

**End of Review**
