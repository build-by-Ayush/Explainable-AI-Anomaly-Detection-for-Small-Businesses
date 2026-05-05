import streamlit as st
import plotly.graph_objects as go
import pandas as pd


def render_signal_timeline(df):
    """
    Signal timeline chart with anomaly overlay.
    """

    st.subheader("Signal Monitoring Timeline")

    # -------------------------------------------
    # Work on local copy to avoid pipeline impact
    # -------------------------------------------

    df_chart = df.copy()

    # -------------------------------------------
    # Focus view on recent activity (last 3 days)
    # -------------------------------------------

    latest_time = df_chart["timestamp"].max()

    df_chart = df_chart[
        df_chart["timestamp"] >= latest_time - pd.Timedelta(days=3)
    ]

    # -------------------------------------------
    # Create smoother rolling mean ONLY for chart
    # -------------------------------------------

    df_chart["rolling_mean_60"] = df_chart["value"].rolling(60).mean()

    anomaly_df = df_chart[df_chart["anomaly"] == 1]

    # -------------------------------------------
    # Create Plotly figure
    # -------------------------------------------

    fig = go.Figure()

    # Signal line
    fig.add_trace(
        go.Scatter(
            x=df_chart["timestamp"],
            y=df_chart["value"],
            mode="lines",
            name="Signal Value",
            line=dict(color="rgba(0,229,255,0.25)", width=1)
        )
    )

    # Rolling mean
    fig.add_trace(
        go.Scatter(
            x=df_chart["timestamp"],
            y=df_chart["rolling_mean_60"],
            mode="lines",
            name="Rolling Mean",
            line=dict(color="#2ECC71", width=2)
        )
    )

    # Anomaly points
    fig.add_trace(
        go.Scatter(
            x=anomaly_df["timestamp"],
            y=anomaly_df["value"],
            mode="markers",
            name="Anomaly",
            marker=dict(
                color="#FF4B4B",
                size=8
            )
        )
    )

    # -------------------------------------------
    # Chart styling
    # -------------------------------------------

    fig.update_layout(

        plot_bgcolor="#11161C",
        paper_bgcolor="#11161C",

        font=dict(color="white"),

        margin=dict(l=20, r=20, t=40, b=20),

        xaxis=dict(
            showgrid=True,
            gridcolor="rgba(255,255,255,0.05)"
        ),

        yaxis=dict(
            showgrid=True,
            gridcolor="rgba(255,255,255,0.05)"
        ),

        legend=dict(
            orientation="h",
            y=1.02
        )
    )

    st.plotly_chart(fig, use_container_width=True)