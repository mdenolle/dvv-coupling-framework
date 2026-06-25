# Coda Window Selection Metrics for `codameter`

## Problem

Ambient-noise and coda-wave `dv/v` studies often report final velocity-change time series without enough information to reproduce why a particular frequency band, substack length, or coda lapse-time window was chosen. This is not a harmless processing detail. The window controls the wave type, depth sensitivity, uncertainty, and susceptibility to source-side changes.

The measurement should therefore be treated as

```text
dv/v = d(frequency band, lapse-time window, window duration, substack length, time)
```

rather than as a single scalar time series or one fixed coda window.

## Scope: a standalone companion paper, not a section of the framework paper

This document develops a Bayesian uncertainty quantification (UQ) of dv/v with
respect to processing choices (window, frequency, wave type, substack, estimator).
After exploring whether it belongs in the unified-framework manuscript, the
decision is that it is a **standalone companion paper + `codameter` software
release**, because it has a distinct thesis (measurement *reproducibility/UQ* vs
physical *interpretation*), its own validation burden (synthetic coverage tests +
a real multi-station reproducibility study), and a self-contained hierarchical
estimator. The framework paper keeps only the *conceptual framing* (the window is
part of the kernel, Eq. 15) and the window-*sensitivity diagnostic*; it does not
ship a turnkey UQ method. Full reasoning, novelty, method, validation plan, and
journal targets are in the prospectus:
[companion_paper_bayesian_dvv_uq.md](companion_paper_bayesian_dvv_uq.md).

## Theoretical Basis

The standard frequency-depth relation can be written as

```math
d(f,t) = \int K(z,f) \delta V_S(z,t)/V_S(z) dz
```

but the coda window also changes the kernel:

```math
d(f,\tau,W,T_{\mathrm{stack}},t)
  = \int K(z; f,\tau,W,\mathbf{g}) \delta V_S(z,t)/V_S(z) dz + \epsilon .
```

Here `tau` is the coda-window center lapse time, `W` is the window duration, `T_stack` is the substack length, and `g` describes station geometry and wavefield directionality.

Takano et al. (2019, JGR Solid Earth, doi:10.1029/2018JB016235) provide a useful empirical anchor: at Izu-Oshima, early 2-7 s lapse windows at 2-4 Hz showed strong sensitivity to tidal strain, whereas later 7-35 s windows had reduced strain sensitivity and apparent velocities suggesting a growing scattered/reflected body-wave contribution. The implication is general even if the exact timing is site-specific: lapse time is a physical axis of the measurement.

## Window Objective

`codameter` should first compute a rolling lapse-time profile from early to late coda. Each overlapping window in that profile is scored with an objective

```math
J = \sum_i w_i Q_i
```

where each `Q_i` is normalized to `[0, 1]` and weights are reported. The goal is not to find one universal window. The goal is to map how measurement quality, wave type, depth targeting, and inferred forcing sensitivity evolve with lapse time, then test whether scientific conclusions survive across a stable window ensemble.

## Core Metrics

1. **Coherence:** mean or robust cross-correlation coherence in the window.
2. **Signal-to-noise ratio:** coda-window energy relative to a pre-signal or late-noise window.
3. **Cycle count:** window duration must contain enough cycles at the low edge of the band.
4. **Wave-type consistency:** apparent velocity or array slowness should match the intended wave type.
5. **Depth targeting:** frequency-depth proxy or full sensitivity-kernel overlap with the target depth range.
6. **Uncertainty:** stretching, MWCS, or wavelet-domain `dv/v` uncertainty.
7. **Lapse-time stability:** recovered `dv/v`, beta, or forcing sensitivity should not change abruptly across adjacent windows unless that transition is the scientific target.
8. **Temporal resolution:** substack length must resolve the shortest target forcing period while retaining adequate precision.
9. **Source stability:** sensitivity to seasonal source spectrum, azimuth, and amplitude changes.

## Rolling Profile Workflow

1. Define the frequency band and substack length to test.
2. Roll a fixed-duration coda window from early to late lapse time.
3. Compute `dv/v` and diagnostic metrics in every window.
4. Score each window, preserving lapse-time order.
5. Inspect the profile for plateaus, transitions, and wave-type changes.
6. Report the profile and any selected stable interval, not only a final `dv/v` trace.

This is the key correction to a single-window workflow: early windows, transitional windows, and late windows are all scientifically useful. Late windows may not be "bad"; they may simply sample a different mixture of body waves, scattered waves, and depth sensitivity.

## Bayesian Interpretation

The rolling-window profile can be turned into a Bayesian analysis by treating each window as a competing measurement model:

```math
M_j = (f_j, \tau_j, W_j, T_{\mathrm{stack},j})
```

For a scientific quantity `theta` such as `dv/v(t)`, a tidal strain sensitivity, a seasonal amplitude, or a hydrological regression coefficient, each window gives a window-conditioned posterior:

```math
p(\theta \mid y, M_j) \approx \mathcal{N}(\hat{\theta}_j, \sigma_j^2).
```

The window metrics define a prior model weight, not a hard accept/reject rule:

```math
p(M_j) \propto \exp(\lambda J_j),
```

where `J_j` is the normalized objective score and `lambda` controls how strongly the score concentrates the prior. The model-averaged posterior is then

```math
p(\theta \mid y) = \sum_j p(M_j \mid y) p(\theta \mid y, M_j).
```

In the first `codameter` implementation, `p(M_j | y)` is approximated from the objective score. A fuller implementation can replace this with a true marginal likelihood or leave-one-out predictive score from the waveform fit.

The uncertainty decomposition follows the law of total variance:

```math
\mathrm{Var}(\theta \mid y)
= \mathbb{E}_{M}[\mathrm{Var}(\theta \mid y, M)]
+ \mathrm{Var}_{M}[\mathbb{E}(\theta \mid y, M)].
```

The first term is the within-window measurement uncertainty. This includes waveform noise, finite stack length, and fit uncertainty from stretching, MWCS, or wavelet methods.

The second term is the method epistemic uncertainty. It measures how much the answer changes because of plausible choices of lapse-time window, frequency band, or substack length. If early and late windows produce different `theta` estimates with high individual precision, this term grows. That is precisely the uncertainty that standard single-window reporting hides.

This gives a direct reproducibility diagnostic:

- Small epistemic / total variance: the result is robust to window choice.
- Large epistemic / total variance: the result depends on the processing model and should be reported as window-sensitive.
- Structured epistemic variance across lapse time: the coda is transitioning between wave types, depths, or mechanisms.

## Initial Implementation

The first implementation lives in `codameter.window_selection` and is intentionally data-agnostic:

```python
from codameter import WindowEstimate, window_sensitivity_diagnostic
from codameter import rolling_lapse_windows, score_lapse_profile

windows = rolling_lapse_windows(
    start_s=2,
    stop_s=35,
    window_duration_s=5,
    step_s=1,
    fmin_hz=2,
    fmax_hz=4,
)

profile = score_lapse_profile(
    windows,
    observations={
        "lapse_000": {"coherence": 0.9, "snr": 10.0, "dvv_sigma": 2e-5},
        "lapse_001": {"coherence": 0.85, "snr": 9.0, "dvv_sigma": 3e-5},
    },
    distance_m=10000.0,
    rayleigh_group_velocity_mps=1000.0,
    vs_mps=1500.0,
    target_depth_range_m=(100, 250),
)

centers = profile.centers_s
scores = profile.objective
eligible = profile.eligible(min_score=0.7)

posterior = window_sensitivity_diagnostic(
    profile,
    estimates={
        "lapse_000": WindowEstimate(mean=1.0e-4, sigma=1.0e-5),
        "lapse_001": WindowEstimate(mean=1.1e-4, sigma=1.2e-5),
        "lapse_002": WindowEstimate(mean=4.0e-4, sigma=1.5e-5),
    },
)

print(posterior.mean)
print(posterior.aleatoric_sigma)
print(posterior.epistemic_sigma)
```

Future waveform-processing layers should compute the observation metrics automatically from cross-correlations and pass them to the same scorer.

---

## Critical Note on the Bayesian Inference (review of the GPT-5.5 proposal)

> Author's note: the Bayesian model-averaging scheme above (the `exp(λJ)`-weighted
> window average implemented in `window_sensitivity_diagnostic`) was drafted by GPT-5.5.
> It is a useful *framing* but an unsound *inference engine*. This section records
> the critique and the recommended replacement so the package does not ship a
> tunable number labelled "uncertainty." The rolling-profile diagnostics, the
> metric set, and the law-of-total-variance *vocabulary* are kept; the weighting
> and averaging mechanism are not.

### Why the proposed scheme is not yet defensible

1. **The weights are heuristic, not Bayesian.** Genuine model averaging uses the
   posterior model probability `p(M_j | y) ∝ p(y | M_j) p(M_j)`, where `p(y | M_j)`
   is the *evidence* (marginal likelihood). The proposal substitutes
   `p(M_j | y) ∝ exp(λ J_j)`, where `J_j` is a weighted sum of hand-normalized
   quality scores (in code, `softmax(score_weight_scale · score)` with
   `score_weight_scale = 4.0`). The reported epistemic variance is therefore a
   function of free constants with no data-driven identification: the metric
   weights `w_i` (`DEFAULT_WEIGHTS`), every `Q_i` normalizer (`target_snr`,
   `target_sigma`, `tolerance_factor`, ...), and the temperature `λ`. An
   uncertainty that moves when you retune a normalizer is not an uncertainty.

2. **It is not invariant to the candidate set.** Rolling windows (2–7 s, 3–8 s,
   4–9 s, ...) share most of their coda samples, so their estimates `θ̂_j` *and*
   their measurement errors are strongly correlated. The law-of-total-variance
   split assumes exchangeable, independent models. As a result (a) the aleatoric
   term `Σ_j w_j σ_j²` ignores the between-window error covariance entirely, so
   `total_sigma` is generically an *under*estimate; and (b) a dense cluster of
   near-duplicate early windows dominates the average by count and swamps a few
   physically distinct late windows. Refining the τ grid changes the answer — a
   multiplicity artifact, not science. A defensible estimator must be invariant
   to how finely the windows are gridded.

3. **It conflates physical signal with processing nuisance.** This document and
   Takano et al. (2019) both argue that lapse time is a *physical axis*: early and
   late windows sample different depths and wave types. So when early and late
   `θ̂_j` disagree, that disagreement is largely **resolved depth/wave-type
   signal**, not "method uncertainty." Averaging it into one scalar `θ` with an
   inflated epistemic bar discards the very information that motivates multi-lapse
   measurement. Only genuinely arbitrary choices that *should* return the same
   answer — substack length, edge jitter within one wave-type regime, stretching
   vs. MWCS — are legitimately epistemic.

4. **It solves the wrong problem.** The scientific target is the depth field
   `δV_S/V_S(z,t)` (and through it β, μ′, stress rate), not a window-averaged
   `dv/v` scalar. The windows differ by a *known* kernel `K(z; f, τ, W)`. When
   competing models differ by a known forward operator, the correct operation is
   **joint inversion**, not averaging. Model averaging is the wrong tool precisely
   when the kernel difference is the structure of interest.

### Recommended approach: a hierarchical measurement model

Treat the windows as **correlated data carrying kernels**, let the latent depth
field carry the resolution uncertainty, and use the quality metrics as a
**heteroscedastic noise model and quality gate** — never as model weights.

- **Forward model.** `d_j = ∫ K_j(z) m(z,t) dz + b_j + ε_j`, with latent
  `m(z,t) = δV_S/V_S(z,t)`, a window/source-side bias `b_j`, and noise `ε_j`.
- **Full data covariance `Σ`** (not diagonal). Estimate the off-diagonals from a
  block/day bootstrap of the cross-correlation stack and from coda decoherence as
  a function of lapse separation. This is the honest fix for window overlap.
- **Quality metrics → noise model.** Map coherence, SNR, cycle count, and
  wave-type consistency to an inflation of `σ_j` and a hard gate on junk windows.
  Quality-as-variance is a valid likelihood; quality-as-`exp(λJ)`-weight is not.
- **Physics priors.** Smoothness/regularization on `m(z)` (the inversion is
  ill-conditioned), log-normal priors on diffusivities, and bounds on β, μ′.
- **Principled epistemic term.** The posterior covariance of `m(z,t)` *is* the
  depth-resolution uncertainty, and it is invariant to adding redundant windows
  (correlated data add little information; `Σ` accounts for it correctly).
- **Segment, don't blur.** Changepoint-detect the lapse profile into wave-type-
  homogeneous regimes (early surface-wave vs. late scattered/body). Invert
  *within* a regime; report cross-regime differences as resolved signal,
  separately, rather than as one error bar.
- **Legitimate averaging only within a regime.** Marginalize the truly arbitrary
  nuisances (substack length, edge jitter, estimator) over windows that share a
  kernel; that residual spread is the honest robustness-to-processing number.

### Minimum defensible fix for `codameter` v1

If a full hierarchical inversion is out of scope for the first release, the two
fatal defects can be removed without one:

1. **Replace the weights.** Use an evidence or leave-one-out predictive score from
   the waveform fit (the "future" option already noted above should be the
   *default*, not optional), or fall back to equal weights over a **deduplicated,
   one-representative-per-regime** window set. Drop `exp(λJ)` heuristic weighting.
2. **Replace the variance.** Replace `Σ_j w_j σ_j²` with a **block/day-bootstrap**
   estimate of `Var(θ)` that includes the between-window error covariance, so the
   reported `total_sigma` stops under-counting correlated error.

Until then, `window_sensitivity_diagnostic` should be documented and used as a
*diagnostic of window sensitivity*, not as a producer of publishable error bars.

---

## Plain-Language Guide to Every Equation

This appendix explains each equation above for a reader who is comfortable with
regression, weighted averages, `softmax`, and bias/variance, but has not worked
with Bayesian inference. Each block gives the **symbols**, the **plain meaning**,
the **closest idea you already know**, and **what you actually compute in code**.

A one-line translation of the whole document up front: *a `dv/v` measurement is
not one number, it is the output of a small pipeline with knobs (frequency band,
where in the coda you look, how long a window, how many days you stack). Changing
a knob changes both the answer and what the answer physically means. The goal is
to handle those knobs honestly instead of hiding them.*

### 1. The measurement is a function, not a scalar

```text
dv/v = d(frequency band, lapse-time window, window duration, substack length, time)
```

- **Symbols.** `dv/v` is the relative velocity change you report. The arguments
  are the processing knobs: the band, the coda lapse time `τ` (how long after the
  source you look), the window length `W`, and the substack length `T_stack` (how
  many days of data you average into one estimate).
- **Plain meaning.** Two analysts who run "the same" measurement on the same data
  can get different `dv/v` if they set the knobs differently.
- **You already know this as.** A model prediction that depends on
  hyperparameters. `dv/v` is `model(data; hyperparameters)`, and the
  hyperparameters are not innocent — they change the target.
- **In code.** A `CodaWindow` dataclass *is* this argument list: `start_s`,
  `end_s`, `fmin_hz`, `fmax_hz`, `substack_days`.

### 2. The depth-sensitivity kernel

```math
d(f,t) = \int K(z,f)\, \frac{\delta V_S(z,t)}{V_S(z)}\, dz
```

- **Symbols.** `z` is depth. `δV_S/V_S(z,t)` is the *true* fractional shear-velocity
  change at depth `z` and time `t` — the physical thing you want. `K(z,f)` is the
  *sensitivity kernel*: how strongly a measurement at frequency `f` "feels" depth `z`.
- **Plain meaning.** Your single measured number is a **depth-weighted average** of
  the real profile. Low frequencies feel deep, high frequencies feel shallow.
- **You already know this as.** A dot product / linear projection. Discretize depth
  into bins and this is exactly `d = K · m`: `K` is one row of a design matrix and
  `m` is the unknown depth profile. The measurement is one weighted sum of the
  unknowns — that is why a single number cannot recover the whole profile.
- **In code.** `characteristic_depth()` returns the crude proxy `z ≈ Vs / (3·f)` —
  a one-number stand-in for "where this kernel peaks" until real kernels are wired in.

### 3. The window also changes the kernel

```math
d(f,\tau,W,T_{\mathrm{stack}},t) = \int K(z; f,\tau,W,\mathbf{g})\, \frac{\delta V_S}{V_S}\, dz + \epsilon
```

- **Symbols.** Same as above, but now `K` depends on the lapse window `(τ, W)` and
  the geometry `g` as well as `f`. `ε` is everything not modeled: measurement noise
  *and* source-side bias (e.g. seasonal changes in the noise sources themselves).
- **Plain meaning.** Moving the coda window is **not** just trading off noise — it
  changes *which depths and wave types you are measuring*. Early coda ≈ shallow
  surface waves; late coda ≈ deeper, scattered/body waves.
- **You already know this as.** Changing the design matrix row, not just the error
  bar. This is the single most important equation in the document: it is why you
  cannot treat window choice as a harmless nuisance to average over (see the
  critique above).
- **In code.** This kernel is not yet computed; `surface_wave_lapse_score()` and
  `depth_score()` are cheap proxies that flag *whether* a window is in the expected
  wave-type/depth regime.

### 4. The window quality score

```math
J = \sum_i w_i Q_i
```

- **Symbols.** `Q_i` are individual quality metrics each rescaled to `[0,1]`
  (coherence, SNR, cycle count, wave-type match, depth match, `dv/v` uncertainty,
  lapse stability). `w_i` are weights expressing how much you care about each.
- **Plain meaning.** One scalar "is this a trustworthy window?" score.
- **You already know this as.** A weighted scorecard / a hand-built composite
  feature. Note: there is no learning here — `w_i` and the `[0,1]` rescalings are
  chosen, not fit. That is fine for *ranking* windows; it becomes a problem only
  when this score is later misused as a probability (see §7 below).
- **In code.** `weighted_objective(metrics, weights)` with `DEFAULT_WEIGHTS`. Each
  `Q_i` is one scorer: `snr_score`, `cycles_score`, `surface_wave_lapse_score`,
  `depth_score`, `uncertainty_score`, `stability_score`. Missing metrics are
  dropped and the weights renormalize over what remains.

### 5. A window written as a "model"

```math
M_j = (f_j, \tau_j, W_j, T_{\mathrm{stack},j})
```

- **Plain meaning.** Index every candidate window with `j`. The proposal calls
  each one a "measurement model" `M_j`.
- **You already know this as.** One configuration in a hyperparameter grid search.
  `M_j` is the j-th grid point.
- **In code.** `candidate_windows(...)` or `rolling_lapse_windows(...)` builds the
  list `{M_j}`.

### 6. Each window gives an estimate with an error bar

```math
p(\theta \mid y, M_j) \approx \mathcal{N}(\hat{\theta}_j, \sigma_j^2)
```

- **Symbols.** `θ` is the scientific quantity you ultimately want (a `dv/v` value,
  a tidal sensitivity `β`, a regression slope). `y` is the data. `θ̂_j` is the
  estimate from window `j`; `σ_j` is its uncertainty. `N(·,·)` is a Gaussian.
- **Plain meaning.** "Given the data and *this* window, my answer is `θ̂_j` give or
  take `σ_j`." `p(θ | y, M_j)` is read "the probability distribution of θ given the
  data and this window."
- **You already know this as.** A point prediction plus a standard error, but
  promoted to a full bell curve. The Bayesian-specific idea is only this: the
  output is a *distribution over the answer*, not a single value. Everything else
  is bookkeeping on distributions.
- **In code.** `WindowEstimate(mean=θ̂_j, sigma=σ_j)`. You supply these from
  whatever estimator you use (stretching, MWCS, wavelet); the module does not
  compute them from waveforms.

### 7. Turning the score into a weight (the contested step)

```math
p(M_j) \propto \exp(\lambda J_j)
```

- **Symbols.** `J_j` is the quality score of window `j`; `λ` ("lambda") is a
  temperature that controls how sharply you favor high-scoring windows; `∝` means
  "proportional to" (normalize so the weights sum to 1).
- **Plain meaning.** Convert quality scores into weights, then trust good windows
  more when combining them.
- **You already know this as.** **Exactly `softmax(λ · J)`.** `λ→0` gives a flat
  average; `λ→∞` keeps only the single best window.
- **Why this is the weak link.** In a real Bayesian average the weight must be the
  *evidence* `p(y | M_j)` — how well the model predicts held-out data — not a
  hand-built quality score. Using `exp(λJ)` means your final uncertainty moves when
  you retune `λ` or the `[0,1]` rescalings, which is not acceptable for a published
  error bar. **Recommended practice:** use these weights only to *rank and gate*
  windows; for combining, prefer an out-of-sample predictive score, or equal
  weights over one representative window per wave-type regime.
- **In code.** `window_sensitivity_diagnostic(..., score_weight_scale=4.0)` — here
  `score_weight_scale` *is* `λ`, and the function literally calls `_softmax`.

### 8. The model-averaged answer

```math
p(\theta \mid y) = \sum_j p(M_j \mid y)\, p(\theta \mid y, M_j)
```

- **Symbols.** `p(M_j | y)` is the (normalized) weight from §7; `p(θ | y, M_j)` is
  the per-window bell curve from §6.
- **Plain meaning.** The final answer is a weighted blend of the per-window answers
  — a mixture of Gaussians.
- **You already know this as.** **Ensemble averaging / model stacking.** Each window
  is a weak learner; you average their predictions weighted by trust.
- **In code.** `posterior.mean = Σ_j weight_j · mean_j` (a weighted average of the
  `WindowEstimate` means).

### 9. Splitting the uncertainty (law of total variance)

```math
\mathrm{Var}(\theta \mid y) = \underbrace{\mathbb{E}_{M}[\mathrm{Var}(\theta \mid y, M)]}_{\text{aleatoric}} + \underbrace{\mathrm{Var}_{M}[\mathbb{E}(\theta \mid y, M)]}_{\text{epistemic}}
```

- **Symbols.** `E_M[·]` is the weighted average over windows; `Var_M[·]` is the
  weighted variance over windows. The first term averages each window's own
  variance `σ_j²`; the second measures how much the window *means* `θ̂_j` disagree.
- **Plain meaning.** Total uncertainty = (typical noise inside a window) + (how much
  the answer jumps when you change the window).
- **You already know this as.** **The ANOVA within-group + between-group split**,
  or the "aleatoric vs epistemic" split in ML. Term 1 = irreducible measurement
  noise; term 2 = disagreement between configurations.
- **The catch (why the critique matters).** This identity is only an *honest*
  uncertainty when the configurations are (a) roughly independent and (b) supposed
  to give the same answer. Overlapping coda windows violate both: they share data
  (so term 1 omits their error *covariance* and under-counts), and by §3 they
  measure physically different depths (so term 2 partly counts real signal as
  "uncertainty"). Treat a large term 2 as a *flag to investigate* — "my answer
  depends on the window" — not as a final error bar.
- **In code.**
  - `aleatoric_var = Σ_j w_j · σ_j²`  → `posterior.aleatoric_sigma`
  - `epistemic_var = Σ_j w_j · (mean_j − mean)²`  → `posterior.epistemic_sigma`
  - `total_sigma = sqrt(aleatoric_var + epistemic_var)`

### 10. The recommended replacement: invert, don't average

```math
d_j = \int K_j(z)\, m(z,t)\, dz + b_j + \epsilon_j, \qquad m(z,t) = \frac{\delta V_S}{V_S}(z,t)
```

- **Symbols.** `d_j` is the `dv/v` measured in window `j`; `K_j(z)` is that window's
  known kernel; `m(z,t)` is the unknown depth profile (the thing you actually want);
  `b_j` is a per-window/source-side bias; `ε_j` is noise.
- **Plain meaning.** Instead of treating windows as rival answers to average, treat
  them as **many measurements of one shared underlying profile**, each looking at a
  different depth mix. Then solve for the profile once, using all windows together.
- **You already know this as.** A single **regularized linear regression**:
  stack the windows into `d = K m + b + ε` and solve for `m`. Because the kernels
  are broad and overlapping, `K` is ill-conditioned, so you add a smoothness penalty
  — i.e. **ridge / Tikhonov regression**. Three upgrades make it honest:
  1. **Correlated errors → generalized least squares.** Estimate a full data
     covariance `Σ` (off-diagonals from a day/block **bootstrap** of the
     cross-correlation stack) instead of assuming independent windows. This is the
     real fix for window overlap.
  2. **Quality scores → a weighting/gating scheme.** Down-weight low-SNR, low-cycle
     windows by inflating their `σ_j` (heteroscedastic / weighted least squares) and
     drop junk windows entirely. This is the statistically valid use of the §4
     metrics — as a noise model, never as model probabilities.
  3. **Resolution as the honest epistemic term.** The covariance of the fitted `m(z)`
     tells you which depths are constrained and which are not — and, unlike §9, it
     does **not** change when you add redundant windows.
- **Practical recipe (what to build).**
  1. Build the candidate windows, score and **gate** them (`rank_windows`,
     `score_lapse_profile`), and **deduplicate**: keep roughly one representative per
     wave-type regime instead of 30 overlapping near-duplicates.
  2. Detect regime changes along lapse time (a changepoint / large
     `stability_score` drop) and **invert within a regime**, reporting
     cross-regime differences as *resolved signal*, not as one error bar.
  3. Form `d`, `K`, and a bootstrap `Σ`; solve the regularized GLS for `m(z,t)`;
     report `m` with its posterior covariance.
  4. Use Equations 17–18 only as a **sanity check** alongside the inversion: if the
     between-window term is small, a single well-chosen window was already enough;
     if it is large, the inversion (not an average) is doing the real work.

In short: Equations 1–9 are a good *vocabulary* and a good *diagnostic*. Equation
10 is the *inference method*. The practical move from one to the other is the move
from "softmax-average a hyperparameter grid" to "regularized regression with
correlated errors and a quality-based noise model."
