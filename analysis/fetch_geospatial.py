"""
fetch_geospatial.py
===================
Fetch per-station geospatial properties needed to interpret rheology,
sensitivity depth, and drainage regime from open APIs and datasets.

All functions return DataFrames indexed by NETSTA, ready to merge
with the Clements & Denolle fit summary.

APIs used (all free, no authentication required unless noted):
  - USGS Earthquake Hazards Vs30/Z1.0/Z2.5   (WS REST)
  - OpenTopography DEM (elevation, slope, curvature)
  - USGS NLDI / NHD for catchment area
  - USGS NWIS groundwater levels (nearby wells)

Datasets to download once (see download functions):
  - Fan et al. (2013) global water table depth  (netCDF, ~200 MB)
  - GLHYMPS v2 hydraulic conductivity          (requires registration)
  - SoilGrids porosity / permeability          (WCS)
"""

import numpy as np
import pandas as pd
import requests
import time
import warnings
from pathlib import Path


# ─────────────────────────────────────────────────────────────────────────────
# 1. USGS Vs30, Z1.0, Z2.5 (NEHRP site parameters)
# ─────────────────────────────────────────────────────────────────────────────

USGS_VS30_URL = "https://earthquake.usgs.gov/ws/designmaps/asce7-22.json"

def fetch_usgs_site_params(lat, lon, risk_category="III"):
    """
    Query USGS NEHRP site parameters for one location.

    Returns dict with: vs30, z1p0_m (depth to Vs=1km/s), z2p5_km
    Falls back to None on failure.
    """
    params = {
        "latitude":       lat,
        "longitude":      lon,
        "riskCategory":   risk_category,
        "siteClass":      "default",
        "title":          "query",
    }
    try:
        r = requests.get(USGS_VS30_URL, params=params, timeout=10)
        if r.status_code == 200:
            d = r.json()
            output = d.get("output", {})
            return {
                "vs30":     output.get("vs30",  None),
                "z1p0_m":   output.get("z1p0",  None),
                "z2p5_km":  output.get("z2p5",  None),
            }
    except Exception as e:
        warnings.warn(f"USGS site params failed for ({lat},{lon}): {e}")
    return {"vs30": None, "z1p0_m": None, "z2p5_km": None}


def fetch_vs30_batch(df, lat_col="lat", lon_col="lon",
                     sleep_s=0.3, cache_path=None):
    """
    Fetch Vs30, Z1.0, Z2.5 for all stations.

    Parameters
    ----------
    df : DataFrame with columns lat, lon (and 'netsta' for indexing)
    sleep_s : float  sleep between API calls (be kind to USGS)
    cache_path : str or None  if set, saves/loads CSV cache

    Returns
    -------
    df_vs30 : DataFrame with columns netsta, vs30, z1p0_m, z2p5_km
    """
    if cache_path and Path(cache_path).exists():
        print(f"Loading Vs30 cache from {cache_path}")
        return pd.read_csv(cache_path)

    records = []
    for i, row in df.iterrows():
        netsta = row.get("netsta", str(i))
        lat    = row[lat_col]
        lon    = row[lon_col]
        result = fetch_usgs_site_params(lat, lon)
        result["netsta"] = netsta
        records.append(result)
        time.sleep(sleep_s)
        if (i + 1) % 50 == 0:
            print(f"  Fetched {i+1}/{len(df)} stations")

    df_out = pd.DataFrame(records)
    if cache_path:
        df_out.to_csv(cache_path, index=False)
        print(f"Saved Vs30 cache to {cache_path}")
    return df_out


# ─────────────────────────────────────────────────────────────────────────────
# 2. Open-Elevation API (SRTM/ASTER DEM)
# ─────────────────────────────────────────────────────────────────────────────

OPEN_ELEVATION_URL = "https://api.open-elevation.com/api/v1/lookup"

def fetch_elevation_batch(df, lat_col="lat", lon_col="lon", batch_size=100):
    """
    Fetch SRTM 90m elevation for all stations.
    Uses open-elevation.com (no API key needed).

    Returns df with column 'elev_srtm_m'
    """
    all_elevs = []
    locations = [
        {"latitude": row[lat_col], "longitude": row[lon_col]}
        for _, row in df.iterrows()
    ]

    for i in range(0, len(locations), batch_size):
        batch = locations[i:i + batch_size]
        payload = {"locations": batch}
        try:
            r = requests.post(OPEN_ELEVATION_URL,
                              json=payload, timeout=30)
            if r.status_code == 200:
                results = r.json()["results"]
                all_elevs.extend([x["elevation"] for x in results])
            else:
                all_elevs.extend([np.nan] * len(batch))
        except Exception as e:
            warnings.warn(f"Elevation batch {i//batch_size} failed: {e}")
            all_elevs.extend([np.nan] * len(batch))
        time.sleep(0.5)

    df_out = df[["netsta"]].copy()
    df_out["elev_srtm_m"] = all_elevs
    return df_out


# ─────────────────────────────────────────────────────────────────────────────
# 3. SoilGrids v2 porosity (ISRIC REST API)
# ─────────────────────────────────────────────────────────────────────────────

SOILGRIDS_URL = "https://rest.isric.org/soilgrids/v2.0/properties/query"

def fetch_soilgrids_porosity(lat, lon, depth_cm=30):
    """
    Query SoilGrids v2 for porosity at 0–30 cm (or other depths).
    Available depths: 0-5, 5-15, 15-30, 30-60, 60-100, 100-200 cm.

    Returns: porosity fraction (float) or None.
    Note: SoilGrids reports 'theta_s' (saturated VWC ≈ porosity)
    """
    depth_str = f"0-{depth_cm}cm"
    params = {
        "lon":      lon,
        "lat":      lat,
        "property": ["theta_s"],
        "depth":    [depth_str],
        "value":    ["mean"],
    }
    try:
        r = requests.get(SOILGRIDS_URL, params=params, timeout=15)
        if r.status_code == 200:
            d = r.json()
            layers = d.get("properties", {}).get("layers", [])
            for layer in layers:
                if layer.get("name") == "theta_s":
                    vals = layer.get("depths", [{}])[0].get("values", {})
                    mean_val = vals.get("mean")
                    if mean_val is not None:
                        return mean_val / 1000.0  # SoilGrids uses cm³/dm³ ×1000
        return None
    except Exception as e:
        warnings.warn(f"SoilGrids failed for ({lat},{lon}): {e}")
        return None


def fetch_porosity_batch(df, lat_col="lat", lon_col="lon",
                         cache_path=None, sleep_s=0.5):
    """
    Fetch SoilGrids porosity for all stations.
    Returns df with column 'porosity_soilgrids'
    """
    if cache_path and Path(cache_path).exists():
        print(f"Loading porosity cache from {cache_path}")
        return pd.read_csv(cache_path)

    records = []
    for i, row in df.iterrows():
        netsta = row.get("netsta", str(i))
        phi = fetch_soilgrids_porosity(row[lat_col], row[lon_col])
        records.append({"netsta": netsta, "porosity_soilgrids": phi})
        time.sleep(sleep_s)
        if (i + 1) % 25 == 0:
            print(f"  Fetched porosity {i+1}/{len(df)}")

    df_out = pd.DataFrame(records)
    if cache_path:
        df_out.to_csv(cache_path, index=False)
    return df_out


# ─────────────────────────────────────────────────────────────────────────────
# 4. Fan et al. (2013) global water table depth
# ─────────────────────────────────────────────────────────────────────────────

def load_fan2013_wtd(netcdf_path, df, lat_col="lat", lon_col="lon"):
    """
    Extract water table depth from Fan et al. (2013) global WTD model.

    Data: http://thredds.hydroshare.org/thredds/catalog/hydroshare/
          resources/3295a17b4cc24d9489d2ebe97d56f7f4/catalog.html
    File: 'WTD_ibased.nc'  (global, ~1 km resolution)

    Parameters
    ----------
    netcdf_path : str  local path to WTD_ibased.nc
    df : DataFrame with lat, lon columns

    Returns
    -------
    df_wtd : DataFrame with columns netsta, wtd_fan2013_m
             Positive = depth below surface [m]
    """
    try:
        import xarray as xr
        ds = xr.open_dataset(netcdf_path)
        wtd_var = [v for v in ds.data_vars if "wtd" in v.lower() or "depth" in v.lower()]
        if not wtd_var:
            wtd_var = list(ds.data_vars)[0]
        else:
            wtd_var = wtd_var[0]

        records = []
        for _, row in df.iterrows():
            try:
                val = float(ds[wtd_var].sel(
                    lat=row[lat_col], lon=row[lon_col], method="nearest"
                ).values)
            except Exception:
                val = np.nan
            records.append({"netsta": row.get("netsta"), "wtd_fan2013_m": abs(val)})

        return pd.DataFrame(records)

    except ImportError:
        warnings.warn("xarray not installed. pip install xarray.")
        return pd.DataFrame({"netsta": df.get("netsta", []), "wtd_fan2013_m": np.nan})


# ─────────────────────────────────────────────────────────────────────────────
# 5. USGS NWIS nearby groundwater wells (for validation)
# ─────────────────────────────────────────────────────────────────────────────

NWIS_URL = "https://waterservices.usgs.gov/nwis/gwlevels/"

def fetch_nearest_well_stats(lat, lon, radius_km=20, start="2000-01-01",
                               end="2021-12-31"):
    """
    Fetch groundwater level statistics from USGS NWIS wells near a station.

    Returns dict: mean_wtd_m, seasonal_amp_m, n_wells
    """
    params = {
        "format":      "json",
        "sites":       f"{lat},{lon}",
        "bBox":        f"{lon-0.2},{lat-0.2},{lon+0.2},{lat+0.2}",
        "parameterCd": "72019",  # depth to water level, ft
        "startDT":     start,
        "endDT":       end,
        "statReportType": "annual",
    }
    try:
        r = requests.get(NWIS_URL, params=params, timeout=15)
        if r.status_code == 200:
            data = r.json()
            series = data.get("value", {}).get("timeSeries", [])
            if series:
                # Average over all nearby wells
                all_vals = []
                for s in series:
                    for v in s.get("values", [{}])[0].get("value", []):
                        try:
                            all_vals.append(float(v["value"]) * 0.3048)  # ft→m
                        except Exception:
                            pass
                if all_vals:
                    return {
                        "mean_wtd_m":      np.mean(all_vals),
                        "seasonal_amp_m":  np.percentile(all_vals, 90) -
                                           np.percentile(all_vals, 10),
                        "n_wells":         len(series),
                    }
    except Exception as e:
        warnings.warn(f"NWIS failed for ({lat},{lon}): {e}")
    return {"mean_wtd_m": np.nan, "seasonal_amp_m": np.nan, "n_wells": 0}


# ─────────────────────────────────────────────────────────────────────────────
# 6. Topographic slope and local relief from SRTM via OpenTopography
# ─────────────────────────────────────────────────────────────────────────────

def compute_local_relief(df, lat_col="lat", lon_col="lon",
                          dem_netcdf_path=None, radius_m=5000):
    """
    Compute local topographic relief (max - min elevation within radius).

    If dem_netcdf_path is provided (e.g. SRTM 1-arc-second NetCDF),
    computes relief directly from the DEM. Otherwise uses elevation range
    from station elevations as a fallback.

    Local relief is a key predictor of drainage regime:
    - High relief → mountain/bedrock → fast drainage → drained regime
    - Low relief  → valley/basin     → slow drainage → undrained regime
    """
    if dem_netcdf_path and Path(dem_netcdf_path).exists():
        try:
            import xarray as xr
            ds = xr.open_dataset(dem_netcdf_path)
            elev_var = [v for v in ds.data_vars][0]

            records = []
            for _, row in df.iterrows():
                lat, lon = row[lat_col], row[lon_col]
                dlat = radius_m / 111000.0
                dlon = radius_m / (111000.0 * np.cos(np.radians(lat)))
                try:
                    patch = ds[elev_var].sel(
                        lat=slice(lat - dlat, lat + dlat),
                        lon=slice(lon - dlon, lon + dlon)
                    ).values.flatten()
                    patch = patch[~np.isnan(patch)]
                    relief = float(patch.max() - patch.min()) if len(patch) > 0 else np.nan
                except Exception:
                    relief = np.nan
                records.append({"netsta": row.get("netsta"), "local_relief_m": relief})
            return pd.DataFrame(records)
        except ImportError:
            warnings.warn("xarray required for DEM relief calculation.")

    # Fallback: use elevation as proxy
    df_out = df[["netsta"]].copy()
    if "elev_m" in df.columns:
        df_out["local_relief_m"] = df["elev_m"].values  # crude proxy
    else:
        df_out["local_relief_m"] = np.nan
    return df_out


# ─────────────────────────────────────────────────────────────────────────────
# 7. USGS Quaternary geology / rock type classification
# ─────────────────────────────────────────────────────────────────────────────

# California lithology lookup table (simplified from CA GEMS / CGS maps)
# Based on Vs30–lithology correspondence for CA stations
CALIFORNIA_LITHOLOGY_PROXIES = {
    # (Vs30 range, elev range) → lithology class
    # These are statistical priors, not hard rules
    "soft_basin":        {"vs30_max": 300,  "elev_max": 200,  "B_prior": 0.85, "phi_prior": 0.35},
    "stiff_sediment":    {"vs30_max": 500,  "elev_max": 600,  "B_prior": 0.65, "phi_prior": 0.20},
    "soft_rock":         {"vs30_max": 700,  "elev_max": 1500, "B_prior": 0.45, "phi_prior": 0.12},
    "hard_rock":         {"vs30_max": 1500, "elev_max": 4500, "B_prior": 0.25, "phi_prior": 0.05},
}


def classify_lithology(vs30, elev_m):
    """
    Heuristic lithology classification from Vs30 and elevation.
    Returns lithology class name and associated B, phi priors.
    """
    vs30  = np.atleast_1d(np.asarray(vs30,  dtype=float))
    elev  = np.atleast_1d(np.asarray(elev_m, dtype=float))
    classes  = np.full(len(vs30), "unknown", dtype=object)
    B_prior  = np.full(len(vs30), 0.5)
    phi_prior = np.full(len(vs30), 0.15)

    for name, lims in CALIFORNIA_LITHOLOGY_PROXIES.items():
        mask = (vs30 <= lims["vs30_max"]) & (elev <= lims["elev_max"])
        classes[mask]   = name
        B_prior[mask]   = lims["B_prior"]
        phi_prior[mask] = lims["phi_prior"]

    return classes, B_prior, phi_prior


def attach_lithology_priors(df, vs30_col="vs30", elev_col="elev_m"):
    """
    Attach Skempton B and porosity priors from Vs30/elevation classification.
    """
    df = df.copy()
    vs30 = df.get(vs30_col, pd.Series(600, index=df.index)).fillna(600).values
    elev = df.get(elev_col, pd.Series(0,   index=df.index)).fillna(0).values

    classes, B_prior, phi_prior = classify_lithology(vs30, elev)
    df["lithology_class"] = classes
    df["B_prior"]         = B_prior
    df["phi_prior"]       = phi_prior
    return df


# ─────────────────────────────────────────────────────────────────────────────
# 8. Convenience: full geospatial fetch pipeline
# ─────────────────────────────────────────────────────────────────────────────

def fetch_all_geospatial(df, cache_dir="data/geospatial_cache",
                          fan_wtd_path=None, dem_path=None,
                          fetch_vs30=True, fetch_porosity=True,
                          fetch_wells=False):
    """
    Run all geospatial fetch functions and merge into station DataFrame.

    Parameters
    ----------
    df : DataFrame  station table with columns netsta, lat, lon
    cache_dir : str  directory for caching API results
    fan_wtd_path : str or None  path to Fan et al. (2013) WTD NetCDF
    dem_path : str or None  path to SRTM DEM NetCDF for relief
    fetch_vs30 : bool  fetch USGS Vs30 (slow, ~0.3s per station)
    fetch_porosity : bool  fetch SoilGrids porosity (slow)
    fetch_wells : bool  fetch NWIS groundwater well stats (slow)

    Returns
    -------
    df_enriched : DataFrame with all available geospatial columns
    """
    Path(cache_dir).mkdir(parents=True, exist_ok=True)
    merged = df.copy()

    if fetch_vs30:
        print("Fetching USGS Vs30/Z1.0/Z2.5...")
        df_vs30 = fetch_vs30_batch(df,
            cache_path=f"{cache_dir}/vs30_cache.csv")
        merged = merged.merge(df_vs30, on="netsta", how="left")

    if fetch_porosity:
        print("Fetching SoilGrids porosity...")
        df_phi = fetch_porosity_batch(df,
            cache_path=f"{cache_dir}/porosity_cache.csv")
        merged = merged.merge(df_phi, on="netsta", how="left")

    if fan_wtd_path:
        print("Extracting Fan et al. WTD...")
        df_wtd = load_fan2013_wtd(fan_wtd_path, df)
        merged = merged.merge(df_wtd, on="netsta", how="left")

    if dem_path:
        print("Computing local relief from DEM...")
        df_relief = compute_local_relief(df, dem_netcdf_path=dem_path)
        merged = merged.merge(df_relief, on="netsta", how="left")

    # Attach lithology priors (fast, no network)
    merged = attach_lithology_priors(merged)

    print(f"\nGeospatial enrichment complete. Shape: {merged.shape}")
    return merged
