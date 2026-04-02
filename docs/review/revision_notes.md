# Paper Revision Notes — Derivation Verification, Notation, and Expanded Content

## Document purpose
This file tracks all revisions to `paper_dvv_unified_framework.md` stemming from the geophysics-derivations skill review. It specifies exact text that should be inserted, replaced, or added.

---

## 1. Notation Homogenization

### 1.1 The measured quantity: $\delta v / v$

**Convention adopted throughout the paper:**

| Symbol | Meaning |
|--------|---------|
| $\delta v / v$ | The measured relative velocity change from coda-wave interferometry (CWI) or stretching. This is the *observable*. |
| $\delta V_S / V_S$ | Relative change in shear-wave velocity at a specific depth $z$. This is the *inferred local quantity*. |
| $\delta c / c$ | Relative change in surface-wave phase velocity at frequency $f$. Intermediate quantity linking $\delta V_S/V_S$ to $\delta v/v$. |

**Rationale and key reference:**

Snieder (2002, *Phys. Rev. E*) showed that after multiple scattering and P-to-S mode conversions reach equipartition, the CWI velocity change $\delta v/v$ is dominated by $\delta V_S/V_S$. Specifically, for a Poisson solid ($V_P/V_S = \sqrt{3}$), the S-wave contribution to the measured $\delta v/v$ is approximately 90% of the total (Snieder, 2002, Eqs. 19–20). Singh et al. (2019, *JGR*) extended this, showing the CWI measurement $[\Delta V/V]_{\text{CWI}}$ varies along the coda as a weighted sum of $\Delta V_P/V_P$ and $\Delta V_S/V_S$, with the S-wave weight $q(t, \gamma) \to 1$ at late coda times.

When surface waves dominate the ambient noise wavefield — as is typical for inter-station cross-correlations at periods > 1 s — the measured $\delta v / v$ corresponds to a phase-velocity change $\delta c / c$ (Ermert et al., 2023; Fokker et al., 2021). This phase-velocity change is related to the depth profile of $\delta V_S / V_S$ through the sensitivity kernel:

$$
\frac{\delta v}{v}(f, t) \approx \frac{\delta c}{c}(f, t) = \frac{1}{c(f)} \int_0^\infty \frac{\partial c}{\partial V_S}(z, f) \, \delta V_S(z, t) \, dz
\tag{R1}
$$

This is the forward model of Fokker et al. (2021, Eq. 13) and Ermert et al. (2023, their surface-wave dispersion modeling). Throughout this paper, we use $\delta v / v$ for the measured quantity and $\delta V_S / V_S$ for the depth-dependent shear-wave velocity change inferred from physical models.

### 1.2 Search-and-replace instructions

All occurrences of `dv/v` in prose → `$\delta v/v$`
All occurrences of `dβ/β` (from Fokker/Tromp notation) → `$\delta V_S / V_S$` when referring to local S-wave change
Keep `$\delta c/c$` when specifically discussing phase-velocity change
The Fokker et al. (2021) equations use $\beta$ for S-wave velocity; clarify that their $d\beta/\beta$ is our $\delta V_S/V_S$.

---

## 2. Derivation Verification

### 2.1 Acoustoelastic relation (Eq. 2 of paper)

**Starting point:** Ostrovsky & Johnson (2001, Eq. 5), 1-D nonlinear stress–strain:

$$
\sigma = M\left(\epsilon + \beta \epsilon^2 + \delta \epsilon^3 + \ldots\right)
$$

where $M = \lambda + 2\mu$ for P-waves. The local velocity is $v = \sqrt{\rho^{-1} d\sigma/d\epsilon}$, so:

$$
v = v_0 \sqrt{1 + 2\beta\epsilon + 3\delta\epsilon^2 + \ldots} \approx v_0(1 + \beta\epsilon + \ldots)
$$

giving $\delta v / v \approx \beta \epsilon_{kk}$ for volumetric strain $\epsilon_{kk}$ under hydrostatic conditions.

**Verification of $\beta$:** From Clements & Denolle (2023, Eq. 2):

$$
\beta = \frac{3}{2} + \frac{l + 2m}{\lambda + 2\mu}
$$

This follows from Hughes & Kelly (1953) who derived the velocity under uniaxial stress using Murnaghan's (1937) third-order constants. The factor 3/2 arises from the geometric (Eulerian vs. Lagrangian) strain correction. ✓ Verified.

**Dimensional check:** $\beta$ is dimensionless (ratio of TOE to second-order constants). $\epsilon_{kk}$ is dimensionless. $\delta v/v$ is dimensionless. ✓

### 2.2 Berger thermoelastic stress (Eq. 8 of paper)

Starting from Berger (1975) and the plane-strain thermoelastic problem with periodic surface temperature $T_0 e^{i\omega t}$:

$$
\sigma = \frac{\alpha E \, T_0}{1 - \nu}\left[-2 e^{-(1+i)\gamma z} + (1+\nu)\frac{(1-i)k}{\gamma}e^{-kz}\right]
$$

**Term 1** decays with $\gamma = \sqrt{\omega/(2\kappa_T)}$ — the thermal skin depth. This is the *direct thermal stress* from thermal expansion of the constrained medium.

**Term 2** decays with $k = 2\pi/L$ — the horizontal wavenumber. This is the *flexural/equilibrium* response needed to satisfy the free-surface boundary condition. It penetrates much deeper than the thermal skin depth.

**Approximation:** $k \ll \gamma$ (horizontal wavelength $\gg$ thermal skin depth). For annual variations with $L \sim 10$ km: $k \approx 6 \times 10^{-4}$ m$^{-1}$, $\gamma \approx 0.5$ m$^{-1}$. Ratio $k/\gamma \approx 10^{-3}$. ✓ Approximation excellent.

**Phase analysis:** Term 1 has the same phase as the subsurface temperature (i.e., follows temperature with depth-dependent lag). Term 2 has a constant phase delay of $-5\pi/4$ relative to surface temperature (Richter et al., 2014, Fig. 9). ✓ Verified.

### 2.3 Tromp & Trampert induced-stress equation (Eq. 3 of paper)

From Tromp & Trampert (2018, Eq. 38 simplified):

$$
\frac{\delta V_S}{V_S} = \frac{\mu' p^0}{2\mu} + \frac{1-\mu'}{4\mu}\hat{\mathbf{k}}\cdot\boldsymbol{\tau}^0\cdot\hat{\mathbf{k}} - \frac{1+\mu'}{4\mu}\hat{\mathbf{a}}\cdot\boldsymbol{\tau}^0\cdot\hat{\mathbf{a}}
$$

**Physical interpretation of each term:**

1. $\mu' p^0 / (2\mu)$: Isotropic velocity change from induced pressure. Positive $p^0$ (compression) increases velocity if $\mu' > 0$ (true for all natural materials).

2. $(1-\mu')/(4\mu) \, \hat{\mathbf{k}}\cdot\boldsymbol{\tau}^0\cdot\hat{\mathbf{k}}$: Propagation-direction dependence. For $\mu' \gg 1$ (typical: 50–200), this term is negative and large, meaning waves propagating along the maximum compressive deviatoric stress direction experience a velocity *decrease* from this term alone.

3. $-(1+\mu')/(4\mu) \, \hat{\mathbf{a}}\cdot\boldsymbol{\tau}^0\cdot\hat{\mathbf{a}}$: Polarization-direction dependence. For $\mu' \gg 1$, this is large and negative, meaning waves polarized along the maximum compressive deviatoric stress direction experience a velocity *increase* (because $\hat{\mathbf{a}}\cdot\boldsymbol{\tau}^0\cdot\hat{\mathbf{a}}$ picks up the compressive stress).

**Key insight:** For $\mu' \gg 1$, the first (isotropic) term dominates. The anisotropic terms 2 and 3 produce SV–SH splitting proportional to $T_{33}^0 / \mu$. ✓ Verified against Fokker et al. (2021, Eqs. 3–4).

### 2.4 Fokker poroelastic decomposition (Eq. 4 of paper)

For uniaxial vertical load $T_{33}^0$ and induced pore pressure $u^0$, the effective stress tensor is:

$$
\tilde{T}^0 = \begin{pmatrix} u^0 & 0 & 0 \\ 0 & u^0 & 0 \\ 0 & 0 & u^0 + T_{33}^0 \end{pmatrix}
$$

Effective pressure: $\tilde{p}^0 = -(u^0 + T_{33}^0/3)$

Effective deviatoric stress: $\tilde{\tau}^0 = -(T_{33}^0/3)\,\text{diag}(1, 1, -2)$

Substituting into Tromp & Trampert (Eq. 3) with specific wave orientations:

**Vertically propagating SV** ($\hat{\mathbf{k}} = \hat{\mathbf{z}}$, $\hat{\mathbf{a}} = \hat{\mathbf{x}}$):

$$
\frac{\delta V_S}{V_S} = -\frac{\mu'}{2\mu}u^0 - \frac{\mu'+1}{4\mu}T_{33}^0
$$

**Vertically propagating SH** ($\hat{\mathbf{k}} = \hat{\mathbf{z}}$, $\hat{\mathbf{a}} = \hat{\mathbf{y}}$): Same as SV (by symmetry).

**Horizontally propagating SV** ($\hat{\mathbf{k}} = \hat{\mathbf{x}}$, $\hat{\mathbf{a}} = \hat{\mathbf{z}}$):

$$
\frac{\delta V_S}{V_S} = -\frac{\mu'}{2\mu}u^0 - \frac{\mu'-1}{4\mu}T_{33}^0
$$

This gives Fokker et al. (2021) Eqs. 9–11. The $\mp$ notation in Eq. 4 of the paper refers to these two cases. ✓ Verified.

---

## 3. Alternative Hypotheses for Interpreting $\delta v/v$

### NEW SECTION 2.5: Alternative Mechanisms

Beyond the nonlinear-elastic framework developed in Sections 2.1–2.4, several alternative or complementary mechanisms can produce temporal changes in seismic velocity:

**3.1 Density changes.** Fokker et al. (2021) note that effective pressure changes can also modify density through compaction: $\delta V_S/V_S = -\frac{1}{2}\delta\rho/\rho$. For the Groningen setting ($\kappa \sim 5$ GPa), this mechanism is 2–3 orders of magnitude smaller than the shear-modulus mechanism and can be neglected. However, in very soft sediments or during rapid loading (e.g., liquefaction), density changes may become significant.

**3.2 Fluid substitution.** Changes in pore-fluid composition (e.g., gas–water replacement during CO$_2$ injection or volcanic degassing) directly modify the bulk modulus through Gassmann's equation, and hence $V_P$. This mechanism is distinct from the effective-stress mechanism and primarily affects P-wave velocities rather than S-wave velocities (which are insensitive to pore-fluid bulk modulus in Gassmann theory). Zhu et al. (2019, *PNAS*) detected CO$_2$ plume migration using coda-wave $\delta v/v$.

**3.3 Mineral alteration and cementation.** Chemical changes — hydration, dissolution, precipitation, bio-cementation — permanently modify the elastic frame. These processes operate on longer timescales (months to years) and are irreversible, unlike the elastic mechanisms. Rodríguez Tribaldos & Ajo-Franklin (2021) observed mineral hydration effects on $\delta v/v$ at a geothermal site.

**3.4 Temperature effects on the elastic moduli.** Beyond the thermoelastic *stress* mechanism (Section 3), temperature also directly modifies the elastic moduli of the solid frame. This is a first-order effect that is usually small for crystalline rocks ($\sim$0.01%/K for $V_S$) but can be significant in ice, permafrost, or near phase transitions (freezing/thawing). James et al. (2017) observed $>$10% velocity changes during permafrost thaw.

**3.5 Scatterer relocation.** Snieder (2006) showed that CWI also responds to changes in scatterer positions (not just velocity). In volcanic settings, the opening of new fractures or the migration of fluids can relocate scatterers, producing apparent $\delta v/v$ that reflects structural change rather than bulk velocity change. Obermann et al. (2013, *JGR*) developed a theory separating scatterer-change from velocity-change contributions.

**3.6 Source-side effects.** Changes in the ambient noise wavefield — seasonal ocean-wave spectra, anthropogenic noise patterns, wind — can produce spurious $\delta v/v$ if not properly handled. Zhan et al. (2013, *GJI*) showed that temporal variations in noise frequency content can cause spurious velocity changes. Okubo et al. (2024) mitigate this through multi-component channel-weighting.

---

## 4. Geological and Material Controls on Higher-Order Elastic Parameters

### NEW SECTION 5.2: What Controls $\beta$, $\mu'$, and $\partial(\rho v^2)/\partial\sigma_c$?

The nonlinear elastic parameters that govern $\delta v/v$ sensitivity are not fundamental material constants — they depend on the *microstructure* of the rock:

**4.1 Compliant porosity and microcracks.**
The dominant source of nonlinearity in natural rocks is compliant porosity: thin, crack-like voids with high aspect ratios (Shapiro, 2003; Walsh, 1965). These features close under compression, stiffening the rock. The key parameters are:

- *Crack density* $\epsilon_c = N \langle a^3 \rangle / V$: number density times cube of crack radius. Hudson (1981) showed that $V_S$ decreases linearly with $\epsilon_c$. Typical values: 0.01–0.15.
- *Aspect ratio* $\xi = w/a$ (aperture/radius): governs the pressure at which cracks close. Thin cracks ($\xi \sim 10^{-3}$) close at low pressures ($\sim$10 MPa), making shallow rocks highly nonlinear. Stiff cracks ($\xi \sim 10^{-1}$) close at higher pressures.
- *Crack orientation distribution*: random orientations produce isotropic nonlinearity; preferential alignment (from tectonic stress, bedding, or foliation) produces anisotropic nonlinearity (Sayers & Kachanov, 1995).

**Implication:** $|\beta|$ and $\mu'$ *decrease with confining pressure* as cracks close, explaining why $\delta v/v$ sensitivity is strongest in the shallowest layers. This is captured by the depth profile of $\mu'(z)$ in Fokker et al. (2021, Fig. 2g): $\mu' > 50$ for unconsolidated sediments but $\mu' < 10$ for deep consolidated rock.

**4.2 Grain contacts and cementation.**
In unconsolidated granular media, elastic moduli depend on contact mechanics (Hertz-Mindlin theory). The effective shear modulus scales as $\mu_{\text{eff}} \propto P_e^{1/3}$ (for Hertzian contacts) or $\mu_{\text{eff}} \propto P_e^{1/2}$ (for cemented contacts; Dvorkin & Nur, 1996). This produces $\mu' = d\ln\mu/d\ln P \sim 1/3$ to $1/2$ for the exponent, but $\mu' = d\mu/dP \sim \mu/P$ for the dimensional derivative, which is very large at low confining pressures.

**Implication:** Near-surface soils and sediments have $\mu' \gg 100$ (Fokker et al., 2021), making them extremely sensitive to stress changes — this is why seasonal $\delta v/v$ is typically $>$0.1% in unconsolidated media but $<$0.01% in crystalline rock.

**4.3 Mineralogy and fabric.**
- *Clay content*: increases compliance and $|\beta|$
- *Cementation type*: calcite cement is more compliant than quartz cement
- *Salt cementation*: produces anomalously high $\partial(\rho v^2)/\partial\sigma_c \sim 1000$ at PATCX (Richter et al., 2014) because salt bridges between grains are stress-sensitive
- *Foliation and bedding*: creates intrinsic anisotropy that interacts with stress-induced anisotropy

**4.4 Fluid saturation state.**
- *Fully saturated*: Gassmann theory applies; $V_S$ insensitive to fluid type but sensitive to effective stress
- *Partially saturated*: capillary suction stiffens the frame (Shi et al., 2026); $|\beta|$ can increase by factors of 2–5
- *Gas-bearing*: dramatic $V_P$ reduction from even small gas saturations (patchy saturation effects)

---

## 5. Spatial Generalization: From 1-D to 3-D

### NEW SECTION 8.3 (replaces part of existing §8): Spatial Heterogeneity and 3-D Effects

The forward models in Sections 3–6 assume laterally homogeneous (1-D) structure. Generalizing to 3-D requires accounting for:

**5.1 Spatially varying velocity structure.**
The sensitivity kernel $K(z, f)$ in Eq. R1 depends on the local $V_S(z)$, $V_P(z)$, and $\rho(z)$ profiles. At sites with laterally varying geology (basins, fault zones, volcanic edifices), the kernel differs between station pairs. Ermert et al. (2023) addressed this by computing station-specific 1-D profiles at each site in Mexico City, using geotechnical classifications (hard, intermediate, soft sites) and aquitard thickness information. A fully 3-D treatment would require:

- *3-D velocity model*: from ambient noise tomography or active-source surveys
- *3-D sensitivity kernels*: computed with adjoint methods or finite-difference simulations (Tromp et al., 2005)
- *Inter-station averaging*: since $\delta v/v$ from cross-correlations samples the volume *between* stations, the effective kernel is a spatial average that depends on station geometry and scattering properties

**5.2 Spatially varying material properties.**
The nonlinear parameters ($\beta$, $\mu'$, $\kappa_T$, $c$) also vary laterally. In a sedimentary basin:
- $\mu'$ is large in the basin fill and small in the basement
- $\kappa_T$ differs between saturated sediments and dry rock
- $c$ (hydraulic diffusivity) can vary by orders of magnitude across fault zones and clay layers

**Consequence:** the same rainfall event produces different $\delta v/v$ at different stations, not just because of different precipitation, but because the subsurface response *amplifies or attenuates* the signal differently. Clements & Denolle (2023) demonstrated this heterogeneity across California: basin sites show low diffusivity (long memory) while mountain sites show high diffusivity (rapid response).

**5.3 What additional observations would we need?**

To generalize from 1-D to 3-D, we need:

1. **3-D $V_S$ model**: From ambient noise tomography at the same frequencies used for $\delta v/v$ monitoring. This provides the base model for computing sensitivity kernels. Dense arrays (e.g., nodal deployments, DAS) can provide resolution at the scale of inter-station spacing.

2. **$V_P/V_S$ ratio**: From joint inversion of Rayleigh and Love waves, or from P-wave extraction. This constrains Poisson's ratio, which enters the thermoelastic stress model (Eq. 8) and the Fokker framework (Eqs. 3–4).

3. **Density model**: From gravity surveys or empirical $V_S$–$\rho$ relations (Gardner et al., 1974). Needed for converting $\delta V_S/V_S$ to $\delta\mu/\mu$ and for computing sensitivity kernels.

4. **Near-surface geotechnical data**: $V_{S30}$, water table depth, soil type, porosity. These constrain $\mu'$, $\kappa_T$, $c$, and saturation state at each site.

5. **Geodetic coverage**: Co-located GNSS for surface strain, InSAR for spatially continuous deformation. These provide the independent stress/strain constraint needed for joint inversion.

6. **Meteorological and hydrological data**: Distributed temperature, precipitation, soil moisture, and groundwater level measurements co-located with the seismic array.

---

## 6. Additional References (15 OA papers)

These should be added to the bibliography and cited in the relevant sections:

1. Yuan, C., Bryan, J., & Denolle, M. A. (2021). Numerical comparison of time-, frequency- and wavelet-domain methods for coda wave interferometry. *GJI*, 226, 828–846. [OA] — Comparison of CWI methods; shows surface waves dominate single-station sensitivity.

2. Obermann, A., Planès, T., Larose, E., & Campillo, M. (2013). Imaging preeruptive and coeruptive structural and mechanical changes of a volcano with ambient seismic noise. *JGR*, 118, 6285–6294. [OA] — Separating scatterer-change from velocity-change.

3. Obermann, A., et al. (2014). Depth sensitivity of seismic coda waves to velocity perturbations in an elastic heterogeneous medium. *GJI*, 194, 372–382. [OA] — Depth sensitivity kernels for scattered waves.

4. Singh, J., Curtis, A., Zhao, Y., Cartwright-Taylor, A., & Main, I. (2019). Coda wave interferometry for accurate simultaneous monitoring of velocity and acoustic source location. *JGR Solid Earth*, 124, 5629–5655. [OA] — Shows CWI measures weighted sum of δVP/VP and δVS/VS.

5. Illien, L., Sens-Schönfelder, C., Andermann, C., Marc, O., Hosseiny, B., & Hovius, N. (2022). Seismic velocity recovery in the subsurface: Transient damage and groundwater drainage following the 2015 Gorkha earthquake, Nepal. *JGR Solid Earth*, 127, e2021JB023402. [OA] — Joint damage and hydrological modeling.

6. Gassenmeier, M., Sens-Schönfelder, C., Eulenfeld, T., Bartsch, M., Victor, P., Tilmann, F., & Korn, M. (2016). Field observations of seismic velocity changes caused by shaking-induced damage and healing due to mesoscopic nonlinearity. *GJI*, 204, 1490–1502. [OA] — Mesoscopic nonlinearity in the field.

7. Hobiger, M., Wegler, U., Shiomi, K., & Nakahara, H. (2016). Coseismic and postseismic velocity changes detected by passive image interferometry. *GJI*, 205, 1053–1073. [OA] — Multi-earthquake healing study, Japan.

8. Hillers, G., Ben-Zion, Y., Campillo, M., & Zigone, D. (2015). Seasonal variations of seismic velocities in the San Jacinto fault area. *GJI*, 202, 920–932. [OA] — Thermoelastic dominance in arid setting.

9. Mao, S., Campillo, M., van der Hilst, R. D., Brenguier, F., Stehly, L., & Hillers, G. (2019). High temporal resolution monitoring of small variations in crustal strain by dense seismic arrays. *GRL*, 46, 128–137. [OA] — Dense array strain monitoring.

10. Donaldson, C., Winder, T., Caudron, C., & White, R. S. (2019). Crustal seismic velocity responds to a magmatic intrusion and seasonal loading in Iceland. *Science Advances*, 5, eaax6642. [OA] — Volcanic + seasonal loading competition.

11. Zhan, Z., Tsai, V. C., & Clayton, R. W. (2013). Spurious velocity changes caused by temporal variations in ambient noise frequency content. *GJI*, 194, 1552–1559. [OA] — Source-side artifact analysis.

12. Rodríguez Tribaldos, V., & Ajo-Franklin, J. B. (2021). Aquifer monitoring using ambient seismic noise recorded with distributed acoustic sensing (DAS) deployed on dark fiber. *JGR Solid Earth*, 126, e2020JB021004. [OA] — DAS for groundwater monitoring.

13. Marc, O., Sens-Schönfelder, C., Illien, L., et al. (2021). Toward using seismic interferometry to quantify landscape-scale erosion rates. *JGR Earth Surface*, 126, e2021JF006112. [OA] — Geomorphological application of δv/v.

14. Feng, K.-F., Huang, H.-H., Hsu, Y.-J., & Wu, Y.-M. (2021). Controls on seasonal variations of crustal seismic velocity in Taiwan. *JGR Solid Earth*, 126, e2021JB022650. [OA] — Joint thermoelastic + hydrological inversion.

15. D'Auria, L., et al. (2023). Spatio-temporal velocity variations during La Palma 2021 eruption. *Scientific Reports*, 13, 12203. [OA] — Pre-eruptive velocity detection.

16. Snieder, R. (2006). The theory of coda wave interferometry. *Pure and Applied Geophysics*, 163, 455–473. — Foundational CWI theory, S-wave dominance.

17. Snieder, R. (2002). Coda wave interferometry and the equilibration of energy in elastic media. *Phys. Rev. E*, 66, 046615. [OA] — P-to-S equipartition; establishes that CWI ≈ δVS/VS.

18. Zhu, T., Ajo-Franklin, J., Daley, T. M., & Marone, C. (2019). Dynamics of geologic CO2 storage and plume motion revealed by seismic coda waves. *PNAS*, 116, 2464–2469. [OA] — Fluid substitution application.

---

## 7. Summary of Required Changes to Paper Markdown

### Section 2.1 (Notation)
Insert new subsection "2.0 Notation and the $\delta v/v$ Observable" before §2.1, defining the three quantities ($\delta v/v$, $\delta V_S/V_S$, $\delta c/c$), citing Snieder (2002, 2006), Singh et al. (2019), and explaining that CWI is dominated by S-waves.

### Section 2.5 (NEW)
Insert "Alternative and Complementary Mechanisms" covering density changes, fluid substitution, mineral alteration, direct temperature effects, scatterer relocation, and source-side effects.

### Section 5.2 (NEW)
Insert "Geological and Material Controls on Nonlinear Parameters" covering compliant porosity, grain contacts, mineralogy, and saturation state.

### Section 8.3 (EXPANDED)
Replace simple spatial discussion with detailed treatment of 3-D generalization, including spatially varying velocity, material properties, and the six categories of additional observations needed.

### Throughout
Replace all `dv/v` with `$\delta v/v$`, all `dβ/β` with `$\delta V_S/V_S$` (when referring to local S-wave change), add 18 new references to bibliography.
