import os
import pandas as pd
import numpy as np
import joblib
from tensorflow.keras.models import load_model
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import tensorflow as tf

from utils.feature_engineering import generate_features
from utils.rule_engine import classify_anomalies


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

model = load_model(os.path.join(BASE_DIR, "models/lstm_anomaly_model.h5"))
scaler = joblib.load(os.path.join(BASE_DIR, "models/scaler.pkl"))
scaler = joblib.load("models/scaler.pkl")


def create_sequences(data, window_size=50):

    sequences = []

    for i in range(len(data) - window_size):
        sequences.append(data[i:i + window_size])

    return np.array(sequences)


def run_pipeline(file_path):

    df = pd.read_csv(file_path)

    df["timestamp"] = pd.to_datetime(df["timestamp"])

    df = generate_features(df)

    features = [
        "value",
        "rolling_mean_10",
        "rolling_mean_30",
        "rolling_std_30",
        "value_diff",
        "pct_change",
        "z_score",
        "rolling_max_10",
        "rolling_min_10"
    ]

    X = df[features].astype(float)

    X_scaled = scaler.transform(X)

    window_size = 50
    X_seq = create_sequences(X_scaled, window_size)

    predictions = model.predict(X_seq).flatten()

    df = df.iloc[window_size:].copy()

    df["anomaly_score"] = predictions
    df["model_anomaly"] = (df["anomaly_score"] > 0.8).astype(int)

    # classify anomalies
    df = classify_anomalies(df)

    return df