import streamlit as st
import plotly.graph_objects as go


def render_zscore_chart(df):
    """
    Z-score anomaly visualization.
    Shows statistical deviation of signal values.
    """

    st.subheader("Z-Score Anomaly Detection")

    # -----------------------------------------
    # Separate anomaly points
    # -----------------------------------------

    anomaly_df = df[df["anomaly"] == 1]

    # -----------------------------------------
    # Create chart
    # -----------------------------------------

    fig = go.Figure()

    # Z-score line
    fig.add_trace(
        go.Scatter(
            x=df["timestamp"],
            y=df["z_score"],
            mode="lines",
            name="Z-Score",
            line=dict(color="rgba(255,77,166,0.35)", width=1)
        )
    )

    # Upper threshold line
    fig.add_trace(
        go.Scatter(
            x=df["timestamp"],
            y=[3] * len(df),
            mode="lines",
            name="Upper Threshold",
            line=dict(color="#FFA500", dash="dash")
        )
    )

    # Lower threshold line
    fig.add_trace(
        go.Scatter(
            x=df["timestamp"],
            y=[-3] * len(df),
            mode="lines",
            name="Lower Threshold",
            line=dict(color="#FFA500", dash="dash")
        )
    )

    # Anomaly markers
    fig.add_trace(
        go.Scatter(
            x=anomaly_df["timestamp"],
            y=anomaly_df["z_score"],
            mode="markers",
            name="Anomaly",
            marker=dict(
                color="#FF4B4B",
                size=8
            )
        )
    )

    fig.add_hrect(
        y0=-3,
        y1=3,
        fillcolor="rgba(0,255,0,0.05)",
        line_width=0
    )

    # -----------------------------------------
    # Chart styling
    # -----------------------------------------

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


def render_anomaly_distribution(df):
    """
    Displays anomaly type distribution.
    """

    st.subheader("Anomaly Type Distribution")

    import plotly.express as px

    # -----------------------------------------
    # Count anomaly types
    # -----------------------------------------

    anomaly_df = df[df["anomaly"] == 1]

    counts = anomaly_df["anomaly_type"].value_counts().reset_index()
    counts.columns = ["anomaly_type", "count"]

    print(df["anomaly_type"].value_counts(dropna=False))

    # -----------------------------------------
    # Create pie chart
    # -----------------------------------------

    fig = px.pie(
        counts,
        names="anomaly_type",
        values="count",
        color="anomaly_type",
        color_discrete_map={
            "normal": "#8B9EBF",
            "spike": "#4079F4",
            "drop": "#5007CE",
            "volatility": "#674CBF"
        }
    )

    # -----------------------------------------
    # Styling
    # -----------------------------------------

    fig.update_layout(
        plot_bgcolor="#11161C",
        paper_bgcolor="#11161C",
        font=dict(color="white"),
        margin=dict(l=20, r=20, t=40, b=20)
    )

    st.plotly_chart(fig, use_container_width=True)