import streamlit as st
import pandas as pd


def render_top_anomalies_table(df):
    """
    Displays most severe anomalies for investigation.
    """

    st.subheader("Top Detected Anomalies")

    # -----------------------------------------
    # Filter anomaly rows
    # -----------------------------------------

    anomaly_df = df[df["anomaly"] == 1].copy()

    # -----------------------------------------
    # Severity calculation
    # -----------------------------------------

    anomaly_df["severity"] = anomaly_df["z_score"].abs()

    # -----------------------------------------
    # Sort by severity
    # -----------------------------------------

    anomaly_df = (
        anomaly_df.sort_values(by="severity", ascending=False)
        .head(10)
        .reset_index(drop=True)
    )

    # -----------------------------------------
    # Select useful columns
    # -----------------------------------------

    display_cols = [
        "timestamp",
        "value",
        "z_score",
        "pct_change",
        "anomaly_type",
        "severity"
    ]

    anomaly_df = anomaly_df[display_cols]

    # -----------------------------------------
    # Show top anomalies
    # -----------------------------------------

    st.dataframe(
        anomaly_df.head(20),
        use_container_width=True
    )