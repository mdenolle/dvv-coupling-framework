# Companion-Paper Prospectus — Reproducible dv/v: Processing-Choice Uncertainty Quantification

**Status:** scoping / prospectus (2026-06-25). Records the decision that a Bayesian
UQ of dv/v with respect to processing choices (window, frequency, wave type,
substack, estimator) should be a **standalone companion paper + `codameter`
software release**, not a section folded into the unified-framework manuscript.
The technical core already lives in [coda_window_selection_metrics.md](coda_window_selection_metrics.md)
(see especially its "Recommended approach: a hierarchical measurement model").

---

## 1. The question this paper answers

dv/v from ambient-noise / coda-wave monitoring is **not reproducible across
analysts**: the reported value depends on the frequency band, coda lapse-time
window (start/end/duration), substack length, wave type (Rayleigh/Love, surface
vs scattered/body), reference selection, and estimator (stretching vs MWCS vs
wavelet). Two groups processing the same data report different dv/v, and almost
no study propagates this *processing-choice* uncertainty. Can a principled,
Bayesian treatment (a) quantify it honestly and (b) reduce it — turning an
under-documented knob-twiddling step into a reproducible, uncertainty-bearing
measurement?

## 2. Why this is a standalone paper, not an add-on to the framework paper

| Criterion | Verdict |
|---|---|
| **Distinct thesis** | Framework paper = dv/v *interpretation* (stress/strain meter, rock physics, 3 sites). This = dv/v *measurement reproducibility & UQ*. Different claim, different reader. |
| **Own validation burden** | Needs synthetic coverage tests + a real multi-station reproducibility demonstration — exactly the end-to-end data work the framework paper explicitly defers (§10.5). Folding it in would force that work into the wrong paper. |
| **Self-contained method** | The hierarchical, correlated-window GLS estimator (with quality-as-noise and regime segmentation) is itself novel and substantial enough to anchor a paper. |
| **Software pairing** | It *is* the `codameter` package (../codameter); a methods+software paper (and/or JOSS) is the natural vehicle. |
| **Avoids overclaim** | The framework paper currently scopes this correctly as a *diagnostic* + future work; expanding it to a turnkey method there would reintroduce the overclaim the audit removed. |
| **Clean complementarity** | Framework paper supplies the forward models + the depth-inversion *vision* (§7.3–7.5); this paper supplies the reproducible *measurement + UQ* that feeds that inversion. No overlap, clear handoff. |

**Decision:** standalone companion. The framework paper keeps only (i) the
conceptual framing that the coda window is part of the sensitivity kernel
(Eq. 15) and (ii) the window-*sensitivity diagnostic* (`codameter.window_selection`,
`WindowSensitivityDiagnostic`) — both already present and caveated as *not* a
publishable error bar.

## 3. What is genuinely novel here (vs existing literature)

- Yuan et al. (2021) compared time/frequency/wavelet dv/v estimators; sensitivity-
  kernel work (Obermann 2014; Margerin) characterizes depth/lapse sensitivity;
  but **no unified estimator propagates processing-choice uncertainty with a
  correlated-window model and validated coverage.**
- Contributions:
  1. **Measurement-as-kernel** formalism: d(f,τ,W,T_stack) carries a known kernel,
     so competing windows are *correlated measurements of one latent field*, not
     rival scalars (the framework paper's Eq. 15).
  2. **Honest separation** of two uncertainties: genuine *method/epistemic*
     uncertainty (choices that should agree) vs *resolved depth/wave-type
     structure* (choices that physically differ). Naive model-averaging conflates
     them; this paper does not.
  3. **Correlated-window data covariance** Σ from a day/block bootstrap of the
     cross-correlation stack — the honest fix for overlapping-window double-counting.
  4. **Quality metrics as a heteroscedastic noise model + gate**, never as model
     weights (the `exp(λJ)` softmax is rejected — see the critique doc).
  5. **Lapse-time regime segmentation** (changepoint) → invert *within* a
     wave-type-homogeneous regime; report cross-regime differences as resolved
     signal, not as one error bar.
  6. **Resolution-as-epistemic**: the posterior covariance of δV_S/V_S(z,t) is the
     depth-resolution uncertainty and is *invariant to grid refinement* (redundant
     windows add little information once Σ is correct).
  7. **Coverage-validated** credible intervals + an open, tested implementation.

## 4. Method (already drafted in the theory doc)

Hierarchical measurement model:
d_j = ∫ K_j(z) m(z,t) dz + b_j + ε_j,  m = δV_S/V_S(z,t),  Cov(ε) = Σ (non-diagonal),
with smoothness/physics priors on m, quality-based inflation of σ_j, and gating of
junk windows. Solve regularized GLS; report m with posterior covariance. The
law-of-total-variance split (within = data noise, between = resolution) reappears
in its *correct* form. Full equations and the rationale are in
[coda_window_selection_metrics.md](coda_window_selection_metrics.md) §"Recommended approach".

## 5. Validation plan (the gating effort — currently the author's TODO)

1. **Synthetic coverage test.** Prescribe δV_S/V_S(z,t); generate coda (1-D kernel
   synthetics or 2-D/3-D scattering/SPECFEM); measure dv/v over a window grid;
   recover m + UQ; check that X% credible intervals contain truth X% of the time,
   and that the answer is invariant to τ-grid refinement.
2. **Real multi-station reproducibility study.** Choose ≥3 stations with public
   continuous data (independent of the 3 framework-paper studies — finding these
   is the author's stated next step). Compute dv/v under a large grid of
   processing choices; show (a) the raw inter-choice scatter (the reproducibility
   problem), (b) that the hierarchical estimate is stable, and (c) reduced scatter
   vs current single-window practice.
3. **Cross-estimator check.** stretching vs MWCS vs wavelet within one regime feed
   the *legitimate* method-uncertainty term.

## 6. Software

`codameter` (independent repo at `../codameter`): `window_selection` (scoring +
`WindowSensitivityDiagnostic`) is the seed. Add: a waveform layer computing the
observation metrics and per-window dv/v + σ from cross-correlations; the
block-bootstrap Σ estimator; the regularized GLS inversion; coverage diagnostics.
Likely a methods paper (Seismica / GJI / SRL) + JOSS software note.

## 7. Relationship to the framework paper (one-line each)

- **Framework paper provides:** forward models (thermo/hydro/poro/anisotropy),
  the bridge relation, the 3-site interpretation, and the depth/joint-inversion
  *vision* (§7.3–7.5).
- **This paper provides:** the reproducible, uncertainty-bearing *measurement*
  d(f,τ,W,…) that those interpretations should be built on, with the software to
  compute it.
- **Handoff:** the framework paper's §7.4 diagnostic and Eq. 15 are the explicit
  entry point; this paper turns the diagnostic into a validated estimator.

## 8. Risks / open questions

- Estimating a trustworthy correlated-window Σ is the hard technical step; if the
  bootstrap is noisy, the resolution claim weakens.
- Distinguishing "resolved structure" from "method error" requires reliable kernels
  K_j(z,τ,W); proxy kernels may be insufficient for the real-data study.
- Scope creep toward full 3-D imaging — keep this paper to the *measurement + 1-D
  depth UQ*; leave 3-D to the framework paper's vision.
