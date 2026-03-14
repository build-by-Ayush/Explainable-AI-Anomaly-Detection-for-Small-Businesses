import os

import pandas as pd
import numpy as np
from utils.feature_engineering import generate_features


def generate_time_series(
    start_date="2026-01-01",
    periods=105120,
    freq="1min",
    base_value=50
):

    timestamps = pd.date_range(start=start_date, periods=periods, freq=freq)

    # seasonality
    daily_cycle = 10 * np.sin(np.linspace(0, 50 * np.pi, periods))

    # noise
    noise = np.random.normal(0, 2, periods)

    values = base_value + daily_cycle + noise

    df = pd.DataFrame({
        "timestamp": timestamps,
        "value": values
    })

    return df


def inject_spike(df, index, magnitude=40):
    df.loc[index, "value"] += magnitude
    return df


def inject_drop(df, index, magnitude=40):
    df.loc[index, "value"] -= magnitude
    return df


def inject_level_shift(df, start_index, shift_value=15):
    df.loc[start_index:, "value"] += shift_value
    return df


def inject_drift(df, start_index, drift_rate=0.01):
    drift = np.arange(len(df) - start_index) * drift_rate
    df.loc[start_index:, "value"] += drift
    return df


def inject_volatility(df, start_index, magnitude=10):
    noise = np.random.normal(0, magnitude, len(df) - start_index)
    df.loc[start_index:, "value"] += noise
    return df


def create_dataset():

    df = generate_time_series()

    size = len(df)

    np.random.seed(42)

    # spikes
    for i in np.random.randint(1000, size - 1000, 20):
        df = inject_spike(df, i)

    # drops
    for i in np.random.randint(1000, size - 1000, 15):
        df = inject_drop(df, i)

    # level shifts
    df = inject_level_shift(df, 12000)
    df = inject_level_shift(df, 30000)

    # drift
    df = inject_drift(df, 20000)

    # volatility
    df = inject_volatility(df, 35000)

    return df


if __name__ == "__main__":

    df = create_dataset()

    df = generate_features(df)

    # ensure folder exists
    os.makedirs("data", exist_ok=True)

    df.to_csv("data/processed_anomaly_data.csv", index=False)

    print("Processed dataset generated successfully")