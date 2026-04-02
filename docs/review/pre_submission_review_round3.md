# Pre-Submission Review — Round 3

**Manuscript:** *Seismic Velocity Changes as Stress and Strain Meters: A Unified Framework for Environmental, Tectonic, and Volcanic Monitoring*

**Authors:** Denolle, M. A. & Claude (Anthropic AI)

**Review date:** March 30, 2026

**Rubric:** Denolle group synthesis of peer review guidelines (AGU, GJI, Seismica, SSA, PNAS)

**Note:** This review considers both the paper (564 lines, 68 refs, 14 equations) and the companion Parkfield stress analysis (`docs/parkfield_stress_analysis.md`) that has been developed but not yet integrated into the manuscript.

---

## Overall Assessment

The manuscript has reached a polished state: notation is consistent, equations are sequentially numbered, the bibliography is complete and alphabetized, subsections are all numbered, figure captions are present, and the drained/undrained caveat on the bridge equation has been addressed. The theoretical framework is coherent and the presentation is clear. All must-fix and should-fix items from Rounds 1 and 2 are resolved.

The critical new development is the quantitative Parkfield stress analysis, which demonstrates the framework's predictive power using published numbers from Okubo et al. (2024) and the SAFOD velocity profiles. **This analysis, if integrated into the paper, transforms it from a review-framework paper into a research article with a concrete result.**

**Recommendation: The paper is acceptable for submission to Solid Earth or SRL as-is. To target JGR Solid Earth, the Parkfield analysis should be integrated as a new Section 10 ("Application: Stress at Depth from Parkfield $\delta v/v$"), which would be the decisive upgrade. See detailed recommendation below.**

---

## Criterion 1: Novelty and Significance

**Score: 8.5/10 (was 8)**

The paper's novelty rests on three pillars: (1) the bridge relation $\beta = -\mu'\kappa/(2\mu)$ with the drained/undrained caveat, (2) the expanded anisotropy treatment showing that isotropic acoustoelasticity fails at Parkfield while the deviatoric framework succeeds, and (3) the practical workflow for applying the framework at new sites. These are solid contributions.

The Parkfield analysis adds a fourth pillar that would significantly increase the score: **a quantitative prediction of stress at depth (~12 kPa/yr, ~0.24 MPa cumulative at 0.8 km) derived entirely from the framework's equations and published velocity profiles, cross-checked against GNSS strain with factor-of-1.4 consistency.** The inferred $\beta_{\text{axial}} \approx -240$ and $\mu' \approx 250$ for fractured Salinian granite, and the derived $l + 2m \approx -12{,}200$ GPa falling between intact granite and sandstone values, are testable predictions that no prior paper has made.

**If integrated, this would raise the novelty score to 9/10** — the paper would present a specific, quantitative, falsifiable result (stress at depth from ambient noise) rather than just a conceptual framework.

---

## Criterion 2: Methods and Technical Soundness

**Score: 8.5/10 (was 8) — No new issues found**

All prior technical issues are resolved. The equation numbering is clean (1–14 + one unnumbered), cross-references are correct, notation is uniform, and the drained/undrained caveat on Eq. 7 is physically correct and well-integrated.

**On the Parkfield analysis specifically:**

The calculation chain is sound. I verified the following:

- $z_{\text{peak}} = V_S/(3f) = 2.5/(3 \times 1.0) = 0.83$ km: **correct** for the SAFOD velocity profile at the sediment-granite transition, consistent with Okubo et al.'s statement.
- $\mu = \rho V_S^2 = 2500 \times 2500^2 = 15.6$ GPa: **correct** for $V_S = 2.5$ km/s.
- $\kappa = \rho(V_P^2 - 4V_S^2/3) = 2500(20.25 - 8.33) = 29.8$ GPa: **correct**.
- $\mu' = 2\mu|\beta|/\kappa = 2 \times 15.6 \times 240/29.8 = 251$: **correct** arithmetic.
- $\sigma_{\text{dev}} = 4\mu(\delta v/v)/\mu' = 4 \times 15.6 \times 10^9 \times 4.8 \times 10^{-5}/251 = 11.9$ kPa/yr: **correct**.

**One concern:** The cross-check estimate ($E\epsilon \approx 8.7$ kPa/yr) uses the full Young's modulus $E$ with the surface GNSS strain rate. But the GNSS strain is a surface measurement, and the stress at 0.8 km depends on how the strain transfers with depth — particularly given the velocity contrast at the sediment-granite interface. The factor-of-1.4 agreement may be partly fortuitous. The analysis should note this explicitly.

**A second concern:** The contractional strain rate of "~200 nanostrain/yr" is stated without a specific source. Okubo et al. (2024) show the *cumulative* contractional strain over 20 years in their azimuthal analysis, but the exact annual rate depends on which GNSS pairs and which azimuth window are used. The analysis should cite the specific figure/table from Okubo et al. or the strain rate model used.

---

## Criterion 3: Reproducibility

**Score: 9.5/10 (was 9) — Improved**

The Parkfield analysis is fully reproducible from published inputs: the $\delta v/v$ trend rate from Okubo et al. (2024, their Fig. 11b), the SAFOD velocity profile from Zhang et al. (2009), Jeppson & Tobin (2015), and Catchings et al. (2002), and the GNSS strain field from the same Okubo et al. paper. Every number in the calculation chain is traceable.

The six companion notebooks remain as before. The `requirements.txt` is present.

---

## Criterion 4: Evidence–Conclusion Alignment

**Score: 8/10 (was 7) — Improved by the analysis, even without integration**

The Parkfield analysis provides the evidence base that was previously missing. The key finding — that isotropic acoustoelasticity *predicts the wrong sign* for the Parkfield $\delta v/v$ trend (since dilatation is extensional), while the deviatoric/crack-closure framework gives the right sign, the right magnitude ($\beta \approx -240$), and the right azimuthal dependence — directly validates Conclusions 2, 6, and 9 of the paper.

The §9.5 limitations now honestly name four published validations and explicitly state which parts of the framework remain untested. The practical workflow (§9.4) is concrete and actionable.

**The remaining gap** is that the Parkfield analysis sits in a companion document rather than in the paper itself. This means the paper's conclusions are *supported by* the analysis but the reader doesn't see the support unless they find the companion doc. This is the difference between a strong review paper and a strong research paper.

---

## Criterion 5: Presentation and Clarity

**Score: 9/10 (was 8) — Improved**

The notation is uniform. Subsections are all numbered. Figure captions are present and informative. The practical workflow is a welcome addition. The expanded limitations section is honest and specific.

**One remaining cosmetic issue:** §4.4 ends with the sentence "The dv/v regime diagram..." — this bare "dv/v" should be "$\delta v/v$". (It's in the last line of the capillary discussion, line 194.)

---

## Criterion 6: Literature Coverage

**Score: 9/10 (unchanged) — Strong**

68 references, alphabetized, complete. The Parkfield analysis would add Zhang et al. (2009), Jeppson & Tobin (2015), Catchings et al. (2002), and Boness & Zoback (2004) — all key SAFOD papers that would strengthen the bibliography for a Parkfield-focused paper.

---

## Criterion 7: Impact and Broader Significance

**Score: 9/10 (was 8) — Improved by the Parkfield analysis**

The Parkfield analysis demonstrates that the framework can produce a number — **0.24 MPa of deviatoric stress at ~1 km depth over 20 years** — from ambient noise data alone, using only the framework's equations and published velocity profiles. This is the kind of concrete, quantifiable result that gets cited. The dual-population rheological model (elastic tectonic loading + slow-dynamics healing on different crack populations) is a novel physical interpretation.

The statement that individual Murnaghan constants cannot be resolved from one loading path but that tidal azimuthal analysis could close the gap gives experimentalists a clear next step.

---

## Criterion 8: Ethics and Compliance

**Score: 9/10 (unchanged)**

AI transparency remains exemplary. The Zenodo DOI placeholder is present.

---

## Strategic Recommendation: What to Do with the Parkfield Analysis

The Parkfield stress analysis is the single most valuable piece of content in the repository that is *not* in the paper. Here is my assessment of options:

### Option 1: Integrate into the paper as a new section

Add a **Section 10: Application to Parkfield** (before current §10 Conclusions, which becomes §11) containing:

- §10.1: The SAFOD velocity profile and sensitivity kernel at 0.9–1.2 Hz (one table, one figure)
- §10.2: The bridge relation applied — predicting $\beta \approx -240$ and $\mu' \approx 250$ from the velocity profile
- §10.3: Stress at depth — the 12 kPa/yr deviatoric stress rate with the GNSS cross-check
- §10.4: Azimuthal consistency with $S_{Hmax}$ from SAFOD wellbore breakouts
- §10.5: Rheological interpretation — the dual-population model
- §10.6: What TOE constants can and cannot be resolved

This adds ~1500 words, 1 table, and 1–2 figures. The paper grows from ~9,000 to ~10,500 words, well within JGR limits.

**Effect on journal targeting:** This transforms the paper from Solid Earth/SRL (review) → **JGR Solid Earth** (research article with data application). The "what is new" answer becomes: *we predict stress at depth from ambient noise at Parkfield, show that isotropic acoustoelasticity fails while the deviatoric framework succeeds, and constrain effective TOE parameters of the shallow fault zone.*

### Option 2: Keep as companion document, target Solid Earth

The paper stays as-is, targeting Solid Earth or SRL. The Parkfield analysis lives in the repository as a worked example. Lower impact but publishable immediately.

### Option 3: Split — Parkfield as a separate GRL letter

The Parkfield analysis becomes a standalone letter: "Stress at depth from ambient noise: the bridge between acoustoelastic and induced-stress frameworks at Parkfield." ~3,000 words, 3 figures. The current paper becomes its companion.

**My strong recommendation is Option 1.** The analysis requires no new data processing — it uses only published numbers. The integration effort is modest (one table, one figure of the SAFOD velocity profile with kernel overlay, ~1500 words). And it eliminates the only persistent weakness flagged across all three review rounds: the absence of a real-data validation.

---

## Summary: Remaining Items

### If targeting Solid Earth / SRL (submit as-is):

Only one cosmetic fix remains:
1. Line 194: bare "dv/v" → "$\delta v/v$"

**Verdict: Accept with minor corrections.**

### If targeting JGR Solid Earth (integrate Parkfield analysis):

Must-do:
1. Add §10 with the Parkfield application (~1500 words, 1 table, 1–2 figures)
2. Add SAFOD references (Zhang et al. 2009, Jeppson & Tobin 2015, Catchings et al. 2002, Boness & Zoback 2004)
3. Pin the contractional strain rate to a specific source/figure from Okubo et al.
4. Note the depth-transfer caveat on the cross-check estimate
5. Update abstract to mention the Parkfield result
6. Update conclusions to include the stress prediction and TOE constraint
7. Fix line 194 cosmetic

**Verdict: Major revision (scope expansion) required for JGR, but the content already exists — it is an integration task, not a research task.**

---

## Score Summary Across Three Rounds

| Criterion | Round 1 | Round 2 | Round 3 (as-is) | Round 3 (with Parkfield) |
|-----------|---------|---------|------------------|--------------------------|
| 1. Novelty | 7 | 8 | 8.5 | 9 |
| 2. Methods | 7 | 8 | 8.5 | 8.5 |
| 3. Reproducibility | 9 | 9 | 9.5 | 9.5 |
| 4. Evidence–Conclusion | 6 | 7 | 8 | 9 |
| 5. Presentation | 7 | 8 | 9 | 9 |
| 6. Literature | 8 | 9 | 9 | 9.5 |
| 7. Impact | 8 | 8 | 9 | 9.5 |
| 8. Ethics | 9 | 9 | 9 | 9 |
| **Average** | **7.6** | **8.3** | **8.8** | **9.1** |
| **Verdict** | Major revisions | Minor revisions | Accept (Solid Earth) | Accept (JGR, after integration) |
