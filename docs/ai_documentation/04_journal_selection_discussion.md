# Journal Selection Discussion: Navigating Scope, Novelty, and Desk-Rejection Risk

**Context:** This document captures a structured dialogue between a geophysicist (M.A. Denolle) and an AI assistant (Claude, Anthropic) about where to submit a manuscript. It is included as part of the AI documentation for transparency, and as a template that may be useful to other researchers facing similar decisions.

**Manuscript under discussion:** *Seismic Velocity Changes as Stress and Strain Meters: A Unified Framework for Environmental, Tectonic, and Volcanic Monitoring* — a synthesis paper with 14 equations, 18 figures, 6 companion Jupyter notebooks, 68 references, and no new observational data.

**Date:** March 29, 2026

---

## The Problem: High Desk-Rejection Rates

Major geoscience journals reject approximately 50% of submissions before peer review, often because the manuscript does not match the journal's scope, novelty expectations, or format requirements. These desk rejections waste weeks to months of author time and delay the dissemination of science. The mismatch is frequently not about quality — it is about *fit*: a strong methods paper sent to an observations journal, a review-length manuscript sent to a letters journal, or a synthesis lacking the "single new result" that a research journal expects.

The discussion below demonstrates how a systematic assessment of a manuscript against specific journal criteria can identify the best target — or reveal that the manuscript needs restructuring before submission.

---

## The Question

> **Scientist:** Would this paper fit in novelty and scope in GRL or GJI? Do I need to add data?

## The Assessment

### Candidate 1: Geophysical Research Letters (GRL)

**Format constraints:** ~3,500 words, ≤4 display items (figures + tables), broad and immediate implications.

**Assessment:** The manuscript is 9,000 words with 18 figures — roughly 2.5× the word limit and 4.5× the figure limit. Even with aggressive cutting, the paper's structure (10 sections, 36 subsections) is fundamentally a long-form treatment, not a letter. More importantly, GRL's editorial criteria emphasize a *specific, new result* with broad implications — not a synthesis of existing frameworks.

**Could a GRL letter be extracted?** Yes. The bridge equation $\beta = -\mu'\kappa/(2\mu)$ (Eq. 7) connecting laboratory acoustoelastic measurements to seismological shear-modulus derivatives is a compact, testable result. A focused letter would: (1) derive Eq. 7 in one paragraph, (2) validate it against published $\mu'(z)$ profiles (e.g., Fokker et al., 2021, Groningen) by predicting $\beta$ and comparing to reported $\delta v/v$ amplitudes, and (3) state the implication — that the same material parameter governs the response to all forcing types, with the isotropic/deviatoric divergence as a diagnostic. This would be ~2,500 words, 3 figures, and a clear "new result."

**Verdict:** The current manuscript does not fit GRL. A derivative letter could.

### Candidate 2: Geophysical Journal International (GJI)

**Format constraints:** No length limit. Publishes theory, methods, and observational papers. Strong history in CWI methodology (Tromp & Trampert, 2018; Obermann et al., 2013, 2014; Clarke et al., 2011; Yuan et al., 2021).

**Assessment:** The scope matches — GJI routinely publishes theoretical frameworks in seismology. The length is not an issue. However, GJI reviewers will ask: *what is new beyond collecting existing results?* The manuscript's contributions are:

1. The bridge equation (Eq. 7) — one line of algebra connecting $\beta$ and $\mu'$
2. The notation clarification ($\delta v/v$ vs. $\delta V_S/V_S$ vs. $\delta c/c$) — a useful service but not a research result
3. The capillary discussion (§4.4) — imported from Shi et al. (2026), not independently modeled
4. The sensitivity notebooks — pedagogical, not novel
5. The 3-D inversion proposal (§7.3–7.4) — aspirational, not demonstrated
6. The alternative hypotheses survey (§2.6) — literature review

A GJI reviewer familiar with Richter et al. (2014), Fokker et al. (2021), and Clements & Denolle (2023) could argue that each individual component already exists and the paper's value is in assembly, not discovery. This is the desk-rejection risk: "this reads as a review, not a research article."

**Could it be restructured for GJI?** Yes, in two ways:
- As a **review article** (GJI publishes these, though they are typically invited). The framing would shift from "we develop a new framework" to "we review and connect existing frameworks, identify gaps, and propose future directions."
- As a **methods paper with validation** — adding a real-data application that demonstrates the framework produces something not achievable with the individual components alone (e.g., multi-frequency depth decomposition at Parkfield, or bridge-equation validation at Groningen).

**Verdict:** Borderline. The paper could survive GJI review if positioned carefully as a methods/tutorial contribution, but risks a "reads as a review" desk rejection if submitted as a standard research article.

### Candidate 3: Solid Earth (SE)

**Format constraints:** OA, no strict length limit, Copernicus interactive review. Published Ermert et al. (2023).

**Assessment:** Solid Earth explicitly welcomes "original research articles, review articles, and short communications" covering "the composition, structure, and dynamics of the Earth." The journal has published synthesis papers with modeling frameworks before (Ermert et al., 2023 is a close precedent — physics-based modeling of $\delta v/v$ at the basin scale). The interactive open review process is well-suited to a paper with companion code.

**Verdict:** Strong fit as-is. Low desk-rejection risk. The review-and-framework nature of the paper aligns with SE's scope.

### Candidate 4: Seismological Research Letters (SRL) / The Seismic Record (TSR)

**Format constraints:** SRL publishes research articles, reviews, and the "Electronic Seismologist" column for computational tools and methods. TSR (newer SSA journal) publishes shorter research articles.

**Assessment:** The companion notebooks would be a strong asset for SRL's Electronic Seismologist column. SRL values community resources and pedagogical contributions. The paper would need to be reframed to emphasize the computational tools and practical guidance rather than the theoretical synthesis.

**Verdict:** Good fit, especially for the Electronic Seismologist format. Lower impact factor than GJI or JGR but higher visibility for the computational component.

### Candidate 5: JGR Solid Earth

**Format constraints:** No strict length limit. Publishes original research. The home of Okubo et al. (2024) and Clements & Denolle (2023).

**Assessment:** JGR Solid Earth requires original research results. The manuscript in its current form — without data application — is unlikely to survive the "what is new?" test. However, JGR is the *ideal* target if the paper is augmented with a data application at a well-characterized site (Parkfield, Groningen, California network, or the Shi et al. agricultural site). The theory sections become the methods backbone; the data application provides the results.

**Verdict:** Not appropriate without data. The top choice *with* data.

---

## Decision Matrix

| Journal | Format fit | Novelty fit | Data required? | Desk-reject risk | Impact |
|---------|-----------|-------------|----------------|-------------------|--------|
| GRL | ✗ (too long) | ✗ (no single result) | Yes (validation) | High | High |
| GJI | ✓ | Borderline | Helps greatly | Medium | High |
| Solid Earth | ✓ | ✓ (review/framework) | No | Low | Medium |
| SRL/TSR | ✓ | ✓ (methods/tools) | No | Low | Medium |
| JGR Solid Earth | ✓ | ✗ without data | Yes (essential) | High without data | High |

---

## Three Publication Strategies

### Option A: Submit as-is to Solid Earth or SRL

**Effort:** Minimal (fix remaining minor issues, mint Zenodo DOI).
**Timeline:** Submit within 1–2 weeks.
**Pros:** Publishable now; the notebooks and framework have pedagogical value; OA and community-visible.
**Cons:** Lower impact; may be perceived as a tutorial rather than a research contribution.
**Recommended framing:** "Review and Framework" paper. Retitle to: *"Interpreting Seismic Velocity Changes: A Review and Unified Computational Framework for Environmental, Tectonic, and Volcanic Monitoring."*

### Option B: Add data, submit to JGR Solid Earth

**Effort:** Moderate (1–3 months). Requires processing $\delta v/v$ at one site, computing sensitivity kernels, applying the forward model chain, comparing with observations.
**Timeline:** Submit in 2–4 months.
**What to add:** Take Parkfield (HRSN data, already processed by Okubo et al., 2024) and:
1. Compute $\mu'(z)$ from the published velocity profile → predict $\beta(z)$ via Eq. 7
2. Forward model thermoelastic + hydrological $\delta v/v(f,t)$ at multiple frequencies with proper sensitivity kernels using actual temperature and precipitation records
3. Show multi-frequency residuals — does the tectonic trend's frequency dependence constrain the depth of strain accumulation?
4. Compare predicted amplitudes with observed — does Eq. 7 give the right $\delta v/v$ magnitude?

**Pros:** High impact; the Parkfield application would be definitive; natural home alongside Okubo et al. (2024).
**Cons:** Requires data access and processing; the scope may expand significantly.
**The key "new result"** would be: *the bridge equation correctly predicts the $\delta v/v$ sensitivity from the independently measured velocity profile, and multi-frequency analysis reveals that the tectonic signal is depth-localized.*

### Option C: Split into two papers

**Paper 1 (GRL letter):** "Connecting acoustoelastic and induced-stress formulations for seismic velocity monitoring: the bridge relation $\beta = -\mu'\kappa/(2\mu)$." Derive Eq. 7, validate at one site, discuss implications. ~3,000 words, 3 figures.

**Paper 2 (Solid Earth or GJI tutorial):** The full framework paper with notebooks, positioned as a review and computational companion to Paper 1. Reference Paper 1 for the theoretical core.

**Effort:** Moderate (Paper 1 needs data validation; Paper 2 is essentially ready).
**Pros:** Maximizes impact of the bridge equation (GRL visibility) while preserving the pedagogical value (Solid Earth reach). Two publications from one body of work.
**Cons:** Coordination overhead; risk of Paper 2 being perceived as derivative if Paper 1 is published first.

---

## The Scientist's Decision

The choice depends on priorities:

- **If the priority is speed and community service** → Option A (Solid Earth). The paper and notebooks serve the field even without data validation.
- **If the priority is impact and rigor** → Option B (JGR). The data application transforms the paper from synthesis to research.
- **If the priority is maximizing output** → Option C (GRL + Solid Earth). Two papers, two audiences.

In all cases, the bridge equation (Eq. 7) and the practical workflow (§9.4) are the most valuable contributions and should be prominent.

---

## Lessons for Journal Selection

This discussion illustrates several general principles:

1. **Match the result type to the journal type.** Letters journals want one specific result with broad implications. Research journals want original findings. Review journals want comprehensive synthesis. A paper that tries to be all three fits none well.

2. **The "what is new?" test is the primary desk-rejection filter.** Before submitting, articulate in one sentence what a reader learns from your paper that they cannot learn from any combination of the cited papers. If the answer is "the equations are assembled in one place," that is a review, not a research article.

3. **Data transforms scope.** A theoretical framework paper without data is a methods/review contribution. The same framework applied to data becomes a research article targeting higher-impact venues. The amount of data needed can be small — even one site, one time series, one comparison — if it validates a specific prediction.

4. **Notebooks and code are assets, but not results.** Companion computational tools increase reproducibility and uptake, and some journals (SRL, JOSS) specifically value them. But in traditional research journals, the code supports the science — it is not the science itself.

5. **Consider the reviewers.** GJI sends CWI papers to CWI experts (Sens-Schönfelder, Obermann, Campillo, Larose). These reviewers know whether a synthesis adds value beyond the individual papers. JGR sends Parkfield papers to Parkfield experts (the Okubo, Brenguier, Ben-Zion groups). Choose the venue where your contribution is clearest relative to the reviewer pool's expectations.

6. **Splitting is underused.** A natural splitting point often exists between the theoretical contribution and its application. Two focused papers frequently receive better reviews than one sprawling paper, because each can be evaluated against a clear standard.
