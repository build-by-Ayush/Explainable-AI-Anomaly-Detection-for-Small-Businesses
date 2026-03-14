import streamlit as st
import plotly.express as px


def render_severity_bar(df):
    """
    Severity distribution of detected anomalies.
    """

    st.subheader("Anomaly Severity Distribution")

    # -----------------------------------------
    # Use only anomalies
    # -----------------------------------------

    anomaly_df = df[df["anomaly"] == 1]

    severity_counts = (
        anomaly_df["severity"]
        .value_counts()
        .reset_index()
    )

    severity_counts.columns = ["severity", "count"]

    severity_order = ["low", "medium", "high", "critical"]

    severity_counts["severity"] = severity_counts["severity"].astype("category")
    severity_counts["severity"] = severity_counts["severity"].cat.set_categories(
        severity_order, ordered=True
    )

    severity_counts = severity_counts.sort_values("severity")
    
    # -----------------------------------------
    # Create chart
    # -----------------------------------------

    fig = px.bar(
        severity_counts,
        x="severity",
        y="count",
        color="severity",
        color_discrete_map={
            "low": "#38bdf8",
            "medium": "#facc15",
            "high": "#fb923c",
            "critical": "#FF4B4B"
        }
    )

    # -----------------------------------------
    # Styling
    # -----------------------------------------

    fig.update_layout(

        plot_bgcolor="#11161C",
        paper_bgcolor="#11161C",

        font=dict(color="white"),

        margin=dict(l=20, r=20, t=40, b=20),

        xaxis_title="Severity Level",
        yaxis_title="Number of Anomalies",

        xaxis=dict(
            showgrid=True,
            gridcolor="rgba(255,255,255,0.05)"
        ),

        yaxis=dict(
            showgrid=True,
            gridcolor="rgba(255,255,255,0.05)"
        )
    )

    st.plotly_chart(fig, use_container_width=True)