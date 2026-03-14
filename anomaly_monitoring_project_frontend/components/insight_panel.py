import streamlit as st
import pandas as pd


def render_insight_panel(df):
    """
    AI Insight Panel

    Shows both:
    1. Latest anomaly detected
    2. Most severe anomaly detected
    """

    st.markdown("## Insight Panel")

    anomaly_df = df[df["anomaly"] == 1]

    # ---------------------------------------------------
    # HEALTHY SYSTEM
    # ---------------------------------------------------

    if anomaly_df.empty:

        st.markdown(
            """
            <div style="
                background:#11161C;
                border:1px solid #00E5FF;
                padding:25px;
                border-radius:12px;
                text-align:center;
            ">

            <h3 style="color:#00E5FF;">System Status: Healthy</h3>

            <p style="color:#9ca3af;font-size:16px;">
            No anomalies detected in the current monitoring window.
            System signals are operating within expected statistical boundaries.
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )

        return

    # ---------------------------------------------------
    # IDENTIFY ANOMALIES
    # ---------------------------------------------------

    latest_anomaly = anomaly_df.sort_values("timestamp", ascending=False).iloc[0]

    most_severe = anomaly_df.loc[anomaly_df["z_score"].abs().idxmax()]

    # ---------------------------------------------------
    # LATEST ANOMALY VALUES
    # ---------------------------------------------------

    latest_type = latest_anomaly["anomaly_type"]
    latest_z = round(latest_anomaly["z_score"], 2)
    latest_time = latest_anomaly["timestamp"]

    # ---------------------------------------------------
    # MOST SEVERE VALUES
    # ---------------------------------------------------

    severe_type = most_severe["anomaly_type"]
    severe_z = round(most_severe["z_score"], 2)
    severe_time = most_severe["timestamp"]

    # ---------------------------------------------------
    # LAYOUT
    # ---------------------------------------------------

    col1, col2 = st.columns(2)

    # ---------------------------------------------------
    # LATEST ANOMALY BOX
    # ---------------------------------------------------

    with col1:

        st.markdown(
            f"""
            <div style="
                background:#11161C;
                border:1px solid #00E5FF;
                padding:25px;
                border-radius:12px;
                height:100%;
            ">

            <h3 style="color:#00E5FF;">Latest Anomaly</h3>

            <p style="color:#9ca3af;">
            Timestamp: <b>{latest_time}</b><br>
            Type: <b>{latest_type}</b><br>
            Severity (Z-score): <b>{latest_z}</b>
            </p>

            <hr style="border-color:#2c3440">

            <h4 style="color:#00E5FF;">Potential Cause</h4>

            <p style="color:#d1d5db;">
            A recent deviation in the monitored signal exceeded the anomaly detection threshold.
            </p>

            <h4 style="color:#00E5FF;">Suggested Solution</h4>

            <ul style="color:#d1d5db;">
            <li>Solution 1</li>
            <li>Solution 2</li>
            </ul>

            <p style="color:#9ca3af;font-size:13px;">
            Note: Solutions shown here are placeholders for demonstration purposes.
            In a production system these would be generated from operational knowledge bases.
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )

    # ---------------------------------------------------
    # MOST SEVERE ANOMALY BOX
    # ---------------------------------------------------

    with col2:

        st.markdown(
            f"""
            <div style="
                background:#11161C;
                border:1px solid #FF4B4B;
                padding:25px;
                border-radius:12px;
                height:100%;
            ">

            <h3 style="color:#FF4B4B;">Most Severe Anomaly</h3>

            <p style="color:#9ca3af;">
            Timestamp: <b>{severe_time}</b><br>
            Type: <b>{severe_type}</b><br>
            Severity (Z-score): <b>{severe_z}</b>
            </p>

            <hr style="border-color:#2c3440">

            <h4 style="color:#FF4B4B;">Potential Cause</h4>

            <p style="color:#d1d5db;">
            This event represents the largest statistical deviation detected in the monitoring window.
            </p>

            <h4 style="color:#FF4B4B;">Suggested Solution</h4>

            <ul style="color:#d1d5db;">
            <li>Solution 1</li>
            <li>Solution 2</li>
            </ul>

            <p style="color:#9ca3af;font-size:13px;">
            Note: Solutions shown here are placeholders for demonstration purposes.
            In a production system these would be generated from operational knowledge bases.
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )