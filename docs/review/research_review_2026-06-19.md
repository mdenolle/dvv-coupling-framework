# Research Review and Submission Readiness Audit

**Date:** 2026-06-19  
**Scope:** manuscript, theory notes, core analysis code, bibliography, and proposed `codameter` transition  
**Reviewer stance:** critical scientific review, with emphasis on claim accuracy, equation consistency, and package-readiness

## Overall Assessment

The research question is strong and publishable: ambient-noise $\delta v/v$ needs a unified physical interpretation across thermoelastic, hydrological, tectonic, and volcanic forcing. The repository has a credible theoretical spine: Murnaghan acoustoelasticity, Tromp and Trampert induced-stress anisotropy, Roeloffs/Fokker poroelastic loading, and recent agricultural-soil dynamic-capillary observations.

The paper should be framed as a **framework and synthesis with calibrated application examples**, not as a completed inversion method or a production implementation. The strongest original contribution is the stress/strain framing plus the Parkfield-Cascadia-Kilauea comparison showing when scalar volumetric strain fails and directional/fracture-fabric sensitivity is needed.

## High-Priority Scientific Corrections Made

1. **Cascadia exact-match overclaim corrected.** The manuscript previously described the 0.58 kPa/yr Cascadia match as an independent exact validation. Because Kidiwela et al. (2026) calibrate $\beta$ using the borehole strain, the stress match is an internal consistency check, not independent validation. The text now states this explicitly.

2. **Fokker et al. coefficient geometry clarified.** The simplified Eq. 5 conflated generic directional terms with surface-wave endmembers. The manuscript now gives the horizontal Rayleigh/SV and Love/SH coefficients and directs component-specific applications back to the full Tromp and Trampert directional form.

3. **Capillary equation made dimensionally defensible.** The previous partially saturated effective-pressure expression mixed terms with inconsistent dimensions. It has been replaced with a compact dynamic-capillary form,
   $$P_e = \sigma_g' + P_c^{eq}(S_w) + \tau(S_w)\partial S_w/\partial t,$$
   with sign-convention caveats.

4. **Depth-resolved inversion claims toned down.** The paper now states that multi-frequency inversion is ill-conditioned and requires kernels, regularization, uncertainty propagation, and resolution tests. It is a proposed workflow, not yet a demonstrated 3-D inversion.

5. **Core code bug fixed.** `analysis/poroelastic_framework.py::beta_eff` documented the undrained amplification as $1/(1-\alpha_BB)$ but implemented $1+\alpha_BB$. The implementation and tests now match the poroelastic limit.

6. **Thermoelastic helper units fixed.** `thermoelastic_sensitivity_s_T` now treats $\partial(\rho V^2)/\partial\sigma_c$ as a dimensionless derivative, consistent with Richter/Ermert notation, instead of multiplying by shear modulus.

## Literature and Citation Audit

Verified central references via DOI/Crossref:

- Clements and Denolle (2023), JGR Solid Earth, DOI `10.1029/2022JB025553`.
- Fokker et al. (2021), Remote Sensing, DOI `10.3390/rs13142684`.
- Okubo et al. (2024), JGR Solid Earth, DOI `10.1029/2023JB028084`.
- Hotovec-Ellis et al. (2022), JGR Solid Earth, DOI `10.1029/2021JB023324`.
- Kidiwela et al. (2026), Science Advances, DOI `10.1126/sciadv.aea3684`.
- Shi et al. (2026), Science, DOI `10.1126/science.aec0970`.

The literature review is relevant but should be sharpened around three axes:

1. **Observable definition:** distinguish CWI/coda $\delta v/v$, surface-wave $\delta c/c$, and local $\delta V_S/V_S$ every time equations move between them.
2. **Mechanism separation:** density, source-spectrum changes, scatterer relocation, direct temperature effects, and fluid substitution must remain explicit alternatives, not footnotes.
3. **Validation level:** distinguish calibrated consistency checks from independent predictions. This is especially important for Cascadia.

## Claims That Still Need Care Before Submission

| Claim | Status | Required framing |
| --- | --- | --- |
| Multi-frequency $\delta v/v$ enables 3-D stress imaging | Aspirational | "May enable" with kernels, priors, and resolution tests |
| Cascadia stress exactly matches borehole strain | Calibration-dependent | "Borehole-calibrated consistency check" |
| Same $\beta$ can compare low-frequency Cascadia segments | Conditional | Requires comparable kernels and material sensitivities |
| Capillary model is part of the framework | Literature-supported, not implemented | State that Shi et al. supplies external evidence; notebooks do not yet implement it |
| Parkfield/Kilauea directional $\beta$ gives $\mu'$ | Approximate | Eq. 7 is isotropic; directional use is order-of-magnitude |

## `codameter` Implementation Requirements

The production package should not start from the notebooks. It should implement the paper workflow as testable modules:

1. **Data layer:** waveform-derived $\delta v/v$ tables, geodetic strain, met/hydro forcings, site metadata, and uncertainty columns.
2. **Earth model layer:** $V_S(z)$, $V_P(z)$, $\rho(z)$, water table, lithology, porosity, permeability, and kernel metadata.
3. **Forward models:** thermoelastic, saturated poroelastic, loading/pore-pressure competition, anisotropic induced-stress projection, healing/slow dynamics, and a future capillary/vadose model.
4. **Diagnostics:** scalar volumetric test, deviatoric/fracture-fabric test, drained-undrained Pe number, frequency-depth resolution test, and residual mechanism triage.
5. **Inversion API:** regularized multi-frequency inversion with priors on $\beta(z)$ or $\mu'(z)$ and explicit posterior/resolution outputs.

Minimum acceptance tests for `codameter`:

- Reproduce Parkfield $\beta_{\text{axial}}\approx240$ and stress rate near 12 kPa/yr from published Okubo inputs.
- Reproduce Cascadia $\mu'\approx620$ from borehole-calibrated $\beta\approx3160$ without calling it independent validation.
- Reproduce Kilauea radial $\beta\approx250$-330 and stress within a factor of two of the simplified spheroid estimate.
- Demonstrate that Fokker Rayleigh and Love coefficients give different loading responses.
- Demonstrate that `beta_eff` approaches drained and undrained poroelastic limits.

## Remaining Submission Blockers

1. **Real data examples are still missing.** The paper needs at least one reprocessed Clements and Denolle (2023) example or a clearly labeled published-data reproduction. Synthetic examples alone are not enough for a research-grade companion package.

2. **Notebook/code consistency needs a pass.** The core helper is fixed, but notebooks may still contain older Fokker coefficient shortcuts and stale outputs. Re-execute notebooks after equation updates.

3. **Bibliography is split.** The manuscript has a full manual reference list and `paper/references.bib` now has a central seed bibliography. Before journal submission, choose one citation workflow and make it complete.

4. **Archive DOI is still pending.** The fake Zenodo DOI has been removed from the manuscript; mint the real archive DOI before submission.

5. **AI co-author policy must match journal requirements.** Many journals allow AI use disclosure but not AI authorship. Verify target-journal policy before submission and adjust title page accordingly.

## Recommended Framing for Submission

Target JGR Solid Earth or GJI as a **framework plus calibrated case-study synthesis**. The pitch should be:

> We show how $\delta v/v$ can be interpreted as stress or strain only after accounting for geometry, fracture fabric, saturation state, and frequency-dependent sensitivity. The same observed velocity trend can imply very different stress rates once $\beta$ and $\mu'$ are normalized across lithologies.

Do not pitch this as a completed 3-D inversion method until `codameter` has a demonstrated inversion and resolution test.
