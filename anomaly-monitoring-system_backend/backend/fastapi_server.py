from fastapi import FastAPI
import numpy as np
import pandas as pd
import glob
import os


app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FOLDER = os.path.join(BASE_DIR, "..", "processed_data")


@app.get("/")
def home():
    return {"message": "Anomaly Detection Backend Running"}


import numpy as np

@app.get("/get-data")
def get_data():

    files = sorted(glob.glob(f"{DATA_FOLDER}/*.csv"))[-26:]

    if not files:
        return {"message": "No data available"}

    df_list = [pd.read_csv(f) for f in files]
    df = pd.concat(df_list)

    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(
            df["timestamp"],
            dayfirst=True,
            errors="coerce"
        ).astype(str)

    df = df.replace([np.inf, -np.inf], None)
    df = df.fillna("")

    return df.to_dict(orient="records")