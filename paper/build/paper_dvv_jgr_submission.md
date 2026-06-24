---
title: "Seismic Velocity Changes as Stress and Strain Meters: A Unified Framework for Environmental, Tectonic, and Volcanic Monitoring"
author: "Marine A. Denolle"
affiliation: "Department of Earth and Space Sciences, University of Washington, Seattle, WA, USA"
corresponding_author: "mdenolle@uw.edu"
---


## Abstract

Ambient seismic noise monitoring of relative seismic velocity changes ($\delta v/v$) has become a powerful tool for probing the subsurface mechanical state across environmental, tectonic, and volcanic settings. Yet interpretation remains fragmented: thermoelastic, hydrological, poroelastic, and tectonic models are applied in isolation, making it difficult to separate competing signals or jointly invert for subsurface rheology. Here we develop a unified theoretical framework that treats $\delta v/v$ simultaneously as a stress meter and a strain meter, grounded in nonlinear (third-order) elasticity, poroelastic theory, and the induced-stress formulation of Tromp and Trampert (2018). Through systematic scenario modeling we quantify the sensitivity of $\delta v/v$ to surface temperature variations (\textasciitilde{}0.01–0.3% annually), hydrological loading and pore-pressure diffusion (\textasciitilde{}0.01–0.1%), ice and snow loading (\textasciitilde{}0.001–0.5%), partially saturated media with dynamic capillary effects, and tectonic strain accumulation (\textasciitilde{}0.001–0.01%/yr). We show that stress-induced anisotropy from oriented microcrack closure explains why $\delta v/v$ correlates with contractional axial strain rather than dilatation, as observed at Parkfield. We demonstrate the framework quantitatively at three contrasting sites: at Parkfield (strike-slip), the isotropic formulation fails and the deviatoric framework predicts a stress accumulation rate of ~12 kPa/yr at ~0.8 km depth in fractured granite ($\beta \approx 240$, $\mu' \approx 250$); at Cascadia (subduction), the isotropic framework succeeds and, using the borehole strain calibration, gives 0.58 kPa/yr in marine sediments ($\beta \approx 3160$, $\mu' \approx 620$); and at Kīlauea (volcanic caldera collapse), concentric ring fractures cause $\delta v/v$ to track radial rather than volumetric strain, with $\beta_{\text{radial}} \approx 300$ giving a reservoir-stress estimate within a factor of two of geodetic constraints. Because $\delta v/v$ depends on both frequency and coda lapse time — with different frequencies and windows sampling different wave types and depth ranges — multi-frequency, multi-lapse $\delta v/v$ combined with geodetic strain from GNSS/InSAR has the potential to enable depth-resolved stress and strain imaging, but only with appropriate kernels, regularization, and independent constraints. We map the parameter space where key assumptions remain valid, identify diagnostic signatures that distinguish elastic, viscoelastic, and slow-dynamics rheologies, and propose a reproducible window-selection framework for constraining subsurface rheological models. Companion notebooks reproduce the main and supporting figures and provide practical computational tools for implementing this framework.

**Keywords:** ambient noise monitoring, seismic velocity changes, nonlinear elasticity, thermoelastic stress, poroelasticity, capillary effects, rheology, GNSS, InSAR


## 1. Introduction

### 1.1 The Promise of Ambient Noise Monitoring

The continuous monitoring of relative seismic velocity changes ($\delta v/v$) using ambient seismic noise has transformed our ability to observe the evolving mechanical state of the Earth's crust. Since Sens-Schönfelder and Wegler (2006) first detected seasonal velocity changes at Mt. Merapi correlated with groundwater fluctuations, the technique has been applied across a remarkable breadth of settings: active faults (Brenguier et al., 2008a; Taira et al., 2015; Okubo et al., 2024), volcanoes (Brenguier et al., 2008b; Hotovec-Ellis et al., 2022), groundwater systems (Clements and Denolle, 2018, 2023; Mao et al., 2022), urban basins (Ermert et al., 2023), glaciated regions (Donaldson et al., 2019), arid deserts (Richter et al., 2014), and agricultural soils (Shi et al., 2026).

The physical basis is that coda waves — scattered waves arriving after ballistic arrivals — are exquisitely sensitive to small perturbations in the medium (Lobkis and Weaver, 2003; Snieder et al., 2002). Ambient noise cross-correlation (Nakata et al., 2019) removes the dependence on earthquake sources, enabling continuous monitoring from seconds to decades. The quantity $\delta v/v$ provides a relative measure of the volume-averaged perturbation in seismic velocity, with depth sensitivity controlled by the frequency content of the measurement (Obermann et al., 2014).

### 1.2 The Interpretation Challenge

The observed $\delta v/v$ time series at any station is a superposition of signals from thermoelastic stresses (Richter et al., 2014; Lecocq et al., 2017), hydrological effects including pore-pressure changes (Clements and Denolle, 2018, 2023; Fokker et al., 2021), surface loading from water, ice, and snow (Tsai, 2011; Donaldson et al., 2019), capillary effects in partially saturated media (Shi et al., 2026), coseismic damage and post-seismic healing (Wegler and Sens-Schönfelder, 2007; Brenguier et al., 2008a), and tectonic strain accumulation (Okubo et al., 2024).

The 20-year $\delta v/v$ record at Parkfield, California (Okubo et al., 2024) exemplifies the challenge: the time series contains seasonal oscillations from environmental effects, coseismic drops from the 2003 San Simeon and 2004 Parkfield earthquakes, logarithmic post-seismic healing, and a statistically significant long-term increase correlating with inter-seismic tectonic strain. In Oklahoma, Zhang et al. (2023) showed that multi-year hydrological effects dominate the overall $\delta v/v$, while annual thermoelastic strains dominate the seasonal cycle. In Greece, Delouche et al. (2023) identified hydrological cycling as the primary driver of seasonal $\delta v/v$ at depth, ruling out thermoelastic strain based on the frequency dependence of the signal.

### 1.3 What Has Been Missing

Several gaps persist:

1. **Fragmented theory.** The thermoelastic model (Berger, 1975; Richter et al., 2014), poroelastic model (Roeloffs, 1988; Clements and Denolle, 2023), and induced-stress framework (Tromp and Trampert, 2018) have been developed independently. A unified treatment through nonlinear elasticity is lacking.

2. **Systematic sensitivity analysis.** While individual studies fit models to specific datasets, a comprehensive parameter-space exploration has not been presented.

3. **Partially saturated media.** Most models assume fully saturated or fully drained conditions, yet Shi et al. (2026) showed that dynamic capillary effects in partially saturated soils produce distinct hysteretic $\delta v/v$ signatures not captured by existing frameworks.

4. **Anisotropy.** Most interpretations assume isotropic media, yet the Parkfield observations (Okubo et al., 2024) and the Tromp and Trampert (2018) theory show that deviatoric stress creates directionally dependent velocity changes.

5. **Depth-resolved inversion.** The frequency and lapse-time dependence of $\delta v/v$ — with different frequencies and coda windows sampling different wave types and depths — represents an underexploited opportunity for 3-D stress/strain imaging when combined with geodetic data.

6. **Processing reproducibility.** There is little field-wide consensus on frequency bands, substack length, and the start and end of the coda window. These choices are often treated as processing details even though they change the sensitivity kernel and therefore the physical interpretation.

7. **Rheological inversion.** A systematic framework for jointly inverting $\delta v/v$ and geodetic strain for subsurface rheology has not been formulated.

### 1.4 Scope and Contribution

This paper addresses these gaps by developing a unified framework connecting $\delta v/v$ to stress, strain, and rheology through nonlinear elasticity. Figure 1 summarizes the workflow, from forcing and sensitivity kernels to mechanism diagnosis and the future `codameter` implementation package. We present the theory (Section 2), quantitative scenario models for thermoelastic (Section 3), hydrological including partially saturated (Section 4), nonlinear elastic (Section 5), and anisotropic (Section 6) effects. We then develop the rheological inversion framework with emphasis on depth-resolved imaging and reproducible coda-window selection (Section 7), map validity ranges (Section 8), apply the framework quantitatively to three contrasting sites — Parkfield (strike-slip), Cascadia (subduction), and Kīlauea (volcanic) — predicting stress at depth from published $\delta v/v$ measurements (Section 9), and discuss implications (Section 10).

---

## 2. Unified Theoretical Framework: $\delta v/v$ as Both Stress and Strain Meter

### 2.0 Notation: What Does $\delta v/v$ Measure?

The quantity $\delta v/v$ (equivalently written $dv/v$ in much of the literature) is the relative velocity change measured from coda-wave interferometry (CWI) via the relation $\delta t/t = -\delta v/v$ (Poupinet et al., 1984; Clarke et al., 2011; Snieder et al., 2002). A critical question is: *what velocity does $\delta v/v$ represent?*

Snieder (2002) showed that in a multiply scattering elastic medium, P-to-S mode conversions drive the wavefield toward equipartition, where the energy ratio $E_S/E_P = 2(V_P/V_S)^3$. For a Poisson solid ($V_P/V_S = \sqrt{3}$), S-waves carry \textasciitilde{}90% of the scattered energy. Consequently, the CWI measurement is dominated by changes in S-wave velocity: $\delta v/v \approx \delta V_S/V_S$. Singh et al. (2019) generalized this, showing that the CWI velocity change varies along the coda as a weighted sum $[\delta V/V]_{\text{CWI}} = q(t,\gamma)\,\delta V_S/V_S + [1-q(t,\gamma)]\,\delta V_P/V_P$, where the S-wave weight $q \to 1$ at late coda times.

When surface waves dominate the ambient noise cross-correlations — as is typical at periods \textgreater{} 1 s — the measured $\delta v/v$ corresponds to a phase-velocity change $\delta c/c$ (Ermert et al., 2023; Fokker et al., 2021). This relates to the depth profile of $\delta V_S / V_S$ through the sensitivity kernel (Fokker et al., 2021, their Eq. 13):

$$\frac{\delta v}{v}(f, t) \approx \frac{\delta c}{c}(f, t) = \frac{1}{c(f)} \int_0^\infty \frac{\partial c}{\partial V_S}(z, f) \, \delta V_S(z, t) \, dz \tag{1}$$

Throughout this paper we adopt the following notation:

| Symbol | Meaning |
|--------|---------|
| $\delta v / v$ | Measured relative velocity change (the observable) |
| $\delta V_S / V_S$ | Local relative change in shear-wave velocity at depth $z$ (inferred) |
| $\delta c / c$ | Relative change in surface-wave phase velocity at frequency $f$ |

The Fokker et al. (2021) notation $d\beta/\beta$ refers to $\delta V_S/V_S$; we use the latter for clarity. Note that Equation 1 establishes that $\delta v/v$ is a *depth-averaged*, *frequency-dependent* measurement — different frequencies probe different depths, a property we exploit for 3-D imaging (Section 7).

### 2.1 Nonlinear Elasticity: The Murnaghan Framework

The sensitivity of seismic velocities to stress originates in nonlinear elastic behavior. Murnaghan (1937) showed that expanding the elastic energy density to third order in strain introduces three additional constants ($l$, $m$, $n$):

$$\rho_0 \phi = \frac{\lambda + 2\mu}{2} I_1^2 - 2\mu I_2 + l I_1^3 + m I_1 I_2 + n I_3 \tag{2}$$

These third-order elastic (TOE) constants cause seismic velocities to depend on the ambient stress state. The acoustoelastic relation (Ostrovsky and Johnson, 2001; Clements and Denolle, 2023) gives:

$$\frac{\delta v}{v} \approx \beta \, \epsilon_{kk}, \quad \beta = \frac{3}{2} + \frac{l + 2m}{\lambda + 2\mu} \tag{3}$$

where $\beta$ ranges from \textasciitilde{}−10 (steel) to \textasciitilde{}−10$^4$ (sandstone), reflecting microstructural compliance (Hughes and Kelly, 1953; Johnson and Rasolofosaon, 1996; Clements and Denolle, 2023).

### 2.2 The Induced-Stress Formulation

Tromp and Trampert (2018) showed that induced stress modifies shear-wave velocity as:

$$\frac{\delta V_S}{V_S} = \frac{\mu' p^0}{2\mu} + \frac{1 - \mu'}{4\mu} \hat{\mathbf{k}} \cdot \boldsymbol{\tau}^0 \cdot \hat{\mathbf{k}} - \frac{1 + \mu'}{4\mu} \hat{\mathbf{a}} \cdot \boldsymbol{\tau}^0 \cdot \hat{\mathbf{a}} \tag{4}$$

where $\hat{\mathbf{k}}$ and $\hat{\mathbf{a}}$ are propagation and polarization directions, $p^0$ is induced pressure, $\boldsymbol{\tau}^0$ is deviatoric stress, and $\mu' = d\mu/dP$. Critically, *deviatoric stress creates anisotropy* without requiring third-order elasticity.

### 2.3 Poroelastic Extension

Fokker et al. (2021) combined Equation 4 with poroelastic theory for surface loading $T_{33}^0$ and pore pressure $u^0$. For horizontally propagating surface-wave endmembers under a positive-compressive load convention, their coefficients reduce to:

$$\left(\frac{\delta V_S}{V_S}\right)_{\mathrm{Rayleigh/SV}} = -\frac{\mu'}{2\mu}u^0 + \frac{\mu' + 1}{12\mu}T_{33}^0,\qquad
\left(\frac{\delta V_S}{V_S}\right)_{\mathrm{Love/SH}} = -\frac{\mu'}{2\mu}u^0 . \tag{5}$$

The pore-pressure term decreases velocity by reducing effective stress. The vertical-load term depends on propagation and polarization geometry; therefore component-specific applications should evaluate the full directional form in Equation 4 rather than using a scalar loading coefficient.

### 2.4 General $\delta v/v$ Model

The observed $\delta v/v$ is modeled as (Okubo et al., 2024):

$$\frac{\delta v}{v}(t) = s_T \cdot T(t - t_{\text{shift}}) + p_1 \cdot \Delta\text{GWL}(t) + \sum_i s_i L_i(t) + b_0 t + a_0 \tag{6}$$

where each term has a clear physical origin: thermoelastic strain (Richter et al., 2014), hydrological pore-pressure change (Sens-Schönfelder and Wegler, 2006), coseismic damage with logarithmic healing (Snieder et al., 2017), and long-term tectonic loading. The unifying insight is that all terms operate through stress-dependent modification of elastic moduli.

### 2.5 Bridging the Strain and Stress Formulations

A central claim of this paper is that the strain formulation (Eq. 3, from acoustoelasticity) and the stress formulation (Eq. 4, from Tromp and Trampert, 2018) describe the same physics from different starting points. We can make this explicit. Under hydrostatic (isotropic) conditions, the induced pressure relates to volumetric strain through the bulk modulus: $p^0 = -\kappa \, \epsilon_{kk}$. Substituting into the isotropic term of Equation 4 gives $\delta V_S/V_S = -\mu' \kappa \, \epsilon_{kk} / (2\mu)$. Equating with the acoustoelastic relation (Eq. 3, $\delta v/v = \beta \, \epsilon_{kk}$) and using $\delta v/v \approx \delta V_S/V_S$ yields:

$$\beta = -\frac{\mu' \kappa}{2\mu} \tag{7}$$

This important relation connects the "materials science" parameter $\beta$ — measured in laboratory acoustoelastic experiments via third-order elastic constants (Hughes and Kelly, 1953) — to the "seismological" parameter $\mu'$ — inferred from the depth profile of shear modulus versus confining pressure (Fokker et al., 2021). For typical shallow sediments ($\mu' \approx 80$, $\kappa \approx 5$ GPa, $\mu \approx 0.5$ GPa), Equation 7 gives $\beta \approx -400$, consistent with the range reported for weakly cemented rocks (Clements and Denolle, 2023).

An important caveat is that Equation 7 uses the *drained* bulk modulus $\kappa$, appropriate for loading timescales longer than the pore-pressure diffusion time. At shorter timescales (the undrained limit), the effective bulk modulus is $\kappa_u = \kappa / (1 - \alpha_B B)$, where $\alpha_B$ is the Biot coefficient and $B$ is the Skempton coefficient (Roeloffs, 1988). In this limit the effective $\beta$ is larger in magnitude — meaning the velocity is *more* sensitive to strain when the pore fluid has not had time to drain. This drained-undrained distinction connects directly to the poroelastic models in Section 4.1 and explains why the $\delta v/v$ response to a rapid loading event (e.g., rainfall) may differ in amplitude from the response to a slow loading event (e.g., seasonal groundwater) even for the same total strain change.

The equivalence holds *only under isotropic loading*. Under deviatoric stress, the Tromp and Trampert formulation (Eq. 4) captures directional effects through the $\hat{\mathbf{k}} \cdot \boldsymbol{\tau}^0 \cdot \hat{\mathbf{k}}$ and $\hat{\mathbf{a}} \cdot \boldsymbol{\tau}^0 \cdot \hat{\mathbf{a}}$ terms, which have no counterpart in the scalar acoustoelastic relation. This divergence is precisely what makes the Parkfield observation — where $\delta v/v$ correlates with contractional but not dilatational strain (Okubo et al., 2024) — a diagnostic for deviatoric stress contributions.

### 2.6 Alternative and Complementary Mechanisms

Beyond the nonlinear-elastic framework, several alternative mechanisms can produce temporal velocity changes. **Density changes** from compaction can modify $V_S$ through $\delta V_S/V_S = -\frac{1}{2}\delta\rho/\rho$, though Fokker et al. (2021) showed this is 2–3 orders of magnitude smaller than the shear-modulus mechanism for typical settings. **Fluid substitution** — changes in pore-fluid composition (e.g., CO$_2$ injection; Zhu et al., 2019) — modifies the bulk modulus via Gassmann's equation and primarily affects $V_P$ rather than $V_S$. **Mineral alteration and cementation** (hydration, dissolution, bio-cementation) permanently modify the elastic frame on timescales of months to years (Rodríguez Tribaldos and Ajo-Franklin, 2021). **Direct temperature effects** on elastic moduli — distinct from the thermoelastic *stress* mechanism — are usually small (\textasciitilde{}0.01%/K) but become significant near phase transitions such as freezing/thawing in permafrost (James et al., 2017). **Scatterer relocation** from fracture opening or fluid migration produces apparent $\delta v/v$ that reflects structural change rather than bulk velocity change; Obermann et al. (2013) developed theory separating these contributions. Finally, **source-side effects** — seasonal changes in ocean-wave spectra or anthropogenic noise — can produce spurious $\delta v/v$ if not mitigated (Zhan et al., 2013; Okubo et al., 2024).

---

## 3. Thermoelastic Effects

### 3.1 Temperature Diffusion and Thermoelastic Stress

Surface temperature fluctuations diffuse into the Earth governed by the heat equation (Berger, 1975):

$$T(z,t) = T_0 \, e^{-\gamma z} \cos(\omega t - \gamma z), \quad \gamma = \sqrt{\omega/(2\kappa_T)} \tag{8}$$

with thermal skin depths of 1.2–4.5 m annually for $\kappa_T = 0.15$–$2.0$ mm$^2$/s (Richter et al., 2014; Ermert et al., 2023; Figure S1). Daily variations penetrate only 0.06–0.24 m, affecting $\delta v/v$ at frequencies above 2–4 Hz, whereas annual variations dominate the seasonal signal at 0.5–2 Hz.

The thermoelastic stress induced by these temperature changes contains two terms with fundamentally different depth behaviors (Berger, 1975; Richter et al., 2014, Eq. 11; Figure S2). The first term decays with the thermal skin depth $1/\gamma$ and represents *direct thermal stressing*: heated rock expands against the confinement of surrounding cooler rock, building compressive stress near the surface. The second term decays with the much longer scale $1/k$ (where $k = 2\pi/L$ is the horizontal wavenumber of the temperature field, $L \sim 10$ km) and represents the *mechanical equilibrium response* — a broad-scale stress adjustment needed to satisfy the free-surface boundary condition, penetrating to kilometer depths with a constant phase delay of $5\pi/4$ relative to surface temperature. For annual variations, $k/\gamma \approx 10^{-3}$, confirming that the two terms operate at well-separated depth scales. Tsai (2011) showed that this thermoelastic framework also explains seasonal GPS position changes, establishing a direct link between geodetically observed strain and seismically observed velocity change.

### 3.2 From Stress to Velocity Change

The thermoelastic stress converts to velocity change via (Richter et al., 2014, Eq. 12):

$$\frac{\delta v}{v} = b \frac{\partial(\rho v^2)}{\partial \sigma_c} \frac{(1-\nu)\Delta\sigma_c}{E} \tag{9}$$

where $b \approx 1.5$ for S-waves at $\nu = 0.2$ (Birch, 1961). The combined temperature sensitivity (Ermert et al., 2023, their Eq. 3) is $s_T = 2b\alpha \, \partial(\rho v^2)/\partial\sigma_c$, where $\alpha$ is the thermal expansion coefficient.

### 3.3 Sensitivity Analysis

Our sensitivity analysis (Figure S3) reveals that $\partial(\rho v^2)/\partial\sigma_c$ — ranging from \textasciitilde{}50 (intact rock) to \textasciitilde{}1000 (salt-cemented sediments at PATCX; Richter et al., 2014) — is the dominant control, varying surface $\delta v/v$ by a factor of 20. The Poisson's ratio dependence is monotonic (higher $\nu$ increases the confinement factor $b$), and the depth profile of thermoelastic $\delta v/v$ is exponential with an e-folding depth equal to the thermal skin depth. Ermert et al. (2023) expand the surface temperature into five Fourier harmonics to capture sub-annual variations in Mexico City (Figure S4). At Parkfield, Okubo et al. (2024) constrain the thermal diffusion delay $t_{\text{shift}}$ to 0–90 days. In the San Jacinto fault zone, Hillers et al. (2015) found that thermoelastic strain dominates the seasonal $\delta v/v$ in this arid setting, whereas in Oklahoma, Zhang et al. (2023) showed that thermoelastic and hydrological contributions are comparable.

---

## 4. Hydrological Loading, Pore Pressure, and Capillary Effects

### 4.1 Pore-Pressure Diffusion in Saturated Media

Roeloffs (1988) derived the poroelastic response at depth to a surface load, containing undrained and drained terms that depend on hydraulic diffusivity $c$ (varying over five orders of magnitude), Skempton coefficient $B$, and undrained Poisson's ratio $\nu_u$ (Clements and Denolle, 2023, Eq. 8–9; Figure S5). Talwani et al. (2007) extended this to time-series precipitation loading.

### 4.2 Groundwater Level Models

Okubo et al. (2024) model $\Delta$GWL from precipitation using exponential decay (their Eq. 4; Figure S6). Clements and Denolle (2023) compared multiple hydrological models across California, finding the drained poroelastic model explains 48% of sites, with basin sites showing lower diffusivities consistent with longer groundwater retention. The CDM$_k$ empirical model (Smail et al., 2019) provides a useful parameter-free alternative.

### 4.3 Competition Between Loading and Pore Pressure

Fokker et al. (2021) showed that surface loading and pore-pressure diffusion produce *opposing* $\delta v/v$ effects. Our scenarios (Figure 3) quantify this for ice loading (loading dominates for impermeable media), seasonal rainfall (pore pressure typically dominates, consistent with anti-correlation observed by Clements and Denolle, 2023), and reservoir impoundment (balance evolves with drainage time).

### 4.4 Partially Saturated Media and Dynamic Capillary Effects

The frameworks of Sections 4.1–4.3 assume fully saturated conditions below the water table. However, much of the near-surface is partially saturated, and the mechanics of the vadose zone differ fundamentally from the saturated case. Shi et al. (2026) recently demonstrated that *dynamic capillary effects* govern the transient stiffness response of partially saturated soils, producing hysteretic $\delta v/v$ signatures not captured by standard poroelastic models.

In partially saturated granular media, the shear-wave velocity depends on the effective shear modulus $\mu_{\text{eff}}$, which Shi et al. (2026) compute from contact mechanics:

$$v_S = \sqrt{\mu_{\text{eff}} / \rho} \tag{10}$$

with $\mu_{\text{eff}}$ controlled by an effective confining pressure that includes both overburden and capillary stress. A compact way to express the dynamic-capillary contribution is:

$$P_e(z,t) = \sigma_g'(z,t) + P_c^{\mathrm{eq}}(S_w) + \tau(S_w)\frac{\partial S_w}{\partial t} \tag{11}$$

Here $S_w$ is the water saturation, $\sigma_g'$ is the gravitational effective overburden, $P_c^{\mathrm{eq}}$ is the equilibrium capillary pressure, and the final term is the rate-dependent dynamic capillary stress of Hassanizadeh and Gray (1990) and Hassanizadeh et al. (2002). Sign conventions differ between soil-physics and rock-mechanics formulations; the important point for $\delta v/v$ is that the dynamic coefficient $\tau$ differs between wetting and drying, producing hysteresis. During rapid drying, dynamic capillary suction can enhance effective stress and stiffen the soil, while during wetting, near-surface saturation and pore-pressure redistribution can soften it.

Shi et al. (2026) showed three key results relevant to our framework:

1. **Dynamic capillarity is essential.** Models with static capillary stress underestimate velocity increases during evaporation by \textasciitilde{}50%, while models without any capillary stress produce significantly smaller velocity variations in both wetting and drying.

2. **Hysteresis is diagnostic.** The distinct wetting and drying $\tau(S_w)$ coefficients produce $\delta v/v$ hysteresis loops that are absent in standard poroelastic models. This hysteresis in the $\delta v/v$–saturation relationship is analogous to, but mechanistically distinct from, the mesoscopic nonlinearity (slow dynamics) observed in earthquake damage recovery (Snieder et al., 2017).

3. **Soil structure matters.** Tillage and compaction alter the pore network, modifying capillary behavior and drainage timescales. High-disturbance soils show pronounced evaporation-driven velocity rebounds and prolonged drainage, while undisturbed soils show minimal capillary effects due to efficient infiltration through well-connected pore networks.

For our unified framework, the capillary effect extends Equation 4 to partially saturated conditions. Above the water table, the effective pressure becomes saturation-dependent, and the $\delta v/v$ response to rainfall involves not just pore-pressure diffusion but also the dynamic redistribution of water between micropores and macropores. This is particularly relevant for high-frequency $\delta v/v$ measurements (\textgreater{} 2 Hz) that sense the shallowest layers where saturation changes are largest (Oakley et al., 2021). The workflow and regime map (Figure 1; detailed frequency-depth domains in Figure S12) should therefore include a "capillary/vadose zone" domain at high frequencies and shallow depths, distinct from the saturated hydrological regime.

---

## 5. Nonlinear Elasticity and the Acoustoelastic Effect

### 5.1 The Acoustoelastic Parameter and Its Detection

The Murnaghan (1937) equation of state under hydrostatic pressure — $p = af + bf^2$ where $a = 3\lambda + 2\mu$ and $b = 15\lambda + 10\mu - 27l - 9m - n$ (Figure S8) — provides the foundation for understanding velocity–pressure relations. The acoustoelastic parameter $\beta$ captures the sensitivity magnitude, spanning three orders across materials (Figure 4; Clements and Denolle, 2023).

The $\delta v/v$–strain crossplot provides a diagnostic for nonlinearity (Figure 6; detailed examples in Figure S7): linear confirms third-order sufficiency, curvature indicates higher-order terms, elliptical trajectories indicate viscoelastic phase lag, and hysteresis indicates slow dynamics. Sens-Schönfelder and Eulenfeld (2019) demonstrated that Earth tides probe in-situ nonlinearity at \textasciitilde{}50 nanostrain amplitude.

### 5.2 Geological and Material Controls on $\beta$, $\mu'$, and Nonlinear Sensitivity

The nonlinear elastic parameters are not fundamental material constants — they depend on rock *microstructure*:

**Compliant porosity and microcracks.** The dominant nonlinearity source in natural rocks is compliant porosity: thin, crack-like voids with high aspect ratios that close under compression (Walsh, 1965; Shapiro, 2003). The key parameters are crack density $\epsilon_c = N\langle a^3\rangle/V$ (Hudson, 1981), aspect ratio $\xi = w/a$ governing the closure pressure, and orientation distribution controlling anisotropic nonlinearity (Sayers and Kachanov, 1995). Critically, $|\beta|$ and $\mu'$ *decrease with confining pressure* as cracks close, explaining why $\delta v/v$ sensitivity is strongest in the shallowest layers. Fokker et al. (2021, Fig. 2g) showed $\mu' > 50$ for unconsolidated sediments but $\mu' < 10$ for consolidated rock.

**Grain contacts and cementation.** In unconsolidated granular media, Hertz-Mindlin contact theory gives $\mu_{\text{eff}} \propto P_e^{1/3}$, producing $\mu' = d\mu/dP \sim \mu/P$ — very large at low confining pressures (Dvorkin and Nur, 1996). This explains why seasonal $\delta v/v$ is typically \textgreater{}0.1% in sediments but \textless{}0.01% in crystalline rock.

**Mineralogy and cementation type.** Clay content increases compliance and $|\beta|$; salt cementation produces anomalously high $\partial(\rho v^2)/\partial\sigma_c \sim 1000$ at PATCX (Richter et al., 2014) because salt bridges are highly stress-sensitive. Foliation and bedding create intrinsic anisotropy that interacts with stress-induced anisotropy.

**Fluid saturation state.** In fully saturated media, $V_S$ is insensitive to fluid type but sensitive to effective stress. In partially saturated media, capillary suction stiffens the frame (Shi et al., 2026); $|\beta|$ can increase by factors of 2–5. Gas saturation dramatically reduces $V_P$ even at small gas fractions (patchy saturation effects).

---

## 6. Stress-Induced Anisotropy

### 6.1 Directional Velocity Changes from Deviatoric Stress

The Tromp and Trampert (2018) framework (Eq. 4) shows that deviatoric stress produces directionally dependent velocity changes. For a uniaxial vertical stress $T_{33}^0$, the induced deviatoric stress is $\boldsymbol{\tau}^0 = -(T_{33}^0/3)\,\text{diag}(1,1,-2)$. Substituting into Equation 4 and evaluating for two end-member propagation geometries — vertically propagating S-waves ($\hat{\mathbf{k}} = \hat{\mathbf{z}}$, $\hat{\mathbf{a}} = \hat{\mathbf{x}}$) versus horizontally propagating S-waves with vertical polarization ($\hat{\mathbf{k}} = \hat{\mathbf{x}}$, $\hat{\mathbf{a}} = \hat{\mathbf{z}}$) — yields a velocity-change difference between these two propagation directions:

$$\Delta\left(\frac{\delta V_S}{V_S}\right)_{\text{vert. vs. horiz.}} = \frac{T_{33}^0}{2\mu} \tag{*}$$

This directional splitting (Fokker et al., 2021, their Eqs. 9–11) is proportional to the deviatoric stress divided by the shear modulus, and is independent of $\mu'$ — meaning it exists even without nonlinear elasticity, arising purely from the stress-modified constitutive relation (Figure 5). For a fixed propagation direction, the SV-SH splitting (velocity difference between vertically and horizontally polarized shear waves) is likewise proportional to the deviatoric stress but depends on the specific geometry of propagation relative to the stress axis.

### 6.2 Microcrack Closure and the Parkfield Observation

At Parkfield, Okubo et al. (2024) found that the long-term $\delta v/v$ increase correlates with the *contractional* axial strain (oriented N35°W to N45°E) but *not* with the dilatational strain, which shows a slight extension. This anisotropic response is naturally explained by stress-induced microcrack closure (Sayers and Kachanov, 1995; Verdon et al., 2008): cracks oriented perpendicular to the maximum compressive stress close preferentially, increasing rigidity and velocity in that direction (Figure 5), while cracks parallel to the compression remain open.

The scalar (isotropic) $\delta v/v$ — as typically measured from coda waves averaging over all propagation directions — integrates over the azimuthal dependence. For a traceless deviatoric sensitivity kernel, this average is zero, meaning the isotropic $\delta v/v$ is blind to deviatoric stress (Tromp and Trampert, 2018). Detecting the deviatoric component therefore requires either *azimuthal binning* of $\delta v/v$ (measuring velocity change as a function of inter-station azimuth) or *multi-component analysis* (separating Rayleigh and Love wave contributions, as in Fokker et al., 2021). This is an underexploited observational strategy that could provide constraints on stress orientation from passive seismic monitoring.

---

## 7. Rheological Models and Depth-Resolved Joint Inversion

### 7.1 Post-Seismic Healing

The logarithmic healing model (Snieder et al., 2017; Okubo et al., 2024):

$$L(t) = -\int_{\tau_{\min}}^{\tau_{\max}} \frac{1}{\tau} \exp\left(-\frac{t - t_{EQ}}{\tau}\right) d\tau \tag{12}$$

encodes the distribution of relaxation timescales. At Parkfield, $\tau_{\max}$ is constrained to 1–30,000 years, meaning post-2004 healing may continue today (Figure 6; detailed healing curves in Figure S9). The trade-off between healing and tectonic trend is a fundamental limitation requiring independent geodetic constraints.

### 7.2 Distinguishing Rheological Models

Different rheologies produce distinct $\delta v/v$–strain signatures (Figure 6): elastic (linear crossplot), Maxwell (exponential decay), Kelvin-Voigt (delayed buildup), SLS (frequency-dependent dispersion, elliptical crossplot), and slow dynamics (logarithmic recovery, hysteresis). Tidal modulation (Sens-Schönfelder and Eulenfeld, 2019) provides the cleanest diagnostic at well-known forcing periods.

### 7.3 Frequency-Dependent Depth Tomography of Stress

A key opportunity that has been underexploited is the *frequency dependence* of $\delta v/v$. Surface waves at different frequencies have sensitivity kernels peaking at different depths (Obermann et al., 2014):

$$\frac{\delta v}{v}(f, t) = \int_0^\infty K(z, f) \cdot \frac{\delta V_S}{V_S}(z, t) \, dz \tag{13}$$

where $K(z, f)$ is the Rayleigh or Love wave phase-velocity sensitivity kernel at frequency $f$ (Figure 2a). The peak sensitivity depth is approximately $V_s / (3f)$, ranging from \textasciitilde{}50 m at 2 Hz to \textasciitilde{}5 km at 0.1 Hz for typical crustal velocities.

By measuring $\delta v/v$ simultaneously at multiple frequency bands (e.g., 0.1–0.5, 0.5–1.0, 1.0–2.0, 2.0–4.0 Hz, as in Okubo et al., 2024 and Ermert et al., 2023), one obtains a set of equations — one per frequency band — each sampling a different depth range. This is formally a linear inverse problem:

$$\mathbf{d} = \mathbf{K} \mathbf{m} \tag{14}$$

where $\mathbf{d}$ is the vector of $\delta v/v$ at $N_f$ frequencies, $\mathbf{K}$ is the kernel matrix (dimensions $N_f \times N_z$), and $\mathbf{m}$ is the depth profile of $\delta V_S / V_S$, which through the nonlinear elastic relation (Eq. 3) maps to the depth profile of stress or strain perturbation.

This inverse problem is strongly ill-conditioned: surface-wave and coda sensitivity kernels are broad, adjacent frequency bands are correlated, and the material sensitivity $\beta(z)$ or $\mu'(z)$ is rarely known independently. Any depth-resolved result therefore requires regularization, uncertainty propagation, and resolution tests. In this paper, depth-dependent inversion is a proposed workflow rather than a demonstrated result.

### 7.4 Lapse-Time Windows as Part of the Sensitivity Kernel

The observable is not simply $\delta v/v(f,t)$. It is better written as

$$d(f,\tau,W,T_{\mathrm{stack}},t) = \int_0^\infty K(z; f,\tau,W,\mathbf{g}) \, \frac{\delta V_S}{V_S}(z,t) \, dz + \epsilon \tag{15}$$

where $f$ is the frequency band, $\tau$ is the coda-window center lapse time, $W$ is the window duration, $T_{\mathrm{stack}}$ is the substack length, $\mathbf{g}$ describes source-receiver geometry and wavefield directionality, and $\epsilon$ includes measurement error and source-side bias. This notation makes explicit that coda-window choice changes the kernel, not merely the uncertainty.

Takano et al. (2019) demonstrated this directly at Izu-Oshima volcano by estimating tidal-strain sensitivity from ambient-noise cross-correlations at different lapse times. In their 2--4 Hz analysis, early lapse windows (2--7 s) showed strong velocity sensitivity to tidal dilatation and contraction, while later windows (7--35 s) showed reduced strain sensitivity. Array analysis indicated apparent velocities close to the local Rayleigh-wave group velocity in the early windows and higher apparent velocities in later windows, consistent with scattered or reflected body-wave contributions from greater depth. The result is not that early windows are universally best, but that lapse time is a physical axis of the measurement.

This creates a reproducibility problem and an opportunity. If different studies choose windows by convention, visual inspection, or inherited defaults, their $\delta v/v$ estimates may differ because they sample different wave types, depths, and nonlinear sensitivities. A reproducible workflow should therefore compute a rolling lapse-time profile from early to late coda and score each overlapping window using explicit metrics:

$$J = \sum_i w_i Q_i(f,\tau,W,T_{\mathrm{stack}}) \tag{16}$$

where $Q_i$ are normalized scores and $w_i$ are analysis-specific weights. The core metrics should include:

1. **Measurement quality:** waveform coherence, signal-to-noise ratio, stretching or MWCS fit sharpness, and estimated $\delta v/v$ uncertainty.
2. **Wave-type consistency:** apparent velocity or array slowness compared with expected Rayleigh/Love group velocities, flagging windows likely dominated by body waves or mixed wave types.
3. **Depth targeting:** overlap between $K(z; f,\tau,W)$ and the hypothesized target depth interval, or a frequency-depth proxy when full kernels are not yet available.
4. **Lapse-time stability:** sensitivity of the recovered $\delta v/v$ or $\beta$ estimate to adjacent windows, used to identify transitions in wave type or scattering regime.
5. **Temporal resolution:** substack length short enough to resolve the forcing period but long enough to maintain measurement precision.
6. **Source stability:** robustness to changes in noise-source spectrum, azimuth, and seasonal source distribution.

The future `codameter` package should implement this as a rolling window-selection layer before mechanism inversion. Rather than reporting a single hand-picked coda window, a study should report the early-to-late lapse profile, the metric weights, the stable intervals or transitions, and the sensitivity of the scientific conclusion to that ensemble. This would turn an under-documented processing choice into a reproducible part of the physical forward model.

A Bayesian version of this workflow treats each window $M_j=(f_j,\tau_j,W_j,T_{\mathrm{stack},j})$ as a competing measurement model. For a target quantity $\theta$ — for example a $\delta v/v$ value, tidal strain sensitivity, or hydrological regression coefficient — each window gives $p(\theta|y,M_j)$ and the window metrics define prior or evidence weights $p(M_j|y)$. The model-averaged posterior is

$$p(\theta|y)=\sum_j p(M_j|y)\,p(\theta|y,M_j). \tag{17}$$

The variance then separates into

$$\mathrm{Var}(\theta|y)=\mathbb{E}_{M}[\mathrm{Var}(\theta|y,M)]+\mathrm{Var}_{M}[\mathbb{E}(\theta|y,M)], \tag{18}$$

where the first term is measurement uncertainty within a window and the second term is epistemic uncertainty from method choice. This directly quantifies whether a conclusion is robust to plausible windows or depends on a particular processing convention.

### 7.5 Toward 3-D Stress/Strain Imaging

When combined with geodetic observations, the system becomes better constrained, although still non-unique:

**Vertical resolution** comes from the frequency dependence of $\delta v/v$ (different frequencies → different depths).

**Horizontal resolution** comes from the spatial array geometry: $\delta v/v$ measured at different station pairs samples different lateral regions, while GNSS provides point measurements of surface displacement and InSAR provides spatially continuous line-of-sight deformation.

**Directional resolution** comes from multi-component $\delta v/v$ analysis (ZZ, RR, TT, RT cross-correlations), which samples different combinations of Rayleigh and Love waves with different sensitivities to isotropic and anisotropic velocity changes.

**Temporal resolution** is inherently different: geodetic observations respond elastically (instantaneously to loading), while $\delta v/v$ integrates both elastic and inelastic effects. The *temporal mismatch* between geodetic strain and $\delta v/v$ is itself a diagnostic of rheology:

- If $\delta v/v$ tracks geodetic strain instantaneously → elastic response
- If $\delta v/v$ lags behind geodetic strain → viscoelastic retardation
- If $\delta v/v$ shows logarithmic recovery while geodetic strain is steady → slow dynamics
- If $\delta v/v$ shows hysteresis with geodetic strain → dynamic capillary or mesoscopic nonlinear effects

The full joint inversion then seeks to determine the 4-D (x, y, z, t) stress/strain field $\sigma_{ij}(\mathbf{x}, t)$ that simultaneously satisfies:

1. **$\delta v/v$ forward model** (Eq. 13): the frequency-dependent, depth-averaged velocity change at each station
2. **Geodetic forward model**: the surface displacement field from elastic/viscoelastic deformation
3. **Constitutive relation**: the mapping between stress/strain and velocity change via nonlinear elasticity (Eqs. 3–5, 7)
4. **Equilibrium constraint**: the induced stress must satisfy $\nabla \cdot \boldsymbol{\tau}^0 = 0$ (Tromp and Trampert, 2018)
5. **Physical forcing models**: thermoelastic (Eqs. 8–9), hydrological (Eq. 5), tectonic (from GNSS velocities)

The model parameters include depth-dependent material properties ($\beta(z)$, $\mu'(z)$, $\kappa_T$, $c$) and rheological parameters ($\tau_{\min}$, $\tau_{\max}$, viscoelastic relaxation time). The frequency dependence of $\delta v/v$ is the key ingredient that can convert a surface measurement into a depth-sensitive probe. With sufficient bandwidth, array aperture, and external constraints, this may support 3-D stress/strain models analogous to time-lapse seismic tomography but operating continuously and passively.

This approach has concrete applications: in volcanic settings, multi-frequency $\delta v/v$ combined with GNSS tilt can distinguish between shallow magma chamber pressurization (high-frequency $\delta v/v$ signal) and deep magma supply (low-frequency signal + GNSS displacement). In hydrological settings, the depth-dependent balance between loading and pore-pressure effects (Section 4.3) can be resolved rather than assumed. In tectonic settings, the depth of stress accumulation can be constrained, potentially distinguishing between shallow fault locking and deeper aseismic creep.

---

## 8. Sensitivity Analysis and Validity

### 8.1 Homogeneous Half-Space

The homogeneous half-space assumption fails when velocity contrasts exceed \textasciitilde{}2:1 within the sensitivity kernel (Figure 2; detailed validity tests in Figure S10). At soft sedimentary sites — such as Mexico City, where $V_S$ ranges from 50 m/s in the lake zone to 800 m/s in bedrock — the homogeneous assumption breaks down at all frequencies, requiring station-specific velocity profiles and proper sensitivity kernels (Ermert et al., 2023). At hard-rock stations above 1 Hz, sensitivity is confined to the upper few meters where the medium is more likely to be approximately uniform.

### 8.2 Linear Acoustoelasticity

The linear acoustoelastic approximation is valid for strains below \textasciitilde{}10$^{-5}$ (Figure S11), covering tidal, thermoelastic, and most hydrological signals, but breaks down for coseismic and strong-motion strains. The regime diagram (Figure 1; detailed version in Figure S12) maps dominant processes versus frequency and depth, including the capillary/vadose zone regime at high frequencies.

Table 1 summarizes the main parameters, ranges, and validity limits needed for applying the framework; the full parameter overview is provided as Table S1.

| Parameter | Typical range | Primary control | Main limitation |
|---|---:|---|---|
| $\kappa_T$ | 0.15–2.0 mm$^2$/s | Thermoelastic skin depth | Strongly site and moisture dependent |
| $c$ | $10^{-3}$–$10^2$ m$^2$/s | Pore-pressure diffusion | Varies by orders of magnitude across lithology |
| $B$, $\nu_u$ | 0.2–0.95, 0.25–0.49 | Drained versus undrained response | Requires saturation and poroelastic constraints |
| $\beta$ | $10$–$10^4$ | Velocity-strain sensitivity | Directional under deviatoric loading |
| $\mu'$ | $10$–$10^3$ | Stress-to-velocity conversion | Depends on pressure, cracks, and sediment fabric |
| $\tau_{\min}$, $\tau_{\max}$ | days to $>10^4$ yr | Slow-dynamics recovery | Trades off with long-term tectonic trend |
| $K(z,f)$ | site specific | Frequency-depth sensitivity | Broad, correlated kernels make inversion ill-conditioned |

### 8.3 Spatial Generalization: From 1-D to 3-D

The forward models in Sections 3–6 assume laterally homogeneous (1-D) structure. Generalizing to 3-D requires accounting for spatially varying velocity structure, material properties, and observation geometry.

**Spatially varying sensitivity kernels.** The kernel $K(z, f)$ in Equation 1 depends on the local $V_S(z)$, $V_P(z)$, and $\rho(z)$ profiles. At sites with laterally varying geology — sedimentary basins (Ermert et al., 2023), fault zones (Hillers et al., 2015), volcanic edifices (Donaldson et al., 2019) — the kernel differs between station pairs. Ermert et al. (2023) addressed this by computing station-specific 1-D profiles using geotechnical classifications and aquitard thickness. A fully 3-D treatment requires 3-D sensitivity kernels computed with adjoint methods (Tromp et al., 2005) or spectral-element simulations.

**Spatially varying material properties.** The nonlinear parameters ($\beta$, $\mu'$, $\kappa_T$, $c$) vary laterally. In a sedimentary basin, $\mu'$ is large in the basin fill and small in the basement; hydraulic diffusivity $c$ can vary by orders of magnitude across fault zones and clay layers. Clements and Denolle (2023) demonstrated this: basin sites show low diffusivity (long hydrological memory) while mountain sites show high diffusivity (rapid drainage).

**What additional Earth observations are needed?** Generalizing to 3-D requires: (1) a **3-D $V_S$ model** from ambient noise tomography at the monitoring frequencies, providing the base model for sensitivity kernels; (2) a **$V_P/V_S$ ratio** from joint Rayleigh-Love inversion, constraining Poisson's ratio for the thermoelastic model; (3) a **density model** from gravity or empirical relations, for converting $\delta V_S/V_S$ to $\delta\mu/\mu$; (4) **near-surface geotechnical data** ($V_{S30}$, water table depth, porosity) constraining $\mu'$, $\kappa_T$, and saturation state at each site; (5) **co-located geodetic coverage** (GNSS, InSAR) for independent strain constraints; and (6) **distributed meteorological and hydrological data** co-located with the seismic array. Dense arrays — nodal deployments, distributed acoustic sensing (DAS; Rodríguez Tribaldos and Ajo-Franklin, 2021; Shi et al., 2026) — provide the spatial resolution needed to resolve lateral variations in both $\delta v/v$ and the material properties controlling it.

---

## 9. Application: Stress at Depth from $\delta v/v$ at Parkfield, Cascadia, and Kīlauea

We now apply the unified framework to three contrasting settings using only published $\delta v/v$ measurements, velocity profiles, and geodetic strain constraints. No new waveform processing is performed; we use the framework's equations (principally Eqs. 3, 4, 7, and 13) to extract quantitative stress predictions from existing observations.

### 9.1 Parkfield: Deviatoric Stress on a Strike-Slip Fault

#### 9.1.1 Published observations

Okubo et al. (2024) measured a linear $\delta v/v$ trend of $b_0 = 0.0048\%$/yr (stretching method, 0.9–1.2 Hz band) over 20 years at the HRSN array straddling the San Andreas Fault. The GNSS-derived dilatational strain shows slight *extension* — opposite to what $\delta v/v = \beta\epsilon_{kk}$ predicts for a velocity *increase*. However, the rotated axial strain shows *contraction* in the azimuth range N35°W to N45°E, consistent with $S_{Hmax} \approx$ N15°E measured from SAFOD wellbore breakouts (Boness and Zoback, 2006). The contractional strain rate from GNSS is approximately 200 nanostrain/yr (Okubo et al., 2024, their Fig. 14).

#### 9.1.2 Velocity profile and depth sensitivity

From the SAFOD Pilot Hole (Boness and Zoback, 2006), the main borehole (Jeppson and Tobin, 2015), and regional tomography (Zhang et al., 2009), the velocity structure at the HRSN site transitions from Tertiary sediments ($V_S \sim 1.2$ km/s) to Salinian granite ($V_S \sim 3.2$ km/s) at ~0.77 km depth. At the 0.9–1.2 Hz measurement band, the peak Rayleigh wave sensitivity is at $z_{\text{peak}} \approx V_S/(3f) \approx 0.8$ km — the weathered granite layer, where $V_S \approx 2.5$ km/s, $\rho \approx 2500$ kg/m³, giving $\mu \approx 15.6$ GPa and $\kappa \approx 29.8$ GPa.

#### 9.1.3 Framework prediction

Since the isotropic formulation fails (dilatation is extensional), the $\delta v/v$ increase is driven by the *deviatoric* component — specifically, microcrack closure under contractional loading (Sayers and Kachanov, 1995; Verdon et al., 2008). From the directional acoustoelastic ratio:

$$|\beta_{\text{axial}}| = \frac{\delta v/v}{\epsilon_{\text{contractional}}} = \frac{4.8 \times 10^{-5}}{2.0 \times 10^{-7}} \approx 240$$

This falls between intact granite ($|\beta| \sim 10$–50) and soft sediments ($|\beta| \sim 500$–10,000), consistent with fractured Salinian granite. The bridge relation (Eq. 7), noting that it was derived under isotropic loading and gives an order-of-magnitude estimate when applied to a directional $\beta$, yields $\mu' = 2\mu|\beta|/\kappa \approx 251$, plausible for fractured rock at ~20 MPa confining pressure.

The deviatoric stress rate from Equation 4 is:

$$\dot{\sigma}_{\text{dev}} = \frac{4\mu \cdot (\delta v/v)}{\mu'} = \frac{4 \times 15.6 \times 10^9 \times 4.8 \times 10^{-5}}{251} \approx 12 \text{ kPa/yr}$$

Over 20 years: **cumulative deviatoric stress ≈ 0.24 MPa** at ~0.8 km depth. A direct cross-check from the GNSS strain ($\sigma = E\epsilon \approx 8.7$ kPa/yr) gives agreement within a factor of 1.4.

#### 9.1.4 Inferred TOE parameters

From $|\beta| \approx 240$ and Equation 3: $l + 2m = (\beta - 3/2)(\lambda + 2\mu) \approx -12{,}200$ GPa — falling between intact Westerly granite ($-3{,}000$ GPa) and sandstone ($-50{,}000$ GPa), consistent with the crack-rich shallow fault zone. Individual Murnaghan constants ($l$, $m$, $n$) cannot be resolved from a single loading path; tidal azimuthal analysis (Sens-Schönfelder and Eulenfeld, 2019) or triaxial laboratory measurements on SAFOD core would be needed.

#### 9.1.5 Rheological model

The $\delta v/v$–strain relationship is linear with no hysteresis, indicating elastic tectonic loading on aligned cracks. The coexisting logarithmic post-seismic healing (Snieder et al., 2017) implies a dual-population model: tectonically aligned cracks respond elastically to interseismic compression, while randomly oriented damage cracks from the 2004 Parkfield earthquake heal via slow dynamics on different timescales.

### 9.2 Cascadia: Volumetric Strain Accumulation on a Subduction Megathrust

#### 9.2.1 Published observations

Kidiwela et al. (2026) monitored $\delta v/v$ from the Ocean Networks Canada seafloor observatory for 13 years. At Northern Cascadia (station NC89, Clayoquot Canyon), the 1–3 Hz $\delta v/v$ shows a persistent linear increase of $+0.038\%$/yr. The borehole pressure data from the nearby Hole 1364A gives a compressional volumetric strain rate of 0.12 μstrain/yr (Davis et al., 2024), and the linear geodetic convergence rate of 4.1 cm/yr over ~100 km gives a strain rate of ~0.4 μstrain/yr. In central Cascadia (stations HYSB1 and HYS14, Hydrate Ridge), a lower background trend is punctuated by a slow slip event (2016, $\delta v/v$ drop of –0.2% at 3–5 Hz) and a transient fluid migration event (2019, $\delta v/v$ decrease with 34-day inter-station lag at 1–3 Hz).

#### 9.2.2 Velocity profile and depth sensitivity

From the Ridge-to-Trench models (Han et al., 2017) and the USGS Cascadia CVM v1.7, the offshore accretionary wedge consists of very soft, fluid-rich marine sediments: $V_S \approx 0.3$–$0.6$ km/s at 0–0.2 km below the seafloor, increasing to $V_S \approx 1.2$–$2.0$ km/s at 1–3 km depth. At 1 Hz, the sensitivity depth is ~0.2–0.3 km, where $V_S \approx 0.5$ km/s, $\rho \approx 1900$ kg/m³, $\mu \approx 0.475$ GPa, and $\kappa \approx 4.86$ GPa — two orders of magnitude softer than the Parkfield granite.

#### 9.2.3 Framework prediction (Northern Cascadia)

Kidiwela et al. (2026) calibrated $\beta = 3160$ from the $\delta v/v$ trend and the borehole strain measurement. This makes the borehole comparison a calibration and internal consistency test, not an independent validation of the stress conversion. The bridge relation (Eq. 7) gives:

$$\mu' = \frac{2\mu|\beta|}{\kappa} = \frac{2 \times 0.475 \times 3160}{4.86} \approx 618$$

This large $\mu'$ is physically consistent with high-porosity, weakly cemented marine sediments where grain-contact mechanics (Dvorkin and Nur, 1996) dominate the elastic response.

The stress rate from the isotropic term of Equation 4:

$$\dot{\sigma}_{\text{iso}} = \frac{2\mu \cdot (\delta v/v)}{\mu'} = \frac{2 \times 0.475 \times 10^9 \times 3.8 \times 10^{-4}}{618} \approx 0.58 \text{ kPa/yr}$$

Cross-checking: $\kappa \cdot \epsilon_{kk} = 4.86 \times 10^9 \times 1.2 \times 10^{-7} = 0.58$ kPa/yr. The agreement is expected because the same borehole strain enters the calibration of $\beta$; the useful result is that the inferred $\mu'$ is physically plausible for weak, high-porosity marine sediment. Over 13 years: cumulative stress ≈ 7.6 kPa at ~0.2 km below the seafloor.

#### 9.2.4 Isotropic success and the loading geometry

Crucially, the isotropic framework *succeeds* at Cascadia where it *fails* at Parkfield. The reason is geometric: subduction convergence compresses the accretionary wedge *volumetrically* (dilatation is compressive), so $\delta v/v = \beta\epsilon_{kk}$ correctly predicts a positive trend. At Parkfield, strike-slip shear produces *negligible dilatation* with the velocity increase driven entirely by the deviatoric component. The unified framework predicts when each formulation is appropriate, based on the loading geometry and the sign of the dilatational strain.

#### 9.2.5 Locking ratio from multi-frequency $\delta v/v$

At low frequencies (0.1–0.3 Hz, sensitivity ~8 km depth near the plate interface), the $\delta v/v$ trend rates are +0.006%/yr (northern) and +0.003%/yr (central). If the effective $\beta$ and kernels are comparable between the two segments, this 2:1 ratio is consistent with a 2:1 strain-rate or locking contrast, broadly matching full locking in northern Cascadia and ~50% locking in central Cascadia inferred from onshore geodetic inversions (Li et al., 2018). This is a promising but conditional example of the multi-frequency depth profiling envisioned in §7.3; a rigorous locking estimate would require segment-specific sensitivity kernels and nonlinear parameters.

#### 9.2.6 Transient pore pressure from the 2019 fluid pulse

The 2019 $\delta v/v$ decrease at central Cascadia corresponds to a transient pore pressure increase, quantified using the poroelastic term (Eq. 5): $u^0 = 2\mu|\delta v/v|/\mu' \approx 2$–4 kPa. This is a small perturbation ($\sim 10^{-4}$ of the background) but seismically detectable because $\mu' \approx 620$ amplifies the sensitivity of the soft sediments. The 34-day inter-station lag yields a horizontal fluid migration velocity of 0.58 km/day, and the frequency-dependent vertical lags give a diffusivity of $D \approx 3.8 \times 10^{-4}$ m²/s — within the range for accretionary wedge sediments.

### 9.3 Kīlauea: Anisotropic Stress from Ring Fractures During Caldera Collapse

#### 9.3.1 Published observations

Hotovec-Ellis et al. (2022) used repeating-earthquake-based coda wave interferometry during the 2018 Kīlauea caldera collapse to measure $\delta v/v$ at stations surrounding the summit. They observed two distinct timescales: (1) short-term sawtooth cycles of ~0.5–1% $\delta v/v$ per collapse event (~hourly), where velocity *increased* during each ~M5 collapse and *decreased* between collapses; and (2) a long-term decrease of –0.2 to –0.4%/day from 1 June to ~26 June, followed by stabilization. The collapse-induced pressure change in the sub-caldera reservoir was ~3 MPa (Segall et al., 2020), with the reservoir modeled as a prolate spheroid centered at 1.94 km depth ($\mu = 3$ GPa, $\nu = 0.25$; Anderson et al., 2019).

#### 9.3.2 The isotropic framework fails — again

The critical finding is that modeled *volumetric* strain from reservoir pressurization predicts *extension* (hence velocity *decrease*) in most regions surrounding the reservoir — the opposite of the observed co-collapse velocity *increase* (Hotovec-Ellis et al., 2022, their Fig. 4a). This is the same diagnostic failure as Parkfield: the isotropic $\delta v/v = \beta\epsilon_{kk}$ predicts the wrong sign.

However, the modeled *radial* strain component (Fig. 4b) does predict the correct sign. Hotovec-Ellis et al. proposed that the dominant ring fractures concentric to the caldera (Neal and Lockwood, 2003) act as the controlling microstructure: reservoir pressurization compresses these vertical ring fractures in the radial direction, closing them and increasing velocity. This is precisely the directional mechanism described by Equation 4 — the deviatoric stress projection $\hat{\mathbf{k}} \cdot \boldsymbol{\tau}^0 \cdot \hat{\mathbf{k}}$ onto the ring-fracture normal determines the sign of $\delta v/v$, not the volumetric trace.

#### 9.3.3 Framework prediction

For the short-term co-collapse signal, the GNSS line-length change across the caldera (CRIM–UWEV, ~2 km baseline) shows ~20–50 mm offsets per collapse, giving a radial strain of $\epsilon_{\text{radial}} \approx 15$–$25$ μstrain per event. With $\delta v/v \approx 0.5\%$ per collapse at ~2 km distance:

$$|\beta_{\text{radial}}| = \frac{\delta v/v}{\epsilon_{\text{radial}}} = \frac{5 \times 10^{-3}}{2 \times 10^{-5}} \approx 250\text{–}330$$

This is remarkably similar to the Parkfield value ($\beta_{\text{axial}} \approx 240$), despite the completely different tectonic setting and rock type (fractured basalt vs. fractured granite). The convergence suggests that $|\beta| \sim 200$–$400$ is characteristic of *fractured crystalline rock* regardless of composition, controlled primarily by crack density and aspect ratio rather than mineralogy.

From the bridge relation (using $\kappa = 2\mu(1+\nu)/(3(1-2\nu)) = 5.0$ GPa for $\mu = 3$ GPa, $\nu = 0.25$): $\mu' = 2\mu|\beta|/\kappa = 2 \times 3 \times 300 / 5 \approx 360$, intermediate between the Parkfield granite ($\mu' \approx 250$) and Cascadia sediment ($\mu' \approx 620$).

The radial stress perturbation at ~2 km from the reservoir, estimated from Equation 4, gives $\sigma_{\text{radial}} = 4\mu(\delta v/v)/\mu' = 4 \times 3 \times 10^9 \times 5 \times 10^{-3}/360 \approx 170$ kPa per collapse. The expected radial stress from a pressurized spheroid ($\Delta P = 3$ MPa, $a \approx 1$ km) at $R = 2$ km decays as $(a/R)^3$, giving $\sigma_{\text{radial}} \sim 3 \times 10^6 \times (0.5)^3 \approx 375$ kPa — agreement within a factor of 2, consistent with the simplified geometry.

#### 9.3.4 The long-term: inelastic fracture creation

The long-term velocity decrease (–0.3%/day for ~26 days, total ~–8%, though Hotovec-Ellis et al. note that whether these accumulated changes combine linearly is unresolved) ceased when the peripheral ring fault completed its formation at the surface. Hotovec-Ellis et al. attribute this to *inelastic* fracture creation during fault growth — a mechanism outside the purely elastic acoustoelastic framework of Equation 3. Using the GNSS shortening rate across the caldera (~40 mm/day, $\epsilon \approx 20$ μstrain/day):

$$|\beta_{\text{long-term}}| = \frac{0.003}{2 \times 10^{-5}} \approx 150$$

The lower effective $|\beta|$ for the long-term signal (150 vs. 300 for the short-term) is physically meaningful: it reflects the competition between elastic crack closure (which increases velocity) and inelastic fracture generation (which decreases velocity). The net $\delta v/v$ per unit strain is smaller because new cracks partially offset the stiffening from closure of existing cracks — a signature of *damage accumulation* that is absent in the purely elastic short-term response.

#### 9.3.5 Implications for fracture geometry as a diagnostic

The Kīlauea case extends the anisotropy diagnostic from §6 to volcanic settings: *the dominant fracture orientation determines which strain component controls $\delta v/v$*. At Parkfield, fault-parallel fractures respond to fault-normal contractional strain. At Kīlauea, ring fractures respond to radial strain from reservoir pressurization. At Piton de la Fournaise, where radial dike fractures dominate (Carter et al., 2007), the *opposite* response to pressurization is observed (Rivet et al., 2014) — consistent with radial fractures opening under radial extension. The unified framework (Eq. 4) captures all three cases through the directional projection of the deviatoric stress onto the fracture-normal direction, without requiring separate physical models for each setting.

### 9.4 Cross-Site Synthesis

**Table 2** summarizes the key parameters and predictions across all three sites; Figure 7 visualizes the same comparison as the main synthesis result.

| Property | Parkfield | Northern Cascadia | Kīlauea (short-term) |
|----------|-----------|-------------------|----------------------|
| Tectonic setting | Strike-slip | Subduction (locked) | Volcanic caldera collapse |
| $\delta v/v$ signal | +0.005%/yr (secular) | +0.038%/yr (secular) | +0.5% per collapse (~hourly) |
| Sensitivity depth | ~0.8 km (granite) | ~0.2 km (sediment) | ~1–2 km (basalt) |
| $V_S$ at depth | 2.5 km/s | 0.5 km/s | ~2.5 km/s |
| $\mu$ at depth | 15.6 GPa | 0.475 GPa | 3.0 GPa |
| $|\beta|$ (effective) | 240 (axial) | 3160 (isotropic) | 250–330 (radial) |
| $\mu'$ (inferred) | 251 | 618 | ~360 |
| Stress perturbation | 12 kPa/yr (deviatoric) | 0.58 kPa/yr (isotropic) | ~170 kPa per collapse |
| Isotropic framework | **Fails** | **Succeeds** | **Fails** |
| Dominant fracture geometry | Fault-parallel cracks | Distributed (no preferred) | Concentric ring fractures |
| Controlling strain component | Fault-normal contraction | Volumetric compression | Radial (reservoir) compression |
| Cross-check | GNSS (factor 1.4) | Borehole-calibrated consistency | Geodetic ΔP (factor ~2) |

The three-site comparison reveals a clear pattern: **the isotropic formulation works only when loading is predominantly volumetric (Cascadia subduction), and fails when loading is deviatoric — whether from strike-slip shear (Parkfield) or magmatic pressurization (Kīlauea)**. In both deviatoric cases, the dominant fracture fabric determines which strain component controls $\delta v/v$: fault-parallel cracks at Parkfield respond to fault-normal contraction, ring fractures at Kīlauea respond to radial compression, and radial dike fractures at Piton de la Fournaise respond to radial extension (producing the opposite $\delta v/v$ sign). The effective $|\beta|$ for fractured crystalline rock (granite, basalt) clusters around 200–400 regardless of composition, while unconsolidated marine sediment gives $|\beta| \sim 3000$ — a factor of ~10 that maps directly onto the difference in compliant porosity and grain-contact mechanics (§5.2).

**Comparing $\delta v/v$ amplitudes across sites without normalizing by $\beta$ leads to qualitatively wrong conclusions about relative stress levels.** The Cascadia dv/v trend is 8× larger than Parkfield's, yet the Parkfield stress rate is 20× larger. The Kīlauea co-collapse signal (~0.5%) is 100× the Parkfield annual trend, but the stress perturbation (~170 kPa) is only 14× larger — the remaining factor of 7 is absorbed by the similar $\beta$ values and the very different timescales.

---

## 10. Discussion

### 10.1 The Unifying Power of Nonlinear Elasticity

All $\delta v/v$ sources — thermoelastic, hydrological, tectonic, volcanic — operate through the same mechanism: stress-dependent modification of elastic moduli via compliant porosity and microcracks. The *same* material parameters ($\beta$, $\mu'$, $\partial(\rho v^2)/\partial\sigma_c$) should consistently explain all forcings at a given site. Inconsistencies diagnose either unmodeled forcings or violations of the isotropic assumption.

### 10.2 The Capillary Frontier

The Shi et al. (2026) results on dynamic capillary effects represent a significant extension of the $\delta v/v$ framework into unsaturated media. The hysteretic $\delta v/v$ response to wetting-drying cycles — governed by the rate-dependent dynamic coefficient $\tau(S_w)$ — is mechanistically distinct from both the Fokker et al. (2021) poroelastic framework (which assumes full saturation) and the Snieder et al. (2017) slow dynamics (which involves crack healing). This opens a "capillary window" for monitoring soil moisture, agricultural disturbance, and vadose-zone hydrology with seismic methods. Future work should integrate the Hertz-Mindlin + dynamic capillarity model of Shi et al. (2026) into the depth-integrated forward model (Eq. 1) to predict multi-frequency $\delta v/v$ in partially saturated settings.

### 10.3 Implications for Monitoring Applications

For **volcanic monitoring**, environmental signals of \textasciitilde{}0.05% can mask pre-eruptive signals. The framework enables forward modeling of expected environmental $\delta v/v$, and the anisotropic formulation can detect oriented magmatic stress. The Kīlauea case (§9.3) demonstrates that the dominant fracture fabric — ring fractures vs. radial dikes — determines the *sign* of the $\delta v/v$ response to reservoir pressurization, a prediction testable at other caldera systems.

For **tectonic monitoring**, the Parkfield case shows $\delta v/v$ detects inter-seismic loading at \textasciitilde{}0.005%/yr. The deviatoric component is essential — dilatational strain alone cannot explain the observation (Okubo et al., 2024).

For **hydrological monitoring**, the depth-resolved approach (Section 7.3) can separate shallow capillary effects from deep pore-pressure changes, and the competition between loading and pore-pressure effects can be resolved rather than assumed.

### 10.4 Practical Workflow for Applying the Framework at a New Site

We summarize the steps a researcher would take to apply this framework:

1. **Characterize the site.** Obtain a 1-D (or 3-D) $V_S(z)$, $V_P(z)$, and $\rho(z)$ profile from ambient noise tomography, active surveys, or geotechnical databases. Estimate $\mu(z)$ and $\kappa(z)$ from these profiles.
2. **Design and score measurement windows.** Define a candidate grid of frequency bands, coda-window starts and ends, and substack lengths. Rank windows using coherence, signal-to-noise ratio, uncertainty, apparent wave type, depth targeting, lapse-time stability, and source-stability metrics (§7.4). Report the candidate grid and the selected-window ensemble.
3. **Compute sensitivity kernels.** Use the velocity profile to compute Rayleigh and Love wave phase-velocity sensitivity kernels $K(z,f)$ at the monitoring frequencies (e.g., using the adjoint method of Tromp et al., 2005, or eigenfunction codes). Where possible, extend the kernel description to include lapse time and window duration, $K(z;f,\tau,W)$.
4. **Estimate nonlinear parameters.** Compute $\mu'(z) = d\mu/dP$ from the shear-modulus–pressure profile, or use empirical values for the local lithology. The bridge relation (Eq. 7) then gives $\beta(z)$.
5. **Forward model environmental $\delta v/v$.** Using local temperature records, compute the thermoelastic $\delta v/v$ via the Berger-Richter model (Eqs. 8–9). Using precipitation and/or groundwater data, compute the hydrological $\delta v/v$ via the Roeloffs-Fokker model (Eq. 5). Integrate depth-dependent $\delta V_S/V_S(z,t)$ through the kernels (Eq. 1 or Eq. 15) to predict $\delta v/v(f,\tau,W,t)$.
6. **Subtract and interpret residuals.** Remove the modeled environmental contributions from the observed $\delta v/v$ time series. Residuals may contain tectonic, volcanic, or anthropogenic signals. A robust residual should persist across the top-ranked window ensemble.
7. **Compare with geodesy.** Overlay residual $\delta v/v$ with GNSS-derived strain or InSAR deformation. The temporal relationship (instantaneous tracking, lag, or hysteresis) diagnoses the rheological regime (§7.2). Multi-frequency and multi-lapse residuals constrain the depth distribution and wave-type dependence of the anomalous signal (§7.3--7.4).

### 10.5 Limitations

The data applications in Section 9 use published $\delta v/v$ measurements and velocity profiles rather than reprocessed waveform data; the quantitative predictions (stress rates, $\beta$, $\mu'$) depend on the accuracy of the input values from Okubo et al. (2024), Kidiwela et al. (2026), Hotovec-Ellis et al. (2022), and the respective velocity models. The Parkfield GNSS cross-check has a factor-of-1.4 discrepancy that may reflect depth-transfer effects between the surface strain measurement and the 0.8 km sensitivity depth. The Cascadia borehole comparison is a calibration-based consistency check rather than an independent validation because the borehole strain is used to determine $\beta$. The Kīlauea estimate uses a simplified spheroidal reservoir geometry; more complex geometries (including the piston and ring fault) would modify the strain field. The directional bridge relation ($\mu'$ from $\beta_{\text{axial}}$ or $\beta_{\text{radial}}$) is an order-of-magnitude approximation; Equation 7 was derived for isotropic loading.

Additional limitations include: the forward models are primarily 1-D, while real geology has lateral heterogeneity (§8.3). Source-side noise-field variations can produce apparent $\delta v/v$ (Zhan et al., 2013; Okubo et al., 2024 mitigate this with multi-component analysis). The decomposition into forcings (Eq. 6) is non-unique without independent geodetic constraints. Mesoscopic nonlinearity at high strains requires constitutive models beyond the Murnaghan framework (Gassenmeier et al., 2016). The capillary model (§4.4) is presented as external evidence from Shi et al. (2026) rather than implemented in the companion notebooks. The proposed lapse-window objective (§7.4) is a design framework, not yet a universal standard; its weights should be tuned to the scientific target and validated against synthetic recovery tests and independent strain or hydrological observations.

---

## 11. Conclusions

1. All major sources of $\delta v/v$ variability operate through nonlinear elasticity. The Murnaghan (1937) framework provides the formal foundation.
2. The strain formulation ($\delta v/v = \beta \epsilon_{kk}$) and stress formulation ($\delta V_S/V_S = \mu' p^0 / 2\mu$) are unified under isotropic loading by the bridge relation $\beta = -\mu'\kappa/(2\mu)$ (Eq. 7), but diverge under deviatoric loading — a divergence that carries diagnostic information about stress orientation.
3. Thermoelastic $\delta v/v$ is controlled primarily by $\partial(\rho v^2)/\partial\sigma_c$ (50–1000), with annual amplitudes of 0.01–0.3%.
4. Hydrological loading produces competing effects whose balance depends on permeability and drainage (Fokker et al., 2021).
5. Dynamic capillary effects in partially saturated media produce hysteretic $\delta v/v$ distinct from standard poroelastic responses (Shi et al., 2026).
6. Stress-induced anisotropy from microcrack closure explains why $\delta v/v$ correlates with contractional but not dilatational strain (Okubo et al., 2024). Detecting deviatoric stress requires azimuthal binning or multi-component analysis.
7. At Parkfield, the framework predicts a deviatoric stress rate of ~12 kPa/yr at ~0.8 km depth with $\beta_{\text{axial}} \approx 240$ and $\mu' \approx 250$, cross-checked against GNSS strain. At Cascadia, the borehole-calibrated framework gives an isotropic stress rate of 0.58 kPa/yr at ~0.2 km depth with $\beta \approx 3160$ and $\mu' \approx 620$. At Kīlauea, co-collapse radial stress of ~170 kPa is recovered from $\delta v/v \approx 0.5\%$ with $\beta_{\text{radial}} \approx 300$ and $\mu' \approx 360$, consistent with the geodetically constrained reservoir pressure change within a factor of 2. The effective $|\beta|$ for fractured crystalline rock (granite, basalt) clusters around 200–400, while unconsolidated marine sediment gives $|\beta| \sim 3000$.
8. The loading geometry and fracture fabric jointly determine which framework applies: isotropic $\delta v/v = \beta\epsilon_{kk}$ succeeds at Cascadia (volumetric compression, no preferred fracture orientation) but fails at both Parkfield (strike-slip shear, fault-parallel cracks) and Kīlauea (magmatic pressurization, concentric ring fractures). The dominant fracture orientation determines the controlling strain component — fault-normal contraction at Parkfield, radial compression at Kīlauea — and this directional sensitivity explains the opposite $\delta v/v$ response to pressurization observed at Piton de la Fournaise (radial dike fractures).
9. Multi-frequency $\delta v/v$ combined with GNSS/InSAR has the potential to enable depth-resolved 3-D stress/strain imaging, provided sensitivity kernels, regularization, and independent material constraints are available. At Cascadia, the 2:1 ratio of low-frequency $\delta v/v$ trends between northern and central segments is consistent with the locking contrast inferred from onshore geodesy under comparable-kernel and comparable-$\beta$ assumptions.
10. Coda-window choice is a physical part of the measurement, not a neutral processing detail. The observable should be reported as $\delta v/v(f,\tau,W,T_{\mathrm{stack}},t)$, and window selection should be based on explicit metrics for coherence, uncertainty, wave type, depth targeting, lapse-time stability, temporal resolution, and source stability. This is the first target for the `codameter` implementation because it directly addresses reproducibility.
11. Rheological diagnostics from $\delta v/v$–strain crossplots and tidal modulation distinguish elastic, viscoelastic, and slow-dynamics behavior. At Parkfield, a dual-population model (elastic tectonic + slow-dynamics healing) is required.
12. Linear acoustoelasticity is valid for strains below \textasciitilde{}10$^{-5}$; the nonlinear parameters ($\beta$, $\mu'$) are controlled by rock microstructure and decrease with confining pressure, spanning $|\beta| \sim 240$ (fractured granite) to $|\beta| \sim 3160$ (marine sediment).

---

## Statement of AI Use

This manuscript was produced through a human–AI collaboration. The human author (M.A. Denolle) provided scientific direction, problem framing, selection of the knowledge base, iterative feedback, and the insight to integrate partially saturated media with dynamic capillary effects. The AI assistant (Claude Opus 4, Anthropic) provided literature synthesis, numerical implementation, figure generation, and manuscript drafting. All scientific claims are grounded in published, peer-reviewed literature. Full documentation of the human prompts, AI reasoning, and model information is provided in `docs/ai_documentation/`. See the model card (`docs/ai_documentation/03_model_card.md`) for details.

---

## Acknowledgments

M.A.D. acknowledges support from the Packard Foundation and the Murdock Charitable Trust. The project knowledge base includes papers by Okubo et al. (2024), Clements and Denolle (2023), Ermert et al. (2023), Richter et al. (2014), Fokker et al. (2021), Tromp and Trampert (2018), Murnaghan (1937), Shi et al. (2026), and Verdon (2008). Additional literature and metadata checks were performed with disclosed AI-assisted search tools and verified against cited sources where used.

## Data Availability

The companion Jupyter notebooks and figure-generation code are maintained in this repository and will be archived on Zenodo before publication; the archive DOI is pending. The notebooks use standard Python scientific libraries (NumPy, SciPy, Matplotlib).

---


---

## References

Ben-Zion, Y., & Leary, P. (1986). Thermoelastic strain in a half-space covered by unconsolidated material. *Bulletin of the Seismological Society of America*, 76, 1447–1460.

Anderson, K. R., Johanson, I. A., Patrick, M. R., Gu, M., Segall, P., Poland, M. P., et al. (2019). Magma reservoir failure and the onset of caldera collapse at Kīlauea volcano in 2018. *Science*, 366, eaaz1822.

Boness, N. L., & Zoback, M. D. (2006). Mapping stress and structurally controlled crustal shear velocity anisotropy with a multi-layered model. *Geophysical Research Letters*, 33, L01304.

Berger, J. (1975). A note on thermoelastic strains and tilts. *Journal of Geophysical Research*, 80, 274–277.

Birch, F. (1961). The velocity of compressional waves in rocks to 10 kilobars, part 2. *Journal of Geophysical Research*, 66, 2199–2224.

Brenguier, F., Campillo, M., Hadziioannou, C., Shapiro, N. M., Nadeau, R. M., & Larose, É. (2008a). Postseismic relaxation along the San Andreas fault at Parkfield. *Science*, 321, 1478–1481.

Brenguier, F., Shapiro, N. M., Campillo, M., Ferrazzini, V., Duputel, Z., Coutant, O., & Nercessian, A. (2008b). Towards forecasting volcanic eruptions using seismic noise. *Nature Geoscience*, 1, 126–130.

Carter, A., van Wyk de Vries, B., Kelfoun, K., Bachèlery, P., & Briole, P. (2007). Pits, rifts and slumps: The summit structure of Piton de la Fournaise. *Bulletin of Volcanology*, 69, 741–756.

Clarke, D., Zaccarelli, L., Shapiro, N. M., & Brenguier, F. (2011). Assessment of resolution and accuracy of the moving window cross spectral technique for monitoring crustal temporal variations using ambient seismic noise. *Geophysical Journal International*, 186, 867–882.

Clements, T., & Denolle, M. A. (2018). Tracking groundwater levels using the ambient seismic field. *Geophysical Research Letters*, 45, 6459–6465.

Clements, T., & Denolle, M. A. (2023). The seismic signature of California's earthquakes, droughts, and floods. *Journal of Geophysical Research: Solid Earth*, 128, e2022JB025553.

D'Auria, L., et al. (2023). Spatio-temporal velocity variations observed during the pre-eruptive episode of La Palma 2021 eruption inferred from ambient noise interferometry. *Scientific Reports*, 13, 12203.

Davis, E. E., Sun, T., Heesemann, M., Becker, K., & Schlesinger, A. (2024). Long-term offshore borehole fluid-pressure monitoring at the northern Cascadia subduction zone and inferences regarding the state of megathrust locking. *Geochemistry, Geophysics, Geosystems*, 24, e2023GC010910.

Delouche, E., et al. (2023). Seasonal seismic velocity variations measured using seismic noise autocorrelations to monitor the dynamic of aquifers in Greece. *Journal of Geophysical Research: Solid Earth*, 128, e2023JB026759.

Donaldson, C., Winder, T., Caudron, C., & White, R. S. (2019). Crustal seismic velocity responds to a magmatic intrusion and seasonal loading in Iceland's Northern Volcanic Zone. *Science Advances*, 5, eaax6642.

Dvorkin, J., & Nur, A. (1996). Elasticity of high-porosity sandstones: Theory for two North Sea data sets. *Geophysics*, 61, 1363–1370.

Ermert, L. A., Cabral-Cano, E., Chaussard, E., et al. (2023). Probing environmental and tectonic changes underneath Mexico City with the urban seismic field. *Solid Earth*, 14, 529–549.

Feng, K.-F., Huang, H.-H., Hsu, Y.-J., & Wu, Y.-M. (2021). Controls on seasonal variations of crustal seismic velocity in Taiwan. *Journal of Geophysical Research: Solid Earth*, 126, e2021JB022650.

Fokker, E., Ruigrok, E., Hawkins, R., & Trampert, J. (2021). Physics-based relationship for pore pressure and vertical stress monitoring using seismic velocity variations. *Remote Sensing*, 13, 2684.

Gassenmeier, M., Sens-Schönfelder, C., Eulenfeld, T., Bartsch, M., Victor, P., Tilmann, F., & Korn, M. (2016). Field observations of seismic velocity changes caused by shaking-induced damage and healing due to mesoscopic nonlinearity. *Geophysical Journal International*, 204, 1490–1502.

Han, S., Bangs, N. L., Carbotte, S. M., Saffer, D. M., & Gibson, J. C. (2017). Links between sediment consolidation and Cascadia megathrust slip behaviour. *Nature Geoscience*, 10, 954–959.

Hotovec-Ellis, A. J., Shiro, B. R., Shelly, D. R., Anderson, K. R., Haney, M. M., Thelen, W. A., et al. (2022). Earthquake-derived seismic velocity changes during the 2018 caldera collapse of Kīlauea volcano. *Journal of Geophysical Research: Solid Earth*, 127, e2021JB023324.

Hassanizadeh, S. M., & Gray, W. G. (1990). Mechanics and thermodynamics of multiphase flow in porous media including interphase boundaries. *Advances in Water Resources*, 13, 169–186.

Hassanizadeh, S. M., Celia, M. A., & Dahle, H. K. (2002). Dynamic effect in the capillary pressure–saturation relationship. *Vadose Zone Journal*, 1, 38–57.

Hillers, G., Ben-Zion, Y., Campillo, M., & Zigone, D. (2015). Seasonal variations of seismic velocities in the San Jacinto fault area observed with ambient seismic noise. *Geophysical Journal International*, 202, 920–932.

Hobiger, M., Wegler, U., Shiomi, K., & Nakahara, H. (2016). Coseismic and post-seismic velocity changes detected by Passive Image Interferometry: comparison of one great and five strong earthquakes in Japan. *Geophysical Journal International*, 205, 1053–1073.

Hotovec-Ellis, A. J., et al. (2022). Earthquake-derived seismic velocity changes during the 2018 caldera collapse of Kīlauea volcano. *Journal of Geophysical Research*, 127, e2021JB023324.

Hudson, J. A. (1981). Wave speeds and attenuation of elastic waves in material containing cracks. *Geophysical Journal International*, 64, 133–150.

Hughes, D., & Kelly, J. L. (1953). Second-order elastic deformation of solids. *Physical Review*, 92, 1145–1149.

Illien, L., Sens-Schönfelder, C., Andermann, C., Marc, O., Hosseiny, B., & Hovius, N. (2022). Seismic velocity recovery in the subsurface: Transient damage and groundwater drainage following the 2015 Gorkha earthquake, Nepal. *Journal of Geophysical Research: Solid Earth*, 127, e2021JB023402.

James, S. R., Knox, H. A., Abbott, R. E., & Screaton, E. J. (2017). Improved moving window cross-spectral analysis for resolving large temporal seismic velocity changes in permafrost. *Geophysical Research Letters*, 44, 4018–4026.

Jeppson, T. N., & Tobin, H. J. (2015). San Andreas fault zone velocity structure at SAFOD at core, log, and seismic scales. *Journal of Geophysical Research: Solid Earth*, 120, 4983–4997.

Johnson, P. A., & Rasolofosaon, P. (1996). Nonlinear elasticity and stress-induced anisotropy in rock. *Journal of Geophysical Research*, 101, 3113–3124.

Kidiwela, M., Denolle, M. A., Wilcock, W. S. D., & Feng, K.-F. (2026). Active protothrusts and fluid highways: Seismic noise reveals hidden subduction dynamics in Cascadia. *Science Advances*, 12, eaea3684. https://doi.org/10.1126/sciadv.aea3684

Lecocq, T., Longuevergne, L., Pedersen, H. A., Brenguier, F., & Stammler, K. (2017). Monitoring ground water storage at mesoscale using seismic noise. *Scientific Reports*, 7, 14468.

Li, S., Wang, K., Wang, Y., Jiang, Y., & Dosso, S. E. (2018). Geodetically inferred locking state of the Cascadia megathrust based on a viscoelastic Earth model. *Journal of Geophysical Research: Solid Earth*, 123, 8056–8072.

Lobkis, O. I., & Weaver, R. L. (2003). Coda-wave interferometry in finite solids. *Physical Review Letters*, 90, 254302.

Mao, S., Campillo, M., van der Hilst, R. D., Brenguier, F., Stehly, L., & Hillers, G. (2019). High temporal resolution monitoring of small variations in crustal strain by dense seismic arrays. *Geophysical Research Letters*, 46, 128–137.

Mao, S., Lecointre, A., van der Hilst, R. D., & Campillo, M. (2022). Space-time monitoring of groundwater fluctuations with passive seismic interferometry. *Nature Communications*, 13, 4643.

Marc, O., Sens-Schönfelder, C., Illien, L., et al. (2021). Toward using seismic interferometry to quantify landscape-scale erosion rates. *Journal of Geophysical Research: Earth Surface*, 126, e2021JF006112.

Mindlin, R. D. (1949). Compliance of elastic bodies in contact. *Journal of Applied Mechanics*, 16, 259–268.

Murnaghan, F. D. (1937). Finite deformations of an elastic solid. *American Journal of Mathematics*, 59(2), 235–260.

Nakata, N., Gualtieri, L., & Fichtner, A. (2019). *Seismic Ambient Noise*. Cambridge University Press.

Neal, C. A., & Lockwood, J. P. (2003). Geologic map of the summit region of Kilauea Volcano, Hawaii. *U.S. Geological Survey Geologic Investigations Series*, I-2759.

Niu, F., Silver, P. G., Daley, T. M., Cheng, X., & Majer, E. L. (2008). Preseismic velocity changes observed from active source monitoring at Parkfield. *Nature*, 454, 204–208.

Oakley, D. O. S., et al. (2021). Seismic ambient noise analyses reveal changing temperature and water signals to 10s of meters depth in the critical zone. *Journal of Geophysical Research: Earth Surface*, 126, e2020JF005823.

Obermann, A., Planès, T., Larose, E., & Campillo, M. (2013). Imaging preeruptive and coeruptive structural and mechanical changes of a volcano with ambient seismic noise. *Journal of Geophysical Research*, 118, 6285–6294.

Obermann, A., Planès, T., Larose, E., Sens-Schönfelder, C., & Campillo, M. (2014). Depth sensitivity of seismic coda waves to velocity perturbations in an elastic heterogeneous medium. *Geophysical Journal International*, 194, 372–382.

Okubo, K., Delbridge, B. G., & Denolle, M. A. (2024). Monitoring velocity change over 20 years at Parkfield. *Journal of Geophysical Research: Solid Earth*, 129, e2023JB028084.

Ostrovsky, L. A., & Johnson, P. A. (2001). Dynamic nonlinear elasticity in geomaterials. *La Rivista del Nuovo Cimento*, 24(7), 1–46.

Poupinet, G., Ellsworth, W. L., & Frechet, J. (1984). Monitoring velocity variations in the crust using earthquake doublets. *Journal of Geophysical Research*, 89, 5719–5731.

Richter, T., Sens-Schönfelder, C., Kind, R., & Asch, G. (2014). Comprehensive observation and modeling of earthquake and temperature-related seismic velocity changes in northern Chile. *Journal of Geophysical Research: Solid Earth*, 119, 4747–4765.

Rivet, D., Campillo, M., Radiguet, M., Dahm, T., & Shapiro, N. M. (2011). Seismic evidence of nonlinear crustal deformation during a large slow slip event in Mexico. *Geophysical Research Letters*, 38, L08308.

Rodríguez Tribaldos, V., & Ajo-Franklin, J. B. (2021). Aquifer monitoring using ambient seismic noise recorded with distributed acoustic sensing (DAS) deployed on dark fiber. *Journal of Geophysical Research: Solid Earth*, 126, e2020JB021004.

Roeloffs, E. (1988). Fault stability changes induced beneath a reservoir. *Journal of Geophysical Research*, 93, 2107–2124.

Sayers, C. M., & Kachanov, M. (1995). Microcrack-induced elastic wave anisotropy of brittle rocks. *Journal of Geophysical Research*, 100, 4149–4156.

Segall, P., Anderson, K. R., Pulvirenti, F., Wang, T., & Johanson, I. (2020). Caldera collapse geometry revealed by near-field GPS displacements at Kīlauea volcano in 2018. *Geophysical Research Letters*, 47, e2020GL088867.

Sens-Schönfelder, C., & Eulenfeld, T. (2019). Probing the in situ elastic nonlinearity of rocks with Earth tides and seismic noise. *Physical Review Letters*, 122, 138501.

Sens-Schönfelder, C., & Wegler, U. (2006). Passive image interferometry and seasonal variations of seismic velocities at Merapi Volcano, Indonesia. *Geophysical Research Letters*, 33, L21302.

Shapiro, S. A. (2003). Elastic piezosensitivity of porous and fractured rocks. *Geophysics*, 68, 482–486.

Shi, Q., Montgomery, D. R., Swann, A. L. S., Cristea, N. C., Williams, E. F., You, N., Jeffery, S., Collins, J., Prada Barrio, A., Misiewicz, P. A., Nissen-Meyer, T., & Denolle, M. A. (2026). Agroseismology and the impact of farming practices on soil hydrodynamics. *Science*, 392, 306–310. https://doi.org/10.1126/science.aec0970

Singh, J., Curtis, A., Zhao, Y., Cartwright-Taylor, A., & Main, I. (2019). Coda wave interferometry for accurate simultaneous monitoring of velocity and acoustic source location changes. *Journal of Geophysical Research: Solid Earth*, 124, 5629–5655.

Smail, T., et al. (2019). Cumulative deviation of precipitation for estimating groundwater levels. *Water Resources Research*, 55, 10672–10689.

Snieder, R. (2002). Coda wave interferometry and the equilibration of energy in elastic media. *Physical Review E*, 66, 046615.

Snieder, R. (2006). The theory of coda wave interferometry. *Pure and Applied Geophysics*, 163, 455–473.

Snieder, R., Grêt, A., Douma, H., & Scales, J. (2002). Coda wave interferometry for estimating nonlinear behavior. *Science*, 295, 2253–2255.

Snieder, R., Sens-Schönfelder, C., Ruigrok, E., & Shiber, K. (2017). Seismic velocity changes in the shallow subsurface due to the non-linear compliance of fractured rock. *Geophysical Journal International*, 211, 1487–1494.

Taira, T., Nayak, A., Brenguier, F., & Manga, M. (2015). Monitoring reservoir response to earthquakes and fluid extraction. *Science Advances*, 4, e1701536.

Takano, T., Nishimura, T., Nakahara, H., Ueda, H., & Fujita, E. (2019). Sensitivity of seismic velocity changes to the tidal strain at different lapse times: Data analyses of a small seismic array at Izu-Oshima volcano. *Journal of Geophysical Research: Solid Earth*, 124, 3011–3023. https://doi.org/10.1029/2018JB016235

Talwani, P., Chen, L., & Gahalaut, K. (2007). Seismogenic permeability. *Journal of Geophysical Research*, 112, B07309.

Tromp, J., & Trampert, J. (2018). Effects of induced stress on seismic forward modelling and inversion. *Geophysical Journal International*, 213, 851–867.

Tromp, J., Tape, C., & Liu, Q. (2005). Seismic tomography, adjoint methods, time reversal and banana-doughnut kernels. *Geophysical Journal International*, 160, 195–216.

Tsai, V. C. (2011). A model for seasonal changes in GPS positions and seismic wave speeds. *Journal of Geophysical Research*, 116, B04404.

Verdon, J. P., Angus, D. A., Kendall, J. M., & Hall, S. A. (2008). The effect of microstructure and nonlinear stress on anisotropic seismic velocities. *Geophysics*, 73, D41–D51.

Walsh, J. B. (1965). The effect of cracks on the compressibility of rock. *Journal of Geophysical Research*, 70, 381–389.

Wegler, U., & Sens-Schönfelder, C. (2007). Fault zone monitoring with passive image interferometry. *Geophysical Journal International*, 168, 1029–1033.

Yuan, C., Bryan, J., & Denolle, M. A. (2021). Numerical comparison of time-, frequency- and wavelet-domain methods for coda wave interferometry. *Geophysical Journal International*, 226, 828–846.

Zhan, Z., Tsai, V. C., & Clayton, R. W. (2013). Spurious velocity changes caused by temporal variations in ambient noise frequency content. *Geophysical Journal International*, 194, 1552–1559.

Zhang, S., Luo, B., Ben-Zion, Y., Lumley, D. E., & Zhu, H. (2023). Monitoring terrestrial water storage, drought and seasonal changes in central Oklahoma with ambient seismic noise. *Geophysical Research Letters*, 50, e2023GL103419.

Zhang, H., Thurber, C., & Bedrosian, P. (2009). Joint inversion for Vp, Vs, and Vp/Vs at SAFOD, Parkfield, California. *Geochemistry, Geophysics, Geosystems*, 10, Q11002.

Zhu, T., Ajo-Franklin, J., Daley, T. M., & Marone, C. (2019). Dynamics of geologic CO$_2$ storage and plume motion revealed by seismic coda waves. *Proceedings of the National Academy of Sciences*, 116, 2464–2469.

\clearpage

## Table Captions


**Table 1.** Key parameters and validity limits for applying the framework. The full parameter overview, including additional ranges and citations, is provided in Table S1.


**Table 2.** Comparison of framework predictions across three tectonic settings: Parkfield (strike-slip, fractured granite), Northern Cascadia (subduction, marine sediment), and Kīlauea (volcanic caldera collapse, fractured basalt). Parameters include the effective acoustoelastic parameter $|\beta|$, inferred shear-modulus pressure derivative $\mu'$, stress perturbation, and the controlling strain component. The isotropic formulation $\delta v/v = \beta\epsilon_{kk}$ succeeds only at Cascadia (volumetric compression) and fails at both Parkfield and Kīlauea (deviatoric loading with preferred fracture orientations). Note that the directional $\beta$ values at Parkfield and Kīlauea use the bridge relation (Eq. 7) as an order-of-magnitude approximation.


\clearpage

\section*{Figure Files}


\clearpage
\begin{figure}[p]
\centering
\includegraphics[width=\textwidth,height=0.72\textheight,keepaspectratio]{figures/main/fig01_unified_workflow.png}
\caption{Unified workflow for interpreting ambient-noise velocity changes. The workflow connects external forcing (temperature, hydrology, surface loading, tectonics, and magmatic pressure) to stress and strain perturbations, material sensitivity parameters ($\beta$, $\mu'$, crack fabric, saturation state, and rheology), frequency-dependent $\delta v/v(f,t)$, and the diagnostic steps targeted for implementation in \texttt{codameter}.}
\end{figure}


\clearpage
\begin{figure}[p]
\centering
\includegraphics[width=\textwidth,height=0.72\textheight,keepaspectratio]{figures/main/fig02_depth_kernels.png}
\caption{Frequency-dependent depth sensitivity and inversion limits. (a) Schematic Rayleigh/Love sensitivity kernels showing broad, overlapping depth sensitivity for representative frequency bands. (b) Peak sensitivity depth $z_{\mathrm{peak}} \approx V_S/(3f)$ for soft sediment, weathered rock, and crystalline rock. (c) Relative uncertainty reduction for independent versus correlated frequency bands, emphasizing that depth-resolved inversion requires regularization, uncertainty propagation, and resolution tests.}
\end{figure}


\clearpage
\begin{figure}[p]
\centering
\includegraphics[width=\textwidth,height=0.72\textheight,keepaspectratio]{figures/main/fig03_hydrological_competition.png}
\caption{Hydrological signals are a sign competition between surface loading and pore pressure. The simplified Fokker et al. (2021) endmember shows the opposing contributions for (a) ice/snow loading, (b) seasonal rainfall, and (c) reservoir impoundment. Positive-compressive vertical loading tends to increase velocity, whereas pore-pressure increase reduces effective stress and decreases velocity.}
\end{figure}


\clearpage
\begin{figure}[p]
\centering
\includegraphics[width=\textwidth,height=0.72\textheight,keepaspectratio]{figures/main/fig04_material_sensitivity.png}
\caption{Material sensitivity controls stress conversion from velocity change. (a) Effective $|\beta|$ spans orders of magnitude across materials, from intact crystalline rock to soft sediment. (b) Observed $\delta v/v$ amplitude ratios across Parkfield, Cascadia, and Kīlauea do not map directly to stress ratios because the conversion depends on $\beta$, $\mu'$, and shear modulus.}
\end{figure}


\clearpage
\begin{figure}[p]
\centering
\includegraphics[width=\textwidth,height=0.72\textheight,keepaspectratio]{figures/main/fig05_anisotropy_fabric.png}
\caption{Deviatoric stress and fracture fabric determine the observed velocity sign. (a) Directional sensitivity increases with fracture fabric strength. (b–d) Parkfield, Cascadia, and Kīlauea select different stress/strain components because the dominant loading geometry and crack fabric differ. (e) The scalar isotropic model succeeds for Cascadia but fails for Parkfield and Kīlauea.}
\end{figure}


\clearpage
\begin{figure}[p]
\centering
\includegraphics[width=\textwidth,height=0.72\textheight,keepaspectratio]{figures/main/fig06_rheology_diagnostics.png}
\caption{Rheology is diagnosed from phase, hysteresis, and recovery shape. (a) Endmember elastic, Maxwell, Kelvin-Voigt, and slow-dynamics responses to a step-like forcing. (b) $\delta v/v$–strain crossplots distinguish elastic, higher-order nonlinear, and viscoelastic lag behavior. (c) Parkfield-like dual-population model combining tectonic loading and postseismic healing. (d) Tidal probing of in-situ nonlinearity through harmonic distortion.}
\end{figure}


\clearpage
\begin{figure}[p]
\centering
\includegraphics[width=\textwidth,height=0.72\textheight,keepaspectratio]{figures/main/fig07_three_site_synthesis.png}
\caption{Three-site synthesis of framework predictions. (a) Effective $|\beta|$, (b) inferred $\mu'$, and (c) normalized stress perturbation for Parkfield, Northern Cascadia, and Kīlauea. (d) Mechanism branch selected by loading geometry: deviatoric crack closure at Parkfield, volumetric compaction at Cascadia, and radial ring-fracture compression at Kīlauea.}
\end{figure}
