import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from mental_analysis.logic.storage import load_data
from mental_analysis.logic.trends import calculate_trend
from mental_analysis.logic.confidence import calculate_confidence
from mental_analysis.logic.interpretation import interpretation_text
from mental_analysis.logic.reflection import reflection_prompt

TESTS = {
    "PHQ-9": "PHQ9",
    "GAD-7": "GAD7",
    "DASS-21": "DASS21",
    "WHO-5": "WHO5"
}

def resample_df(df, view):
    df = df.copy()
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.set_index("timestamp")

    # keep only numeric column
    df_numeric = df[["score"]]

    if view == "daily":
        return df_numeric

    if view == "weekly":
        return df_numeric.resample("W").mean().dropna()

    if view == "yearly":
        return df_numeric.resample("Y").mean().dropna()


def render_view(df, view, title):
    if df.empty or len(df) < 2:
        st.info(f"Not enough data for {title}")
        return

    trend = calculate_trend(df)
    confidence = calculate_confidence(df, view)
    interpretation = interpretation_text(trend, confidence, view)
    reflections = reflection_prompt(view)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df["score"],
        mode="lines+markers",
        name="Score"
    ))

    st.subheader(title)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(f"**Trend:** {trend}")
    st.markdown(f"**Confidence:** {confidence}")
    st.markdown(f"**Interpretation:** {interpretation}")

    st.markdown("**Reflection prompts:**")
    for r in reflections:
        st.markdown(f"- {r}")

def render_dashboard():
    st.title("📊 Mental Health Intelligence Dashboard")

    test_label = st.selectbox("Select Test", list(TESTS.keys()))
    df = load_data(TESTS[test_label])

    if df.empty:
        st.info("No data available for this test.")
        return

    df["timestamp"] = pd.to_datetime(df["timestamp"])

    daily = resample_df(df.copy(), "daily")
    weekly = resample_df(df.copy(), "weekly")
    yearly = resample_df(df.copy(), "yearly")

    render_view(daily, "daily", "Daily (Day-by-Day)")
    render_view(weekly, "weekly", "Weekly Overview")
    render_view(yearly, "yearly", "Yearly / Long-Term View")
