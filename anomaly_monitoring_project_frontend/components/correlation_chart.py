import streamlit as st
import plotly.express as px


def render_feature_correlation(df):
    """
    Displays correlation between engineered features.
    Handles missing columns gracefully.
    """

    st.subheader("Feature Correlation Heatmap")

    # Expected engineered features
    expected_columns = [
        "value",
        "rolling_mean_5",
        "rolling_std_5",
        "pct_change",
        "z_score",
        "value_diff"
    ]

    # Keep only columns that exist in dataframe
    available_columns = [col for col in expected_columns if col in df.columns]

    # If too few columns exist, skip visualization
    if len(available_columns) < 2:
        st.warning("Not enough feature columns available to compute correlation.")
        return

    corr = df[available_columns].corr()

    fig = px.imshow(
        corr,
        text_auto=True,
        color_continuous_scale="RdBu",
        aspect="auto"
    )

    fig.update_layout(
        plot_bgcolor="#11161C",
        paper_bgcolor="#11161C",
        font=dict(color="white"),
        margin=dict(l=20, r=20, t=40, b=20)
    )

    st.plotly_chart(fig, use_container_width=True)