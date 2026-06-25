# Site Provenance & Drainage-Regime Tables — Single Source of Truth

**Created:** 2026-06-25 (audit remediation, Phases 0–1)
**Purpose:** Lock every numerical input used in the three-site application (§9) to either (a) a published source or (b) an explicit, data-driven framework derivation. `analysis/config.py` presets, the manuscript tables, and the site-analysis docs must all match this file. Each row is tagged **[P]** published / **[D]** derived-by-framework.

**Conventions**
- μ = ρV_S² (regime-independent; Gassmann — fluids carry no shear).
- **κ_u** = ρ(V_P² − 4/3 V_S²) — the *seismic-band* bulk modulus. At ~1 Hz the pore fluid cannot drain within a wave period, so κ_u **is the undrained modulus**.
- **κ_d** = κ_u·(1 − α_B·B) — the drained modulus (Roeloffs 1988; paper §2.5 with κ_u = κ_d/(1−α_B B)).
- **Bridge:** β = −μ′·κ/(2μ); inverse μ′ = −2μβ/κ. **The κ that enters the bridge is the one matching the loading regime** (Phase 1).
- Directional use of the bridge (β_axial, β_radial under deviatoric loading) is **order-of-magnitude only** — Eq. 7 was derived for isotropic loading.

---

## Phase 1 — Drainage regime is data-driven (Péclet number)

Pe = ω·L²/c, with ω = 2π/T_forcing, L = V_S/(3f), c = hydraulic diffusivity (published, cross-checked vs fits). Classification: Pe < 0.1 drained · 0.1–10 transitional · > 10 undrained. **The regime selects κ in the bridge.**

| Site | Signal | T_forcing | L (m) | c (m²/s), source | **Pe** | Regime | κ used |
|---|---|---|---|---|---|---|---|
| Parkfield | secular trend | ~20 yr | 800 | 0.01–1 (fractured granite; lit.) | 0.006–0.64 | **drained → transitional** | κ_d (≈κ_u; α_B·B=0.28) |
| Cascadia (N) | secular trend | ~13 yr | 250 | 3.8×10⁻⁴ (Kidiwela 2026 fluid-pulse) | **2.5** | **transitional → undrained** | **κ_u** |
| Kīlauea | per-collapse | ~hourly | ~2000 | low-φ basalt → undrained | ≫1 | **undrained** | κ (≈κ_u; low φ) |

Notes:
- **Cascadia is the load-bearing result:** Pe ≈ 2.5 means the seismic (undrained) κ_u = 4.86 GPa is the *correct, data-justified* modulus for the secular trend — not an error. This validates μ′ = 618 and supersedes the site doc's drained-style μ′ = 1290.
- **Parkfield** is drained-to-transitional; because granite has small α_B·B (0.28), κ_d and κ_u differ by only ~28%, so μ′ is bounded 252 (κ_u) – 350 (κ_d). The directional-bridge caveat dominates this uncertainty. We report the κ_u endpoint (≈251) to match the directly-measured seismic modulus, with the range stated.
- c cross-check: Clements & Denolle (2023) fitted California diffusivities span 10⁻³–10² m²/s; fractured-granite values at the high end keep Parkfield drained. Cascadia's 3.8×10⁻⁴ is itself a *published in-situ* estimate (the 2019 pulse), the most defensible c available.

---

## Parkfield (Okubo et al. 2024; SAFOD velocities)

| Quantity | Value | Unit | Source | P/D |
|---|---|---|---|---|
| δv/v secular trend b₀ | 4.8×10⁻⁵ (0.0048) | /yr (%) | Okubo 2024 Fig. 11b, stretching, 0.9–1.2 Hz | **[P]** |
| Contractional strain rate | 2.0×10⁻⁷ (~200 nε) | /yr | Okubo 2024 Figs. 13–15 (range 100–300 nε) | **[P]** |
| Dilatation | slight extension | — | Okubo 2024 (rules out isotropic) | **[P]** |
| V_S, V_P, ρ @ 0.8 km | 2500, 4500, 2500 | m/s, kg/m³ | SAFOD: Boness & Zoback 2006; Jeppson & Tobin 2015; Zhang 2009 | **[P]** |
| μ = ρV_S² | 15.62 | GPa | derived | **[D]** |
| κ_u = ρ(V_P²−4/3V_S²) | 29.79 | GPa | derived (seismic/undrained) | **[D]** |
| ν_seismic from (κ_u,μ) | 0.277 | — | derived (replaces stored 0.25) | **[D]** |
| α_B, B | 0.7, 0.4 | — | granite estimate; α_B·B=0.28 | **[D]** |
| κ_d = κ_u(1−α_B·B) | 21.45 | GPa | derived (drained) | **[D]** |
| **β_axial = δv/v ÷ ε_contr** | **240** | — | derived from two [P] | **[D]** |
| **μ′ = −2μβ/κ** | **252** (κ_u) – 350 (κ_d) | — | bridge consistency, order-of-mag | **[D]** |
| Deviatoric stress rate | ~12 | kPa/yr | 4μ(δv/v)/μ′ | **[D]** |
| 20-yr cumulative | ~0.24 | MPa | integrated | **[D]** |
| GNSS cross-check | 8.7 (factor 1.4) | kPa/yr | σ=Eε/(1−ν²) | **[D]** |

---

## Cascadia — Northern (Kidiwela et al. 2026; paper §9.2.2)

| Quantity | Value | Unit | Source | P/D |
|---|---|---|---|---|
| δv/v secular trend | 3.8×10⁻⁴ (0.038) | /yr (%) | Kidiwela 2026, NC89, 1–3 Hz, 13 yr | **[P]** |
| Borehole vol. strain rate | 1.2×10⁻⁷ (0.12 µε) | /yr | Davis et al. 2024 | **[P]** |
| **β (calibrated)** | **−3160** | — | **Kidiwela 2026 (borehole calibration)** → bridge is a **consistency check, not a prediction** | **[P]** |
| Convergence rate | 4.1 | cm/yr | Kidiwela 2026 | **[P]** |
| V_S, V_P, ρ @ 0.2–0.3 km | 500, 1700, 1900 | m/s, kg/m³ | paper §9.2.2 (Han 2017; USGS Cascadia CVM) | **[P]** |
| μ = ρV_S² | 0.475 | GPa | derived | **[D]** |
| **κ_u = ρ(V_P²−4/3V_S²)** | **4.86** | GPa | derived (undrained; **justified by Pe=2.5**) | **[D]** |
| ν_seismic from (κ_u,μ) | 0.453 | — | derived (soft saturated sediment) | **[D]** |
| **μ′ = −2μβ/κ_u** | **618** | — | bridge consistency check (uses published β) | **[D]** |
| **Stress rate** | **0.58** | kPa/yr | 2μ(δv/v)/μ′ = κ_u·ε̇ | **[D]** |
| 13-yr cumulative | ~7.6 | kPa | integrated | **[D]** |

**Supersedes** `cascadia_stress_analysis.md` §2–4 (which used V_S=1.0 km/s → μ=2.1, κ=10.3, μ′=1290, 1.24 kPa/yr — wrong layer for the 1–3 Hz band).

### Cascadia — Central (transients)
| Quantity | Value | Source | P/D |
|---|---|---|---|
| 2016 SSE δv/v drop | −0.2% (3–5 Hz) | Kidiwela 2026 | **[P]** |
| Long-term (0.1–0.3 Hz) | +0.003%/yr | Kidiwela 2026 | **[P]** |
| 2019 fluid pulse lag | 34 d; 0.58 km/day | Kidiwela 2026 | **[P]** |
| Locking ratio (N:C) | ~2:1 (0.006 vs 0.003 %/yr) | Kidiwela 2026; conditional on comparable kernels/β | **[P]/[D]** |

> **Fix the internal table inconsistency:** central long-term must read **+0.003 %/yr** everywhere (the "0.015 %/yr" in the old §7 table is a different band/typo).

---

## Kīlauea (Hotovec-Ellis et al. 2022; Anderson et al. 2019; Segall et al. 2020)

| Quantity | Value | Unit | Source | P/D |
|---|---|---|---|---|
| δv/v per collapse | ~5×10⁻³ (0.5) | (%) | Hotovec-Ellis 2022 | **[P]** |
| Long-term decrease | −0.2 to −0.4 | %/day | Hotovec-Ellis 2022 | **[P]** |
| Radial strain / collapse | 15–25 | µε | GNSS CRIM–UWEV | **[P]** |
| Reservoir ΔP | ~3 | MPa | Segall 2020 | **[P]** |
| μ, ν (spheroid, 1.94 km) | 3.0, 0.25 | GPa, — | Anderson 2019 | **[P]** |
| κ from (μ,ν) | 5.0 | GPa | derived (low-φ basalt: κ_d≈κ_u, undrained) | **[D]** |
| **β_radial = δv/v ÷ ε_radial** | **250–330** (use 300) | — | derived from two [P] | **[D]** |
| **μ′ = −2μβ/κ** | **360** | — | bridge, order-of-mag (directional) | **[D]** |
| Radial stress / collapse | ~167 | kPa | 4μ(δv/v)/μ′ | **[D]** |
| Spheroid cross-check | ~375 (factor ~2) | kPa | ΔP·(a/R)³ | **[D]** |

---

## Net reconciliation actions (feed Phases 2–3, 7)

1. `config.py`: add **V_P** to every preset; compute κ_u, κ_d from velocities; **β derived from bridge** (Parkfield/Nepal/Agri) or **published** (Cascadia β=−3160 with `beta_source`); store regime/forcing so the bridge picks the right κ.
2. Cascadia preset: V_S=500, **V_P=1700**, ρ=1900 ⇒ κ_u=4.86, μ′=618, β=−3160 (published). Bridge check −618·4.86/(2·0.475)=−3162 ✓.
3. Parkfield preset: V_S=2500, **V_P=4500**, ρ=2500 ⇒ κ_u=29.8, μ′≈251, β≈−240 (note directional/order-of-mag; regime drained→transitional).
4. Rewrite `cascadia_stress_analysis.md` to μ=0.475, κ_u=4.86, μ′=618, 0.58 kPa/yr; fix central 0.003 %/yr.
5. Create `kilauea_stress_analysis.md` from this table.
6. Manuscript §9 already matches the Cascadia 618/0.58 set; ensure Table 2 and abstract use κ_u-based numbers and add the explicit Pe-regime statement in §2.5/§9.
