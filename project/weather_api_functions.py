import glob
import os
import time
import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns
import contextily as ctx
import datetime as dt

from fmiopendata.wfs import download_stored_query



RANDOM_STATE = 69
DATA_DIR = "datasets"            # folder that holds tieliikenne_YYYY.csv
YEARS = list(range(2015, 2025))


FMI_QUERY = "fmi::observations::weather::daily::multipointcoverage"
FMI_BBOX = "19,59,32,71"            # lon_min, lat_min, lon_max, lat_max = all of Finland
FMI_PARAMS = "tday,rrday,snow"      # mean temperature, precipitation, snow depth
WEATHER_DIR = os.path.join(DATA_DIR, "fmi_cache")
os.makedirs(WEATHER_DIR, exist_ok=True)


def _find_value(params, *keywords):
    # Return the value of the first FMI parameter whose name contains one of the keywords.
    for name, item in params.items():
        if any(k in name.lower() for k in keywords):
            value = item.get("value")
            return np.nan if value is None else float(value)
    return np.nan


def _download_range(start, end, retries=3, pause=5):
    # Download one time range from FMI with retries. Returns obs.data or None.
    for attempt in range(1, retries + 1):
        try:
            result = download_stored_query(
                FMI_QUERY,
                args=[f"bbox={FMI_BBOX}",
                      f"starttime={start:%Y-%m-%dT%H:%M:%SZ}",
                      f"endtime={end:%Y-%m-%dT%H:%M:%SZ}",
                      f"parameters={FMI_PARAMS}"],
            )
            # aikaisemmin if result.data nyt palautetaan kaikki data
            if result:
                return result.data, result.location_metadata
            reason = "empty response"
        except Exception as err:
            reason = f"{type(err).__name__}: {str(err)[:80]}"
        print(f"[{reason}; attempt {attempt}]", end=" ")
        time.sleep(pause * attempt)
    return None


def fetch_fmi_month(year, month):
    # Daily weather for one calendar month -> DataFrame(date, station, tday, rrday, snow, location).
    start = pd.Timestamp(year, month, 1)
    end = start + pd.offsets.MonthBegin(1)

    data_parts = []
    metadata_parts = []
    data, location_metadata = _download_range(start, end)
    if data is not None:
        data_parts.append(data)
        metadata_parts.append(location_metadata)

    else:                                   # fall back to two half-month requests
        middle = start + pd.Timedelta(days=15)
        for a, b in [(start, middle), (middle, end)]:
            part, metadata_part = _download_range(a, b, retries=2)
            if part is None:
                return None
            data_parts.append(part)
            metadata_parts.append(metadata_part)


    # flatten list of dicts
    location_dict = {}
    for location_datas in metadata_parts:
        for key, value in location_metadata.items():
            location_dict[key] = value


    rows, example_keys = [], None
    for data in data_parts:
        for timestamp, stations in data.items():
            for station, params in stations.items():
                example_keys = example_keys or list(params.keys())
                rows.append({
                    "date": pd.Timestamp(timestamp).normalize(),
                    "station": station,
                    "tday": _find_value(params, "temperature"),
                    "rrday": _find_value(params, "precip", "rain"),
                    "snow": _find_value(params, "snow"),
                    "location" : location_dict[station]
                })
    df = pd.DataFrame(rows)
    if df["tday"].isna().all():
        raise RuntimeError("Temperature not found in the FMI response. "
                           f"Parameter names returned by FMI: {example_keys}")

    return df.drop_duplicates(["date", "station"])


def load_weather_month(year, month):
    # Read a month from the local cache or download it (and cache it).
    path = os.path.join(WEATHER_DIR, f"fmi_daily_{year}-{month:02d}.csv")
    if os.path.exists(path):
        return pd.read_csv(path, parse_dates=["date"])
    print(f"FMI {year}-{month:02d}: downloading ...", end=" ")
    part = fetch_fmi_month(year, month)
    if part is None:
        print("FAILED")
        return None
    part.to_csv(path, index=False)
    print(f"{len(part)} rows, {part['station'].nunique()} stations")
    return part