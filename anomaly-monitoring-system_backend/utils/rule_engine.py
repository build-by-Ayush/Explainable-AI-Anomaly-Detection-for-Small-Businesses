def classify_anomalies(df):

    df["anomaly_type"] = "normal"

    mask = df["model_anomaly"] == 1

    spike = (
        (df["value"] > df["rolling_mean_30"] + 3 * df["rolling_std_30"]) &
        (df["value_diff"] > 0)
    )

    drop = (
        (df["value"] < df["rolling_mean_30"] - 3 * df["rolling_std_30"]) &
        (df["value_diff"] < 0)
    )

    volatility = (
        df["rolling_std_30"] > 1.8 * df["rolling_std_60"]
    )

    drift = (
        abs(df["rolling_mean_30"] - df["rolling_mean_30"].shift(30))
        > 2 * df["rolling_std_60"]
    )

    level_shift = (
        abs(df["rolling_mean_30"] - df["rolling_mean_30"].shift(10))
        > 3 * df["rolling_std_60"]
    )

    df.loc[mask & spike, "anomaly_type"] = "spike"
    df.loc[mask & drop, "anomaly_type"] = "drop"
    df.loc[mask & volatility, "anomaly_type"] = "volatility"
    df.loc[mask & drift, "anomaly_type"] = "drift"
    df.loc[mask & level_shift, "anomaly_type"] = "level_shift"

    return df