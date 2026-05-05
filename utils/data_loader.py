from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


def _read_week_file(path: Path) -> pd.DataFrame | None:
    try:
        df = pd.read_csv(path)
    except Exception:
        return None

    if df.empty or "timestamp" not in df.columns:
        return None

    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce", dayfirst=True)
    df = df.dropna(subset=["timestamp"])

    if df.empty:
        return None

    # numeric cleanup for known columns
    numeric_columns = [
        "value",
        "rolling_mean_10",
        "rolling_mean_30",
        "rolling_std_30",
        "rolling_std_60",
        "rolling_max_10",
        "rolling_min_10",
        "value_diff",
        "pct_change",
        "z_score",
        "anomaly_score",
    ]

    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    if "anomaly" in df.columns:
        df["anomaly"] = pd.to_numeric(df["anomaly"], errors="coerce").fillna(0).astype(int)
    elif "model_anomaly" in df.columns:
        df["anomaly"] = pd.to_numeric(df["model_anomaly"], errors="coerce").fillna(0).astype(int)
    else:
        df["anomaly"] = 0

    if "model_anomaly" in df.columns:
        df["model_anomaly"] = pd.to_numeric(df["model_anomaly"], errors="coerce").fillna(0).astype(int)

    if "anomaly_type" not in df.columns:
        df["anomaly_type"] = "normal"
    else:
        df["anomaly_type"] = df["anomaly_type"].fillna("normal").astype(str)

    return df


def load_data() -> pd.DataFrame:
    week_files = sorted(DATA_DIR.glob("processed_week_*.csv"))

    if not week_files:
        return pd.DataFrame()

    frames = []
    for file in week_files:
        temp = _read_week_file(file)
        if temp is not None and not temp.empty:
            frames.append(temp)

    if not frames:
        return pd.DataFrame()

    df = pd.concat(frames, ignore_index=True)

    df = df.dropna(subset=["timestamp"])
    df = df.sort_values("timestamp")
    df = df.drop_duplicates(subset=["timestamp"], keep="last")
    df = df.reset_index(drop=True)

    iso = df["timestamp"].dt.isocalendar()
    df["year"] = iso.year.astype(int)
    df["week"] = iso.week.astype(int)
    df["date"] = df["timestamp"].dt.date
    df["month"] = df["timestamp"].dt.month
    df["day"] = df["timestamp"].dt.day
    df["year_week"] = iso.year.astype(str) + "-" + iso.week.astype(str).str.zfill(2)

    return df