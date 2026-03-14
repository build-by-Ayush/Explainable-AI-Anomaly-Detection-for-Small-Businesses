import streamlit as st
import plotly.express as px
import pandas as pd


def render_weekly_anomaly_trend(df):

    st.subheader("Weekly Anomaly Trend")

    df = df.copy()

    # ---------------------------------------------------
    # Create a proper weekly timestamp (start of week)
    # ---------------------------------------------------

    df["week_start"] = df["timestamp"].dt.to_period("W").apply(lambda r: r.start_time)

    # ---------------------------------------------------
    # Weekly aggregation
    # ---------------------------------------------------

    weekly = (
        df.groupby("week_start")
        .agg(
            total_records=("anomaly", "count"),
            anomalies=("anomaly", "sum")
        )
        .reset_index()
    )

    weekly["anomaly_rate"] = (
        weekly["anomalies"] / weekly["total_records"]
    ) * 100

    # ---------------------------------------------------
    # Plot
    # ---------------------------------------------------

    fig = px.line(
        weekly,
        x="week_start",
        y="anomaly_rate",
        markers=True
    )

    # ---------------------------------------------------
    # Chart styling
    # ---------------------------------------------------

    fig.update_layout(
        plot_bgcolor="#11161C",
        paper_bgcolor="#11161C",
        font=dict(color="white"),
        xaxis_title="Week",
        yaxis_title="Anomaly Rate (%)"
    )

    st.plotly_chart(fig, use_container_width=True)