import streamlit as st


def render_system_health(df):

    week = df["week"].max()
    week_df = df[df["week"] == week]

    week_rate = (week_df["anomaly"].sum() / len(week_df)) * 100

    critical_pct = (
        len(df[df["severity"] == "critical"]) / len(df)
    )

    avg_z = df["z_score"].abs().mean()

    health_score = (
        100
        - (week_rate * 1.5)
        - (critical_pct * 40)
        - (avg_z * 2)
    )

    if health_score > 85:
        label = "System Health : HEALTHY"
        color = "#22c55e"

    elif health_score > 65:
        label = "System Health : WARNING"
        color = "#f59e0b"

    else:
        label = "System Health : CRITICAL"
        color = "#ef4444"

    st.markdown(
        f"""
        <div style="
            background:{color};
            padding:10px 20px;
            border-radius:10px;
            text-align:center;
            font-weight:700;
            color:white;
            margin-top:25px;
        ">
        {label}
        </div>
        """,
        unsafe_allow_html=True
    )