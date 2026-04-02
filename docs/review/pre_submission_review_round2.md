# Pre-Submission Review — Round 2

**Manuscript:** *Seismic Velocity Changes as Stress and Strain Meters: A Unified Framework for Environmental, Tectonic, and Volcanic Monitoring*

**Authors:** Denolle, M. A. & Claude (Anthropic AI)

**Review date:** March 29, 2026

**Rubric:** Denolle group synthesis of peer review guidelines (AGU, GJI, Seismica, SSA, PNAS)

---

## Overall Assessment

The authors have substantially improved the manuscript in response to the first review. The duplicate equation numbering is resolved, notation is homogenized, the bibliography is alphabetized and complete, and the two most important structural additions — the β↔μ' bridge equation (new §2.5) and the expanded anisotropy section (§6) — significantly strengthen the theoretical contribution. The paper now reads as a coherent synthesis that makes an explicit, verifiable unifying claim (Eq. 7) rather than a loose assertion of conceptual connection.

**Recommendation: Minor revisions.**

---

## Criterion 1: Novelty and Significance

**Score: 8/10 (was 7) — Improved**

The bridge relation $\beta = -\mu'\kappa/(2\mu)$ (Eq. 7) is now the paper's centerpiece. This is a compact, testable equation that any researcher can verify against their own site parameters — the numerical check ($\beta \approx -400$ from $\mu' \approx 80$, $\kappa \approx 5$ GPa, $\mu \approx 0.5$ GPa) is convincing and the stated equivalence conditions (isotropic loading only) are honest. The explicit statement that the equivalence *breaks down* under deviatoric stress, and that this breakdown is diagnostic, gives the paper a predictive edge rather than a purely retrospective one.

**Remaining concern:** The bridge relation (Eq. 7) is derived by substituting $p^0 = -\kappa\epsilon_{kk}$ into the isotropic term of Eq. 4. This substitution assumes that the induced pressure is related to volumetric strain through the *drained* bulk modulus $\kappa$. In poroelastic media, one should distinguish between the drained bulk modulus $K$, undrained bulk modulus $K_u$, and the Biot effective stress coefficient $\alpha_B$. The paper should note that Eq. 7 applies to the drained (long-time) limit, and that the undrained equivalent would use $K_u = K / (1 - \alpha_B B)$, producing a different effective $\beta$ at short timescales. This is directly relevant to the drained-undrained transition discussed in §4.1.

---

## Criterion 2: Methods and Technical Soundness

**Score: 8/10 (was 7) — Improved**

**Issues resolved from Round 1:**
- Duplicate Eq. 6: Fixed. Equations are now 1–14 sequential.
- Cross-references: §2.3 correctly cites Eq. 4, §6.1 correctly cites Eq. 4, §7.4 constraint list correctly references Eqs. 3–5, 7 and Eqs. 8–9.
- External equation references now use "their Eq. X" — clear and unambiguous.
- §6 SV-SH splitting is correctly derived from Eq. 4 with $\boldsymbol{\tau}^0 = -(T_{33}^0/3)\text{diag}(1,1,-2)$.

**Remaining issues:**

1. **§2.0 line 60 has a tautology.** "The quantity $\delta v/v$ (equivalently $\delta v/v$)" — the parenthetical should read "(equivalently written $dv/v$ in the literature)" or similar. This appears to be a remnant of the notation replacement.

2. **Unnumbered equation in §6.1.** The SV-SH splitting equation is tagged `(*)` rather than given a number. Since the paper cites numbered equations throughout, this should either be numbered (as Eq. 15, or inserted into the sequence) or the `(*)` convention should be explained. The tag also introduces an inconsistency because the equation is labeled as "SV-SH" splitting but the derivation compares vertically propagating SV to horizontally propagating SV — these are not the same as SV vs. SH polarization for a fixed propagation direction. The text should clarify: the comparison is between waves with different *propagation directions*, not different polarizations at the same propagation direction.

3. **§5 numbering gap.** Section 5 has a subsection "5.2 Geological and Material Controls" but no subsection 5.1. The first paragraph of §5 is unnumbered prose. It should be labeled §5.1 (e.g., "5.1 The Acoustoelastic Parameter and Its Detection") for consistency with §§3, 4, and 6 which all have numbered subsections.

4. **§8 numbering gap.** Section 8 has subsection 8.3 but no 8.1 or 8.2. The opening paragraphs on homogeneous validity and linear acoustoelasticity should be labeled §8.1 and §8.2.

5. **Eq. 9 notation.** The thermoelastic velocity change is written $\Delta v / v$ (capital Delta) rather than $\delta v / v$ (lowercase delta). For consistency with the notation convention established in §2.0, this should be $\delta v / v$ unless there is a deliberate distinction being made (e.g., $\Delta$ for finite change vs. $\delta$ for infinitesimal).

---

## Criterion 3: Reproducibility

**Score: 9/10 (unchanged) — Excellent**

The addition of `requirements.txt` addresses the previous concern. All six notebooks remain self-contained. The response to review correctly notes that the NB1 label issue and the missing capillary notebook are deferred.

**Minor:** The `requirements.txt` lists minimum versions but does not pin exact versions. For full reproducibility, consider adding a pinned `environment.yml` or specifying the Python version.

---

## Criterion 4: Evidence–Conclusion Alignment

**Score: 7/10 (was 6) — Improved**

**Improvements:**
- Conclusion 2 (bridge relation) is now directly supported by the derivation in §2.5.
- Conclusion 6 (anisotropy) is now supported by the expanded §6 with explicit splitting derivation and the tracelessness argument.
- Conclusion 7 (3-D imaging) is appropriately hedged with "has the potential to enable."
- Conclusion 9 (material controls) is now supported by the new §5.2.

**Remaining concerns:**

1. **No real-data comparison.** This was flagged as a must-fix in Round 1 and acknowledged as deferred. It remains the single largest gap between the framework's claims and its demonstrated capability. Reviewer 2 at a journal will almost certainly require at least one worked example. Even reproducing a single panel from Okubo et al. (2024, their Fig. 7) or Fokker et al. (2021, their Fig. 12) — overlaying the model prediction on the observed $\delta v/v$ — would close this gap without requiring new data processing.

2. **§4.4 capillary conclusions remain imported.** The three key claims (dynamic capillarity essential, hysteresis diagnostic, soil structure matters) are attributed to Shi et al. (2026) rather than derived or validated here. This is now explicitly framed as external evidence ("Shi et al. 2026 recently demonstrated"), which is acceptable for a review paper. But the reader may wonder why the companion notebooks don't include a capillary example. A one-paragraph note acknowledging this gap and stating it as planned future work would be transparent.

---

## Criterion 5: Presentation and Clarity

**Score: 8/10 (was 7) — Improved**

**Improvements:**
- Notation is consistent ($\delta v/v$ throughout).
- The notation table in §2.0 is clear and the three-level hierarchy is well-motivated.
- §3 is now balanced with §4 (three subsections each).
- §6 is now substantive with two subsections, explicit derivation, and the azimuthal-binning strategy.
- Bibliography is fully alphabetized.
- External equation references are disambiguated.

**Remaining issues:**

1. **Line 60 tautology** (see Criterion 2, item 1).

2. **§2.4 header says "General dv/v Model"** — should be "General $\delta v/v$ Model" for consistency. The bare text "dv/v" without dollar signs appears here.

3. **Figure captions.** The paper references 18 figures but includes no caption text. The reader (and reviewers) cannot evaluate whether the figures support the claims without captions. This should be addressed before submission — either inline or as a collected section at the end.

4. **The §2.6 label "Alternative and Complementary Mechanisms"** — this section was numbered §2.5 in the first revision's response document but is now §2.6 (because the bridge equation was inserted as §2.5). The numbering is correct in the manuscript; just note for consistency with the response document.

---

## Criterion 6: Literature Coverage

**Score: 9/10 (was 8) — Improved**

**Improvements:**
- 67 references, fully alphabetized.
- Birch (1961), Clarke et al. (2011), Rivet et al. (2011), Verdon et al. (2008) added.
- Snieder et al. (2017) now complete with volume and pages.
- Hughes & Kelly (1953) confirmed present.

**Minor remaining:**
- Clarke et al. (2011) is in the bibliography but not explicitly cited in the body text. Either add an in-text citation (e.g., in §2.0 where the MWCS method is implicitly referenced) or remove from the bibliography.
- Obermann et al. (2013) appears twice in the bibliography (line 439 as "Imaging preeruptive..." and indirectly through Obermann et al. 2014, which is a different paper — this is actually fine). However, the first Obermann 2013 entry is for the *scatterer relocation* paper, and the body text at line 26 cites "Obermann et al., 2013" for *depth sensitivity*, which is actually the 2014 paper. Check that each in-text Obermann citation matches the correct bibliography entry.
- Tromp et al. (2005) is cited in §8.3 for adjoint sensitivity kernels but is not in the bibliography.

---

## Criterion 7: Impact and Broader Significance

**Score: 8/10 (unchanged) — High potential**

The bridge equation (Eq. 7) and the expanded material-controls section (§5.2) make the paper more useful to practitioners: a researcher at a new site can estimate $\beta$ from a $V_S(z)$ profile via $\mu'(z)$, predict the expected $\delta v/v$ amplitude for known forcings, and assess whether their observations are consistent with the nonlinear-elastic framework. The azimuthal binning strategy (§6.2) gives experimentalists a concrete next step.

The paper would benefit from a short "Practical Workflow" box or subsection — perhaps in §9 — that summarizes the steps a researcher would take to apply this framework at a new site: (1) estimate $V_S(z)$ profile, (2) compute sensitivity kernels, (3) estimate $\mu'(z)$ from the profile, (4) forward model thermoelastic + hydrological $\delta v/v$, (5) subtract to isolate tectonic/volcanic residuals, (6) compare with geodetic data. This would significantly increase uptake.

---

## Criterion 8: Ethics and Compliance

**Score: 9/10 (unchanged) — Exemplary**

AI transparency documentation remains thorough. The response-to-review document is professional and tracks all changes clearly. The updated prompts log (4 sessions) accurately records the iterative process.

**Minor:** The Data Availability statement still reads "[repository URL]" — this placeholder must be replaced before submission.

---

## Summary: What Remains Before Submission

### Must-fix:
1. Fix the §2.0 tautology: "equivalently $\delta v/v$" should be "equivalently written $dv/v$"
2. Fix §2.4 header: "dv/v" → "$\delta v/v$"
3. Add figure captions (either inline or as appendix section)
4. Add Tromp et al. (2005) to bibliography (cited in §8.3)
5. Fill in "[repository URL]" in Data Availability
6. Verify Obermann (2013) vs. (2014) citation mapping

### Should-fix:
7. Note drained vs. undrained $\kappa$ in the bridge equation derivation (§2.5)
8. Clarify the §6.1 splitting derivation: "different propagation directions" not "SV vs. SH"
9. Number the subsections in §5 (add §5.1) and §8 (add §8.1, §8.2)
10. Fix Eq. 9 notation: $\Delta v/v$ → $\delta v/v$
11. Add in-text citation for Clarke et al. (2011)
12. Consider adding a "Practical Workflow" summary in §9
13. Add one real-data comparison figure (strongly recommended)

### Disposition relative to Round 1:

| Round 1 Must-Fix | Status |
|---|---|
| 1. Duplicate Eq. 6 | ✅ Resolved |
| 2. β↔μ' bridge | ✅ Resolved (new §2.5, Eq. 7) |
| 3. Cross-refs Eq. 3→4 | ✅ Resolved |
| 4. Notation dv/v→δv/v | ✅ Resolved (one residual at §2.4 header) |
| 5. Bibliography | ✅ Resolved (67 entries, alphabetized) |
| 6. Real-data comparison | ⚠️ Still missing (acknowledged in response) |
| 7. Conclusion 6 overclaim | ✅ Resolved ("has the potential to enable") |

**Overall: The paper has improved from "Major Revisions Required" to "Minor Revisions." The remaining items are formatting fixes, one missing bibliography entry, and the persistently deferred real-data comparison. The theoretical content is now solid and the claims are appropriately scoped.**
