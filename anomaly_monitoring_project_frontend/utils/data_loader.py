import pandas as pd

def load_data():

    df = pd.read_csv("data/processed_anomaly_data.csv")

    df["timestamp"] = pd.to_datetime(df["timestamp"])

    return df