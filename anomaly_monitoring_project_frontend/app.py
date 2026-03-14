import streamlit as st
import pandas as pd
import requests

from components.kpi_cards import render_kpis
from components.signal_charts import render_signal_timeline
from components.anomaly_charts import (
    render_zscore_chart,
    render_anomaly_distribution
)
from components.system_health import render_system_health
from components.tables import render_top_anomalies_table
from components.weekly_charts import render_weekly_anomaly_trend
from components.daily_charts import render_daily_anomaly_trend
from components.severity_charts import render_severity_bar
from components.correlation_chart import render_feature_correlation
from components.insight_panel import render_insight_panel


# ---------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------

st.set_page_config(
    page_title="Intelligent Anomaly Monitoring System",
    page_icon="data/logo.png",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------
# GLOBAL CSS
# ---------------------------------------------------

st.markdown("""
<style>

.stApp{
    background: linear-gradient(
        to right,
        #0b0f14 40%,
        #0b0f14 80%,
        #121922 100%
    );
}

.block-container{
    padding-top: 1rem;
    padding-bottom: 4rem;
}

section[data-testid="stSidebar"]{
    background-color:#0b0f14;
    padding-top:1rem;
}

.chart-card{
    background:#11161C;
    padding:20px;
    border-radius:12px;
    border:1px solid rgba(255,255,255,0.08);
}

h1{
    text-shadow:0px 0px 10px rgba(0,255,255,0.45);
}

.kpi-title{
    font-size:20px;
    color:#9ca3af;
}

.kpi-value{
    font-size:46px;
    font-weight:800;
}

.kpi-blue{color:#38bdf8;}
.kpi-green{color:#22c55e;}
.kpi-orange{color:#fb923c;}
.kpi-yellow{color:#facc15;}
.kpi-purple{color:#a78bfa;}

</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

@st.cache_data
def load_data():

    df = pd.read_csv("anomaly_monitoring_project_frontend/data/processed_anomaly_data.csv")

    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

    df = df.dropna(subset=["timestamp"])
    
    # Explicit datetime format
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # Standardized time features
    df["date"] = df["timestamp"].dt.date
    df["week"] = df["timestamp"].dt.isocalendar().week
    df["year"] = df["timestamp"].dt.year

    df["year_week"] = (
        df["timestamp"].dt.isocalendar().year.astype(str)
        + "-"
        + df["timestamp"].dt.isocalendar().week.astype(str)
    )

    return df


df = load_data()

latest_year_week = df["year_week"].max()

recent_df = df[df["year_week"] == latest_year_week]

# ---------------------------------------------------
# CREATE SEVERITY LEVEL (Derived from Z-score)
# ---------------------------------------------------

def classify_severity(z):

    z = abs(z)

    if z < 2:
        return "normal"
    elif z < 3:
        return "low"
    elif z < 4:
        return "medium"
    elif z < 5:
        return "high"
    else:
        return "critical"


df["severity"] = df["z_score"].apply(classify_severity)


# ---------------------------------------------------
# TITLE
# ---------------------------------------------------

st.markdown("<br>", unsafe_allow_html=True)
title_col, badge_col = st.columns([5,1])

with title_col:
    st.title("Intelligent Anomaly Monitoring System")
    st.caption("Machine Learning Based System Monitoring Dashboard")

with badge_col:
    render_system_health(df)

st.markdown("---")


# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.header("Dashboard Filters")

anomaly_types = st.sidebar.multiselect(
    "Select Anomaly Type",
    options=df["anomaly_type"].unique(),
    default=df["anomaly_type"].unique()
)

min_severity = st.sidebar.slider(
    "Minimum Z-Score Severity",
    min_value=0.0,
    max_value=float(df["z_score"].abs().max()),
    value=0.0
)

start_date = st.sidebar.date_input(
    "Start Date",
    df["timestamp"].min()
)

end_date = st.sidebar.date_input(
    "End Date",
    df["timestamp"].max()
)


# ---------------------------------------------------
# FILTER DATA
# ---------------------------------------------------

filtered_df = df.copy()

filtered_df = filtered_df[
    filtered_df["anomaly_type"].isin(anomaly_types)
]

filtered_df = filtered_df[
    filtered_df["z_score"].abs() >= min_severity
]

filtered_df = filtered_df[
    (filtered_df["timestamp"] >= pd.to_datetime(start_date)) &
    (filtered_df["timestamp"] <= pd.to_datetime(end_date))
]


# ---------------------------------------------------
# KPI
# ---------------------------------------------------

render_kpis(df)

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    render_daily_anomaly_trend(df)

with col2:
    render_weekly_anomaly_trend(df)


# ---------------------------------------------------
# ROW 1
# ---------------------------------------------------

col3, col4 = st.columns(2)

with col3:
    render_signal_timeline(filtered_df)

with col4:
    render_zscore_chart(filtered_df)


# ---------------------------------------------------
# ROW 2
# ---------------------------------------------------

col5, col6 = st.columns(2)

with col5:
    render_anomaly_distribution(df)

with col6:
    render_top_anomalies_table(filtered_df)


# ---------------------------------------------------
# ROW 3
# ---------------------------------------------------

col7, col8 = st.columns(2)

with col7:
    render_severity_bar(df)

with col8:
    render_feature_correlation(filtered_df)


st.markdown("---")

render_insight_panel(filtered_df)
