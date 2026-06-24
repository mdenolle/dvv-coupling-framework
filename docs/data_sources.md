# External Data Sources

The framework runs out of the box on **synthetic data generators** (see
`generate_california_synthetic` and `generate_parkfield_synthetic` in
[analysis/coupling_diagnostic_cases.py](../analysis/coupling_diagnostic_cases.py)),
so no external download is required to reproduce the diagnostic-case figures.

The optional real-data paths reference the datasets below.

## Clements & Denolle (2023) California dv/v

- **Use cases:** Case 1 (Ridgecrest), Case 2 (drought-to-flood), Tier 1 validation.
- **Reference / DOI:** https://doi.org/10.1029/2022JB025553
- **Format:** Parquet, one file per station, columns include `DATE`, `DVV`, `CC`.
- **Access:** Available by request from the corresponding author (R. Clements, Caltech),
  or from the dataset's published archive where available.
- **Local placement:** put files under `data/clements_denolle_2023/` named `NET.STA.parquet`,
  then load with `load_parquet_dvv()`.

## Okubo et al. (2024) Parkfield dv/v

- **Use case:** Case 3 (M2 tidal beta evolution).
- **Access:** IRIS DMC Parkfield products or by request from the authors.

## Reproducibility notes

- Synthetic generators are deterministic once the NumPy global seed is set
  (`np.random.seed(42)`); the tests pin the seed before comparing outputs.
- Figure outputs are written to `figures/coupling/` by default; override the
  directory with the `DVV_FIGDIR` environment variable.
