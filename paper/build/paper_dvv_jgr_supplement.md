---
title: "Supporting Information for: Seismic Velocity Changes as Stress and Strain Meters: A Unified Framework for Environmental, Tectonic, and Volcanic Monitoring"
author: "Marine A. Denolle"
affiliation: "Department of Earth and Space Sciences, University of Washington, Seattle, WA, USA"
corresponding_author: "mdenolle@uw.edu"
---


## Contents of this file

- Text S1: preliminary application of the framework to three published datasets (Parkfield, Cascadia, Kīlauea).
- Figures S1–S12: supporting forward-model and validity figures (synthetic $\delta v/v$ with realistic shapes, illustrating the framework).
- Figure 7: three-site synthesis of the preliminary application.
- Table 2 (inline in Text S1) and Table S1: three-site comparison and parameter overview.

All quantitative inputs are traced to their sources in \texttt{docs/site\_analyses/provenance\_tables.md}.

\clearpage

## Text S1. Preliminary Application to Field Observations

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

Kidiwela et al. (2026) calibrated $\beta = 3160$ from the $\delta v/v$ trend and the borehole strain measurement. This makes the borehole comparison a calibration and internal consistency test, not an independent validation of the stress conversion. The drainage regime is fixed by the data: for the 13-year secular trend at $L\approx 0.25$ km with the in-situ diffusivity $c\approx 3.8\times10^{-4}$ m$^2$/s inferred from the 2019 fluid pulse, $\mathrm{Pe}=\omega L^2/c \approx 2.5$ (transitional-to-undrained), so the seismic-band (undrained) modulus $\kappa_u = \rho(V_P^2-\tfrac{4}{3}V_S^2) = 4.86$ GPa is the appropriate value (not the smaller drained modulus). The bridge relation (Eq. 7), used here as a consistency check on the published $\beta$, gives:

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

The long-term velocity decrease (–0.3%/day for ~26 days, total ~–8%, though Hotovec-Ellis et al. note that whether these accumulated changes combine linearly is unresolved) ceased when the peripheral ring fault completed its formation at the surface. Hotovec-Ellis et al. attribute this to *inelastic* fracture creation during fault growth — a mechanism outside the purely elastic acoustoelastic framework of Equation 3. Because the process is inelastic, the ratio of velocity change to strain is **not** an acoustoelastic $\beta$; we report it only as an *apparent* $\delta v/v$–strain ratio that summarizes the net response. Using the GNSS shortening rate across the caldera (~40 mm/day, $\epsilon \approx 20$ μstrain/day):

$$R_{\text{app}} = \frac{\delta v/v}{\epsilon} = \frac{0.003}{2 \times 10^{-5}} \approx 150 \quad (\text{apparent, not an elastic } \beta)$$

The apparent ratio is lower than the short-term elastic value ($\beta_{\text{radial}} \approx 300$), and this contrast is physically meaningful precisely because the two regimes are governed by different physics: the short term is elastic crack closure (which increases velocity), while the long term superposes *inelastic* fracture generation (which decreases velocity). The smaller $R_{\text{app}}$ reflects new cracks partially offsetting the stiffening from closure of existing cracks — a signature of *damage accumulation* that the elastic acoustoelastic relation cannot represent and that should not be inverted for stress with Equation 4.

#### 9.3.5 Implications for fracture geometry as a diagnostic

The Kīlauea case extends the anisotropy diagnostic from §6 to volcanic settings: *the dominant fracture orientation determines which strain component controls $\delta v/v$*. At Parkfield, fault-parallel fractures respond to fault-normal contractional strain. At Kīlauea, ring fractures respond to radial strain from reservoir pressurization. At Piton de la Fournaise, where radial dike fractures dominate (Carter et al., 2007), the *opposite* response to pressurization is observed (Rivet et al., 2014) — consistent with radial fractures opening under radial extension. The unified framework (Eq. 4) captures all three cases through the directional projection of the deviatoric stress onto the fracture-normal direction, without requiring separate physical models for each setting.

### 9.4 Cross-Site Synthesis

**Table 2** summarizes the key parameters and predictions across all three sites; Figure 7 visualizes the same comparison as the main synthesis result.

**Table 2.** Comparison of framework predictions across three tectonic settings: Parkfield (strike-slip, fractured granite), Northern Cascadia (subduction, marine sediment), and Kīlauea (volcanic caldera collapse, fractured basalt). Parameters include the effective acoustoelastic parameter $|\beta|$, inferred shear-modulus pressure derivative $\mu'$, stress perturbation, and the controlling strain component. The isotropic formulation $\delta v/v = \beta\epsilon_{kk}$ succeeds only at Cascadia (volumetric compression) and fails at both Parkfield and Kīlauea (deviatoric loading with preferred fracture orientations). Note that the directional $\beta$ values at Parkfield and Kīlauea use the bridge relation (Eq. 7) as an order-of-magnitude approximation.

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

\clearpage

\section*{Supporting Figures}


\clearpage
\begin{figure}[p]
\centering
\includegraphics[width=\textwidth,height=0.78\textheight,keepaspectratio]{figures/main/fig07_three_site_synthesis.png}
\caption{\textbf{Figure 7.} Three-site synthesis of framework predictions. (a) Effective $|\beta|$, (b) inferred $\mu'$, and (c) normalized stress perturbation for Parkfield, Northern Cascadia, and Kīlauea. (d) Mechanism branch selected by loading geometry: deviatoric crack closure at Parkfield, volumetric compaction at Cascadia, and radial ring-fracture compression at Kīlauea.}
\end{figure}


\clearpage
\begin{figure}[p]
\centering
\includegraphics[width=\textwidth,height=0.78\textheight,keepaspectratio]{figures/notebooks/fig01_temperature_diffusion.png}
\caption{\textbf{Figure S1.} Annual temperature diffusion into the subsurface for three thermal diffusivities (0.15, 0.6, 2.0 mm$^2$/s), showing depth profiles at different phases of the annual cycle. Red dashed lines mark the thermal skin depth $1/\gamma$}
\end{figure}


\clearpage
\begin{figure}[p]
\centering
\includegraphics[width=\textwidth,height=0.78\textheight,keepaspectratio]{figures/notebooks/fig02_berger_stress.png}
\caption{\textbf{Figure S2.} Berger (1975) thermoelastic stress solution. Left: shallow view dominated by term 1 (direct thermal stress, decaying with skin depth $1/\gamma$). Right: deep view dominated by term 2 (equilibrium response, decaying with horizontal wavenumber $1/k$)}
\end{figure}


\clearpage
\begin{figure}[p]
\centering
\includegraphics[width=\textwidth,height=0.78\textheight,keepaspectratio]{figures/notebooks/fig03_thermoelastic_sensitivity.png}
\caption{\textbf{Figure S3.} Thermoelastic $\delta v/v$ sensitivity analysis. Panels show the depth profile for varying nonlinear response strength $\partial(\rho v^2)/\partial\sigma_c$, surface $\delta v/v$ versus temperature amplitude, sensitivity to Poisson's ratio, and thermal skin depth versus diffusivity}
\end{figure}


\clearpage
\begin{figure}[p]
\centering
\includegraphics[width=\textwidth,height=0.78\textheight,keepaspectratio]{figures/notebooks/fig04_synthetic_thermoelastic_dvv.png}
\caption{\textbf{Figure S4.} Synthetic thermoelastic $\delta v/v$ time series, including surface temperature with Fourier fit, $\delta v/v$ for different temperature sensitivities, and thermal diffusion time delay}
\end{figure}


\clearpage
\begin{figure}[p]
\centering
\includegraphics[width=\textwidth,height=0.78\textheight,keepaspectratio]{figures/notebooks/fig05_pore_pressure_diffusion.png}
\caption{\textbf{Figure S5.} Poroelastic pore-pressure response to surface loading following Roeloffs (1988), including depth profiles after loading, hydraulic diffusivity dependence, undrained versus drained components, and Skempton coefficient sensitivity}
\end{figure}


\clearpage
\begin{figure}[p]
\centering
\includegraphics[width=\textwidth,height=0.78\textheight,keepaspectratio]{figures/notebooks/fig06_gwl_model.png}
\caption{\textbf{Figure S6.} Groundwater-level model following Okubo et al. (2024), including synthetic precipitation, $\Delta$GWL response for different hydrological memory timescales, and resulting hydrological $\delta v/v$}
\end{figure}


\clearpage
\begin{figure}[p]
\centering
\includegraphics[width=\textwidth,height=0.78\textheight,keepaspectratio]{figures/notebooks/fig18_regime_diagram.png}
\caption{\textbf{Figure S7.} Detailed regime diagram showing which physical process dominates $\delta v/v$ as a function of measurement frequency and depth sensitivity, including capillary/vadose-zone, hydrological, thermoelastic, and tectonic domains}
\end{figure}


\clearpage
\begin{figure}[p]
\centering
\includegraphics[width=\textwidth,height=0.78\textheight,keepaspectratio]{figures/notebooks/fig10_murnaghan_EOS.png}
\caption{\textbf{Figure S8.} Murnaghan (1937) equation-of-state diagnostics, including pressure-volume relations and velocity versus confining pressure for different nonlinear response strengths}
\end{figure}


\clearpage
\begin{figure}[p]
\centering
\includegraphics[width=\textwidth,height=0.78\textheight,keepaspectratio]{figures/notebooks/fig09_nonlinear_detection.png}
\caption{\textbf{Figure S9.} Detailed nonlinear-elasticity diagnostics from $\delta v/v$--strain crossplots, including tidal/thermal strain, linear and nonlinear velocity response, and curvature from higher-order nonlinearity}
\end{figure}


\clearpage
\begin{figure}[p]
\centering
\includegraphics[width=\textwidth,height=0.78\textheight,keepaspectratio]{figures/notebooks/fig13_healing_models.png}
\caption{\textbf{Figure S10.} Logarithmic healing models, including sensitivity to $\tau_{\max}$ and $\tau_{\min}$, a Parkfield-like synthetic time series, and the $\sim 1/t$ healing-rate decay}
\end{figure}


\clearpage
\begin{figure}[p]
\centering
\includegraphics[width=\textwidth,height=0.78\textheight,keepaspectratio]{figures/notebooks/fig15_homogeneous_validity.png}
\caption{\textbf{Figure S11.} Detailed homogeneous-half-space validity tests, including sensitivity kernels, peak sensitivity depth versus frequency, and relative error from velocity contrasts within the sensitivity kernel}
\end{figure}


\clearpage
\begin{figure}[p]
\centering
\includegraphics[width=\textwidth,height=0.78\textheight,keepaspectratio]{figures/notebooks/fig16_linearity_validity.png}
\caption{\textbf{Figure S12.} Validity of the linear acoustoelastic approximation $\delta v/v = \beta\epsilon_{kk}$ as a function of strain magnitude, including tidal, thermoelastic, and coseismic/strong-motion regimes}
\end{figure}


\clearpage
\begin{figure}[p]
\centering
\includegraphics[width=\textwidth,height=0.78\textheight,keepaspectratio]{figures/notebooks/fig17_parameter_table.png}
\caption{\textbf{Table S1.} Comprehensive parameter overview table summarizing typical ranges, controlling physical effects, and validity limits for all key model parameters ($\kappa_T$, $c$, $\nu$, $\nu_u$, $B$, $\beta$, $\mu'$, $\alpha$, $\phi$, $\epsilon_c$, $\tau_{\min}$, $\tau_{\max}$)}
\end{figure}
