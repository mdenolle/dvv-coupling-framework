DENOLLE GROUP PRE-SUBMISSION REVIEW
=====================================
Manuscript: *Seismic Velocity Changes as Stress and Strain Meters: A Unified Framework for Environmental, Tectonic, and Volcanic Monitoring*
Target: JGR: Solid Earth — research article
Date: 2026-06-29
Reviewer: Pre-Submission Orchestrator (9 subagents → 8-criterion synthesis)
Note: **Advisory.** All findings require human judgment before submission.
Profile: default
Provenance: Skill v2.3 | Model claude-opus-4-8[1m] | Iteration 1 | Manuscript hash 0f7208382759
Mode: Full first review

SUMMARY
-------
A theoretically strong, carefully bounded synthesis paper that unifies thermoelastic,
hydrological/poroelastic, nonlinear-elastic, and induced-stress treatments of δv/v
through nonlinear elasticity, with a genuinely novel cross-disciplinary join
(multiphase-flow thermodynamics × third-order elasticity). The core equations are
sound and independently re-derived; the three-site application is internally
consistent (16/16 numbers verified) and unusually well-hedged; the reproducible
substrate (pixi.lock, 53 tests, [P]/[D] provenance ledger) is above the genre norm.
The work is **not yet ready to submit** — but the blockers are finishing items, not
science. The main gaps are: an over-length abstract with no Key Points, a pending
software/data DOI (AGU-mandatory), two theory-consistency loose ends, and figure
numbering/citation order. No fatal soundness issue.

SUBMISSION READINESS
--------------------
[ ] Ready — minor issues only
[x] Revise before submission — issues an external reviewer will flag
[ ] Major revision required
[ ] Not ready — fatal issue(s) first

FATAL: (none)

MAJOR:
  M1 [C5 | S-AB.1, S-AB.11] Abstract is ~378 words (JGR cap ~250) AND the mandatory
     JGR **Key Points** (3 bullets, ≤140 char) are absent. → issue #12
  M2 [C3/C8 | S-RP.4] Software/data **Zenodo DOI is pending**; AGU mandates a
     resolvable DOI at submission ("upon request" = non-compliant). → issue #4
  M3 [C2 | S-ME.4] §10.1 claims the "same material parameters (β, μ′, ∂(ρv²)/∂σ_c)"
     explain all forcings, but ∂(ρv²)/∂σ_c (thermoelastic) is never related to μ′/β —
     the thermoelastic limb is not actually bridged. Reconcile or soften. → issue #13
  M4 [C2 | S-ME.7] §9.3.4 assigns an elastic acoustoelastic β≈150 to a process the
     text calls explicitly *inelastic* — self-contradictory; relabel as apparent
     compliance or drop the number. → issue #13
  M5 [C5 | S-FD.3] Figures are not in numerical citation order (main Fig 2 first cited
     in §7.3 after Figs 3–6; supporting S12 before S7–S11). → issue #14
  M6 [C4 | S-CO.7] Conclusion 7 states the three-site numbers without the §10.5 hedges
     (Cascadia = borehole-calibration consistency check, not validation; directional
     β/μ′ = order-of-magnitude). → issue #15

MINOR:
  m1  Sharpen and front-load the one-sentence novelty in abstract + §1.4 (S-AB.6, S-IN.4).
  m2  Add an explicit stakes sentence in §1.2 (why unifying interpretation matters) (S-IN.5).
  m3  Fix §7.4/§10.4 "step 5" cross-ref: Eq. 5 is a surface-wave endmember, not the
      general hydrological loading coefficient — point to Eq. 4 (S-ME.5).
  m4  Number the starred equation `(*)` (§6.1) for consistency with Eqs 1–18 (S-FD.9).
  m5  Trim interpretive clauses from captions Fig 2c, 4b, 5e; reconcile in-figure titles
      with MD captions (Figs 4, 7) (S-FD.4).
  m6  De-duplicate the Hotovec-Ellis et al. (2022) reference (listed twice) (S-CD.9). → issue #5
  m7  Cascadia digit collision: the §9.2.3 stress equation substitutes 3.8×10⁻⁴ (the
      δv/v rate) in the same subsection that uses c = 3.8×10⁻⁴ m²/s — label it (S-RE.2).
  m8  Standardize Kīlauea β as "β_radial≈300 (range 250–330)" everywhere (S-RE.3).
  m9  Add a Move-1 findings summary (or pointer to Table 2) opening §10 (S-DI.1).
  m10 Surface ≥1 genuine contrasting/competitor result in §10; weigh model-inadequacy
      as an alternative to the factor-1.4/factor-2 "agreements" (S-DI.5, S-DI.6). → issue #15
  m11 Soften §10.3 "can be resolved rather than assumed" to in-principle (no worked
      example) (S-DI.10).
  m12 Reproducibility housekeeping: seed `analysis/jgr_main_figures.py`; reconcile the
      documented seed (docs say 42, code uses 20260401); unify version strings
      (pixi 0.1.0 / pyproject 0.2.0 / CITATION 1.0.0); state in Data Availability that
      figures derive from deterministic synthetic generators (S-RP.10, fixes 2–5).

STRENGTHS
---------
1. Theory correct and unusually well-bounded — Eq. 7 bridge and Eq. (*) directional
   splitting independently re-derived; §8 gives concrete validity limits (strain <10⁻⁵,
   2:1 contrast, Pe-gated drained/undrained); 16/16 §9 numbers consistent (S-ME, S-RE).
2. Honest, complete limitations (§10.5) and consistent hedging — Cascadia
   "consistency check, not validation" stated 3×; bridge tagged order-of-magnitude
   throughout (S-DI.7, S-RE.7, S-CO.9).
3. Reproducible substrate above genre norm — pixi.lock, 53 tests, deterministic
   synthetic generators, [P]/[D] provenance ledger; reconstructable given the code
   (S-RP verdict).
4. High reference-combination novelty (poroelastic thermodynamics × third-order
   elasticity) with healthy 7.5% self-citation and 1937–2026 temporal spread (S-CD).
5. Clean three-move Introduction with an explicit 7-item gap list mapping to the
   contribution (S-IN).

SECTION-BY-SECTION
------------------
[S-AB] ~378 words / ~250 target (OVER); structure present; all numbers trace; missing
       Key Points; novelty diffuse. Fixes: cut to ≤250, add Key Points, lead with the
       joint stress+strain-meter claim.
[S-IN] Moves M1/M2/M3 all PASS; citations resolve; self-citation modest. Fixes: add a
       stakes sentence (§1.2); sharpen the single objective sentence (§1.4).
[S-ME] Six-question coverage complete; Eq. 7 and Eq. (*) re-derived sound; 2μ/4μ
       inversion factors correct. Two conceptual gaps: ∂(ρv²)/∂σ_c not unified with μ′/β
       (S-ME.4); inelastic-β at Kīlauea (S-ME.7). Eq. 5 now matches Fokker (prior
       caveat resolved).
[S-RE] Results-before-interpretation FAIL by strict rubric / ACCEPTABLE for a
       theory+application genre (§9.x.1 observations vs §9.x.3 prediction already split);
       hedging strong; one digit-collision readability trap. Fix: make the
       observations/prediction split explicit at the head of §9.
[S-DI] Interpretation marked, no new results, limitations excellent; comparison is
       multi-community but competitor-light and confirmation-weighted. Fixes: surface a
       contrasting result; weigh model inadequacy on the factor-N agreements.
[S-CO] 12 conclusions, all trace to body; Pols ~6/7 (context/relevance reminder thin).
       C7 under-hedged; C12 partly redundant. Fixes: add §10.5 hedges to C7; trim C12.
[S-FD] 7 main figs (inline) + 12 SI figs + 2 tables + 18 eqs; figures-cited-in-order
       FAIL; 4 interpretive captions; color audit PASS; starred eq unnumbered; Zenodo
       DOI pending. Fixes: renumber to citation order; trim captions; number Eq. (*).
[S-RP] Env reproducibility STRONG; 53 tests; seeds in scripted path; REPRODUCTION
       VERDICT = reconstructable given released code, 0 in-text stops; the one blocker is
       administrative — software DOI pending. Fixes: mint DOI; seed the figure driver;
       reconcile seed docs + version strings.
[S-CD] 80 unique refs; self-citation 7.5% (healthy); temporal 1937–2026; venues
       discipline-appropriate; reference-combination novelty HIGH (protect under C1).
       Fixes: de-duplicate Hotovec-Ellis 2022; note references.bib is a partial seed.

DIVERSITY SIGNALS (surfaced, not scored)
----------------------------------------
Self-citation 7.5% (6/80). Temporal 1937–2026, well balanced. 49 venues, top-4 ≈ 53%
(field-appropriate), with generalist + physics + hydrology breadth. Author-team
geography skews US/W-Europe/Japan; non-Western study *sites* appear, mostly via
Western-led teams (informational, human-verify). Identity axes not inferred (profile
off). Cross-disciplinary recombination is the paper's deliberate novelty — a strength,
not a focus deficiency (C1 guardrail).

DETAILED FINDINGS BY CRITERION
------------------------------
C1 — Scientific Question & Novelty ........ GOOD. Real unified-framework contribution,
   grounded and demonstrated (forward conversions). Lead sentence buries the one-line
   novelty (S-AB.6, S-IN.4). Cross-disciplinary join is a protected strength (S-CD).
C2 — Methods & Soundness .................. GOOD (two must-fix). No fatal error; Eqs
   verified. M3 (∂(ρv²)/∂σ_c not unified with μ′/β; soften §10.1) and M4 (inelastic β at
   Kīlauea) must be resolved. Directional-bridge order-of-magnitude is well disclosed.
C3 — Reproducibility & Open Science ....... GOOD → flips to Excellent on minting the
   software DOI (M2/S-RP.4). Everything else at/above Excellent.
C4 — Evidence–Conclusion Alignment ........ GOOD. Abstract numbers all trace; under-
   hedged Conclusion 7 (M6); favored-interpretation on factor-N agreements (m10).
C5 — Presentation & Communication ......... FAIR. Abstract over length + missing Key
   Points (M1); figure numbering/citation order (M5); interpretive captions (m5).
C6 — Literature Integration ............... GOOD. Diverse and fair; duplicate reference
   (m6); thin on contrasting results (m10).
C7 — Impact & Broader Significance ........ GOOD. Significance stated and hedged; minor
   §10.3 overgeneralization (m11).
C8 — Ethics & Compliance .................. GOOD. AI use disclosed (sole author, AGU-
   compliant); CC BY 4.0; funding acknowledged (Packard, Murdock); sole-author CRediT
   trivial. Only gap = the pending data/software DOI (shared with C3/M2).

JOURNAL-SPECIFIC NOTES (JGR: Solid Earth)
-----------------------------------------
- Abstract ≤250 words and 3 Key Points (≤140 char) are required — currently 378 words,
  no Key Points (M1).
- Data & software DOI mandatory at submission (M2).
- Merged Results/Discussion is acceptable for a theory+application article; making the
  observations-vs-prediction split explicit pre-empts a reviewer objection.

ITEMS REQUIRING HUMAN VERIFICATION
----------------------------------
- All DOIs/URLs resolve — especially the 2026 in-press DOIs (Kidiwela sciadv.aea3684,
  Shi science.aec0970) and the GitHub URL (agent cannot resolve links).
- Once minted, that the Zenodo deposit actually contains pixi.lock, notebooks 01–06,
  jgr_main_figures.py, presets/, figures/main.
- That `pixi install && pixi run python analysis/jgr_main_figures.py` reproduces
  figures/main/fig01–fig07 (agent cannot run code).
- Geographic/author-team inferences in the diversity block.

AI-REVIEW DISCLOSURE STAMP (for the manuscript's AI-use statement)
------------------------------------------------------------------
"This manuscript was checked prior to submission with an advisory, AI-assisted
pre-submission review tool (Denolle-group pre-submission-reviewer, skill v2.3; model
claude-opus-4-8[1m]; iteration 1). The tool flags candidate issues against an
8-criterion rubric; it does not assess or assert the correctness, soundness, or
acceptability of the work. All findings were reviewed by the author before submission."
(Process disclosure only — not an endorsement of validity. Governance rule 6.)

LEDGER FOR NEXT ITERATION
-------------------------
See `docs/review/dvv_unified_framework.review.json` (Issue Ledger + provenance). On the
next draft, supply a before/after of `paper_dvv_unified_framework.md`; the review will
reconcile each ID (RESOLVED / PARTIAL / NOT / REGRESSED) and raise new issues only on
changed text.
