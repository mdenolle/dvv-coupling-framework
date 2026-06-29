# Continuation Handoff — State of the Paper & Path to Pre-Submission

**Date:** 2026-06-25  **Author:** M. A. Denolle (sole)  **Last commit:** `3014189` on `main`
**Purpose:** Everything needed to pick this back up and drive the framework paper to a
pre-submission review for *JGR: Solid Earth*. Read this first; it points to the
single-source-of-truth files for everything else.

---

## 0. TL;DR — resume in 5 lines

1. The framework paper is internally consistent, grounded, and builds to PDF.
2. Two deliberate holds: the **data application (§9) is a placeholder** in the submission build (full analysis exists, moved to SI), and **real-data validation is deferred** to future work.
3. Verify anytime: `pixi run test` (expect **53 passed**) and `pixi run paper-pdf` (main + SI PDFs).
4. Single source of truth for all site numbers: `docs/site_analyses/provenance_tables.md`.
5. To start the pre-submission review, see **§5** below.

---

## 1. What this paper is (and is not)

- **Thesis:** δv/v as a unified stress *and* strain meter, reconciled through nonlinear
  elasticity; the bridge relation β = −μ′κ/(2μ); and the isotropic-vs-deviatoric
  diagnostic that predicts *when* scalar δv/v = βε_kk works.
- **Two novelty claims:**
  1. **Stress↔strain reconciliation (bridge).** Now *implemented and enforced* in code
     (`SiteConfig` validator) and grounded site-by-site. Status: **solid.**
  2. **Coupling mechanisms** (thermo-poro-elastic; damage–permeability; saturation–
     nonlinearity). Status: **framed honestly as proposed constitutive structure** with
     one *emergent* demonstration (β_eff(ω)); the rest are labeled illustrative /
     estimator-validation, not discoveries.
- **NOT in this paper:** a turnkey Bayesian UQ of δv/v processing choices (→ standalone
  companion paper, `docs/theory/companion_paper_bayesian_dvv_uq.md`); end-to-end real-data
  reprocessing (author TODO); the full `codameter` package (separate repo, see §7).

---

## 2. Locked decisions (do NOT relitigate without cause)

| Decision | Rationale | Pointer |
|---|---|---|
| **Sole author** = M. A. Denolle; AI = directed tool, not co-author | AGU policy: AI ineligible for authorship | paper "Statement of AI Use"; README; CITATION.cff |
| **Drained/undrained regime is data-driven** via Pe = ωL²/c | Not assumed; Cascadia Pe≈2.5 justifies κ_u | paper §2.5; provenance_tables.md |
| **Cascadia β = −3160 is PUBLISHED** (Kidiwela 2026) → bridge is a *consistency check* | Borehole-calibrated, not a prediction | §9.2; provenance_tables.md |
| **Cascadia μ′=618, 0.58 kPa/yr** (NOT 1290 / 1.24) | Old site-doc used wrong velocity layer | cascadia_stress_analysis.md (reconciled) |
| **Bayesian window UQ → standalone companion paper** | Distinct thesis + own validation burden | companion_paper_bayesian_dvv_uq.md |
| **§9 placeholder in submission build; full §9 → SI** | Real-data application deferred | build_jgr_pdf.py |
| **Figs 1–6 main; Fig 7 + S1–S12 → SI** | Fig 7 is the data-application synthesis | build_jgr_pdf.py |
| Illustrative presets (Nepal, Agricultural) labeled as such | Not in the 3-site application | analysis/config.py |

---

## 3. Single sources of truth (numbers, history)

- **All site inputs (published [P] vs derived [D]) + Pe regimes:** `docs/site_analyses/provenance_tables.md`
- **Per-site detail:** `docs/site_analyses/{parkfield,cascadia,kilauea}_stress_analysis.md`
- **Equation verification:** `docs/theory/equation_verification_log.md`
- **Full audit + remediation log:** `docs/ai_documentation/08_full_research_audit_2026-06-25.md` (§9 = what was fixed)
- **What changed (machine-ish):** `CHANGELOG.md` [0.3.0]
- **Window-selection theory + the rejected naive Bayesian scheme + correct hierarchical method:** `docs/theory/coda_window_selection_metrics.md`

Grounded headline numbers (memorize these; everything must agree):
- Parkfield: μ=15.6 GPa, κ_u=29.8 GPa, β_axial≈240 (derived), μ′≈251, ~12 kPa/yr (deviatoric). Regime drained→transitional.
- Cascadia (N): μ=0.475 GPa, κ_u=4.86 GPa, β=−3160 (published), μ′≈618, 0.58 kPa/yr. Regime transitional→undrained (Pe≈2.5).
- Kīlauea: μ=3 GPa, κ=5 GPa, β_radial≈300 (derived), μ′≈360, ~167 kPa/collapse. Directional bridge = order-of-magnitude.

---

## 4. Current build & verification

```bash
pixi run test        # -> 53 passed (bridge consistency, nu_u>=nu_d, golden site values, YAML<->Python)
pixi run paper-pdf   # -> paper/build/paper_dvv_jgr_submission.pdf (main, 51 pp, Figs 1-6, §9 placeholder)
                     #    paper/build/paper_dvv_jgr_supplement.pdf  (SI, 27 pp, §9 + Fig 7 + S1-S12)
                     #    paper/build/paper_dvv_agutex_jgr_solid_earth.tex (Overleaf AGUTeX source)
```
- Canonical manuscript: `paper/paper_dvv_unified_framework.md` (still contains the FULL §9; the
  placeholder split happens only in the build script — important for the reviewer to know).
- Build logic (placeholder + main/SI split + figure routing): `paper/build_jgr_pdf.py`.

---

## 5. How to resume: running the pre-submission review

The project has a pre-submission review history (`docs/review/pre_submission_review*.md`,
rounds 1–5, converged "Accept 9.3" but **self-generated** — treat as internal) and a
later, more skeptical `docs/review/research_review_2026-06-19.md`. A new pre-submission
pass should be run against the **current** state.

**To launch the pre-submission agent, give it:**
1. **Target:** `paper/paper_dvv_unified_framework.md` (the canonical MD), reviewed for
   *JGR: Solid Earth*. Tell it §9 will be a placeholder in the submitted version (full
   analysis is in the SI) and that real-data reprocessing is explicitly deferred — so it
   should NOT flag "no real data" as a fatal blocker, but may note it as a limitation.
2. **Context files:** this handoff, `provenance_tables.md`, the audit (`08_*`), and the
   equation verification log. These pre-empt re-discovery of already-fixed issues.
3. **Rubric (8-criterion, from prior rounds):** novelty/significance; theoretical
   soundness; internal consistency (numbers must match provenance_tables.md);
   reproducibility; clarity/structure; figure quality & sufficiency; references/attribution;
   limitations honesty. Score each, list must-fix vs should-fix.
4. **Known focus areas to verify (don't re-derive from scratch):**
   - Bridge self-consistency at all sites (now enforced in code — spot-check the prose).
   - Directional-bridge caveat is stated wherever β_axial/β_radial appear (order-of-magnitude).
   - Cascadia framed as consistency check, not independent validation (§9.2, §10.5).
   - Pe-regime statement present (§2.5) and Table 1 has the Pe row.
   - μ′ (=dμ/dP) vs S_σ (=∂(ρv²)/∂σ_c) not conflated in prose.
   - Illustrative/synthetic figures labeled (captions header; §10.5).
   - AI-use statement present and AGU-policy compliant.

**Suggested invocation pattern:** dispatch an Agent (subagent) as a JGR:SE reviewer with
the above; or, if a `pre-submission-reviewer` skill/command exists in the environment, use
it with `paper/paper_dvv_unified_framework.md` as the target. There is also
`.github/agents/research-code-reviewer.agent.md` and `.agent/code-reviewer.md` for code.

---

## 6. Open items before submission (prioritized)

**P0 — content/consistency (do before review or have the reviewer confirm):**
- [ ] Confirm every number in §9 prose matches `provenance_tables.md` (the canonical MD still
      has the original §9; verify it carries the reconciled Cascadia 618 / 0.58, not 1290 / 1.24).
      *(The site doc and code are reconciled; double-check the paper body itself.)*
- [ ] Decide final §9 treatment for submission: keep placeholder (current build) vs include the
      preliminary application in-text with strong caveats. (Current default: placeholder + SI.)

**P1 — external readiness:**
- [ ] Real-data example (the persistent reviewer ask) — author TODO: find ~3 public-data stations
      independent of the 3 cited studies; this is the companion-paper validation too.
- [ ] Mint the Zenodo archive DOI (currently "pending" in Data Availability).
- [ ] Cross-check references.bib vs the manuscript reference list (two workflows; known drift risk).

**P2 — polish:**
- [ ] Overfull \hbox warnings in the build (cosmetic; long URLs/headings).
- [ ] Confirm AGUTeX (`paper_dvv_agutex_jgr_solid_earth.tex`) compiles on Overleaf with the
      official `agujournal2019.cls` (not vendored here).

**Out of scope here (separate track):**
- Companion Bayesian-UQ paper + `codameter` package (see companion_paper prospectus; `../codameter` repo).

---

## 7. File map (the few that matter)

```
paper/paper_dvv_unified_framework.md     # canonical manuscript (full §9 inside)
paper/build_jgr_pdf.py                    # MD->tex->PDF; placeholder + main/SI split
paper/supporting_information.md           # S-figure captions (drives SI build)
paper/build/*.pdf                          # built main + SI PDFs (committed)
analysis/config.py                         # SiteConfig (Vp, kappa_u/d, bridge validator, presets)
analysis/poroelastic_framework.py          # bridge_beta, drained_bulk_modulus, mu_prime_from_bridge
analysis/coupling_tier_tests.py            # emergent beta_eff(omega) Tier-1 demo
docs/site_analyses/provenance_tables.md    # *** single source of truth for numbers ***
docs/site_analyses/{parkfield,cascadia,kilauea}_stress_analysis.md
docs/theory/coda_window_selection_metrics.md      # window UQ theory + critique
docs/theory/companion_paper_bayesian_dvv_uq.md    # standalone-paper prospectus
docs/ai_documentation/08_full_research_audit_2026-06-25.md  # audit + remediation log
docs/ai_documentation/09_continuation_handoff_2026-06-25.md # THIS FILE
```

`codameter/` here is a *prototype* (window-selection). The real package is the separate repo
at `../codameter` (`/Users/marinedenolle/GitHub/codameter`) — **do not modify without
explicit instruction** (a prior blind copy was reverted; its `window_selection.py` was untracked).

---

## 8. Gotchas for the next session

- The placeholder/SI split is **build-only**; never gut §9 in the canonical MD.
- `μ′` means dμ/dP (O(1–10)) here; `S_σ` means ∂(ρv²)/∂σ_c (O(50–1000)). Keep distinct.
- `SiteConfig` will *raise* if a `beta_source="bridge"` preset's β violates the bridge — that's intended.
- Memory files (project context) live in `~/.claude/.../memory/`, outside the repo.
- Prior "Accept 9.3" review is self-generated; weight the June research review and this audit higher.
