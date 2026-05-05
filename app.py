import streamlit as st
import pandas as pd

from utils.data_loader import load_data
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


st.set_page_config(
    page_title="Intelligent Anomaly Monitoring System",
    page_icon="data/logo.png",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown(
    """
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
    """,
    unsafe_allow_html=True
)


def classify_severity(z):
    if pd.isna(z):
        return "normal"

    z = abs(float(z))

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


@st.cache_data(ttl=300)
def get_dashboard_data():
    df = load_data()
    if df.empty:
        return df

    if "timestamp" not in df.columns:
        return pd.DataFrame()

    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce", dayfirst=True)
    df = df.dropna(subset=["timestamp"]).sort_values("timestamp").reset_index(drop=True)

    if "z_score" in df.columns:
        df["z_score"] = pd.to_numeric(df["z_score"], errors="coerce")
    else:
        df["z_score"] = 0.0

    if "anomaly_type" not in df.columns:
        df["anomaly_type"] = "normal"

    if "anomaly" not in df.columns:
        df["anomaly"] = 0

    iso = df["timestamp"].dt.isocalendar()
    df["year"] = iso.year.astype(int)
    df["week"] = iso.week.astype(int)
    df["year_week"] = (
        iso.year.astype(str) + "-" + iso.week.astype(str).str.zfill(2)
    )
    df["date"] = df["timestamp"].dt.date

    df["severity"] = df["z_score"].apply(classify_severity)

    return df


df = get_dashboard_data()

if df.empty:
    st.error("No processed data found in the data folder.")
    st.stop()

latest_year_week = df["year_week"].max()
recent_df = df[df["year_week"] == latest_year_week].copy()

st.markdown("<br>", unsafe_allow_html=True)
title_col, badge_col = st.columns([5, 1])

with title_col:
    st.title("Intelligent Anomaly Monitoring System")
    st.caption("Machine Learning Based System Monitoring Dashboard")

with badge_col:
    render_system_health(df)

st.markdown("---")

st.sidebar.header("Dashboard Filters")

anomaly_types = st.sidebar.multiselect(
    "Select Anomaly Type",
    options=sorted(df["anomaly_type"].dropna().unique().tolist()),
    default=sorted(df["anomaly_type"].dropna().unique().tolist())
)

z_abs = df["z_score"].abs().fillna(0)
min_severity = st.sidebar.slider(
    "Minimum Z-Score Severity",
    min_value=0.0,
    max_value=float(z_abs.max()) if len(z_abs) else 0.0,
    value=0.0
)

start_date = st.sidebar.date_input(
    "Start Date",
    value=df["date"].min()
)

end_date = st.sidebar.date_input(
    "End Date",
    value=df["date"].max()
)

filtered_df = df.copy()

filtered_df = filtered_df[
    filtered_df["anomaly_type"].isin(anomaly_types)
]

filtered_df = filtered_df[
    filtered_df["z_score"].abs().fillna(0) >= min_severity
]

filtered_df = filtered_df[
    (filtered_df["date"] >= start_date) &
    (filtered_df["date"] <= end_date)
]

if filtered_df.empty:
    st.warning("No rows match the current filters.")
    st.stop()

render_kpis(df)

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    render_daily_anomaly_trend(df)

with col2:
    render_weekly_anomaly_trend(df)

col3, col4 = st.columns(2)

with col3:
    render_signal_timeline(filtered_df)

with col4:
    render_zscore_chart(filtered_df)

col5, col6 = st.columns(2)

with col5:
    render_anomaly_distribution(df)

with col6:
    render_top_anomalies_table(filtered_df)

col7, col8 = st.columns(2)

with col7:
    render_severity_bar(df)

with col8:
    render_feature_correlation(filtered_df)

st.markdown("---")
render_insight_panel(filtered_df)