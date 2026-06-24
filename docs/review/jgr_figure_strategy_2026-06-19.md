# JGR Solid Earth Figure Strategy Review

**Date:** 2026-06-19  
**Reviewer:** OpenAI Codex assistant, requested by M. A. Denolle  
**Target journal:** *Journal of Geophysical Research: Solid Earth*

## Executive Assessment

The manuscript currently has 18 numbered figures in the main text. That is too many for a clean JGR Solid Earth research paper. The present figure set reads like a companion tutorial or methods monograph: it is valuable for the repository and for `codameter`, but it dilutes the manuscript story.

For JGR Solid Earth, the main text should carry the argument with about 7-8 display items plus the cross-site synthesis table. The rest should move to Supporting Information or appendices, where they can remain useful as validation and pedagogy without interrupting the paper's central arc.

I could not verify the live AGU author-resource pages from this environment because `agu.org` was Cloudflare-blocked. The recommendation below therefore uses standard AGU-style publication-unit and reviewer-load logic rather than a freshly verified hard figure limit. Verify the current AGU instructions before submission.

## Recommended Story

The paper should be framed as:

1. A unified stress/strain interpretation framework for `delta v/v`.
2. A diagnostic split between isotropic, deviatoric, hydrological, capillary, and rheological mechanisms.
3. Three published-data applications showing when the scalar formulation works and when it fails.
4. A forward path toward `codameter` as the implementation package.

Figures should serve those four points. Parameter sweeps, derivation illustrations, and tutorial panels should move to the supplement unless they directly support one of the three case-study claims.

## Main-Text Figure Plan

| Proposed main display | Source | Role in story | Action |
|---|---|---|---|
| **Fig. 1: Unified workflow / mechanism map** | New figure, or adapt current Fig. 18 | Establish the paper's intellectual contribution at first glance: forcing -> stress/strain -> material sensitivity -> observed `delta v/v` -> diagnostic/inversion workflow. | Create or promote Fig. 18 with a workflow overlay. |
| **Fig. 2: Kernel/depth sensitivity and inversion limits** | Current Fig. 15 | Justifies frequency-dependent depth sensitivity and the `codameter` workflow. | Keep main, but caption should emphasize ill-conditioning and need for kernels. |
| **Fig. 3: Hydrological loading versus pore pressure** | Current Fig. 7 | Shows the key sign competition and why hydrological interpretation is not scalar. | Keep main. Move Roeloffs/GWL details to SI. |
| **Fig. 4: Material sensitivity / acoustoelastic scaling** | Current Fig. 8 | Explains why the same `delta v/v` amplitude maps to very different stresses across lithologies. | Keep main. |
| **Fig. 5: Deviatoric anisotropy and crack fabric** | Merge current Figs. 11 and 12 | Shows why Parkfield and Kīlauea require directional stress/fracture geometry. | Merge into one main figure. |
| **Fig. 6: Rheological diagnostic crossplots** | Merge current Figs. 9 and 14 | Gives the elastic/viscoelastic/slow-dynamics diagnostic toolkit. | Keep one merged main figure; move extra model panels to SI. |
| **Fig. 7: Three-site application synthesis** | New figure from Table 2 | This is the decisive JGR figure: Parkfield, Cascadia, Kīlauea side-by-side with `delta v/v`, controlling strain component, beta, mu prime, stress estimate, and validation/cross-check. | Add as main. |
| **Table 1 or Fig. 8: Parameter/validity summary** | Current Fig. 17, shortened | Useful for a framework paper, but only if compressed. | Prefer a real table in main; full parameter table becomes Table S1. |

This plan leaves 7 figures plus one table, or 8 displays total. That is much more defensible for JGR Solid Earth than 18 figures.

## Move to Supporting Information

| Current figure | Recommendation | Rationale |
|---|---|---|
| Fig. 1 temperature diffusion | Fig. S1 | Background derivation support; not central to new contribution. |
| Fig. 2 Berger thermoelastic stress | Fig. S2 | Useful validation/tutorial figure; too detailed for main story. |
| Fig. 3 thermoelastic sensitivity | Fig. S3, or one panel merged into main workflow | Parameter sweep; keep out of main unless reviewer asks. |
| Fig. 4 synthetic thermoelastic time series | Fig. S4 | Tutorial/example output. |
| Fig. 5 Roeloffs pore-pressure diffusion | Fig. S5 | Derivation support for hydrology; current Fig. 7 carries the main point better. |
| Fig. 6 groundwater level model | Fig. S6 | Useful for implementation; not needed for the narrative. |
| Fig. 9 nonlinear detection | Merge into main rheology figure or Fig. S7 | Redundant with Fig. 14. |
| Fig. 10 Murnaghan EOS | Fig. S8 | Pedagogical; equations already carry the theory. |
| Fig. 13 healing models | Fig. S9, or one panel merged into rheology figure | Detailed slow-dynamics model behavior belongs in SI. |
| Fig. 16 linearity validity | Fig. S10 | Important caveat but not a main-display result. |
| Fig. 17 parameter table | Table S1, unless drastically shortened | A large table as a figure is not ideal for JGR production. |

## Required New or Revised Main Figures

1. **New synthesis/case-study figure.** The paper's strongest claim is that Parkfield, Cascadia, and Kīlauea exercise different branches of the same framework. A table is not enough; JGR reviewers should see this as a visual result.

2. **Merged anisotropy figure.** Current Figs. 11 and 12 are individually useful but together they over-explain. One figure should show: applied stress, fracture fabric, expected sign of `delta v/v`, and observational examples.

3. **Merged rheology diagnostic figure.** Current Figs. 9, 13, and 14 can be reduced to one main figure plus supporting figures. The main point is diagnostic shape, not every model curve.

4. **Workflow figure tied to `codameter`.** The manuscript should make clear that the companion package will implement a reproducible workflow: ingest `delta v/v`, compute kernels, evaluate environmental forward models, run mechanism diagnostics, and report stress/strain/rheology with uncertainty.

## Text Edits Needed After Figure Triage

- Replace most main-text references to Figs. 1-6, 9-10, 13, 16-17 with supporting-figure references.
- Make Sections 3-5 shorter and less tutorial-like. Keep the equations, then point detailed validation to SI.
- Expand Section 9 around the new three-site synthesis figure. This is the part that makes the paper JGR rather than a framework note.
- Convert current "Figure 17" into a true table or move it to SI. A table rendered as a figure is production-awkward.
- Remove "Six companion notebooks with 18 figures" from the abstract. Replace with "Companion notebooks reproduce the main and supporting figures."

## AGU/JGR Policy Risk: AI Authorship

The current title page lists "Claude (Anthropic AI)" as a co-author. That is likely a submission risk for JGR Solid Earth. Even if AGU allows AI use disclosure, many publishers do not allow AI systems to be listed as authors because authorship requires accountability, conflict-of-interest disclosure, and approval of the final manuscript.

Recommended submission posture:

- Remove the AI system from the author line before journal submission.
- Keep a transparent **Statement of AI Use** in the manuscript and repository.
- Keep detailed AI traceability files in `docs/ai_documentation/`.
- Verify the current AGU/Wiley policy before submission, because the live AGU page could not be accessed from this environment.

## Bottom Line

The scientific story is strong enough for JGR Solid Earth, but the figure strategy should be tightened. Move roughly 10 of 18 figures to Supporting Information, add one high-impact three-site synthesis figure, and make the main display set support the paper's central claim rather than the repository's full tutorial scope.

## Implementation Status

Implemented after this review:

- Added a reproducible main-figure script: `analysis/jgr_main_figures.py`.
- Generated seven main figures in `figures/main/`.
- Updated the manuscript to cite the seven main figures and move derivation/tutorial plots to Supporting Information.
- Added a concise Table 1 in the manuscript and retained the three-site Table 2 as the quantitative synthesis table.
- Added `paper/supporting_information.md` with Figure S1-S12 and Table S1 captions.
- Updated the README to describe the main/supporting figure split and the regeneration command.
