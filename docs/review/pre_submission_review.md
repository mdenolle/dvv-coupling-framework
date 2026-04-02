# Pre-Submission Peer Review

**Manuscript:** *Seismic Velocity Changes as Stress and Strain Meters: A Unified Framework for Environmental, Tectonic, and Volcanic Monitoring*

**Authors:** Denolle, M. A. & Claude (Anthropic AI)

**Target journals:** JGR Solid Earth, Reviews of Geophysics, or Solid Earth (review/framework paper)

**Review date:** March 29, 2026

**Rubric:** Denolle group synthesis of peer review guidelines (AGU, GJI, Seismica, SSA, PNAS)

---

## Overall Assessment

This is an ambitious synthesis paper that connects disparate theoretical frameworks — Murnaghan third-order elasticity, Berger thermoelastic stress, Roeloffs poroelastic diffusion, Tromp & Trampert induced stress, Hertz-Mindlin contact mechanics, and Hassanizadeh dynamic capillarity — into a unified interpretation framework for ambient-noise $\delta v/v$. The scope is appropriate for a review-framework hybrid targeting a broad geophysics audience. The companion notebooks and open repository are strong assets. However, several issues need attention before submission.

**Recommendation: Major revisions required.**

---

## Criterion 1: Novelty and Significance

**Score: 7/10 — Good, with caveats**

**Strengths:**
- The unification of the stress-meter (Tromp & Trampert) and strain-meter (Murnaghan/acoustoelastic) formulations through a common nonlinear-elastic thread is a genuine conceptual contribution.
- The explicit three-level notation ($\delta v/v$, $\delta V_S/V_S$, $\delta c/c$) with the Snieder (2002) S-wave dominance argument is a service to the community — this distinction is often blurred in the literature.
- Integration of the Shi et al. (2026) dynamic capillary effects into the $\delta v/v$ framework is novel; no prior work has connected Hassanizadeh-Gray theory to ambient noise monitoring.
- The proposed 3-D joint inversion framework (§7.3–7.4) articulating how multi-frequency $\delta v/v$ + geodetic data yields depth-resolved stress is forward-looking.

**Weaknesses:**
- The paper does not contain new observational results or a worked inversion example. The novelty is in synthesis and framing, which is legitimate for a review but must be positioned explicitly.
- The claim of "unified framework" may be overstated since the paper does not formally prove equivalence between the Murnaghan and Tromp-Trampert formulations — it argues they address the same physics from different starting points, but the mathematical bridge is only sketched (§2.1 vs §2.2). The connection between the acoustoelastic $\beta$ (Eq. 3) and the $\mu'$-based formulation (Eq. 4) should be made explicit: what is $\beta$ in terms of $\mu'$? Under what conditions do they predict the same $\delta V_S/V_S$?
- Several of the "gaps" claimed (§1.3) have been partially addressed by recent work not cited — e.g., Illien et al. (2022) jointly model damage and hydrology, and Ermert et al. (2023) already use station-specific kernels for basin heterogeneity.

**Recommendation:** Add a derivation or table showing the explicit mapping between $\beta$ and $\mu'$ for the isotropic case. Soften the novelty claims where recent literature has addressed specific gaps. Consider positioning as a "review and framework" paper rather than purely a "new framework" paper.

---

## Criterion 2: Methods and Technical Soundness

**Score: 7/10 — Mostly sound, some issues**

**Strengths:**
- The derivation verification documented in `revision_notes.md` is thorough, including dimensional checks and approximation validity assessment.
- The chain from Berger → Richter → Ermert for thermoelastic modeling is correctly reproduced.
- The Fokker poroelastic decomposition from Tromp & Trampert is correctly derived (verified in revision notes).
- Parameter ranges are drawn from specific published values with citations.

**Weaknesses:**

1. **Equation numbering conflict.** Equations 6 appears twice — once as the base dv/v model (line 110) and once as the temperature diffusion (line 124). This is a significant formatting error that will confuse readers.

2. **Notation inconsistency persists.** The abstract and §1 still use `$dv/v$` (lowercase italic) while §2+ use `$\delta v/v$`. The paper should use $\delta v/v$ throughout, or clearly state the equivalence once and use one form consistently.

3. **Missing formal connection between §2.1 and §2.2.** Equation 3 ($\delta v/v = \beta \epsilon_{kk}$) operates on *strain*, while Equation 4 (Tromp & Trampert) operates on *stress* ($p^0$, $\tau^0$). The paper claims these are "complementary" but does not show the bridge: for a linear elastic medium, $p^0 = -\kappa \epsilon_{kk}$, so Eq. 3 becomes $\delta v/v = -\beta p^0/\kappa$, while Eq. 4 gives $\delta V_S/V_S = \mu' p^0/(2\mu)$ for the isotropic part. Equating these yields $\beta = -\mu' \kappa/(2\mu)$. This relation should be stated and discussed — it connects the "materials science" parameter ($\beta$) to the "seismological" parameter ($\mu'$).

4. **The 1-D models are never integrated with the sensitivity kernels.** The thermoelastic, hydrological, and capillary models all produce $\delta V_S/V_S(z,t)$, but the paper never shows Eq. 1 applied to produce the predicted $\delta v/v(f,t)$ that would actually be compared to observations. This is the core forward modeling step that reviewers from Ermert-type or Fokker-type work will expect. Even a schematic figure showing $\delta V_S/V_S(z)$ → kernel → $\delta c/c(f)$ would help.

5. **Capillary model not in notebooks.** §4.4 discusses the Shi et al. (2026) dynamic capillary framework, but none of the six notebooks implement it. This creates a disconnect between the text and the companion material.

6. **Section 6 is underdeveloped.** The anisotropy section (§6) is only one paragraph for what the paper claims is a key contribution. It should include: the explicit expression for SV-SH splitting from Eq. 4 under uniaxial stress; a discussion of how azimuthal binning of $\delta v/v$ could be used to constrain deviatoric stress (as suggested by Okubo et al., 2024); and the connection to the Verdon (2008) stress-geomechanics paper in the project knowledge base.

7. **Section 7.4 lacks mathematical specificity.** The 3-D inversion framework lists five constraints but does not write down the cost function, regularization, or how the under-determined parts of the problem would be handled. The listing is closer to a research agenda than a method.

**Recommendations:**
- Fix duplicate Eq. 6.
- Add the $\beta$-to-$\mu'$ bridge equation with discussion.
- Add one figure showing the forward modeling chain: $\delta V_S/V_S(z) \to K(z,f) \to \delta c/c(f) \to \delta v/v$.
- Add a notebook implementing the Shi et al. capillary model, or remove the claim that "six companion notebooks" cover all the topics.
- Expand §6 to match the claimed novelty.
- In §7.4, either sketch the cost function or reframe as "future work."

---

## Criterion 3: Reproducibility

**Score: 9/10 — Excellent**

**Strengths:**
- Six Jupyter notebooks with 18 figures, using only NumPy/SciPy/Matplotlib — no proprietary code or data.
- Repository structure with README, LICENSE (CC BY 4.0), and clear directory organization.
- Parameter values are cited with specific literature sources.
- The notebooks are self-contained and generate all figures from scratch.

**Weaknesses:**
- Notebook 1 has a minor execution error (label parsing issue) that would cause the figure not to regenerate exactly as shown. The standalone fix script works, but the notebook itself should be corrected.
- No `requirements.txt` or `environment.yml` is provided — adding one (even a minimal one) would improve reproducibility.
- The notebooks do not embed the sensitivity-kernel integration (Eq. 1), which is the key step that connects the depth-dependent models to observable $\delta v/v(f)$.

**Recommendations:** Fix NB1 label issue, add `requirements.txt`, consider adding a seventh notebook implementing the forward model chain (Eq. 1).

---

## Criterion 4: Evidence–Conclusion Alignment

**Score: 6/10 — Needs work**

**Strengths:**
- The parameter sensitivity analyses (Figs. 3, 5, 7) directly support the stated conclusions about which parameters matter most.
- The regime diagram (Fig. 18) concisely communicates which process dominates in which setting.
- The Parkfield case study from Okubo et al. (2024) anchors the anisotropy and rheology discussions.

**Weaknesses:**

1. **No comparison to real data.** The paper's models are entirely synthetic. Not a single $\delta v/v$ time series from an actual station is shown and compared to the models. For a framework paper, at least one worked example — e.g., the Parkfield environmental decomposition (Okubo et al., 2024, Fig. 7) or the Fokker et al. (2021) Groningen validation (their Fig. 12) — should be reproduced to demonstrate that the framework actually explains observations.

2. **Capillary conclusions are imported, not derived.** The conclusions in §4.4 ("dynamic capillarity is essential," "hysteresis is diagnostic," "soil structure matters") are stated as results of Shi et al. (2026), not as results of this paper. Since the current paper doesn't model capillary effects in its notebooks, these are claims supported by external evidence rather than internal analysis.

3. **The 3-D inversion "framework" has no validation.** §7.3–7.4 proposes a joint inversion but provides no synthetic test, no resolution analysis, and no discussion of ill-conditioning. The conclusion "multi-frequency $\delta v/v$ + GNSS/InSAR enables depth-resolved 3-D stress/strain imaging" (Conclusion 6) is aspirational rather than demonstrated.

4. **Fig. 18 regime boundaries are not quantitatively justified.** The regime diagram assigns frequency and depth ranges to each process, but these boundaries appear subjective. How were they determined? They should be derived from the sensitivity analyses in the notebooks.

**Recommendations:**
- Add at least one real-data comparison figure (even a schematic overlay).
- Either implement capillary modeling or reframe §4.4 conclusions as imported from Shi et al.
- Tone down Conclusion 6 from "enables" to "has the potential to enable" or demonstrate with a synthetic test.
- Justify Fig. 18 boundaries quantitatively, or label them as approximate.

---

## Criterion 5: Presentation and Clarity

**Score: 7/10 — Good overall, structural issues**

**Strengths:**
- The notation table (§2.0) is clear and helpful.
- The progression from theory (§2) through specific effects (§3–6) to inversion (§7) to validity (§8) is logical.
- The writing is generally clear and accessible.
- The alternative-hypotheses section (§2.5) is well-organized.

**Weaknesses:**

1. **The abstract uses both $dv/v$ and does not mention the notation convention.** It should use $\delta v/v$ or at least be internally consistent.

2. **§3 (Thermoelastic) is underdeveloped relative to §4.** The thermoelastic section is about 15 lines while the hydrological section is 60+. Given that thermoelastic effects are comparably important, §3 deserves expansion — particularly the Berger two-term solution (shallow vs. deep), which is one of the key physical insights.

3. **Some figure references appear incorrect.** §6 references "Eq. 3" for the Tromp & Trampert equation, but Eq. 3 is now the acoustoelastic relation ($\beta \epsilon_{kk}$). The Tromp equation is Eq. 4. Similarly, §2.3 says "combined Equation 3 with poroelastic theory" when it should say Equation 4.

4. **The bibliography is not alphabetized.** References from the original list (Berger through Zhang) are roughly alphabetical, but the added references (Zhan, Zhu, D'Auria, Gassenmeier, ...) are appended at the end. This will be caught by any journal.

5. **Some notation slips remain.** Line 200: "Eq. 3" should be "Eq. 4". Line 222: `$\frac{dv}{v}$` should be `$\frac{\delta v}{v}$`. Line 230: `$\delta v_s / v_s$` should be `$\delta V_S / V_S$` (capital V for consistency).

6. **Missing figure captions in the manuscript.** The previous version had a full figure captions section; this version references figures but the captions are not included. They should be restored.

**Recommendations:**
- Alphabetize the full bibliography.
- Fix cross-reference errors (Eq. 3→4 in §2.3 and §6).
- Standardize notation slips.
- Restore figure captions section.
- Expand §3 to match the depth of §4.

---

## Criterion 6: Literature Coverage

**Score: 8/10 — Strong**

**Strengths:**
- 64 references spanning 1937–2026, covering the core theoretical and observational papers.
- Includes all the major recent OA monitoring papers (Okubo 2024, Clements & Denolle 2023, Ermert 2023, Fokker 2021, Zhang 2023, Delouche 2023).
- Cites foundational work (Murnaghan 1937, Berger 1975, Roeloffs 1988, Snieder 2002).
- Includes the new Shi et al. (2026) *Science* paper.

**Weaknesses:**

1. **Missing key CWI methodology papers.** Yuan et al. (2021) is cited but the stretching technique original (Sens-Schönfelder & Wegler, 2006) and the MWCS method (Clarke et al., 2011; Poupinet et al., 1984) deserve mention in §2.0 where the measurement is defined.

2. **Missing Tsai (2011) derivation details.** Tsai (2011) jointly modeled thermoelastic and hydrological GPS and seismic velocity changes — this is one of the foundational papers for the thermoelastic model and should be more prominent in §3.

3. **No Birch (1961) or Hughes & Kelly (1953) in bibliography.** These are foundational for third-order elastic constants and are cited in the text (via Richter et al.) but not in the reference list. Hughes & Kelly is cited in §2.1 but not listed.

4. **Sens-Schönfelder & Eulenfeld (2019) is PRL, not OA.** Several claimed "OA" papers may actually be behind paywalls. The paper should be accurate about which are truly open access.

5. **Missing: Rivet et al. (2011)** on slow-slip detection with $\delta v/v$ in Mexico — this is a key tectonic application that supports the framework.

6. **Snieder et al. (2017) reference is incomplete** — missing volume, pages, and DOI.

**Recommendations:**
- Add Birch (1961), Hughes & Kelly (1953), Clarke et al. (2011), Rivet et al. (2011).
- Complete the Snieder et al. (2017) reference.
- Don't claim OA status unless verified.

---

## Criterion 7: Impact and Broader Significance

**Score: 8/10 — High potential**

**Strengths:**
- The framework has genuine cross-disciplinary reach: seismology, hydrology, volcanology, geodesy, geotechnical engineering, and agriculture (via Shi et al.).
- The open-source notebooks lower the barrier to entry for researchers wanting to model $\delta v/v$ at new sites.
- The proposed 3-D inversion concept, if implemented, would be transformative.
- The regime diagram (Fig. 18) is the kind of synthesis figure that becomes widely cited.

**Weaknesses:**
- Without a real-data demonstration, the impact remains potential rather than demonstrated.
- The paper may fall between two stools: too theoretical for observational journals, too qualitative for theoretical journals. The target venue should be chosen carefully — Reviews of Geophysics may be the best fit given the synthesis scope.

**Recommendations:** Consider targeting Reviews of Geophysics or a Solid Earth review article. Adding one real-data example would dramatically increase impact.

---

## Criterion 8: Ethics and Compliance

**Score: 9/10 — Exemplary AI transparency, minor issues**

**Strengths:**
- The AI co-authorship is transparently declared with a footnote and a dedicated Statement of AI Use.
- Full prompt logs, chain-of-thought, and model card are provided.
- CC BY 4.0 licensing is appropriate and explicitly stated.
- The AI documentation distinguishes human vs. AI contributions clearly.

**Weaknesses:**
- Some journals (e.g., *Science*, *Nature*) do not accept AI co-authors. The author list should be adapted to the target journal's policy. For AGU journals, the current approach (listing AI as co-author with full transparency) should be checked against the latest AGU AI policy.
- Data availability statement says "available at [repository URL]" — this placeholder needs to be filled before submission, or a DOI should be minted (e.g., via Zenodo).
- The Shi et al. (2026) *Science* paper lists Denolle as corresponding author, creating a potential self-citation concern that should be disclosed (though self-citation is appropriate here given the direct relevance).

**Recommendations:**
- Check target journal's AI authorship policy.
- Mint a DOI for the repository via Zenodo before submission.
- Disclose the self-citation of Shi et al. (2026) in the cover letter.

---

## Summary of Required Revisions

### Must-fix before submission (Major):
1. Fix duplicate Eq. 6 (temperature diffusion and base model have same tag)
2. Add the $\beta \leftrightarrow \mu'$ bridge equation connecting §2.1 and §2.2
3. Fix cross-references: §2.3 and §6 cite "Eq. 3" when they mean "Eq. 4"
4. Standardize notation: $dv/v$ → $\delta v/v$ throughout (abstract, §1, several locations in §6–8)
5. Alphabetize the full bibliography; complete incomplete references (Snieder et al. 2017)
6. Add at least one real-data or quasi-real comparison figure
7. Tone down Conclusion 6 from "enables" to "has the potential to enable"

### Should-fix (Moderate):
8. Expand §3 (Thermoelastic) to match depth of §4
9. Expand §6 (Anisotropy) with explicit SV-SH splitting formula and azimuthal binning discussion
10. Add forward-modeling figure: $\delta V_S/V_S(z) \to K(z,f) \to \delta c/c(f)$
11. Add `requirements.txt` to repo
12. Fix NB1 label execution error
13. Restore figure captions section
14. Justify Fig. 18 regime boundaries quantitatively
15. Add missing references (Birch, Hughes & Kelly, Clarke et al., Rivet et al.)

### Nice-to-have (Minor):
16. Add a 7th notebook for the capillary model (or reframe §4.4 as external evidence)
17. Write the 3-D inversion cost function explicitly, or reframe §7.4 as future work
18. Mint a Zenodo DOI for the repository
19. Check target journal AI policy for author listing
