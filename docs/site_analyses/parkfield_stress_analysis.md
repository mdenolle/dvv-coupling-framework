# Quantitative Parkfield Stress Analysis: Applying the Unified Framework

## 1. Observed Quantities from Okubo et al. (2024)

### 1.1 The $\delta v/v$ tectonic trend

From Okubo et al. (2024, their Fig. 11b):
- **Linear trend rate:** $b_0 = 0.0048\%$/yr (stretching method, median across station pairs)
- **MWCS estimate:** $b_0 = 0.0027\%$/yr (more conservative)
- **Frequency band used:** 0.9–1.2 Hz
- **Depth sensitivity:** ~1 km (from Rayleigh wave sensitivity kernel, their Fig. S10)
- **Duration:** 2002–2022 (20 years), so cumulative $\delta v/v \approx 0.05$–$0.1\%$

### 1.2 The GNSS strain field

From Okubo et al. (2024, their Figs. 13–15):
- **Dilatational strain:** shows *slight extension* — **opposite** to what $\delta v/v = \beta \epsilon_{kk}$ would predict. This rules out isotropic acoustoelasticity as the explanation.
- **Contractional axial strain:** shows compression in azimuth range **N35°W to N45°E** (~N350°–N045°), correlating with the $\delta v/v$ increase.
- **GNSS strain rate at Parkfield:** The SAF at Parkfield accommodates ~30–35 mm/yr of relative plate motion. For a ~15 km locking depth and ~10 km half-width of the strain accumulation zone, the shear strain rate is approximately $\dot{\gamma} \sim v/(2W) \sim 0.033/(2 \times 10^4) \approx 1.6 \times 10^{-6}$/yr = **1600 nanostrain/yr** of maximum shear strain rate. The contractional component across the fault is a fraction of this — from InSAR/GNSS models, the fault-normal contractional strain rate near Parkfield is roughly **100–300 nanostrain/yr**.

### 1.3 Frequency dependence

From Okubo et al. (2024, their Fig. S9):
- The long-term trend rate $b_0$ **increases with frequency**, suggesting the velocity change is concentrated at *shallow* depths (higher frequencies have shallower sensitivity).
- This is consistent with a near-surface stress perturbation (upper ~1 km) and inconsistent with a deep (>3 km) perturbation.

---

## 2. Velocity Structure from SAFOD

### 2.1 The $V_S(z)$ profile

From the SAFOD Pilot Hole (Boness & Zoback, 2004; Jeppson & Tobin, 2015) and regional tomography (Zhang et al., 2009; Thurber et al., 2006):

| Depth (km) | Lithology | $V_P$ (km/s) | $V_S$ (km/s) | $V_P/V_S$ | $\rho$ (kg/m³) |
|------------|-----------|-------------|-------------|-----------|----------------|
| 0–0.2 | Quaternary sediments | 1.5–2.5 | 0.5–1.2 | ~2.5–3.0 | 1800–2100 |
| 0.2–0.77 | Tertiary sediments | 2.5–4.0 | 1.2–2.3 | ~1.8–2.1 | 2100–2400 |
| 0.77–1.5 | Salinian granite (weathered) | 4.0–5.5 | 2.3–3.2 | ~1.73 | 2500–2650 |
| 1.5–3.0 | Salinian granite (intact) | 5.5–6.0 | 3.2–3.5 | ~1.72 | 2650–2700 |
| >3 | Deep crust (NE: Great Valley Seq.) | 5.5–6.5 | 3.0–3.8 | ~1.75–1.90 | 2600–2750 |

**Key features:**
- Strong velocity contrast across the SAF (SW Salinian side faster; NE Franciscan/GVS side slower)
- Low-velocity zone along the SAF trace extending to 7 km depth
- $V_P/V_S > 1.93$ in fluid-rich zones (depths < 3 km on SW side) — virtually devoid of seismicity
- Seismicity restricted to $V_S > 2.0$ km/s

### 2.2 Crude Rayleigh wave sensitivity kernel

For the 0.9–1.2 Hz band used by Okubo et al., the peak sensitivity depth is approximately:

$$z_{\text{peak}} \approx \frac{V_S}{3f} \approx \frac{2.5 \text{ km/s}}{3 \times 1.0 \text{ Hz}} \approx 0.8 \text{ km}$$

using an average $V_S \approx 2.5$ km/s for the upper 1 km (the geometric mean of the sediment-granite transition). The sensitivity kernel extends from the surface to ~2 km, with most weight in the **0.2–1.5 km** range — the Tertiary sediment and weathered granite layers. This is consistent with Okubo et al.'s statement that the 0.9–1.2 Hz band corresponds to ~1 km depth.

---

## 3. Predicting Stress at Depth

### 3.1 Strategy

We use two approaches:

**Approach A (acoustoelastic/strain):** From $\delta v/v = \beta \epsilon_{kk}$, invert for volumetric strain, then convert to stress.

**Approach B (induced-stress/Tromp):** From $\delta V_S/V_S = \mu' p^0 / (2\mu)$ (isotropic part), invert for induced pressure.

But Okubo et al. showed that the dilatational strain is *extensional* while $\delta v/v$ is *increasing*. This means:

**The isotropic formulation fails.** We must use the full anisotropic framework (Eq. 4 of the paper).

### 3.2 Approach C: Deviatoric stress from contractional strain

Since only the contractional component correlates with $\delta v/v$, we use:

$$\frac{\delta V_S}{V_S} = \frac{\mu'}{2\mu} p^0 + \text{deviatoric terms}$$

For the Parkfield case, the isotropic pressure $p^0$ is near zero (dilatation is negligible or slightly extensional). The velocity change is driven by the *deviatoric* component — specifically, microcrack closure under the contractional axial strain.

Under the microcrack closure model (Sayers & Kachanov, 1995; Verdon et al., 2008), the $\delta v/v$ along the maximum contractional direction is:

$$\frac{\delta v}{v} \approx \beta_{\text{axial}} \cdot \epsilon_{\text{contractional}}$$

where $\beta_{\text{axial}}$ is the directional acoustoelastic coefficient for the contractional axis. For crack-dominated media with preferentially oriented cracks, $\beta_{\text{axial}}$ can be significantly larger than the isotropic $\beta$ because it captures the full closure stiffening rather than the volumetric average.

### 3.3 Numerical estimates

**Given:**
- $\delta v/v \approx 0.0048\%$/yr $= 4.8 \times 10^{-5}$/yr
- $\epsilon_{\text{contractional}} \approx 200$ nanostrain/yr $= 2.0 \times 10^{-7}$/yr (typical for Parkfield fault-normal contraction)

**The effective $\beta$:**

$$|\beta_{\text{eff}}| = \frac{\delta v/v}{\epsilon_{\text{contractional}}} = \frac{4.8 \times 10^{-5}}{2.0 \times 10^{-7}} \approx 240$$

This is within the expected range for weakly cemented to fractured crystalline rock ($|\beta| \sim 100$–$1000$; Clements & Denolle, 2023). The value is lower than soft sediments ($|\beta| \sim 500$–$10,000$) and higher than intact granite ($|\beta| \sim 10$–$50$), consistent with the **weathered/fractured Salinian granite** at the sensitivity depth of ~0.8 km.

### 3.4 Stress at ~1 km depth

Using the bridge relation $\beta = -\mu'\kappa/(2\mu)$ and the velocity profile:

**At z ≈ 0.8 km (weathered granite):**
- $V_S \approx 2.5$ km/s, $\rho \approx 2500$ kg/m³
- $\mu = \rho V_S^2 \approx 2500 \times 2500^2 = 15.6$ GPa
- $V_P \approx 4.5$ km/s → $\kappa = \rho(V_P^2 - 4V_S^2/3) \approx 2500(20.25 - 8.33) \approx 29.8$ GPa
- From $|\beta| \approx 240$: $\mu' = 2\mu|\beta|/\kappa = 2 \times 15.6 \times 240 / 29.8 \approx 251$

This $\mu' \approx 250$ is high but plausible for fractured granite at relatively shallow confining pressure (~20 MPa at 0.8 km). Fokker et al. (2021) reported $\mu' \sim 50$–$150$ for consolidated sediments at comparable depths in Groningen; the higher value here reflects the fractured, crack-rich SAFOD granite.

> **Grounding/regime note (2026-06-25).** The $\kappa = 29.8$ GPa above is the *seismic-band* (undrained) modulus computed directly from $V_P, V_S$ (it implies $\nu \approx 0.28$; the prior config value $\nu = 0.25$ is superseded — moduli are now derived from velocities, not an assumed $\nu$). For the secular interseismic signal the Péclet number is $Pe<1$ (drained–transitional) for plausible fractured-granite diffusivities, but because granite has small $\alpha_B B \approx 0.28$ the drained modulus $\kappa_d = \kappa_u(1-\alpha_B B) \approx 21.5$ GPa differs only modestly, bounding $\mu' \approx 251$ (using $\kappa_u$) to $\approx 350$ (using $\kappa_d$). Since $\beta_{\text{axial}}$ is directional, Eq. 7 is an **order-of-magnitude** relation here regardless; we report the $\kappa_u$ endpoint to match the directly-measured seismic modulus. See `provenance_tables.md`.

**The contractional stress change per year:**

Using $\delta V_S/V_S = \mu' \sigma_{\text{deviatoric}} / (4\mu)$ (the deviatoric term from Eq. 4):

$$\sigma_{\text{deviatoric}} = \frac{4\mu \cdot \delta V_S/V_S}{\mu'} = \frac{4 \times 15.6 \times 10^9 \times 4.8 \times 10^{-5}}{251} \approx 12 \text{ kPa/yr}$$

Over 20 years: **cumulative deviatoric stress change ≈ 240 kPa ≈ 0.24 MPa** at ~1 km depth.

**Cross-check with strain:**

$\sigma = E \cdot \epsilon / (1-\nu^2) \approx 40 \text{ GPa} \times 2 \times 10^{-7} / 0.92 \approx 8.7$ kPa/yr

This is within a factor of 1.4 of the $\delta v/v$-derived estimate — remarkably consistent given the crude assumptions. The slight discrepancy could reflect: (a) depth averaging through the sensitivity kernel, (b) the nonlinear (pressure-dependent) response giving more weight to the shallowest, most compliant layers, or (c) partial healing contributing to the apparent trend.

### 3.5 Summary of stress prediction

| Quantity | Value | Source |
|----------|-------|--------|
| $\delta v/v$ trend | $4.8 \times 10^{-5}$/yr | Okubo et al. (2024), stretching |
| Depth of sensitivity | ~0.8 km (0.2–1.5 km range) | $V_S/(3f)$ with SAFOD $V_S$ |
| Contractional strain rate | ~200 nanostrain/yr | GNSS (Parkfield) |
| Effective $\beta_{\text{axial}}$ | ~240 | $\delta v/v / \epsilon$ |
| Inferred $\mu'$ at 0.8 km | ~250 | Bridge relation (Eq. 7) |
| Deviatoric stress rate | ~12 kPa/yr | Tromp & Trampert framework |
| 20-year cumulative stress | ~0.24 MPa | Integrated over observation period |

---

## 4. Stress Anisotropy Direction

### 4.1 The azimuthal signature

Okubo et al. (2024) rotated the GNSS-derived strain tensor to all azimuths and found that $\delta v/v$ correlates with the axial strain only in the azimuth range **N35°W to N45°E**. This corresponds to the **maximum horizontal contractional strain direction** at Parkfield, which is roughly perpendicular to the SAF strike (~N41°W).

### 4.2 Comparison with SAFOD stress measurements

Boness & Zoback (2004) measured the maximum horizontal stress direction from wellbore breakouts in the SAFOD Pilot Hole: $S_{Hmax}$ is oriented **N15°E ± 20°** in the granite section (0.77–2.15 km depth). This is at a high angle to the SAF strike (N41°W) and falls within the contractional-strain azimuth range where $\delta v/v$ correlates.

The consistency between: (a) the azimuth of GNSS-derived contractional strain, (b) the $S_{Hmax}$ direction from wellbore breakouts at SAFOD, and (c) the azimuthal range where $\delta v/v$ shows positive correlation, strongly supports the **microcrack closure mechanism**: cracks oriented perpendicular to $S_{Hmax}$ (i.e., roughly fault-parallel) close preferentially under the increasing contractional stress, stiffening the medium in the $S_{Hmax}$ direction and producing a positive $\delta v/v$.

### 4.3 Implications

The fact that $\delta v/v$ responds to the contractional component rather than to dilatation means:

1. **Standard acoustoelasticity ($\delta v/v = \beta \epsilon_{kk}$) is insufficient.** The deviatoric component dominates at Parkfield.
2. **Azimuthal $\delta v/v$ analysis can constrain $S_{Hmax}$ orientation** — this is a passive, continuous measurement of stress direction from ambient noise, complementing borehole-based methods.
3. **The dominant mechanism is crack closure, not bulk compression.** This implies the rock has significant *aligned* compliant porosity — consistent with the high fracture density observed in the SAFOD Pilot Hole.

---

## 5. Rheological Model from the $\delta v/v$–strain relation

### 5.1 What kind of relationship?

From Okubo et al. (2024, their Fig. 14):
- The $\delta v/v$ shows a **monotonically increasing** cumulative contractional strain over the 20-year period.
- The relationship is approximately **linear** after removing environmental and coseismic effects.
- No clear hysteresis, no curvature, no saturation.

### 5.2 Rheological interpretation

Using the diagnostic crossplots from §7.2 of our paper:

- **Linear $\delta v/v$–strain:** consistent with **elastic (time-independent)** rheology. The medium stiffens linearly with accumulating contractional strain via crack closure.
- **No hysteresis:** rules out significant *viscoelastic* retardation (which would produce elliptical crossplots) and *dynamic capillary* effects (irrelevant at 0.8 km depth in granite).
- **No saturation:** the cracks have not fully closed after 20 years of loading. This sets a lower bound on the total compliant porosity: if each crack contributes $\delta V_S/V_S \sim \epsilon_c \xi$ upon closure, and the total observed $\delta V_S/V_S \sim 10^{-3}$ corresponds to partial closure, the total crack density must be $\epsilon_c > 0.01$, consistent with SAFOD fracture observations.
- **The logarithmic healing component** (from the 2004 Parkfield earthquake) is superimposed on the linear tectonic trend. The healing follows slow dynamics ($\tau$ range 0.1 yr to $>$10,000 yr; Snieder et al., 2017). The coexistence of elastic tectonic loading and slow-dynamics healing suggests that **the tectonic signal operates on a different population of cracks** than the coseismic damage: the tectonic signal closes pre-existing, tectonically-aligned cracks, while the coseismic damage activates new, randomly-oriented microcracks that then heal.

### 5.3 The rheological model

The simplest consistent model is:

$$\frac{\delta v}{v}(t) = \underbrace{\beta_{\text{axial}} \cdot \epsilon_{\text{contract}}(t)}_{\text{elastic, tectonic}} + \underbrace{\sum_i s_i L_i(t)}_{\text{slow dynamics, healing}} + \underbrace{s_T T(t) + p_1 \Delta\text{GWL}(t)}_{\text{environmental}}$$

where:
- The tectonic term is purely elastic (no time delay, no retardation)
- The healing term follows slow dynamics (logarithmic spectrum of relaxation times)
- The environmental terms are approximately elastic with known phase delays (thermal diffusion lag)

This is a **dual-population model**: aligned cracks respond elastically to tectonic loading, while damage-induced cracks heal via slow dynamics. The two populations can coexist because they have different geometries (oriented vs. random), different aperture distributions, and different creation mechanisms (tectonic preconditioning vs. coseismic rupture).

---

## 6. Can We Infer Third-Order Elastic (TOE) Constants?

### 6.1 What we can determine

From the Parkfield observations, we can estimate:

1. **$\beta_{\text{axial}} \approx -240$** (from $\delta v/v / \epsilon_{\text{contractional}}$). This is an *effective* nonlinear parameter for the contractional direction.

2. **$\mu' \approx 250$** at ~0.8 km depth (from the bridge relation $\beta = -\mu'\kappa/(2\mu)$).

3. The **anisotropy** of the nonlinear response (contractional vs. dilatational) constrains the crack orientation distribution: the response is dominated by fault-parallel cracks (~perpendicular to $S_{Hmax}$).

### 6.2 What we cannot determine

The *individual* Murnaghan constants ($l$, $m$, $n$) cannot be resolved from the Parkfield data alone because:

1. **$\beta$ depends on a combination:** $\beta = 3/2 + (l + 2m)/(\lambda + 2\mu)$ (Eq. 3). A single $\beta$ measurement gives one equation with two unknowns ($l + 2m$).

2. **We need independent loading paths.** To resolve $l$, $m$, $n$ separately, one needs velocity measurements under at least three independent loading configurations (e.g., hydrostatic, uniaxial horizontal, uniaxial vertical). At Parkfield, we have effectively one loading path (interseismic contraction).

3. **$\mu'$ is an aggregate.** The shear-modulus pressure derivative $\mu'$ is an effective-medium property of the crack ensemble, not a single-crystal parameter. It depends on crack density, aspect ratio distribution, and saturation state — all of which trade off.

### 6.3 What additional data would resolve the ambiguity

To determine individual TOE constants at Parkfield, one would need:

1. **Tidal $\delta v/v$ with azimuthal resolution** (Sens-Schönfelder & Eulenfeld, 2019): Earth tides provide a known, well-characterized loading with both volumetric and deviatoric components that vary with azimuth and time. Measuring $\delta v/v$ as a function of azimuth and tidal phase provides multiple independent equations.

2. **Multi-frequency $\delta v/v$** to resolve depth dependence: if $\beta(z)$ varies with depth (as it should, since crack density decreases with confining pressure), then measuring $\delta v/v$ at 0.5, 1.0, 2.0, 4.0 Hz gives depth-resolved $\beta$ and hence depth-resolved TOE parameters.

3. **Laboratory measurements** on SAFOD core at relevant confining pressures: ultrasonic velocity measurements under triaxial loading would give $l$, $m$, $n$ directly. Niu et al. (2008) measured velocity changes from barometric pressure at SAFOD — extending this to multi-axial loading would be ideal.

### 6.4 What we *can* say from the observations

Even without resolving individual TOE constants, the Parkfield data constrain the *ratio*:

$$\frac{l + 2m}{\lambda + 2\mu} = \beta - \frac{3}{2} \approx -241.5$$

For $\lambda + 2\mu = \rho V_P^2 \approx 2500 \times 4500^2 \approx 50.6$ GPa at 0.8 km depth:

$$l + 2m \approx -241.5 \times 50.6 \text{ GPa} \approx -12{,}200 \text{ GPa}$$

This is enormous compared to the second-order constants ($\lambda + 2\mu \approx 50$ GPa), confirming the highly nonlinear character of the fractured shallow crust. For comparison, intact Westerly granite has $l + 2m \approx -3000$ GPa (Johnson & Rasolofosaon, 1996), while sandstones reach $l + 2m \approx -50{,}000$ GPa. The Parkfield value of $-12{,}200$ GPa sits between these, consistent with fractured granite.

---

## 7. Summary

| Question | Answer |
|----------|--------|
| **Stress at ~1 km depth** | Deviatoric stress rate ~12 kPa/yr; cumulative ~0.24 MPa over 20 years |
| **Stress anisotropy direction** | N35°W–N45°E (contractional), consistent with $S_{Hmax}$ ≈ N15°E from SAFOD breakouts |
| **Depth sensitivity** | Peak at ~0.8 km (range 0.2–1.5 km) from SAFOD $V_S$ profile and 0.9–1.2 Hz kernel |
| **Rheological model** | Dual-population: elastic tectonic loading (aligned cracks) + slow-dynamics healing (damage cracks) |
| **Effective $\beta$** | ~−240 (directional, contractional axis) |
| **Inferred $\mu'$** | ~250 at 0.8 km depth |
| **Can TOE constants be resolved?** | Only $l + 2m \approx -12{,}200$ GPa; individual $l$, $m$, $n$ require tidal azimuthal data |
| **Key finding** | Standard isotropic $\delta v/v = \beta\epsilon_{kk}$ fails at Parkfield; the deviatoric/anisotropic framework is essential |
