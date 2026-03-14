import streamlit as st


def render_kpis(df):

    if "week" not in df.columns:
        df["week"] = df["timestamp"].dt.isocalendar().week

    latest_week = df["week"].max()

    week_df = df[df["week"] == latest_week]

    # -----------------------------
    # WEEK METRICS
    # -----------------------------

    week_records = len(week_df)

    week_anomalies = week_df["anomaly"].sum()

    week_rate = (week_anomalies / week_records) * 100 if week_records > 0 else 0

    # -----------------------------
    # OVERALL METRICS
    # -----------------------------

    total_records = len(df)

    total_anomalies = df["anomaly"].sum()

    overall_rate = (total_anomalies / total_records) * 100 if total_records > 0 else 0

    # -----------------------------
    # KPI LAYOUT
    # -----------------------------

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.markdown(f"""
        <div class="kpi-title kpi-blue">Latest Data Week</div>
        <div class="kpi-value kpi-blue">{latest_week}</div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="kpi-title kpi-green">Week Observations</div>
        <div class="kpi-value kpi-green">{week_records}</div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="kpi-title kpi-orange">This Week Anomalies</div>
        <div class="kpi-value kpi-orange">{week_anomalies}</div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="kpi-title kpi-yellow">Week Anomaly Rate</div>
        <div class="kpi-value kpi-yellow">{week_rate:.2f}%</div>
        """, unsafe_allow_html=True)

    with col5:
        st.markdown(f"""
        <div class="kpi-title kpi-purple">Overall Anomaly Rate</div>
        <div class="kpi-value kpi-purple">{overall_rate:.2f}%</div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)