# Quantitative Cascadia Stress Analysis: Applying the Unified Framework to Subduction Zone Monitoring

This analysis parallels the Parkfield stress analysis but applies the unified $\delta v/v$ framework to the Cascadia subduction zone using published results from Kidiwela et al. (2026, *Science Advances*).

---

## 1. Key Numbers from Kidiwela et al. (2026)

**Northern Cascadia (NC89, Clayoquot Canyon):** $\delta v/v$ trend = **+0.038%/yr** (1–3 Hz, 13 years). Borehole volumetric strain = 0.12 $\mu$strain/yr (Davis et al., 2024). Calibrated $\beta = 3160$. Convergence rate = 4.1 cm/yr. Setting: fully locked megathrust.

**Central Cascadia (HYSB1/HYS14):** 2016 slow slip $\delta v/v$ drop = **−0.2%** (3–5 Hz). Long-term $\delta v/v$ (0.1–0.3 Hz) = +0.003%/yr (half of northern). 2019 fluid pulse with 34-day horizontal lag at 0.58 km/day. Locking ratio ~50%.

**Depth sensitivity (Table S2):** 5 Hz → 0.03 km, 3 Hz → 0.1 km, 1 Hz → 0.2 km, 0.5 Hz → 0.5 km, 0.3 Hz → 1 km, 0.1 Hz → 8 km.

---

## 2. Bridge Relation: $\beta = 3160$ and What It Means

> **Grounding note (2026-06-25 reconciliation).** $\beta = 3160$ is **published** — it is the borehole-calibrated value of Kidiwela et al. (2026). The bridge relation is therefore used here as a **consistency check** (does the implied $\mu'$ come out physically plausible?), *not* as an independent prediction. All numbers below match `docs/site_analyses/provenance_tables.md` and the manuscript §9.2. An earlier draft of this section used a stiffer/deeper velocity layer ($V_S\approx1.0$ km/s, $\mu=2.1$, $\kappa=10.3$ GPa, $\mu'\approx1290$, 1.24 kPa/yr); that layer is **not** the one sampled by the 1–3 Hz band and is superseded.

At the 1–3 Hz sensitivity depth (~0.2–0.3 km below seafloor), the published velocity model (paper §9.2.2; Han et al. 2017; USGS Cascadia CVM) gives $V_S \approx 0.5$ km/s, $V_P \approx 1.7$ km/s, $\rho \approx 1900$ kg/m³, so

- $\mu = \rho V_S^2 = 0.475$ GPa,
- $\kappa_u = \rho(V_P^2 - \tfrac{4}{3}V_S^2) = 4.86$ GPa (seismic-band = **undrained** modulus; implied $\nu \approx 0.45$, consistent with soft saturated sediment).

**Why the undrained modulus is the correct one here (data-driven).** For the secular trend (forcing time ~13 yr), the Péclet number is $Pe = \omega L^2/c \approx 2.5$ using $L\approx250$ m and the *published in-situ* diffusivity $c\approx3.8\times10^{-4}$ m²/s (Kidiwela et al. 2026, 2019 fluid pulse). $Pe\gtrsim1$ places the secular signal in the **transitional-to-undrained** regime, so $\kappa_u$ — not the drained $\kappa_d = \kappa_u(1-\alpha_B B)\approx1.4$ GPa — is the modulus that enters the bridge.

The consistency check (inverse bridge $\mu' = -2\mu\beta/\kappa_u$):

$$\mu' = \frac{2 \times 0.475 \times 3160}{4.86} \approx 618.$$

This $\mu'\approx620$ is physically plausible for high-porosity, weakly cemented marine sediment where grain-contact mechanics (Dvorkin & Nur 1996) dominate — confirming the published $\beta$ is internally consistent with the framework.

---

## 3. Stress at Depth: Northern Cascadia

**Volumetric strain rate:** $\dot{\epsilon}_{kk} = (\delta v/v)/\beta = 0.00038/3160 = 1.2 \times 10^{-7}$/yr = 0.12 $\mu$strain/yr (matches the borehole — by construction, since $\beta$ was borehole-calibrated).

**Compressive pressure rate:** $\dot{p} = \kappa_u \cdot \dot{\epsilon}_{kk} = 4.86 \times 10^9 \times 1.2 \times 10^{-7}$ = **0.58 kPa/yr** at ~0.2 km depth (equivalently $2\mu(\delta v/v)/\mu'$). Over 13 years: **~7.6 kPa cumulative**.

**Cross-check:** Geodetic convergence → $\dot{\epsilon} = 0.41$ $\mu$strain/yr → corrected for Poisson's ratio: $(1-2\nu)\dot{\epsilon} \approx 0.04$ $\mu$strain/yr. The borehole and $\delta v/v$ agree by construction (shared calibration); the useful result is the physically plausible inferred $\mu'$, not an independent stress validation.

---

## 4. Stress from Slow Slip and Fluid Pulses: Central Cascadia

**2016 slow slip stress drop:** $\Delta\epsilon = 0.002/\beta$. Using $\beta = 3160$: $\epsilon = 0.63$ $\mu$strain → $\Delta\sigma = 6.5$ kPa. Using $\beta = 1000$: $\epsilon = 2$ $\mu$strain → $\Delta\sigma = 21$ kPa. **Range: 7–21 kPa** — consistent with global slow slip stress drops.

**Slip:** $D_{\max} = 4(1-\nu)a\epsilon$ = 0.4–1 cm for $a = 3$ km, $\nu = 0.5$. Consistent with Nankai and Hikurangi.

**2019 fluid pulse pore pressure:** Using $\delta V_S/V_S = -\mu' u^0/(2\mu)$ with $\delta v/v \approx -0.1$ to $-0.2\%$ and the grounded moduli ($\mu = 0.475$ GPa, $\mu' = 618$): $u^0 = 2\mu|\delta v/v|/\mu' \approx$ **1.5–3 kPa**. The soft sediments ($\mu' \approx 620$) amplify the velocity sensitivity, making this small perturbation ($\sim10^{-4}$ of background) seismically detectable.

**Locking ratio from $\delta v/v$ contrast:** (0.1–0.3 Hz) North: 0.006%/yr, Central: 0.003%/yr. Ratio = **2:1** — consistent with the geodetic locking contrast under comparable-kernel and comparable-material-sensitivity assumptions.

---

## 5. Direction of Stress

The Cascadia analysis cannot yet determine stress azimuth as directly as Parkfield because only 2–3 seafloor stations exist. However, the **cross-component analysis (ZE vs. ZN vs. NE)** provides a potential path: if ZN (sensitive to N–S propagating waves, ~25° from convergence direction) shows a larger $\delta v/v$ trend than ZE (sensitive to E–W waves, ~65° from convergence), this would indicate deviatoric loading aligned with the convergence direction.

At northern Cascadia, the loading is expected to be approximately **isotropic** (volumetric compaction) because the wedge compacts uniformly under horizontal contraction. At central Cascadia, deviatoric effects may be more significant near the protothrusts.

---

## 6. Multi-Frequency Depth Resolution in Action

The 2019 fluid pulse at central Cascadia demonstrates the depth-resolved framework: the signal appears *first* at low frequencies (deep) and *later* at high frequencies (shallow), with lag times quantifying **upward fluid migration at 2.5–9 m/day**. This is the first direct observation of the depth-tomographic concept proposed in §7.3 of our paper — multi-frequency $\delta v/v$ literally images fluid migration in 4-D.

---

## 7. Parkfield vs. Cascadia Comparison

| | Parkfield | N. Cascadia | C. Cascadia |
|---|---|---|---|
| Material | Fractured granite | Marine sediments | Sediments + protothrusts |
| $\beta$ | ~240 (derived) | **−3160 (published)** | −3160 (published) |
| $\mu'$ | ~251 | **~618** | ~618 |
| $\delta v/v$ rate | +0.005%/yr | +0.038%/yr | +0.003%/yr (0.1–0.3 Hz) |
| Stress rate | ~12 kPa/yr (deviatoric) | **~0.58 kPa/yr (volumetric)** | ~0.3 kPa/yr |
| Isotropic $\delta v/v = \beta\epsilon_{kk}$ | **Fails** | **Works** | Works (long-term) |
| Key physics | Crack closure (deviatoric) | Wedge compaction (isotropic) | Pore pressure (poroelastic) |

> Numbers reconciled to `provenance_tables.md` (2026-06-25): $\mu'=618$, stress 0.58 kPa/yr (was 1290 / 1.24 kPa/yr in an earlier draft using the wrong velocity layer); central long-term rate is +0.003%/yr at 0.1–0.3 Hz.

**The two sites validate complementary branches of the unified framework.** Parkfield needs the deviatoric/anisotropic formulation (Eq. 4); Cascadia works with the isotropic/volumetric formulation (Eq. 3) for the long-term signal but needs the poroelastic extension (Eq. 5) for the fluid transients. Together, they exercise the full theoretical machinery.
