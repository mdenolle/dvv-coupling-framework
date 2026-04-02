# Theoretical Reflection: Integrating Coupling Mechanisms into the Unified δv/v Framework

**Working document for manuscript revision — Marine Denolle & Claude**

---

## 1. The Pedagogical Gap in the Current Manuscript

The unified framework manuscript (Sections 2–9) rests on a foundational assumption that is stated but never critically examined: **linear superposition of contributions to δv/v**. Equation 6 writes:

$$\frac{\delta v}{v}(t) = s_T \cdot T(t - t_{\text{shift}}) + p_1 \cdot \Delta\text{GWL}(t) + \sum_i s_i L_i(t) + b_0 t + a_0$$

This additive decomposition implicitly assumes that the coefficients ($s_T$, $p_1$, $s_i$, $b_0$) are **constants** — that the medium's sensitivity to one forcing is independent of its state under all other forcings. The three-site application (Section 9) successfully uses this assumption at Parkfield, Cascadia, and Kīlauea. The question the revised paper must answer is: **under what conditions does this assumption break down, and what replaces it?**

The coupling analysis identifies three first-order mechanisms and two second-order mechanisms where the coefficients become state-dependent. This transforms Equation 6 from a linear regression into a **state-dependent constitutive model** — a significant theoretical upgrade.

---

## 2. Where Coupling Fits in the Paper Structure

The current manuscript has a clean logical flow:

> Theory (§2) → Environmental forcing models (§3–4) → Nonlinear elasticity (§5) → Anisotropy (§6) → Rheology & inversion (§7) → Validity (§8) → Applications (§9) → Discussion (§10)

The coupling analysis belongs as a new Section between the current §8 (Validity) and §9 (Applications), or alternatively as an extension of §8. The recommended structure is:

### Option A: New Section 8B — "Coupling Between Forcings: When Linear Superposition Fails"

This section would:

1. **State the superposition assumption explicitly** and identify where in Sections 3–6 it was used (everywhere).
2. **Introduce the coupling hierarchy** — three tiers organized by mathematical form:
   - **Tier 1: Poroelastic bidirectional coupling** ($\alpha_B B$ parameterization) — always present in saturated media, but reducible to an effective $\beta$ in many cases. The existing Fokker et al. (2021) treatment (§4.1) already handles this correctly, but the manuscript does not discuss the coupling strength or when the undrained/drained separation fails.
   - **Tier 2: Damage–permeability feedback** ($k(D, t, \sigma_{\text{eff}})$) — activated by earthquakes, persisting for months to years. This modifies the hydrological transfer function itself, meaning the coefficients in Equation 6 change after each significant earthquake.
   - **Tier 3: Saturation-dependent nonlinear elasticity** ($\beta(S)$) — dominant in the vadose zone, creating multiplicative rather than additive interactions between hydrological state and the response to any other forcing.
3. **Present the modified constitutive model** (Equation 6'):

$$\frac{\delta v}{v}(t) = F_{\text{NL}}\!\left[\varepsilon_{\text{total}}(t),\; S(t)\right] + G_{\text{poroelastic}}\!\left[\sigma_{\text{eff}}(t),\; P(t)\right] + R_{\text{damage}}(t)$$

where $F_{\text{NL}}$ encodes the saturation-dependent nonlinear elastic response, $G_{\text{poroelastic}}$ solves the coupled Biot equations for effective stress and pore pressure, and $R_{\text{damage}}$ follows the universal relaxation function of Snieder et al. (2017).

4. **Map coupling importance onto the regime diagram** (Figure 18). The existing diagram partitions the frequency–depth space by dominant process; the revised version adds coupling boundaries:
   - Below the water table at timescales shorter than the drainage time → poroelastic coupling is first-order.
   - After earthquakes (PGV > ~0.2 cm/s) → damage–permeability coupling is first-order for months to years.
   - In the vadose zone above the water table → saturation-dependent nonlinearity dominates.
   - At all timescales when thermal and hydraulic cycles are correlated (most continental sites) → thermoporoelastic coupling is conditionally first-order.

### Option B: Extend §8.2 ("Linear Acoustoelasticity Validity") into a broader "Validity and Coupling" section

This is more compact and preserves the existing section numbering. The trade-off is that the coupling analysis deserves more space than a subsection typically affords.

**Recommendation**: Option A, as a new §8B. The coupling material is substantial enough (hierarchy, equations, diagnostics, regime diagram update) to warrant a dedicated section, and it provides the theoretical motivation for the observational diagnostics proposed in the Discussion.

---

## 3. How Coupling Connects to Each Existing Section

### Section 2 (Theory): Bridge relation needs a drainage-state qualifier

Equation 7 ($\beta = -\mu'\kappa/(2\mu)$) uses the drained bulk modulus $\kappa$. The manuscript already notes (§2.5) that the undrained effective bulk modulus $\kappa_u = \kappa/(1 - \alpha_B B)$ applies at short timescales, making $|\beta_{\text{undrained}}| > |\beta_{\text{drained}}|$. The coupling section should formalize this as:

$$\beta_{\text{eff}}(\omega) = -\frac{\mu' \kappa(\omega)}{2\mu}, \quad \kappa(\omega) = \begin{cases} \kappa & \omega \ll \omega_{\text{drain}} \\ \kappa_u = \kappa/(1-\alpha_B B) & \omega \gg \omega_{\text{drain}} \end{cases}$$

where $\omega_{\text{drain}} \sim \kappa_{\text{perm}}/(\mu_f L^2 S_s)$ is the drainage transition frequency. This connects the Zimmerman (2000) coupling parameter $\alpha_B B$ directly to the bridge relation.

### Section 3 (Thermoelastic): Thermal pressurization adds a coupling term

The Richter et al. (2014) treatment assumes dry conditions (Atacama Desert). For saturated or partially saturated sites, the McTigue (1986) thermal pressurization coefficient $\Lambda = (\alpha_f - \alpha_\phi)/(\phi/K_f + (\alpha-\phi)/K_s)$ generates excess pore pressure under undrained thermal loading. This adds a second pathway from temperature to δv/v:

$$\left(\frac{\delta v}{v}\right)_{\text{thermo}} = \underbrace{\left(\frac{\delta v}{v}\right)_{\text{thermoelastic stress}}}_{\text{Eq. 9, existing}} + \underbrace{\left(\frac{\delta v}{v}\right)_{\text{thermal pressurization}}}_{\text{new: } -\frac{\mu'}{2\mu}\Lambda\Delta T}$$

The second term is first-order when the water table lies within the thermal skin depth (5–15 m for annual) and permeability is low enough to sustain undrained conditions.

### Section 4 (Hydrological): Drained-undrained transition needs explicit treatment

Fokker et al. (2021) already model pore pressure diffusion (§4.1), but the manuscript does not discuss the frequency dependence of the transition. The coupling section should note that tidal forcing (~12 hr) is undrained in most rocks, while seasonal forcing (~months) is typically drained. The sign of δv/v–GWL correlation depends on this drainage state (Fokker et al., 2021, their §5): below the water table in the drained regime, rising GWL increases pore pressure and decreases velocity; in the undrained regime, the same event increases both loading stress and pore pressure, with the net effect depending on $\alpha_B B$.

### Section 4.4 (Capillary): Saturation-dependent β is the Tier 3 coupling mechanism

The Shi et al. (2026) dynamic capillary framework already in the manuscript is the entry point for Tier 3 coupling. The connection to make explicit is that the Hertz-Mindlin effective modulus $\mu_{\text{eff}} \propto P_e^{1/3}$ means $\mu' = d\mu_{\text{eff}}/dP \propto P_e^{-2/3}$ — which diverges as effective pressure approaches zero (i.e., at the water table). This means $\beta(S)$ has a singularity near full saturation in unconsolidated media, creating extreme sensitivity precisely where the drained-to-undrained transition occurs. The Van Den Abeele et al. (2002) laboratory data showing maximum nonlinearity at 1–20% saturation provides the experimental confirmation.

### Section 5 (Nonlinear Elasticity): β depends on saturation — a multiplicative coupling

The current treatment (§5.2) lists "Fluid saturation state" as a control on $|\beta|$ but treats it as a static parameter. The coupling upgrade is to make $\beta$ explicitly saturation-dependent in the acoustoelastic relation:

$$\frac{\delta v}{v} = \beta(S_w) \cdot \varepsilon_{kk}$$

where $\beta(S_w)$ incorporates the Winkler and McGowan (2004) laboratory measurements showing that all three Murnaghan constants change with saturation. This means the response to tidal, thermoelastic, and tectonic forcing all depend on the instantaneous saturation state — a multiplicative coupling that cannot be captured by adding independent terms.

### Section 7 (Healing): Damage–permeability feedback modifies the hydrological transfer function

The logarithmic healing model (Eq. 12) currently treats damage recovery as independent of hydrology. The Illien et al. (2022) Gorkha earthquake results show that this is incorrect: the transient drainage efficiency parameter $a(t)$ that decays with $\tau_{\text{hydro}} \approx 6$ months means that the seasonal δv/v regression coefficients change after the earthquake. The coupling section should introduce:

$$k(t) = k_0 \cdot \exp\!\left[D_{\text{co-seismic}} - \int_0^t H(t')\,dt'\right]$$

where $D_{\text{co-seismic}}$ is the initial permeability increase (Elkhoury et al., 2006: up to 3× per event, scaling with PGV) and $H(t)$ is the healing rate ($\tau_{\text{heal}} \sim$ months to years, Xue et al., 2013).

### Section 9 (Applications): Post-hoc coupling assessment for each site

For each of the three sites, the coupling section should assess whether coupling was significant:

- **Parkfield**: The 2003 San Simeon and 2004 Parkfield earthquakes almost certainly modified permeability (PGV well above 0.2 cm/s). The seasonal regression coefficients should differ pre- vs. post-earthquake. This is testable with the existing Okubo et al. (2024) dataset.
- **Cascadia**: Marine sediments are fully saturated; the poroelastic coupling parameter $\alpha_B B$ is likely 0.5–0.8 for soft sediment. The isotropic framework succeeds because the coupling is already implicitly included via the effective stress formulation (Fokker et al., 2021).
- **Kīlauea**: The caldera collapse events are rapid enough to be undrained, and the basalt is fractured with hydrothermal circulation. The short-term co-collapse signals are likely in the undrained regime; the long-term damage signal may involve permeability changes from the ring fault formation.

---

## 4. New References Required

The coupling analysis introduces references not in the current manuscript. Key additions:

1. **Elkhoury, J. E., Brodsky, E. E., & Agnew, D. C. (2006).** Seismic waves increase permeability. *Nature*, 441, 1135–1138. [Permeability increase scaling with PGV]
2. **Xue, L., et al. (2013).** Continuous permeability measurements record healing inside the Wenchuan earthquake fault zone. *Science*, 340, 1555–1559. [Permeability healing timescale]
3. **McTigue, D. F. (1986).** Thermoelastic response of fluid-saturated porous rock. *JGR*, 91, 9533–9542. [Thermal pressurization coefficient Λ]
4. **Palciauskas, V. V., & Domenico, P. A. (1982).** Characterization of drained and undrained response of thermally loaded repository rocks. *Water Resources Research*, 18, 281–290. [Λ ≈ 0.59 MPa/°C for sandstone]
5. **Van Den Abeele, K., et al. (2002).** Influence of water saturation on the nonlinear elastic mesoscopic response in Earth materials. *JGR*, 107, 2121. [Saturation-dependent nonlinear elasticity]
6. **Winkler, K. W., & McGowan, L. (2004).** Nonlinear acoustoelastic constants of dry and saturated rocks. *JGR*, 109, B10204. [Saturation modifies Murnaghan constants]
7. **Zimmerman, R. W. (2000).** Coupling in poroelasticity and thermoelasticity. *Int. J. Rock Mech. Min. Sci.*, 37, 79–87. [Coupling parameters αB and thermoelastic coupling ~10⁻³]
8. **Illien, L., et al. (2022).** Seismic velocity recovery in the subsurface: Transient damage and groundwater drainage following the 2015 Gorkha earthquake, Nepal. *JGR: Solid Earth*, 127, e2021JB023402. [Transient drainage efficiency a(t)]
9. **Illien, L., et al. (2021).** Subsurface moisture regulates Himalayan groundwater storage and discharge. *AGU Advances*, 2, e2021AV000398. [Vadose zone "gatekeeper" effect]
10. **Snieder, R., Sens-Schönfelder, C., & Wu, R.-S. (2017).** The time dependence of rock healing as a universal relaxation process. *GJI*, 208, 1–9. [Universal log-time relaxation]
11. **Wang, Q.-Y., et al. (2021).** Near-surface softening and healing in eastern Honshu. *Nature Communications*, 12, 1215. [Fluid-mediated healing mechanism]
12. **Carcione, J. M., et al. (2019).** Physics and simulation of wave propagation in linear thermoporoelastic media. *JGR: Solid Earth*, 124, 8577–8596. [Thermoporoelastic wave propagation]
13. **Sens-Schönfelder, C., & Eulenfeld, T. (2019).** Probing the in situ elastic nonlinearity of rocks with Earth tides and seismic noise. *Physical Review Letters*, 122, 138501. [Already in manuscript; sum-frequency cross-coupling evidence]
14. **Rattanavetchasit, P., et al. (2026).** Frequency-dependent seismic velocity variations reveal layered aquifer behavior under groundwater fluctuations. *GRL*. [Frequency-dependent drainage diagnostics]
15. **Coussy, O. (2004).** *Poromechanics*. Wiley. [Thermoporoelastic constitutive equations]

---

## 5. Conceptual Figure: The Coupling Regime Diagram

The existing Figure 18 (regime diagram: frequency vs. depth, showing which process dominates) should be expanded to include coupling boundaries. The revised figure would show:

- **X-axis**: Forcing timescale (from tidal ~12 hr to decadal)
- **Y-axis**: Depth below surface (0–10 km)
- **Color regions**: Dominant process (thermoelastic, hydrological, tectonic, volcanic, capillary)
- **Hatched overlays**: Coupling zones
  - Diagonal hatching: poroelastic coupling dominant ($\alpha_B B > 0.3$ and $\tau_{\text{forcing}} < \tau_{\text{drain}}$)
  - Vertical hatching: damage–permeability coupling active (post-earthquake, shaded to indicate decay)
  - Dotted overlay: saturation-dependent nonlinearity ($S_w < 0.8$, above water table)
- **Key boundaries**:
  - Drained/undrained transition line (depends on permeability; shown for 3 representative values)
  - Thermal skin depth (annual and daily)
  - Water table depth (typical range)
  - Coda sensitivity kernel peak depth (for 0.5, 1, 2, 4 Hz)

---

## 6. Implications for the Three-Site Applications

The coupling analysis does not invalidate the existing applications — it clarifies their domain of validity:

**Parkfield**: The linear trend ($b_0 = 0.0048\%$/yr) is measured over 20 years that include two major earthquakes. If the seasonal regression coefficients changed post-earthquake (Tier 2 coupling), the linear trend extraction may be biased. The recommended test: fit Equation 6 separately for 2001–2003 (pre-San Simeon), 2005–2010 (post-Parkfield), and 2010–2020 (late recovery) and compare the thermoelastic and hydrological coefficients.

**Cascadia**: The isotropic success ($\delta v/v$-derived stress exactly matches borehole strain) is expected because the coupling is already handled correctly by the effective stress formulation. The poroelastic coupling parameter $\alpha_B B$ for marine sediment is high (0.5–0.8), but this is accounted for by using the appropriate $\mu'$ value from the saturated shear-modulus-vs-pressure profile.

**Kīlauea**: The co-collapse events (hourly timescale) are almost certainly undrained in fractured basalt, so the undrained $\beta_u$ should be used rather than the drained $\beta$. This would increase $|\beta|$ by a factor of $1/(1-\alpha_B B)$ — potentially 1.5–2× — which would bring the geodetic cross-check (currently factor ~2 discrepancy) into closer agreement.

---

## 7. Summary: The Revised Paper's Central Argument

The original paper's central argument is:

> "All δv/v sources operate through nonlinear elasticity, and the unified framework connects strain formulation ($\beta$) to stress formulation ($\mu'$) via the bridge relation."

The revised paper's enhanced argument becomes:

> "All δv/v sources operate through nonlinear elasticity with state-dependent sensitivity. The framework connects strain and stress formulations via the bridge relation, but the coefficients in that relation depend on three state variables: **drainage condition** (through $\kappa(\omega)$ and $\alpha_B B$), **damage state** (through $k(D,t)$), and **saturation** (through $\beta(S_w)$). Linear superposition is valid when these state variables are approximately constant over the analysis window — a condition that holds for interseismic periods at sites with stable hydrology, but fails after earthquakes, during drought-to-flood transitions, and wherever the vadose zone falls within the coda sensitivity kernel."

This is a more nuanced and powerful statement. It preserves all the quantitative results of the original paper (which were derived under conditions where the superposition assumption holds) while mapping the boundaries of validity and providing the mathematical framework for extensions.
