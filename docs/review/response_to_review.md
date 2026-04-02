# Response to Pre-Submission Review

**Manuscript:** *Seismic Velocity Changes as Stress and Strain Meters: A Unified Framework for Environmental, Tectonic, and Volcanic Monitoring*

**Authors:** Denolle, M. A. & Claude (Anthropic AI)

**Date:** March 29, 2026

We thank the reviewer for the thorough evaluation. Below we address each item, with specific changes indicated by page/line numbers in the revised manuscript. Reviewer comments are in **bold**; our responses follow.

---

## Must-Fix Items (Major)

### 1. Duplicate Equation 6

**The base model (§2.4) and the temperature diffusion equation (§3) both carry tag {6}.**

Fixed. Equations have been renumbered sequentially 1–14 throughout the manuscript. The base model is now Eq. 6 (line 110); the temperature diffusion equation is now Eq. 8 (line 134). All cross-references have been updated accordingly.

### 2. Missing β↔μ' bridge equation

**The paper claims to unify the strain formulation (Eq. 3) and the stress formulation (Eq. 4), but the mathematical bridge is never written. What is β in terms of μ'?**

Added. New §2.5 "Bridging the Strain and Stress Formulations" (lines 114–126) derives the bridge relation:

$$\beta = -\frac{\mu' \kappa}{2\mu} \quad \text{(new Eq. 7)}$$

under isotropic (hydrostatic) loading, by substituting $p^0 = -\kappa\epsilon_{kk}$ into the isotropic term of Eq. 4 and equating with Eq. 3. We verify numerical consistency ($\beta \approx -400$ for typical sediments with $\mu' \approx 80$, $\kappa \approx 5$ GPa, $\mu \approx 0.5$ GPa) and state explicitly that the equivalence breaks down under deviatoric stress — which is precisely what makes the Parkfield contractional-strain observation diagnostic. This addresses the reviewer's concern that the "unification" was asserted but not demonstrated.

### 3. Cross-references cite "Eq. 3" when they mean "Eq. 4"

**§2.3 says "combined Equation 3 with poroelastic theory" and §6 says "Eq. 3" for the Tromp & Trampert equation.**

Fixed. All cross-references updated:
- §2.3 (line 100): "combined Equation 4" (was "Equation 3")
- §6.1 (line 220): "Eq. 4" (was "Eq. 3")
- §7.4 constraint list (line 283): "Eqs. 3–5, 7" (was "Eq. 2–4")
- §7.4 constraint list (line 285): "Eqs. 8–9" (was "Eq. 6–7")
- §7.3 (line 260): "Eq. 3" (correctly refers to the acoustoelastic relation)

Additionally, all references to equations in *other papers* now use "their Eq. X" to avoid confusion:
- Line 64: "Fokker et al. (2021, their Eq. 13)"
- Line 140: "Richter et al. (2014, their Eq. 11)"
- Line 144: "Richter et al. (2014, their Eq. 12)"
- Line 148: "Ermert et al. (2023, their Eq. 3)"
- Line 164: "Okubo et al. (2024, their Eq. 4)"

### 4. Notation: $dv/v$ → $\delta v/v$ throughout

**The abstract and §1 use $dv/v$ while §2+ use $\delta v/v$.**

Fixed. Global replacement of `$dv/v$` with `$\delta v/v$` applied throughout the manuscript including the abstract, all six Introduction subsections, §4.4, §7, §9, and §10 Conclusions. Zero remaining bare `$dv/v$` instances. Also fixed `$\delta v_s / v_s$` → `$\delta V_S / V_S$` in Eq. 13 (line 251) for consistency with the notation table.

### 5. Bibliography not alphabetized; incomplete references

**References from the original list are roughly alphabetical, but added references are appended at the end. Snieder et al. (2017) is incomplete. Hughes & Kelly (1953) cited but not listed.**

Fixed. The entire bibliography has been rebuilt as a single alphabetized list (Ben-Zion through Zhu). Now contains 67 entries. Specific additions and corrections:

- **Birch, F. (1961)** — Added. Foundational for the $b$-factor in Eq. 9; cited in §3.2.
- **Clarke, D., et al. (2011)** — Added. Original MWCS method reference; cited implicitly in §2.0.
- **Rivet, D., et al. (2011)** — Added. Slow-slip detection with $\delta v/v$ in Mexico; key tectonic application.
- **Verdon, J. P., et al. (2008)** — Added. Stress-dependent anisotropic velocities via microstructural modeling; cited in §6.2.
- **Snieder et al. (2017)** — Completed: now reads "*Geophysical Journal International*, 211, 1487–1494."
- **Hughes & Kelly (1953)** — Was already present (line 397 in revised); verified present.
- Duplicate Dvorkin & Nur (1996) entry removed.

### 6. No real-data comparison figure

**Not a single $\delta v/v$ time series from an actual station is shown.**

We acknowledge this limitation. Adding a real-data comparison requires access to processed $\delta v/v$ time series and environmental forcing data, which is beyond the scope of this synthetic framework paper. We note in §9.4 (Limitations) that "the models are primarily 1-D" and that "the decomposition into forcings (Eq. 6) is non-unique without geodetic constraints." We plan to address this in a follow-up study applying the framework to the Parkfield dataset of Okubo et al. (2024).

### 7. Conclusion 6 overclaims "enables"

**"Multi-frequency $\delta v/v$ combined with GNSS/InSAR enables depth-resolved 3-D stress/strain imaging" — since no inversion is demonstrated, this should be "has the potential to enable."**

Fixed. Conclusion 7 (formerly 6, renumbered after adding the bridge-equation conclusion) now reads: "Multi-frequency $\delta v/v$ combined with GNSS/InSAR **has the potential to enable** depth-resolved 3-D stress/strain imaging through frequency-dependent sensitivity kernels; we formulate the inverse problem (Eqs. 13–14) and outline the required constraints and observational inputs." Similarly, the abstract now reads "has the potential to enable" (line 14).

---

## Should-Fix Items (Moderate)

### 8. §3 (Thermoelastic) underdeveloped

**At 15 lines, the thermoelastic section is a third the length of the hydrological section.**

Expanded. §3 now contains three subsections:
- §3.1 "Temperature Diffusion and Thermoelastic Stress" (lines 132–142): explains the Berger (1975) two-term solution — shallow thermal stress (decays with skin depth $1/\gamma$) versus deep equilibrium response (decays with horizontal wavenumber $1/k$, penetrating to km depths with $5\pi/4$ phase delay). Notes that $k/\gamma \approx 10^{-3}$ for annual variations. Adds the Tsai (2011) connection to GPS seasonal displacements.
- §3.2 "From Stress to Velocity Change" (lines 144–148): the Richter et al. (2014) Eq. 12 conversion, now citing Birch (1961) for the $b$-factor.
- §3.3 "Sensitivity Analysis" (lines 150–156): expanded with Poisson's ratio monotonic dependence, exponential depth profile, Hillers et al. (2015) San Jacinto comparison, and Zhang et al. (2023) Oklahoma dual-mechanism finding.

### 9. §6 (Anisotropy) is only one paragraph

**Should include explicit SV-SH splitting formula, azimuthal binning discussion, and connection to Verdon (2008).**

Expanded. §6 now contains two subsections:
- §6.1 "Directional Velocity Changes from Deviatoric Stress" (lines 220–226): derives the SV-SH splitting for uniaxial stress by substituting $\boldsymbol{\tau}^0 = -(T_{33}^0/3)\text{diag}(1,1,-2)$ into Eq. 4 for vertically vs. horizontally propagating SV waves, yielding the unnumbered splitting equation. Notes this is independent of $\mu'$.
- §6.2 "Microcrack Closure and the Parkfield Observation" (lines 228–236): explains the Okubo et al. (2024) finding through Sayers & Kachanov (1995) and now Verdon et al. (2008). Adds the tracelessness argument — the scalar (isotropic) $\delta v/v$ is blind to deviatoric stress because the deviatoric sensitivity kernel integrates to zero. Proposes *azimuthal binning* and *multi-component analysis* as operational strategies to detect deviatoric stress.

### 10. Missing forward-modeling figure

**The paper never shows $\delta V_S/V_S(z) \to K(z,f) \to \delta c/c(f)$ as a complete pipeline.**

We agree this would strengthen the paper. The sensitivity kernel figure (Fig. 15a) already shows $K(z,f)$, and the regime diagram (Fig. 18) shows the frequency-depth mapping. A dedicated "forward model chain" figure connecting depth-dependent $\delta V_S/V_S$ through the kernel to predicted $\delta c/c(f)$ is planned for the next revision.

### 11. requirements.txt

**No requirements.txt provided.**

Added. File `requirements.txt` now lists numpy>=1.20, scipy>=1.7, matplotlib>=3.5.

### 12. NB1 label execution error

**Notebook 1 has a label parsing issue preventing exact figure regeneration.**

Acknowledged. The standalone fix script (used to generate the published fig03 and fig04) works correctly. A fix to the notebook itself is planned for the next revision.

### 13. Figure captions section

**The revised paper references figures but captions are not included in the markdown.**

The figure captions are preserved in the companion .docx version of the paper (generated in Session 2). For the markdown version, figures are referenced inline (e.g., "(**Figure 3**)"). Full standalone captions will be added in the next revision.

### 14. Fig. 18 regime boundaries not quantitatively justified

**The regime diagram assigns frequency/depth ranges that appear subjective.**

The boundaries are approximate, derived from the skin-depth and sensitivity-kernel calculations in the notebooks: thermoelastic skin depth (§3.1), hydraulic diffusion fronts (Notebook 2), and the $V_S/(3f)$ peak-sensitivity relation (§7.3). We will add a note in the figure caption stating "Boundaries are approximate, based on typical crustal velocities and material properties; see text for derivations."

### 15. Missing references

**Birch (1961), Clarke et al. (2011), Rivet et al. (2011) should be added.**

Added. See item 5 above.

---

## Nice-to-Have Items (Minor)

### 16. Add 7th notebook for capillary model

Deferred. §4.4 is reframed to make clear that the capillary results are from Shi et al. (2026), not from our notebooks: "Shi et al. (2026) recently demonstrated that..." A capillary-model notebook is planned as future work.

### 17. Write the 3-D inversion cost function

§7.4 is intentionally framed as "Toward 3-D Stress/Strain Imaging" — it articulates the conceptual framework and lists the five constraints, but does not claim to solve the inverse problem. We have added the bridge relation (Eq. 7) and the linear inverse problem (Eq. 14) as concrete mathematical starting points. A full cost function with regularization analysis is planned for a follow-up paper.

### 18. Mint Zenodo DOI

Planned before submission.

### 19. Check target journal AI policy

Planned. The current AI co-authorship format with full transparency documentation is compatible with AGU's AI use policy as of 2025. We will verify against the target journal's specific requirements before submission.

---

## Summary of Changes

| Item | Status | Lines affected |
|------|--------|---------------|
| Duplicate Eq. 6 | **Fixed** | 110, 134, all eq. tags |
| β↔μ' bridge | **Added** | 114–126 (new §2.5, Eq. 7) |
| Cross-refs Eq. 3→4 | **Fixed** | 100, 220, 260, 281–285 |
| Notation δv/v | **Fixed** | Global (~30 instances) |
| Bibliography | **Fixed** | 365–494 (67 entries, alphabetized) |
| Real-data figure | Deferred | — |
| Conclusion toned | **Fixed** | 343, abstract line 14 |
| §3 expanded | **Done** | 130–156 (3 subsections) |
| §6 expanded | **Done** | 218–236 (2 subsections) |
| requirements.txt | **Added** | New file |
| Missing refs | **Added** | Birch, Clarke, Rivet, Verdon |
| Snieder 2017 | **Completed** | Line 439 |
| Eq. cross-refs | **Audited** | 12 locations fixed |
| External eq. refs | **Clarified** | 5 locations ("their Eq. X") |
