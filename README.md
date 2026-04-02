# dv/v as Stress and Strain Meter: Unified Framework

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

**Seismic Velocity Changes as Stress and Strain Meters: A Unified Framework for Environmental, Tectonic, and Volcanic Monitoring**

Marine A. Denolle$^1$ and Claude (Anthropic AI)$^2$

$^1$ Department of Earth and Space Sciences, University of Washington  
$^2$ Anthropic, San Francisco, CA

---

## Overview

This repository contains the manuscript, companion Jupyter notebooks, and figures for a research paper that develops a unified theoretical framework for interpreting ambient-noise-derived seismic velocity changes (dv/v) across environmental, tectonic, and volcanic settings.

The framework connects:
- **Murnaghan (1937)** third-order elasticity → acoustoelastic parameter β
- **Berger (1975)** thermoelastic stress → temperature-induced dv/v
- **Roeloffs (1988)** poroelastic diffusion → hydrological dv/v
- **Tromp & Trampert (2018)** induced stress → anisotropic dv/v
- **Fokker et al. (2021)** loading vs. pore pressure → competing effects
- **Shi et al. (2026)** dynamic capillary effects → partially saturated media
- **Snieder et al. (2017)** logarithmic healing → post-seismic recovery

through the common thread of **nonlinear elasticity**.

## Repository Structure

```
├── README.md                              # This file
├── LICENSE                                # CC BY 4.0
├── CITATION.cff                           # Machine-readable citation metadata
├── pixi.toml                              # Reproducible environment (pixi)
│
├── paper/
│   ├── paper_dvv_unified_framework.md     # Full manuscript (Markdown + LaTeX math)
│   └── references.bib                     # BibTeX bibliography (to populate)
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
│
├── figures/
│   ├── notebooks/                         # Outputs from scenario model notebooks
│   │   └── fig01–fig18 (.png)           # 18 publication-quality figures
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

Dependencies (numpy, scipy, matplotlib, jupyterlab) are resolved automatically via `pixi.toml`.
No proprietary code, data, or API keys are needed.

## Reproducing Figures

```bash
# Launch JupyterLab directly in the analysis folder
pixi run lab
# Execute notebooks 01 through 06 in order
```

Figures are committed under `figures/notebooks/` (scenario models) and `figures/coupling/` (data analysis).

## Key Results

1. **Notation clarified**: measured $\delta v/v$ ≈ $\delta V_S/V_S$ via S-wave dominance in coda (Snieder, 2002; Singh et al., 2019).
2. **Thermoelastic $\delta v/v$** controlled by ∂(ρv²)/∂σ_c (50–1000), amplitudes 0.01–0.3% annually.
3. **Hydrological loading** produces competing load (+$\delta v/v$) and pore pressure (−$\delta v/v$) effects.
4. **Dynamic capillary effects** produce hysteretic $\delta v/v$ in partially saturated soils (Shi et al., 2026).
5. **Stress-induced anisotropy** from microcrack closure explains Parkfield's contractional-strain correlation.
6. **Material microstructure** (crack density, cementation, grain contacts) controls nonlinear sensitivity.
7. **Multi-frequency $\delta v/v$ + GNSS/InSAR** enables depth-resolved 3-D stress/strain imaging.
8. **Six alternative mechanisms** beyond nonlinear elasticity are systematically assessed.
9. **Spatial generalization** requires 3-D velocity models, $V_P/V_S$, density, geotechnical, and geodetic data.
10. **Linear acoustoelasticity** valid for strains below ~10⁻⁵; bibliography now contains ~60 OA references.

## Citation

If you use this work, please cite:

```
Denolle, M. A., & Claude (Anthropic AI). (2026). Seismic velocity changes as 
stress and strain meters: A unified framework for environmental, tectonic, 
and volcanic monitoring. [Preprint/Working paper].
```

## AI Transparency

This work was produced through human–AI collaboration. Full documentation of prompts, reasoning, and model information is in `docs/ai_documentation/`. See the [Statement of AI Use](docs/ai_documentation/03_model_card.md) for details.

## License

This work is licensed under [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).
