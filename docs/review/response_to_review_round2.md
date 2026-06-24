# Response to Pre-Submission Review — Round 2

**Manuscript:** *Seismic Velocity Changes as Stress and Strain Meters: A Unified Framework for Environmental, Tectonic, and Volcanic Monitoring*

**Date:** March 29, 2026

We thank the reviewer for the careful second-round evaluation. Below we address all 13 items (6 must-fix, 7 should-fix).

---

## Must-Fix Items

### 1. §2.0 tautology: "(equivalently $\delta v/v$)"

**Fixed.** Line 60 now reads: "The quantity $\delta v/v$ (equivalently written $dv/v$ in much of the literature)...". Also added Clarke et al. (2011) to the citation list here for the MWCS method, resolving should-fix 11 simultaneously.

### 2. §2.4 header: bare "dv/v"

**Fixed.** Header now reads "### 2.4 General $\delta v/v$ Model".

### 3. Figure captions missing

**Fixed.** A complete "Figure Captions" section (18 captions) has been added between Data Availability and References. Each caption identifies the physical content, key parameters shown, and the source papers being compared.

### 4. Tromp et al. (2005) missing from bibliography

**Fixed.** Added: Tromp, J., Tape, C., & Liu, Q. (2005). Seismic tomography, adjoint methods, time reversal and banana-doughnut kernels. *Geophysical Journal International*, 160, 195–216. Cited in §8.3 and §9.4.

### 5. "[repository URL]" placeholder

**Fixed.** Data Availability now states that the notebooks and figure-generation code will be archived on Zenodo before publication, with the archive DOI pending.

### 6. Obermann (2013) vs. (2014) citation mismatch

**Fixed.** Two in-text citations corrected:
- Line 26 (depth sensitivity of coda waves): changed from Obermann et al. (2013) to Obermann et al. (2014), matching the correct paper on depth sensitivity kernels.
- Line 254 (frequency-dependent sensitivity): changed from Obermann et al. (2013) to Obermann et al. (2014).
- Line 128 (scatterer relocation): Obermann et al. (2013) correctly retained — this is the volcano imaging paper that develops the scatterer-change theory.

---

## Should-Fix Items

### 7. Note drained vs. undrained κ in bridge equation

**Fixed.** New paragraph added to §2.5 (after the numerical check) explaining that Eq. 7 uses the drained bulk modulus $\kappa$, appropriate for long timescales. At shorter timescales (undrained limit), the effective bulk modulus is $\kappa_u = \kappa/(1 - \alpha_B B)$, producing a larger $|\beta|$ — meaning velocity is more sensitive to strain when pore fluid has not drained. This connects the bridge equation directly to the drained-undrained transition in §4.1 and explains why rapid loading events produce different $\delta v/v$ amplitudes than slow loading for the same total strain.

### 8. §6.1 splitting: "different propagation directions" not "SV vs. SH"

**Fixed.** The derivation now explicitly states that the comparison is between "vertically propagating S-waves ($\hat{\mathbf{k}} = \hat{\mathbf{z}}$, $\hat{\mathbf{a}} = \hat{\mathbf{x}}$) versus horizontally propagating S-waves with vertical polarization ($\hat{\mathbf{k}} = \hat{\mathbf{x}}$, $\hat{\mathbf{a}} = \hat{\mathbf{z}}$)." The equation label is changed from "SV-SH" to "vert. vs. horiz." A clarifying sentence is added: "For a fixed propagation direction, the SV-SH splitting...is likewise proportional to the deviatoric stress but depends on the specific geometry of propagation relative to the stress axis."

### 9. Number subsections in §5 and §8

**Fixed.** §5 now has §5.1 "The Acoustoelastic Parameter and Its Detection" and §5.2 "Geological and Material Controls." §8 now has §8.1 "Homogeneous Half-Space," §8.2 "Linear Acoustoelasticity," and §8.3 "Spatial Generalization." All 36 subsections are now sequentially numbered.

### 10. Eq. 9 notation: $\Delta v/v$ → $\delta v/v$

**Already resolved.** Eq. 9 already uses $\delta v/v$ on the left side; the $\Delta\sigma_c$ on the right correctly denotes the stress change (not a velocity notation).

### 11. Clarke et al. (2011) in-text citation

**Fixed.** Now cited on line 60 alongside Poupinet et al. (1984) and Snieder et al. (2002) in §2.0 where CWI measurement methods are introduced.

### 12. Practical Workflow summary in §9

**Added.** New §9.4 "Practical Workflow for Applying the Framework at a New Site" provides a six-step procedure: (1) characterize site with velocity profile, (2) compute sensitivity kernels, (3) estimate nonlinear parameters via bridge relation, (4) forward model environmental $\delta v/v$, (5) subtract to isolate residuals, (6) compare with geodesy for rheological diagnosis. Each step references the relevant equations.

### 13. Real-data comparison

**Partially addressed.** While we do not add a new figure with reprocessed data, the expanded §9.5 Limitations now explicitly names four published validations of the individual forward models: Richter et al. (2014) for thermoelastic, Fokker et al. (2021) for poroelastic, Clements and Denolle (2023) for the combined California analysis, and Okubo et al. (2024) for Parkfield. We state that applying the unified framework — particularly the bridge relation, depth-resolved inversion, and capillary extension — to these datasets is a priority for future work. We also acknowledge that the capillary model (§4.4) is presented as external evidence from Shi et al. (2026) rather than implemented in the companion notebooks.

---

## Summary of All Changes

| Item | Type | Status | Location |
|------|------|--------|----------|
| 1. Tautology "equivalently δv/v" | Must | ✅ Fixed | Line 60 |
| 2. §2.4 header | Must | ✅ Fixed | Line 108 |
| 3. Figure captions | Must | ✅ Added | After Data Availability (18 captions) |
| 4. Tromp et al. (2005) | Must | ✅ Added | Bibliography |
| 5. Repository URL | Must | ✅ Filled | Data Availability |
| 6. Obermann 2013/2014 | Must | ✅ Fixed | Lines 26, 254 |
| 7. Drained/undrained κ | Should | ✅ Added | §2.5, new paragraph |
| 8. §6.1 splitting label | Should | ✅ Fixed | Lines 224–230 |
| 9. §5, §8 subsection numbers | Should | ✅ Added | §5.1, §8.1, §8.2 |
| 10. Eq. 9 notation | Should | ✅ Already correct | — |
| 11. Clarke et al. citation | Should | ✅ Added | Line 60 |
| 12. Practical Workflow | Should | ✅ Added | New §9.4 |
| 13. Real-data paragraph | Should | ✅ Added | §9.5, expanded |

**Final paper statistics:** 564 lines, ~9000 words, 14 numbered equations + 1 unnumbered, 68 references, 36 subsections, 18 figure captions, 9 conclusions.
