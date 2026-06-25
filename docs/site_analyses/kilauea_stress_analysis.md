# Quantitative Kīlauea Stress Analysis: Anisotropic Ring-Fracture Response During the 2018 Caldera Collapse

This analysis applies the unified $\delta v/v$ framework to the 2018 Kīlauea summit caldera collapse, the third site in the three-site application (with Parkfield and Cascadia). It is the most speculative of the three; all numbers match `docs/site_analyses/provenance_tables.md` and the manuscript §9.3.

---

## 1. Published Observations (Hotovec-Ellis et al. 2022; Anderson et al. 2019; Segall et al. 2020)

| Quantity | Value | Source |
|---|---|---|
| $\delta v/v$ per collapse (co-collapse increase) | ~+0.5% (~hourly sawtooth) | Hotovec-Ellis 2022 |
| Long-term $\delta v/v$ | −0.2 to −0.4 %/day (1–26 Jun), then stabilizes | Hotovec-Ellis 2022 |
| Radial strain per collapse (CRIM–UWEV, ~2 km baseline) | 15–25 µstrain | GNSS line-length |
| Reservoir pressure change $\Delta P$ | ~3 MPa | Segall 2020 |
| Reservoir geometry | prolate spheroid, centered 1.94 km | Anderson 2019 |
| $\mu$, $\nu$ at reservoir | 3.0 GPa, 0.25 | Anderson 2019 |

The diagnostic observation: modeled **volumetric** strain from reservoir pressurization predicts *extension* (velocity decrease) in most surrounding regions — the **opposite** of the observed co-collapse velocity *increase*. The modeled **radial** strain predicts the correct sign. The isotropic $\delta v/v = \beta\epsilon_{kk}$ fails, exactly as at Parkfield.

---

## 2. Bridge Relation as a Directional Consistency Check

Kīlauea basalt is low-porosity crystalline rock; the per-collapse forcing is ~hourly (undrained), and with small $\alpha_B B$ the drained and undrained moduli nearly coincide, so we use $\kappa$ from $(\mu, \nu)$:

$$\kappa = \frac{2\mu(1+\nu)}{3(1-2\nu)} = \frac{2 \times 3 \times 1.25}{3 \times 0.5} = 5.0\ \text{GPa} \quad (\mu = 3\ \text{GPa},\ \nu = 0.25).$$

The effective **radial** acoustoelastic parameter is data-driven from two published quantities:

$$|\beta_{\text{radial}}| = \frac{\delta v/v}{\epsilon_{\text{radial}}} = \frac{5\times10^{-3}}{2\times10^{-5}} \approx 250\text{–}330 \quad (\text{use } 300).$$

The bridge (inverse, order-of-magnitude because it is directional):

$$\mu' = \frac{2\mu|\beta_{\text{radial}}|}{\kappa} = \frac{2 \times 3 \times 300}{5} \approx 360.$$

$\beta_{\text{radial}} \approx 250$–330 clusters with the Parkfield $\beta_{\text{axial}} \approx 240$ despite the completely different setting (fractured basalt vs granite), supporting the headline claim that $|\beta| \sim 200$–400 characterizes **fractured crystalline rock** regardless of composition.

---

## 3. Stress per Collapse and Cross-Check

Radial stress perturbation at ~2 km from the reservoir (deviatoric term of Eq. 4):

$$\sigma_{\text{radial}} = \frac{4\mu(\delta v/v)}{\mu'} = \frac{4 \times 3\times10^9 \times 5\times10^{-3}}{360} \approx 167\ \text{kPa per collapse}.$$

**Geodetic cross-check.** A pressurized spheroid ($\Delta P = 3$ MPa, $a \approx 1$ km) at $R = 2$ km gives $\sigma_{\text{radial}} \sim \Delta P (a/R)^3 \approx 3\times10^6 \times 0.125 \approx 375$ kPa — agreement **within a factor of ~2**, acceptable given the simplified geometry.

---

## 4. Long-Term Signal: Inelastic Fracture Creation (outside the elastic framework)

The long-term decrease (−0.3 %/day for ~26 days; Hotovec-Ellis et al. caution the ~−8% cumulative may not combine linearly) ceased when the peripheral ring fault reached the surface, and is attributed to **inelastic fracture creation** — a mechanism outside the purely elastic acoustoelastic relation (Eq. 3). Using the GNSS shortening (~40 mm/day, $\epsilon \approx 20$ µstrain/day):

$$|\beta_{\text{long-term}}| = \frac{0.003}{2\times10^{-5}} \approx 150.$$

The lower effective $|\beta|$ (150 vs ~300 short-term) is physically meaningful: new-crack generation (velocity-decreasing) partially offsets elastic closure of existing cracks (velocity-increasing) — a signature of damage accumulation absent in the elastic short-term response.

---

## 5. Fracture Geometry as the Diagnostic

The dominant fracture orientation sets which strain component controls $\delta v/v$:
- **Parkfield:** fault-parallel cracks → respond to fault-normal contraction.
- **Kīlauea:** concentric ring fractures (Neal & Lockwood 2003) → respond to radial reservoir compression.
- **Piton de la Fournaise:** radial dike fractures (Carter et al. 2007) → *opposite* $\delta v/v$ sign under pressurization (Rivet et al. 2014).

Equation 4 captures all three through the directional projection $\hat{\mathbf{k}}\cdot\boldsymbol{\tau}^0\cdot\hat{\mathbf{k}}$ onto the fracture-normal, without separate physical models.

---

## 6. Summary

| Quantity | Value | P/D |
|---|---|---|
| $\beta_{\text{radial}}$ | 250–330 (use 300) | derived from two [P] |
| $\mu'$ | ~360 | derived (directional, order-of-mag) |
| Radial stress/collapse | ~167 kPa | derived |
| Spheroid cross-check | ~375 kPa (factor ~2) | derived |
| Isotropic $\delta v/v=\beta\epsilon_{kk}$ | **Fails** (volumetric predicts wrong sign) | — |
| Key physics | Ring-fracture radial closure (deviatoric) | — |

**Caveats.** Simplified spheroidal geometry (real piston + ring fault would modify the strain field); the directional bridge is order-of-magnitude; the −8% cumulative linearity is unresolved. This is the weakest of the three legs but the cleanest demonstration that **fracture fabric, not the volumetric trace, sets the sign of $\delta v/v$.**
