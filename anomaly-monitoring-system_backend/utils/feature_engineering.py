import pandas as pd
import numpy as np


def generate_features(df):

    df = df.copy()

    df["rolling_mean_10"] = df["value"].rolling(10).mean()
    df["rolling_mean_30"] = df["value"].rolling(30).mean()

    df["rolling_std_30"] = df["value"].rolling(30).std()
    df["rolling_std_60"] = df["value"].rolling(60).std()

    df["rolling_max_10"] = df["value"].rolling(10).max()
    df["rolling_min_10"] = df["value"].rolling(10).min()

    df["value_diff"] = df["value"].diff()
    df["pct_change"] = df["value"].pct_change()

    # rolling z-score (no leakage)
    df["z_score"] = (
        (df["value"] - df["rolling_mean_30"]) /
        df["rolling_std_30"]
    )

    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.dropna()

    return df