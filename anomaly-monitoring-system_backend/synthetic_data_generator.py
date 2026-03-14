import pandas as pd
import numpy as np


def generate_time_series(
    start_date=None,
    periods=10080,   # 1 week of minute data
    freq="1min",
    base_value=50
):

    if start_date is None:
        start_date = pd.Timestamp.now().floor("D")  # today
    timestamps = pd.date_range(start=start_date, periods=periods, freq=freq)

    # realistic machine signal
    daily_cycle = 8 * np.sin(np.linspace(0, 14 * np.pi, periods))
    noise = np.random.normal(0, 1.5, periods)

    values = base_value + daily_cycle + noise

    return pd.DataFrame({
        "timestamp": timestamps,
        "value": values
    })


def inject_spike(df, index, magnitude=40):
    df.loc[index, "value"] += magnitude
    return df


def inject_drop(df, index, magnitude=40):
    df.loc[index, "value"] -= magnitude
    return df


def inject_level_shift(df, start_index, shift_value=12):
    df.loc[start_index:, "value"] += shift_value
    return df


def inject_drift(df, start_index, drift_rate=0.015):
    drift = np.arange(len(df) - start_index) * drift_rate
    df.loc[start_index:, "value"] += drift
    return df


def inject_volatility(df, start_index, magnitude=8):
    noise = np.random.normal(0, magnitude, len(df) - start_index)
    df.loc[start_index:, "value"] += noise
    return df


def create_dataset(start_date=None):
    if start_date is None:
        start_date = pd.Timestamp.now().floor("D")  # today's date

    df = generate_time_series()

    # Inject anomalies (hidden from model)
    df = inject_spike(df, 1500)
    df = inject_drop(df, 3000)
    df = inject_level_shift(df, 4500)
    df = inject_drift(df, 6000)
    df = inject_volatility(df, 8000)

    return df


if __name__ == "__main__":
    df = create_dataset()
    df.to_csv("incoming_data/synthetic_machine_data.csv", index=False)