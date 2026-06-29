# dv/v as Stress and Strain Meter: Unified Framework

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

**Seismic Velocity Changes as Stress and Strain Meters: A Unified Framework for Environmental, Tectonic, and Volcanic Monitoring**

Marine A. Denolle$^1$

$^1$ Department of Earth and Space Sciences, University of Washington

AI tools were used as a research and writing assistant under the author's direction; see the [Statement of AI Use](docs/ai_documentation/03_model_card.md).

---

## Overview

This repository contains the manuscript, companion Jupyter notebooks, and figures for a research paper that develops a unified theoretical framework for interpreting ambient-noise-derived seismic velocity changes (dv/v) across environmental, tectonic, and volcanic settings.

This repository is the research and validation substrate for the planned `codameter` software package. The reusable package should implement the workflow here as stable APIs, while this repository keeps the paper, derivations, sensitivity studies, and worked examples.

The framework connects:
- **Murnaghan (1937)** third-order elasticity → acoustoelastic parameter β
- **Berger (1975)** thermoelastic stress → temperature-induced dv/v
- **Roeloffs (1988)** poroelastic diffusion → hydrological dv/v
- **Tromp & Trampert (2018)** induced stress → anisotropic dv/v
- **Fokker et al. (2021)** loading vs. pore pressure → competing effects
- **Shi et al. (2026)** dynamic capillary effects → partially saturated media
- **Snieder et al. (2017)** logarithmic healing → post-seismic recovery

through the common thread of **nonlinear elasticity**.

### What this code does — and doesn't

**It does:**
- Compute forward models of dv/v under thermoelastic, hydrological, and poroelastic forcing.
- Provide a validated input schema (`SiteConfig` / `AnalysisConfig`) with literature-sourced presets (Parkfield, Cascadia, Nepal, agricultural soil).
- Run tier-wise coupling diagnostics and three synthetic case studies (Ridgecrest, drought-flood, Parkfield tidal).

**It does not:**
- Process raw seismic waveforms or compute ambient-noise cross-correlations.
- Perform full Bayesian or 3-D stress/strain inversion (the joint-inversion framework is proposed in the manuscript, not implemented here). A lightweight Bayesian model average is included for coda-window method uncertainty.
- Ship the proprietary Clements & Denolle (2023) parquet data; synthetic generators are used by default (see [docs/data_sources.md](docs/data_sources.md)).

## Repository Structure

```
├── README.md                              # This file
├── LICENSE                                # CC BY 4.0
├── CITATION.cff                           # Machine-readable citation metadata
├── pixi.toml                              # Reproducible environment (pixi)
│
├── paper/
│   ├── paper_dvv_unified_framework.md     # Full manuscript (Markdown + LaTeX math)
│   └── references.bib                     # Machine-readable bibliography
│
├── analysis/                              # All executable code in one place
│   ├── 01_thermoelastic_model.ipynb       # Berger (1975) + Richter (2014) model
│   ├── 02_hydrological_loading.ipynb      # Roeloffs (1988) + Fokker (2021) model
│   ├── 03_nonlinear_elasticity.ipynb      # Murnaghan (1937) + acoustoelastic β
│   ├── 04_stress_anisotropy.ipynb         # Tromp & Trampert (2018) + crack closure
│   ├── 05_rheological_models.ipynb        # Snieder (2017) healing + viscoelasticity
│   ├── 06_sensitivity_validity.ipynb      # Parameter space & regime diagram
│   ├── coupling_diagnostic_cases.py       # Ridgecrest / drought-flood / Parkfield tidal cases
│   └── coupling_tier_tests.py             # Tier 1/2/3 coupling validation tests
├── codameter/                             # Prototype core APIs for reproducible dv/v workflows
│   └── window_selection.py                # Coda-window scoring and ranking metrics
│
├── figures/
│   ├── main/                              # Streamlined JGR main figure set
│   │   └── fig01–fig07 (.png)
│   ├── notebooks/                         # Supporting outputs from scenario notebooks
│   │   └── fig01–fig18 (.png)
│   └── coupling/                          # Outputs from coupling analysis scripts
│       └── case1–case3, tier1–tier3 (.png)
│
└── docs/
    ├── theory/                            # Working derivation & theory documents
    │   ├── equation_verification_log.md
    │   ├── combined_paper_thread.md
    │   └── application_cases_revisiting_data.md
    ├── site_analyses/                     # Quantitative site-specific write-ups
    │   ├── parkfield_stress_analysis.md
    │   └── cascadia_stress_analysis.md
    ├── review/                            # Pre-submission reviews & author responses
    │   ├── pre_submission_review.md       # Rounds 1–5
    │   ├── response_to_review.md          # Author responses rounds 1–2
    │   └── revision_notes.md
    └── ai_documentation/                  # AI transparency & traceability logs
        ├── 01_prompts_log.md
        ├── 02_chain_of_thought.md
        ├── 03_model_card.md
        ├── 04_journal_selection_discussion.md
        ├── 05_convergence_and_evaluation.md
        └── 06_ai_traceability.md
```

## Installation

This project uses [pixi](https://pixi.sh) for reproducible environment management.

```bash
# Install pixi (if not already installed)
curl -fsSL https://pixi.sh/install.sh | bash

# Clone the repo and install all dependencies
git clone https://github.com/mdenolle/dvv-coupling-framework.git
cd dvv-coupling-framework
pixi install
```

Dependencies (numpy, scipy, matplotlib, pydantic, jupyterlab) are resolved automatically via `pixi.toml`.
No proprietary code, data, or API keys are needed.

Alternatively, install the Python package directly with pip:

```bash
pip install -e ".[test]"   # editable install with test extras
```

## Quick Start

Compute a coda sensitivity depth and drainage regime for a named preset in
under two minutes:

```python
from analysis import PARKFIELD, AnalysisConfig, validate_and_summarize, sensitivity_depth

# One number: depth sampled by 2 Hz coda in granite (third-wavelength rule)
print(sensitivity_depth(Vs_mps=2500, freq_hz=2.0))   # -> 416.7 m

# Full diagnostic summary for a validated configuration
cfg = AnalysisConfig(site=PARKFIELD, frequency_hz=3.0)
print(validate_and_summarize(cfg))
```

Load a named recipe from `presets/` instead of building a config by hand:

```python
from analysis.config import load_analysis_config
cfg = load_analysis_config("presets/cascadia_subduction.yaml")
```

Compute a rolling coda-window profile before committing to a `dv/v` interpretation:

```python
from codameter import WindowEstimate, window_sensitivity_diagnostic
from codameter import rolling_lapse_windows, score_lapse_profile

windows = rolling_lapse_windows(
    start_s=2,
    stop_s=35,
    window_duration_s=5,
    step_s=1,
    fmin_hz=2,
    fmax_hz=4,
)

profile = score_lapse_profile(
    windows,
    observations={
        "lapse_000": {"coherence": 0.9, "snr": 10.0, "dvv_sigma": 2e-5},
        "lapse_001": {"coherence": 0.85, "snr": 9.0, "dvv_sigma": 3e-5},
    },
    distance_m=10000.0,
    rayleigh_group_velocity_mps=1000.0,
    vs_mps=1500.0,
    target_depth_range_m=(100, 250),
)
print(profile.centers_s, profile.objective)

posterior = window_sensitivity_diagnostic(
    profile,
    estimates={
        "lapse_000": WindowEstimate(mean=1.0e-4, sigma=1.0e-5),
        "lapse_001": WindowEstimate(mean=1.1e-4, sigma=1.2e-5),
        "lapse_002": WindowEstimate(mean=4.0e-4, sigma=1.5e-5),
    },
)
print(posterior.mean, posterior.epistemic_sigma)
```

Run the test suite with `pixi run test` (or `pytest tests/`).
The machine-readable list of worked examples lives in [docs/tutorials.yaml](docs/tutorials.yaml).

## Reproducing Figures

```bash
# Launch JupyterLab directly in the analysis folder
pixi run lab
# Execute notebooks 01 through 06 in order

# Regenerate the streamlined JGR main figure set
pixi run python analysis/jgr_main_figures.py
```

Figures are committed under `figures/notebooks/` (scenario models) and `figures/coupling/` (data analysis).
The JGR-ready main figure set is generated by `analysis/jgr_main_figures.py` and written to `figures/main/`; detailed notebook figures are cited as Supporting Information in `paper/supporting_information.md`.

## Building the Manuscript PDF

```bash
pixi run paper-pdf
```

This converts `paper/paper_dvv_unified_framework.md` to LaTeX with Pandoc and compiles two PDFs with XeLaTeX:

- `paper/build/paper_dvv_jgr_submission.pdf` — the **main manuscript** (§1–8, §10–11) with the main figure set (Figures 1–6). The data application (§9) is rendered as a **placeholder**; the detailed quantitative application is moved to the Supporting Information.
- `paper/build/paper_dvv_jgr_supplement.pdf` — the **Supporting Information**: the preliminary three-site application (Text S1), the three-site synthesis figure (Figure 7), the comparison table, and Figures S1–S12 (synthetic forward-model and validity figures) plus the parameter table.

The local template is a JGR-style submission layout (12 pt, double-spaced, line numbered); it is not the official AGU `agujournal2019.cls`, which is not vendored in this repository.

### Three rendered formats from one source

The manuscript (`paper/paper_dvv_unified_framework.md`) is the single source of truth; three build targets stay in sync with it:

1. **Markdown** — the canonical `paper/paper_dvv_unified_framework.md` (full paper, including §9).
2. **JGR tex + PDF** — `pixi run paper-pdf` (main PDF with §9 placeholder + Figs 1–6, plus a Supporting Information PDF; AGUTeX source for Overleaf).
3. **Quarto HTML website** — `pixi run paper-site` builds a small website under `paper/site/` (rendered to `paper/site/_site/`): a **Paper** page (full text, Figures 1–7) and a **Supporting Information** page (Figures S1–S12). Pages are self-contained (`embed-resources: true`), so `paper/site/_site/index.html` opens standalone and is deployable as-is (e.g., GitHub Pages). Requires [Quarto](https://quarto.org) on the PATH.

The same command also writes `paper/build/paper_dvv_agutex_jgr_solid_earth.tex`, an AGUTeX source file configured with `\journalname{JGR: Solid Earth}` for the official AGU/Overleaf `agujournal2019` template. Overleaf lists official AGU JGR templates for the shared AGUTeX class, but no separate JGR: Solid Earth template was found; use the official AGU JGR template and preserve the `figures/main/` paths when uploading the generated source and figures.

## Key Results

1. **Notation clarified**: measured $\delta v/v$ ≈ $\delta V_S/V_S$ via S-wave dominance in coda (Snieder, 2002; Singh et al., 2019).
2. **Thermoelastic $\delta v/v$** controlled by ∂(ρv²)/∂σ_c (50–1000), amplitudes 0.01–0.3% annually.
3. **Hydrological loading** produces competing load (+$\delta v/v$) and pore pressure (−$\delta v/v$) effects.
4. **Dynamic capillary effects** produce hysteretic $\delta v/v$ in partially saturated soils (Shi et al., 2026).
5. **Stress-induced anisotropy** from microcrack closure explains Parkfield's contractional-strain correlation.
6. **Material microstructure** (crack density, cementation, grain contacts) controls nonlinear sensitivity.
7. **Multi-frequency $\delta v/v$ + GNSS/InSAR** may enable depth-resolved 3-D stress/strain imaging when sensitivity kernels and material constraints are available.
8. **Coda-window selection** is treated as a physical part of the measurement, with reproducible metrics implemented in `codameter.window_selection`.
9. **Six alternative mechanisms** beyond nonlinear elasticity are systematically assessed.
10. **Spatial generalization** requires 3-D velocity models, $V_P/V_S$, density, geotechnical, and geodetic data.
11. **Linear acoustoelasticity** valid for strains below ~10⁻⁵; the manuscript includes a full reference list and a BibTeX seed bibliography.

## Citation

If you use this work, please cite:

```
Denolle, M. A. (2026). Seismic velocity changes as stress and strain meters:
A unified framework for environmental, tectonic, and volcanic monitoring.
[Preprint/Working paper].
```

## AI Transparency

M. A. Denolle is the sole author and is responsible for all content. AI tools (Claude, Anthropic) were used as a research and writing assistant under the author's direction; they are not eligible for authorship under AGU policy. Full documentation of prompts, reasoning, and model information is in `docs/ai_documentation/`. See the [Statement of AI Use](docs/ai_documentation/03_model_card.md) for details.

## License

This work is licensed under [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).
