# Application Cases: Revisiting Published δv/v Datasets Through the Coupling Framework

**Working document — M. A. Denolle & Claude**
**Companion to the Coupling Tier analysis**

---

## Overview

This document identifies specific published δv/v datasets where the coupling framework developed in the paper could yield new scientific insights. Each case identifies: the dataset, the coupling mechanism that was either ignored or unrecognized, the specific diagnostic test enabled by the coupling framework, and the expected scientific outcome. Cases are prioritized by data availability (especially those available as parquet files from Clements & Denolle 2023, Okubo et al. 2024, Kidiwela et al. 2026, and Malone et al. on Mt. St. Helens).

---

## Case 1: Clements & Denolle (2023) — California-wide seasonal coefficient change around Ridgecrest (Tier 2)

**The opportunity.** Clements & Denolle (2023) fitted a linear combination of thermoelastic and hydrological models to δv/v at ~647 California stations with constant coefficients $a_1$ (thermal) and $a_2$ (hydrological) over the entire 22-year record. Yet three M7+ earthquakes (Hector Mine 1999, El Mayor-Cucapah 2010, Ridgecrest 2019) occurred during this period, and the authors themselves noted: "We have not coupled the hydrological terms with the tectonic signals as did Illien et al. (2022). Our approximation may be valid in the cases of southern California earthquakes, given the low water table and occurrence during dry periods. Still, they may be important in northern California or during wet winters."

**The coupling diagnostic.** Split the parquet time series at each near-fault station into pre-earthquake and post-earthquake windows. Refit the thermoelastic and hydrological coefficients separately for each window. The Tier 2 coupling predicts that $a_2$ (hydrological sensitivity) should increase after the earthquake because enhanced permeability allows faster pore-pressure diffusion, while $a_1$ (thermoelastic) should remain unchanged. The magnitude of the change scales with PGV. Stations within the Ridgecrest damage zone (CI.JRC2 and neighbors) are the most promising targets because the 2019 M7.1 occurred during a relatively dry period, simplifying the decomposition.

**The test.** For each station within 50 km of the Ridgecrest epicenter: fit Eq. 6 using 2015–2019 data (pre-EQ) and 2020–2023 data (post-EQ) separately. Compare the fitted hydraulic diffusivity $c$ and hydrological amplitude $a_2$. A statistically significant increase in $c$ or $a_2$ after the earthquake would constitute direct evidence for Tier 2 coupling at the network scale.

**Expected outcome.** The Clements & Denolle (2023) Figure 4 mixing ratio map ($R_T = a_2/(a_1 + a_2)$) should shift toward more hydrological dominance (bluer) for post-Ridgecrest windows at near-fault stations, while remaining unchanged at distant stations. This would be the first California-wide demonstration of earthquake-modified hydrological sensitivity.

**Broader impact.** If the seasonal coefficients change post-earthquake, the 22-year linear trend extracted by Okubo et al. (2024) at Parkfield (which spans the 2003 San Simeon and 2004 Parkfield earthquakes) may need reassessment. The same split-window test at Parkfield HRSN stations would determine whether the $b_0 = 0.0048\%$/yr secular trend is robust to time-varying hydrological coefficients.

---

## Case 2: Clements & Denolle (2023) — Drought-to-flood transitions and saturation-dependent β (Tier 3)

**The opportunity.** The 2004–2005 winter brought record precipitation to Southern California after a dry period. Clements & Denolle (2023) documented δv/v drops exceeding 1% at station CI.LJR, with cumulative precipitation 3× the mean. They also documented the 2011–2016 drought as a multi-year δv/v increase. The key observation for Tier 3 coupling is that the magnitude of the δv/v response to precipitation appears non-linear: the 2004–2005 wet winter produced disproportionately large drops compared to normal wet winters.

**The coupling diagnostic.** If β depends on saturation (Tier 3), the sensitivity of δv/v to precipitation should depend on antecedent moisture conditions. Specifically, the same amount of rain should produce a larger δv/v drop at the transition from dry-to-wet (when saturation crosses from the capillary to the liquid bridge window, where |β| is maximized) than during already-wet conditions (when pore space is nearly saturated and |β| decreases).

**The test.** For stations with the parquet time series: compute a running 90-day antecedent precipitation index (API). Then compute the sensitivity $d(\delta v/v)/d(\text{precip})$ in sliding 180-day windows. Plot this sensitivity against API. A non-monotonic or state-dependent relationship would confirm Tier 3 coupling. In particular, the sensitivity should be highest when API transitions from "drought" to "moderate" (crossing through the capillary and liquid-bridge sensitivity windows), and lower during sustained wet conditions.

**Expected outcome.** The CI.LJR station and San Gabriel Valley basin stations should show the clearest signatures because they have the shallowest water tables and the most dramatic drought-to-flood transitions. The 2004–2005 super-response and the 2017 post-drought flood response should both show elevated sensitivity relative to normal wet winters, confirming that the transfer function is state-dependent.

**Broader impact.** If confirmed, this non-linearity has direct implications for water resource management: δv/v could serve as a non-invasive probe of the vadose-zone moisture state, with sensitivity that peaks precisely when drought-to-flood transitions create the highest flood risk.

---

## Case 3: Okubo et al. (2024) — Parkfield tidal sensitivity as a coupling diagnostic (Tiers 1 + 2)

**The opportunity.** Okubo et al. (2024) measured δv/v at Parkfield over 20 years at multiple frequency bands (0.5–1.2 Hz). They focused on the secular trend and seasonal cycle, but the Earth tide response at the same stations provides a direct probe of the coupled hydromechanical state. Sens-Schönfelder & Eulenfeld (2019) showed that tidal δv/v encodes the in-situ nonlinear elastic parameters, and Takano et al. (2023) demonstrated that tidal δv/v sensitivity varies seasonally in Japan.

**The coupling diagnostic.** The tidal strain at Parkfield is well-known (M2 and O1 components). The δv/v response to tidal strain measures $\beta_{\rm eff}(\omega_{\rm tide})$ — the undrained effective acoustoelastic parameter. If damage–permeability coupling (Tier 2) modified the drainage state after the 2004 Parkfield earthquake, the tidal β should have changed: specifically, enhanced permeability would shift the tidal frequency closer to the drained regime, decreasing $|\beta_{\rm eff}|$ at tidal periods.

**The test.** Extract the M2 tidal amplitude of δv/v from the Okubo et al. (2024) parquet time series using harmonic regression in sliding 6-month windows. Track the tidal β = δv/v(M2) / ε(M2) over time. Look for a step change after the 2004 Parkfield earthquake followed by gradual recovery, mirroring the permeability healing observed by Xue et al. (2013) at Wenchuan.

**Expected outcome.** If the tidal β decreased after the 2004 earthquake and recovered over 2–5 years, this would provide direct, independent evidence for Tier 2 coupling — earthquake-modified drainage state altering the hydromechanical response at tidal frequencies. This test is particularly powerful because it uses a forcing (Earth tides) that is completely independent of meteorology.

**Broader impact.** Tidal β monitoring could become a standard post-earthquake assessment tool, providing a passive, continuous measure of subsurface damage and recovery without requiring dedicated borehole instrumentation.

---

## Case 4: Kidiwela et al. (2026) — Cascadia slow-slip event as a drainage-state probe (Tier 1)

**The opportunity.** Kidiwela et al. (2026) detected a δv/v drop of –0.2% at 3–5 Hz during the 2016 Cascadia slow-slip event, and a transient fluid migration event in 2019. The framework paper (Section 9.2.6) quantified the pore pressure perturbation as 2–4 kPa using the isotropic Fokker formulation.

**The coupling diagnostic.** The slow-slip event provides a natural experiment in Tier 1 coupling. During the slow slip, both mechanical stress and pore pressure change simultaneously (the fault unloads, and fluids may be released or redistributed). The question is whether the δv/v change is proportional to the total stress change (undrained response) or the effective stress change (drained response). The answer depends on the drainage timescale of the accretionary wedge sediment relative to the slow-slip duration (~2 weeks).

**The test.** Using the Kidiwela parquet data, compare the δv/v drop at 1–3 Hz (deeper sensitivity, ~300 m) versus 3–5 Hz (shallower sensitivity, ~100 m) during the 2016 slow-slip event. At shallower depths, the more permeable sediment should be closer to drained, giving a smaller δv/v response per unit strain. At deeper depths, lower permeability keeps the response closer to undrained, giving a larger δv/v per unit strain. The ratio of high-freq to low-freq δv/v during the slow-slip should differ from their ratio during the secular trend (which is steady-state drained).

**Expected outcome.** If the slow-slip frequency ratio differs from the secular-trend frequency ratio by more than ~50%, this diagnoses a frequency-dependent drainage transition — direct evidence that the Biot poroelastic coupling parameter αBB is active at slow-slip timescales at Cascadia.

**Broader impact.** Slow-slip events are hypothesized to be modulated by fluid pressure on the subduction interface. Demonstrating that δv/v can distinguish drained from undrained response during slow slip would provide a new observable constraining the role of fluids in episodic tremor and slip.

---

## Case 5: Mt. St. Helens (Malone et al.) — Coupled volcanic, hydrological, and thermoelastic signals (Tiers 1 + 3)

**The opportunity.** Mt. St. Helens represents a volcanic setting where thermoelastic, hydrological, and magmatic signals all operate simultaneously, and where snowmelt produces large seasonal loading and saturation changes. If δv/v time series are available from the Malone et al. dataset, this site offers a natural laboratory for testing coupling because the annual snow cycle produces massive surface loading (several meters of snow water equivalent) that simultaneously changes saturation, pore pressure, and elastic loading.

**The coupling diagnostic.** At Mt. St. Helens, spring snowmelt produces three simultaneous effects: surface unloading (velocity decrease from reduced compression), pore-pressure increase from infiltration (velocity decrease from reduced effective stress), and saturation increase in the vadose zone (velocity change depending on β(S)). In the decoupled framework, these would be additive. In the coupled framework, the saturation increase during snowmelt modifies |β| itself, amplifying or damping the response to the simultaneous loading change.

**The test.** Correlate δv/v with SNOTEL snow water equivalent (SWE) and temperature records at multiple frequencies. During the snowmelt-to-bare-ground transition (April–July), the rate of δv/v change per unit SWE loss should be non-constant if β depends on the evolving saturation state. Specifically, early melt (when the ground is still frozen or nearly saturated) should show different sensitivity than late melt (when partial saturation develops). The diagnostic signature is hysteresis in the δv/v-vs-SWE relationship between the accumulation and melt seasons.

**Expected outcome.** The volcano setting adds the complication of potential magmatic signals, but these should be identifiable at longer periods or through correlation with seismicity and deformation. The seasonal snowmelt coupling test is most cleanly conducted during quiescent periods. If the δv/v–SWE relationship shows counter-clockwise hysteresis (different paths during accumulation vs. melt), this diagnoses saturation-dependent β plus asymmetric drainage.

**Broader impact.** Snowmelt-driven coupling is relevant not only for volcanic monitoring (where environmental signals mask pre-eruptive anomalies) but also for water resource management in snowmelt-dominated catchments (most of the western US).

---

## Case 6: Lecocq et al. (2017) — Gräfenberg Array 30-year record: thermoporoelastic coupling at annual timescale

**The opportunity.** Lecocq et al. (2017) analyzed 30 years of δv/v from the Gräfenberg Array in southern Germany and found the highest correlation (r = 0.83) when thermoelastic and hydrological contributions were weighted equally at 50% each. They explicitly noted that "both effects are correlated—and difficult to separate—at annual timescales." This is precisely the thermoporoelastic coupling regime.

**The coupling diagnostic.** The near-degeneracy of annual temperature and precipitation cycles creates a fundamental multicollinearity that the decoupled framework cannot resolve by regression alone. The coupling framework predicts that the thermal pressurization coefficient Λ generates excess pore pressure during the summer warming (undrained thermal expansion of pore water), which augments the hydrological signal. This means the "hydrological" coefficient fitted by Lecocq et al. is actually a composite of true hydrological and thermal pressurization contributions.

**The test.** If raw data or digitized time series are available, fit the δv/v record using: (a) the standard decoupled model (temperature + GWL as independent regressors), and (b) a coupled model where the pore pressure includes a McTigue thermal pressurization term Λ·ΔT(z,t). The coupled model should show improved fit at interannual timescales where temperature and precipitation diverge (e.g., warm-dry summers vs. cool-wet winters of different years).

**Expected outcome.** The fitted Λ value should be physically reasonable (0.1–1 MPa/K for the Jurassic carbonate basement). The interannual residuals should decrease with the coupled model. Most importantly, the apparent "50/50 thermal-hydrological split" should resolve into a different ratio once thermal pressurization is properly attributed.

---

## Case 7: Richter et al. (2014) — Atacama Desert as a "coupling null test" (validation)

**The opportunity.** Richter et al. (2014) at PATCX in the Atacama Desert found a purely thermoelastic δv/v signal with negligible hydrological contribution, as expected for one of the driest places on Earth. This site serves as a **null test** for the coupling framework: in the absence of water, Tiers 1 and 3 should vanish, and the thermoporoelastic coupling should be zero.

**The coupling diagnostic.** The Richter et al. data is already in the project knowledge base. The coupling framework predicts that: the thermal pressurization term Λ·ΔT is zero (no pore fluid to pressurize), the saturation-dependent β is constant (dry rock), and the only signal is thermoelastic stress through the Berger (1975) model. The observed 2–3 month phase delay between temperature and δv/v should be entirely explained by thermal diffusion, with no additional delay from pore-pressure equilibration.

**The test.** Fit the Richter et al. data with both the decoupled and coupled models. The coupled model should provide no improvement (since Λ = 0 in dry rock), confirming that the coupling is physically grounded rather than an artifact of adding free parameters. This is essential for establishing that the coupling framework improves fit only where the physics predicts it should.

---

## Case 8: Donaldson et al. (2019) — Iceland Northern Volcanic Zone: decomposition of strain contributions with seasonal pore pressure coupling

**The opportunity.** Donaldson et al. (2019) decomposed δv/v at Iceland's NVZ into contributions from the 2014 Bárðarbunga-Holuhraun dike intrusion and seasonal loading (snow + water). They found pore pressure effects were ~4× stronger than elastic loading for the same water input. This factor of 4 is itself a Tier 1 coupling diagnostic: it reflects the ratio of pore-pressure sensitivity (through μ'/μ) to mechanical loading sensitivity (through the T33 coefficient in Fokker et al. 2021).

**The coupling diagnostic.** Donaldson et al. treated the strain contributions as additive and separable. During the dike intrusion, however, the magmatic stress change simultaneously alters the confining pressure on fractures, which can modify both permeability and the drainage state. If the intrusion opened new fractures (plausible for a 48-km-long dike), the post-intrusion hydrological sensitivity should differ from the pre-intrusion sensitivity.

**The test.** Compare the seasonal δv/v amplitude at each station during 2013–2014 (pre-intrusion) versus 2015–2016 (post-intrusion). A change in seasonal amplitude at stations near the dike, but not at distant stations, would indicate intrusion-modified hydrological properties — Tier 2 coupling in a volcanic context.

---

## Prioritized Test Plan with Available Datasets

Given the available parquet files (Clements & Denolle 2023 California-wide, Okubo et al. 2024 Parkfield, Kidiwela et al. 2026 Cascadia, Malone et al. Mt. St. Helens), the recommended priority order is:

**Priority 1 — Cases 1 and 3 (California + Parkfield, Tier 2).** These use the same parquet infrastructure and test the same coupling mechanism (post-earthquake coefficient change). Case 1 provides the network-scale context; Case 3 provides the tidal diagnostic at a single well-instrumented site. Together they make the strongest argument for Tier 2 coupling.

**Priority 2 — Case 2 (California drought-to-flood, Tier 3).** This reuses the Clements & Denolle parquet files and tests a different coupling mechanism. The drought-to-flood transitions of 2004–2005 and 2016–2017 are already documented in the dataset.

**Priority 3 — Case 4 (Cascadia slow-slip, Tier 1).** This uses the Kidiwela parquet files and tests the frequency-dependent drainage transition during a well-constrained transient event.

**Priority 4 — Case 5 (Mt. St. Helens, Tiers 1+3).** This uses the Malone parquet files and tests snowmelt coupling at a volcanic site.

**Priority 5 — Cases 6–8 (external datasets).** These require either digitized data or new collaborations but provide important cross-validation.

---

## Summary Table

| Case | Dataset | Coupling Tier | Key diagnostic | Data available? |
|------|---------|--------------|----------------|----------------|
| 1. CA Ridgecrest | Clements & Denolle 2023 | Tier 2 | Split-window regression coefficients | ✅ parquet |
| 2. CA drought-flood | Clements & Denolle 2023 | Tier 3 | Non-linear sensitivity vs. API | ✅ parquet |
| 3. Parkfield tidal β | Okubo et al. 2024 | Tiers 1+2 | Time-varying tidal sensitivity | ✅ parquet |
| 4. Cascadia slow-slip | Kidiwela et al. 2026 | Tier 1 | Frequency-dependent drainage | ✅ parquet |
| 5. Mt. St. Helens | Malone et al. | Tiers 1+3 | Snowmelt hysteresis in δv/v–SWE | ✅ parquet |
| 6. Gräfenberg 30-yr | Lecocq et al. 2017 | Thermal pressurization | Coupled vs. decoupled fit improvement | ❌ external |
| 7. Atacama null test | Richter et al. 2014 | Null (validation) | No improvement from coupling model | Partial (PK) |
| 8. Iceland NVZ | Donaldson et al. 2019 | Tier 2 | Pre/post-intrusion seasonal change | ❌ external |
