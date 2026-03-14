import streamlit as st
import plotly.express as px
import pandas as pd


def render_daily_anomaly_trend(df):

    st.subheader("Daily Anomaly Trend (Latest Week)")

    df = df.copy()

    df["date"] = df["timestamp"].dt.date
    df["year_week"] = (
        df["timestamp"].dt.isocalendar().year.astype(str)
        + "-"
        + df["timestamp"].dt.isocalendar().week.astype(str)
    )

    latest_week = df["year_week"].max()

    week_df = df[df["year_week"] == latest_week]

    daily = (
        week_df.groupby("date")
        .agg(
            total_records=("anomaly", "count"),
            anomalies=("anomaly", "sum")
        )
        .reset_index()
    )

    daily["anomaly_rate"] = (daily["anomalies"] / daily["total_records"]) * 100

    # ensure full 7 days
    date_range = pd.date_range(
        start=min(daily["date"]),
        periods=7
    )

    daily = (
        daily.set_index("date")
        .reindex(date_range.date, fill_value=0)
        .reset_index()
    )

    daily.columns = ["date", "total_records", "anomalies", "anomaly_rate"]

    fig = px.line(
        daily,
        x="date",
        y="anomaly_rate",
        markers=True
    )

    fig.update_layout(
        plot_bgcolor="#11161C",
        paper_bgcolor="#11161C",
        font=dict(color="white")
    )

    st.plotly_chart(fig, use_container_width=True)