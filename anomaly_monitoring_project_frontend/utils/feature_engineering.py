import pandas as pd
import numpy as np


def generate_features(df):

    df = df.copy()

    # ------------------------------------------------
    # Rolling statistics (MATCH BACKEND)
    # ------------------------------------------------

    df["rolling_mean_10"] = df["value"].rolling(10).mean()

    df["rolling_mean_30"] = df["value"].rolling(30).mean()

    df["rolling_std_30"] = df["value"].rolling(30).std()

    # ------------------------------------------------
    # Rolling extremes
    # ------------------------------------------------

    df["rolling_max_10"] = df["value"].rolling(10).max()

    df["rolling_min_10"] = df["value"].rolling(10).min()

    # ------------------------------------------------
    # Value difference
    # ------------------------------------------------

    df["value_diff"] = df["value"].diff()

    # ------------------------------------------------
    # Percent change
    # ------------------------------------------------

    df["pct_change"] = df["value"].pct_change()

    # ------------------------------------------------
    # Rolling Z-score (NO DATA LEAKAGE)
    # ------------------------------------------------

    df["z_score"] = (
        (df["value"] - df["rolling_mean_30"]) /
        df["rolling_std_30"]
    )

    # ------------------------------------------------
    # Clean dataset
    # ------------------------------------------------

    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.dropna()

    # ------------------------------------------------
    # Rule Engine Anomaly Detection
    # ------------------------------------------------

    df["anomaly"] = (df["z_score"].abs() > 3).astype(int)

    df["anomaly_type"] = "normal"

    # spike
    spike = (
        (df["value"] > df["rolling_mean_30"] + 3 * df["rolling_std_30"])
        & (df["value_diff"] > 0)
    )

    # drop
    drop = (
        (df["value"] < df["rolling_mean_30"] - 3 * df["rolling_std_30"])
        & (df["value_diff"] < 0)
    )

    # volatility
    df["rolling_std_60"] = df["value"].rolling(60).std()

    volatility = (
        df["rolling_std_30"] > 1.8 * df["rolling_std_60"]
    )

    # drift
    drift = (
        abs(df["rolling_mean_30"] - df["rolling_mean_30"].shift(30))
        > 2 * df["rolling_std_60"]
    )

    # level shift
    level_shift = (
        abs(df["rolling_mean_30"] - df["rolling_mean_30"].shift(10))
        > 3 * df["rolling_std_60"]
    )

    df.loc[spike, "anomaly_type"] = "spike"
    df.loc[drop, "anomaly_type"] = "drop"
    df.loc[volatility, "anomaly_type"] = "volatility"
    df.loc[drift, "anomaly_type"] = "drift"
    df.loc[level_shift, "anomaly_type"] = "level_shift"

    return df