# Full Research Audit — State of Knowledge

**Project:** Seismic Velocity Changes as Stress and Strain Meters — A Unified Framework
**Audit date:** 2026-06-25
**Auditor:** Claude Opus 4.8 (1M), acting as reviewer in ambient-noise seismology, wavefield scattering, and rock physics, directed by M. A. Denolle
**Scope:** Theory ↔ implementation ↔ results ↔ scientific contribution, across the full repository (paper, notebooks, analysis scripts, `codameter` prototype, docs, tests).

> Purpose of this document: mark the current state of knowledge for the research spine. This repository is the **research/validation substrate**; `codameter` (a separate repository) will be the production package. The audit therefore judges the paper as a theory+synthesis contribution with *synthetic* validation, and judges the code by whether it faithfully supports the paper's two novelty claims:
> 1. **dv/v reconciled as both a stress meter and a strain meter** via the bridge relation β = −μ′κ/(2μ).
> 2. **Identification of coupling mechanisms** between effects (thermo–poro–elastic; damage–permeability; saturation–nonlinearity).

---

## 1. Executive summary

The manuscript is a genuinely useful **synthesis with a clean central idea**. The strongest, most defensible scientific contribution is *not* the bridge relation itself but the **isotropic-vs-deviatoric diagnostic**: the prediction of *when* the scalar relation δv/v = βε_kk works (volumetric loading → Cascadia) versus when it must fail (deviatoric loading with oriented fracture fabric → Parkfield, Kīlauea). That diagnostic is well-grounded in Tromp & Trampert (2018) and is supported by three independent published observations. It is the part of the paper most likely to survive peer review intact.

The two headline novelty claims are in different states of health:

- **Claim 1 (stress↔strain reconciliation).** The bridge relation β = −μ′κ/(2μ) is correctly *derived* (EQ-C2 verified). But it is **not self-consistently applied or implemented**. At every application site the κ that enters the bridge is the wrong κ (seismic/undrained, not the drained κ the derivation requires), and no code path actually computes a bridge-consistent β — all β values are hardcoded and several violate the relation they are meant to demonstrate. This is the single most important issue to fix because it sits on the load-bearing claim.

- **Claim 2 (coupling mechanisms).** This is currently **asserted, not demonstrated**. The "tier 1/2/3" coupling scripts and the three diagnostic cases either (a) cancel algebraically, (b) recover hand-injected synthetic parameters, (c) rely on invented constitutive curves, or (d) use circular diagnostics that assume their conclusion. As of today there is no figure in which a coupling effect *emerges* from coupled physics rather than being inserted by hand.

Supporting facts: the equation-verification log is honest and mostly correct (8/10 clean); the test suite passes (42/42) but covers only plumbing; and the prior review chain's "Accept, 9.3/10" verdict is partly self-generated and predates the more skeptical June research review. The most material *external* risks remain (i) no real-data example, (ii) AI co-authorship policy, and (iii) internal numerical inconsistencies between the Cascadia site document and every review document.

**Overall maturity:** Theory ~B+ (sound, one load-bearing inconsistency). Paper-as-synthesis ~B+ (publishable as a perspective/methods paper after the κ fix and honest reframing of coupling as proposed). Implementation supporting the novelty ~C (plumbing solid; the novelty-bearing code does not yet demonstrate the novelty).

---

## 2. Theory audit

### 2.1 What is correct and well-founded

- **Notation discipline (§2.0).** The three-level distinction δv/v (observable) ≈ δV_S/V_S (local, via Snieder 2002 equipartition / Singh 2019 weighting) and δc/c (phase velocity, via Fokker kernel Eq. 1) is correct and is a real pedagogical contribution. Grounding δv/v ≈ δV_S/V_S in S-wave dominance of the equipartitioned coda is the right move.
- **Tromp & Trampert (2018) form (Eq. 4, EQ-C4).** Verified against Fokker et al. (2021) Eq. 4. Correct.
- **Acoustoelastic β (Eq. 3, EQ-C5).** β = 3/2 + (l+2m)/(λ+2μ) is the standard hydrostatic-pressure S-wave result; verified.
- **Murnaghan EOS (EQ-C3).** Exact match to Murnaghan (1937) p. 252, including the b = 5a one-parameter identity.
- **Snieder healing integral (Eq. 12, EQ-C8).** Correct unnormalized template, consistent with Okubo et al. (2024).
- **Bridge derivation (Eq. 7, EQ-C2).** The *derivation* p⁰ = −κε_kk → β = −μ′κ/(2μ) is algebraically and dimensionally correct. The drained/undrained caveat in §2.5 is correctly stated in prose.

### 2.2 Load-bearing problem: the bridge relation is not self-consistently applied

The derivation of Eq. 7 explicitly uses the **drained** bulk modulus κ (p⁰ = −κε_kk under slow, drained loading). But the κ used at the application sites is the **undrained/seismic** modulus K = ρ(V_P² − 4/3 V_S²), which is the high-frequency saturated modulus — the opposite limit.

Verified numerically:

| Site | μ (GPa) | κ used in paper | κ_drained from (μ, ν=0.25) | β from paper κ | β from drained κ |
|---|---|---|---|---|---|
| Parkfield | 15.6 | 29.8 GPa (⇒ implies ν≈0.28) | 26.0 GPa | −240 (stored) | −209 |
| Cascadia | 0.475 | 4.86 GPa (seismic, undrained) | 0.79 GPa | −3160 (stored) | **−515** |

Consequences:
- **Parkfield** has a milder version of the problem: κ = 29.8 GPa is internally consistent only with ν ≈ 0.28, while `config.py` stores ν = 0.25 (which gives κ = 26 GPa and β = −209, not −240). A ~15% inconsistency, plus an undocumented ν drift.
- **Cascadia is the serious case.** κ = 4.86 GPa is the seismic (undrained) modulus. The drained κ from the same μ and a plausible ν is ~0.79 GPa, which would give β ≈ −515 — a factor of ~6 different from the reported β = −3160. Because the entire Cascadia stress estimate flows through this β (and β is *itself calibrated* from the borehole strain), the number is internally circular **and** uses the wrong modulus for the bridge. The "physically plausible μ′ ≈ 618" conclusion inherits this.

**Recommendation:** Decide explicitly which modulus the bridge uses at each site and at which forcing timescale (the paper's own §2.5 says the undrained limit gives a *larger* |β| via κ_u = κ/(1−α_B B) — so if Cascadia is genuinely undrained at the seasonal-to-secular timescale of the trend, *say so and use κ_u derived from the drained κ*, not the raw seismic K). Either way, the κ entering the bridge must be derived consistently from (μ, ν) and the stated drainage state, not silently substituted with the seismic K. Then re-derive μ′ at all three sites and reconcile against the site docs.

### 2.3 Other theory caveats (already partly flagged, kept on the record)

- **Eq. 5 coefficient (EQ-C1, ⚠️).** The compact `(μ′∓1)/4μ` form does not match the geometry-specific Fokker coefficients (SV: (μ′+1)/12μ; SH: 0). The verification log correctly catches this and the code (NB2) uses the correct (μ′+1)/12μ. Keep the manuscript's Eq. 5 explicitly labeled as the *general directional form*, with the surface-wave endmembers stated separately.
- **Directional use of Eq. 7 at Parkfield/Kīlauea.** Eq. 7 was derived for isotropic loading; applying it to β_axial / β_radial is order-of-magnitude only. This is acknowledged, which is good — but it means the μ′ values at the two deviatoric sites (251, 360) are not quantitatively meaningful, only indicative. Keep that framing prominent.
- **Zimmerman coupling parameter (EQ-C7).** K vs K² typo; corrected in the log to ζ = Kα_T²T₀/(ρC_p) ~ 10⁻³. The conclusion (one-directional coupling) stands. Ensure the manuscript/coupling text uses the corrected K¹ form.

### 2.4 The "μ′" symbol is overloaded — a pervasive hazard

Across the notebooks and the parameter table, the single symbol μ′ is used for **two physically distinct quantities**:
- μ′ = dμ/dP (the Tromp/Fokker shear-modulus pressure derivative, dimensionless, **O(1–10)**; the bridge relation requires this), and
- ∂(ρV²)/∂σ_c (the Richter/Ermert thermoelastic stress-sensitivity, dimensionless, **O(50–1000)**).

NB2/NB4 use μ′ = 80–100 in Fokker/Tromp formulas where the bridge requires μ′ ~ O(1–10); NB6's parameter table prints the symbol μ′ against the range "5–1000." `config.py` and the quickstart correctly treat μ′ as O(10). This conflation inflates notebook dv/v amplitudes by 1–2 orders of magnitude and is the most pervasive physics error in the synthetic suite. **Recommendation:** rename one of them (e.g., keep μ′ = dμ/dP; use S_σ ≡ ∂(ρV²)/∂σ_c for the thermoelastic sensitivity) and propagate consistently through notebooks, the parameter table, and the paper.

---

## 3. Implementation audit

### 3.1 `codameter/window_selection.py` — the production-target prototype

This is the cleanest, best-engineered module in the repository and is appropriate as the first `codameter` target. Strengths: frozen dataclasses with validation, NaN-aware renormalizing objective, sensible log-normal scoring for wave-type and depth proxies, `np.trapezoid` kernel overlap, rolling-window generator. Caveats:

- **The Bayesian window average is correctly *labeled* by the author's own theory doc as not a defensible uncertainty.** The softmax(λ·J) weights are heuristic, not model evidence, and the between-window variance term double-counts because overlapping lapse windows share coda samples and (by Eq. 15) measure physically different depth-weighted averages. The manuscript §7.4 already says this. **Keep it a window-sensitivity diagnostic; do not present the epistemic σ as a publishable error bar.** Consider renaming `BayesianWindowAverage` → `WindowSensitivityDiagnostic` to prevent misuse downstream.
- `np.trapezoid` requires NumPy ≥ 2.0 (the env uses NumPy 2.4, so fine here, but pin it in `codameter`).
- Minor: `score_window` computes `substack_resolution` but `DEFAULT_WEIGHTS` has no entry for it, so it never contributes to the objective unless a custom weight dict includes it. Either add a default weight or document that it is opt-in.

### 3.2 `analysis/poroelastic_framework.py` — physics core (imported widely)

Mostly sound; two real bugs and one definitional hazard:

- **MODERATE bug — `skempton_B_from_velocities` uses the wrong Biot coefficient.** `alpha_B = 1 - K_dry/K_sat` (line ~180), but the Biot coefficient is α_B = 1 − K_dry/K_**grain** (mineral modulus). The docstring even states the correct form, then the code substitutes K_sat. Result is not the Biot coefficient. Used only in the from-velocities path; replace with K_grain (mineral modulus input) or remove.
- **Definitional hazard — `bulk_modulus` returns the seismic (undrained/total) K** but is consumed as κ in bridge contexts that assume drained κ (see §2.2). Add an explicit `drained=True/False` flag or two named functions (`bulk_modulus_undrained_from_velocities` vs `bulk_modulus_drained_from_moduli`).
- `beta_drained` returns the **stress-domain** −μ′/(2μ) [1/Pa]; there is **no function for the strain-domain bridge β = −μ′κ/(2μ)** that the paper's claim 1 rests on. Add it; have the presets compute β from it rather than hardcoding.
- Earlier audit-fixed items confirmed in code: `beta_eff` now uses 1/(1−α_B·B) (correct), `thermoelastic_sensitivity_s_T` treats ∂(ρV²)/∂σ_c as dimensionless (correct).

### 3.3 `analysis/config.py` — schema and presets

- **CRITICAL for claim 1 — presets hardcode β values that violate the bridge.** Parkfield β = −240 vs bridge (−209 from stored ν), Cascadia β = −3160 vs bridge (~−515 from drained κ). The presets should *derive* β from (μ′, κ, μ) via a single helper so the paper's central equation is enforced, not contradicted, by the reference configurations.
- **MODERATE — Nepal/Agricultural β expressions are obfuscated and self-canceling** (`-150.0 * (2μ(1+ν)/(3(1-2ν)))/(2μ)` reduces to −150·(1+ν)/(3(1−2ν)); the μ cancel), and the inline comment's stated value disagrees with the code by ~1.5×. Replace with a documented call.
- Solid otherwise: good pydantic validation, literature-sourced presets, clean YAML loader. 42 tests pass against it.

### 3.4 Coupling scripts — `coupling_tier_tests.py`, `coupling_diagnostic_cases.py`, `interpret_fitted_params.py`, `07_tier1_california_test.py`

These carry novelty claim 2 and are the weakest part of the repository:

- **CRITICAL — `coupling_tier_tests.py` undrained Poisson formula is wrong and non-physical.** Inline ν_u gives 0.151 for ν_d = 0.25 (verified; correct value 0.311). ν_u < ν_d is thermodynamically impossible. `undrained_poisson()` already exists and should be called.
- **CRITICAL — Tier-1 amplification cancels algebraically.** `dvv_undrained = β_u·(−ΔP/κ_u)` with β_u = −μ′κ_u/(2μ): the κ_u cancels, so undrained ≡ drained (both 8.03×10⁻⁶). The plotted contrast comes only from the *buggy* pore-pressure term, i.e., the Tier-1 "coupling effect" in the figure is an artifact of the ν_u bug, not physics.
- **Tier 2 / Tier 3 are hand-inserted, not emergent.** The damage–permeability figure's signal is a manually imposed −0.5% coseismic step + analytic healing; the permeability evolution `exp(D·exp(−t/τ))` is not the documented k(t) = k₀·exp[D − ∫H dt] form. Tier 3 β(S_w) is an invented curve with magic coefficients and a hidden sign flip removed by `np.abs`.
- **Diagnostic cases recover their own inputs.** `generate_california_synthetic` injects a₂_post = −0.0028 vs a₂_pre = −0.0015; `case1` "discovers" exactly that. `generate_parkfield_synthetic` steps tidal β 240→180 and `case3` recovers it. These validate the *estimator*, not any coupling physics — and the printouts are framed as findings. The tidal case is additionally **aliased**: M2 (0.5175 d) is injected below the Nyquist of daily-sampled synthetics; the docstring even warns sub-daily resolution is needed.
- **The California "coupling mismatch" diagnostic is circular.** `coupling_mismatch_score` = (1−R²_best) × Gaussian-in-log-Pe peaked at Pe = 1. It will light up at Pe ≈ 1 for *any* low-R² site regardless of cause, and `plot_tier1.py` overlays the *same* R²(Pe) curve used to construct the score as "Theory." Agreement is guaranteed by construction.
- **Unit confusion** in `interpret_fitted_params.py` day↔second conversions (lines ~421/423/430: one multiplies, one divides by 86400 for the same nominal unit).
- **Reproducibility:** `np.random` used without seeds in the coupling scripts; `warnings.filterwarnings('ignore')` hides the very aliasing/rank-deficiency warnings that would expose the above.
- **`fetch_geospatial.py`:** the USGS ASCE7-22 design-maps endpoint and the NWIS query are both likely non-functional against the real APIs and fail silently to defaults — so any "enriched" pipeline quietly degrades to placeholder values.

### 3.5 Notebooks (synthetic validation suite)

Correctly implemented: acoustoelastic β and Murnaghan EOS (NB3), the Tromp–Trampert deviatoric construction (NB4, modulo μ′), the Fokker SV/SH structure (NB2, modulo μ′), the Snieder healing integral (NB5), the disba kernels and λ/3 rule (NB6 a/b), the linearity-breakdown panel (NB6). Problems:

- **NB1 `berger_stress` component equations are ad-hoc/invented** (one term marked `# approximate`, another hardcoded to 0) and mislabeled as Richter (2014); only the scalar invariant (which is what gets plotted) is correct.
- **Fabricated quantitative figures:** NB6 panel (c) "error from homogeneous assumption" = (VC−1)·LF·50 (pure invention with a magic ×50, presented as a % error contour map); NB3 panel (a) extrapolates the linear acoustoelastic law to −10% dv/v at 10 μstrain and labels it a literature value.
- **Non-demonstrating "nonlinearity" demos:** NB3 cell 5 and NB5 panel (d) use β_quadratic = 1e5, which at the relevant strains is 10³–10⁵× below the linear term — the panels claim to show curvature/tidal nonlinearity but show a straight line.
- **Heuristics dressed as cited theory:** NB4 `crack_velocity` "Hudson (1981)" with a magic 8/3 and an inert aspect-ratio term.
- **Prose magic numbers off:** NB1 skin depths (1.9 m stated vs 2.46 m actual) and b-factors (the headline "1.5" while figures use ν = 0.25 → 1.667).

None of these break the *figures actually used in the paper's main set* catastrophically (the worst offenders are in supporting notebook panels), but several captions imply quantitative agreement with published figures that the code does not deliver.

---

## 4. Results / site applications

| Site | State | What is solid | What is soft/speculative |
|---|---|---|---|
| **Parkfield** | Most developed | The qualitative diagnostic (isotropic fails: dilatation extensional while dv/v rises ⇒ deviatoric/crack-closure required) is the paper's cleanest novel result. Arithmetic self-consistent (240, ~12 kPa/yr). | β_axial via Eq. 7 is order-of-magnitude; κ implies ν≈0.28 ≠ stored 0.25; 200 nstrain/yr is approximate; factor-1.4 GNSS cross-check self-described as crude. |
| **Cascadia** | Numbers internally circular | Isotropic framework *works* (compressive), good foil to Parkfield. | "Borehole match" is a β-calibration consistency check, **not** independent validation. β uses undrained seismic κ in a drained-κ relation (§2.2). Site doc and all review docs **disagree by ~2×** on μ′ (1290 vs 618) and stress rate (1.24 vs 0.58 kPa/yr). Locking-ratio result conditional on comparable kernels. |
| **Kīlauea** | Weakest leg | β_radial ≈ 250–330 clusters with Parkfield (nice falsifiable claim); ring-fracture sign logic is elegant. | No dedicated analysis doc; geodetic cross-check is "factor ~2"; −8% cumulative dv/v linearity unresolved; simplified spheroid geometry. |

The **cross-site message** — that dv/v amplitudes cannot be compared without normalizing by β (Cascadia dv/v is 8× Parkfield's, yet Parkfield's stress rate is 20× larger) — is correct, important, and well-made. The **β-clustering claim** (fractured crystalline rock β ≈ 200–400 regardless of granite vs basalt; sediment β ~ 3000) is the headline falsifiable result and is reasonably stated, though it rests on only two crystalline points whose β both come from the approximate directional bridge.

---

## 5. Reproducibility & process

- **Tests:** 42/42 pass in ~3.6 s. But coverage is config/window-selection/poroelastic plumbing + a reproducibility smoke test — **no test exercises the coupling-tier physics, the notebook forward models, or the bridge self-consistency.** Add: (i) a test asserting each preset's β equals the bridge value within tolerance; (ii) a test asserting ν_u ≥ ν_d for all coupling computations; (iii) golden-value tests for the site stress estimates.
- **Environment:** pixi-locked, NumPy 2.4 / Python 3.14 — modern and reproducible.
- **Self-review bias:** the "Accept 9.3/10" verdict is from an AI rubric reviewer of AI-generated text; `05_convergence_and_evaluation.md` §7 honestly flags rubric saturation. Treat the 9.3 as an internal consistency score, not external readiness.

---

## 6. Internal inconsistencies to reconcile (consolidated)

1. **Cascadia μ′: 1290 (site doc) vs 618 (all review docs)** — root cause: μ = 2.1 vs 0.475 GPa for the same site. Pick one.
2. **Cascadia stress rate: 1.24 vs 0.58 kPa/yr** — same root cause (κ = 10.3 vs 4.86 GPa).
3. **Cascadia central long-term dv/v: 0.003%/yr (§1) vs 0.015%/yr (Table)** within the site doc.
4. **Bridge κ:** undrained seismic K used where drained κ is required (§2.2); β presets violate the bridge.
5. **ν drift:** Parkfield κ = 29.8 GPa implies ν ≈ 0.28; config stores ν = 0.25.
6. **μ′ symbol overload** (§2.4): dμ/dP vs ∂(ρV²)/∂σ_c.
7. **"Independent exact validation" framing** for Cascadia stands in the R4 review doc but is retracted by the June research review.
8. **Kīlauea** appears in the synthesis with no analysis document.

---

## 7. Prioritized recommendations

**P0 — fixes that protect the novelty claims (do before any submission)**
1. Make the **bridge relation self-consistent**: derive κ from (μ, ν) at the stated drainage state for every site; recompute β and μ′; decide drained vs undrained per timescale and state it. Re-reconcile Cascadia μ′/stress to one set of numbers. (§2.2, §6.1–6.2)
2. Have `config.py` presets **compute β from the bridge** (add the strain-domain bridge function to `poroelastic_framework.py`); add a test enforcing it. (§3.2–3.3)
3. **Reframe claim 2 honestly.** Either (a) build at least one coupling figure where the effect *emerges* from coupled physics (e.g., a true β_eff(ω) frequency sweep, or a forward poroelastic model with an actual Green's-function convolution), or (b) relabel the tier/diagnostic material as *proposed* state-dependent constitutive structure with synthetic round-trip *estimator validation*, removing language that implies discovery. (§3.4)
4. Fix the **undrained-Poisson bug** and the **Tier-1 cancellation** in `coupling_tier_tests.py`. (§3.4)

**P1 — correctness and credibility**
5. Resolve the **μ′ symbol overload** across notebooks, table, and paper. (§2.4)
6. Fix NB1 Berger component equations (or delete the unused components); replace the fabricated NB6(c) error map with a real kernel comparison or remove it; choose β_quadratic large enough to actually show the nonlinearity the panels claim. (§3.5)
7. Fix the Biot-coefficient bug in `skempton_B_from_velocities` and the day/second unit confusion in `interpret_fitted_params.py`. (§3.2, §3.4)
8. Seed all `np.random` in figure scripts; remove the global `warnings.filterwarnings('ignore')`. (§3.4)

**P2 — external readiness**
9. Add a **real-data example** (the persistent reviewer blocker) — even one reprocessed station with a published comparison.
10. Verify **AGU/JGR AI co-authorship policy**; the "Claude (Anthropic AI)" co-author line is a live rejection risk. Keep the Statement of AI Use regardless.
11. Rename `BayesianWindowAverage` → window-sensitivity diagnostic in `codameter`; pin NumPy ≥ 2.0. (§3.1)
12. Write a Kīlauea analysis doc to match Parkfield/Cascadia, or downgrade Kīlauea to an illustrative example. (§4)

---

## 8. Bottom line

The science has a real and defensible core (the isotropic-vs-deviatoric diagnostic and the β-normalization message), the theory is mostly verified, and the engineering of the `codameter` prototype is good. The two stated novelties need work of opposite kinds: **claim 1 needs a correctness fix** (make the bridge self-consistent and actually implemented), and **claim 2 needs a framing/demonstration fix** (stop asserting coupling that the code inserts by hand, and either demonstrate it or label it as proposed). The test suite, equation log, and review history show a disciplined process — but the discipline has not yet reached the coupling-tier code or the bridge's numerical application, which is exactly where the paper's originality lives.

---

## 9. Remediation log (2026-06-25)

The fixes below were implemented this session. Numbers are grounded in
`docs/site_analyses/provenance_tables.md` (the new single source of truth).

**Resolution of the drained/undrained question (was unspecified).** The regime
is now **data-driven** via the Péclet number Pe = ωL²/c, not assumed. Seismic
moduli are treated as undrained (κ_u); the drained modulus follows
κ_d = κ_u(1−α_B B). Cascadia's secular trend computes to Pe ≈ 2.5
(transitional→undrained), which *justifies* the undrained κ_u = 4.86 GPa that
was previously used without justification — converting an apparent bug into a
documented result.

| Audit finding | Status | Resolution |
|---|---|---|
| Bridge not self-consistent / not implemented (P0-1,2) | **Fixed** | `bridge_beta`, `mu_prime_from_bridge`, `drained_bulk_modulus` added; `SiteConfig` gains `Vp`, `kappa_u/kappa_d`, and a validator that *enforces* β = −μ′κ/2μ for bridge-sourced presets. |
| Cascadia κ uses undrained modulus in drained-derived relation | **Fixed/justified** | Pe ≈ 2.5 ⇒ undrained regime ⇒ κ_u correct; documented in §2.5/§9.2 and provenance table. |
| Cascadia μ′ 1290 vs 618 / 1.24 vs 0.58 kPa/yr | **Fixed** | Reconciled to μ′=618, 0.58 kPa/yr; site doc was the wrong velocity layer, now corrected. β=−3160 marked **published** (Kidiwela) → bridge = consistency check. |
| Parkfield ν drift (κ⇒ν≈0.28 vs stored 0.25) | **Fixed** | ν now derived from velocities; regime note added (drained–transitional; μ′ bounded 251–350). |
| Kīlauea had no analysis doc | **Fixed** | `kilauea_stress_analysis.md` created. |
| Tier-1 cancellation + wrong undrained-Poisson | **Fixed** | Panel replaced by emergent β_eff(ω) sweep grounded in drainage frequency. |
| Tier-2 non-physical pore-pressure convolution | **Fixed** | Single dimensionally-consistent exponential-memory convolution. |
| Biot coefficient bug (K_sat vs K_grain) | **Fixed** | Uses grain modulus. |
| μ′ symbol overload (notebooks/table) | **Fixed** | Split into μ′=dμ/dP and S_σ=∂(ρv²)/∂σ_c. |
| NB1 ad-hoc Berger components; NB6 fabricated error map; NB3/NB5 inert nonlinearity panels; prose constants | **Fixed** | Removed/replaced with real disba-kernel computation; corrected coefficients. |
| Diagnostic-case discovery framing; circular Pe–R² overlay; day/sec unit bugs; unseeded RNG; global warning suppression | **Fixed** | Relabeled as estimator validation; overlay relabeled as diagnostic prior; units corrected; RNG seeded. |
| Tests cover only plumbing | **Improved** | 53 tests (was 42): bridge consistency, ν_u ≥ ν_d, golden site values, YAML↔Python agreement. |

**Still open (out of scope this session, unchanged from §7 P2):** real-data
example; AGU AI co-authorship policy; rename `codameter.BayesianWindowAverage`.
