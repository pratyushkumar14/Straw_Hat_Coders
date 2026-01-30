import streamlit as st
from mental_analysis.context_builder import build_insight_context
from mental_analysis.logic.baseline import calculate_baseline

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
def get_baseline_status(df, baseline):
    if baseline is None:
        return "baseline not established"

    current = df["score"].iloc[-1]

    if current > baseline + 1:
        return "above usual level"
    elif current < baseline - 1:
        return "below usual level"
    else:
        return "close to usual level"

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




def render_view(df, view, title, test_name):


    if df.empty or len(df) < 2:
        st.info(f"Not enough data for {title}")
        return
    baseline = calculate_baseline(df)
    baseline_status = get_baseline_status(df, baseline)

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
    st.plotly_chart(fig, width="stretch")


    st.markdown(f"**Trend:** {trend}")
    st.markdown(f"**Confidence:** {confidence}")
    st.markdown(f"**Interpretation:** {interpretation}")

    st.markdown("**Reflection prompts:**")

    
    for idx, r in enumerate(reflections):
        if st.button(r, key=f"reflect_{test_name}_{view}_{idx}"):

            # 🔴 THIS LINE MUST EXECUTE
            st.session_state.insight_context = build_insight_context(
            test=test_name,
            view=view,
            trend=trend,
            confidence=confidence,
            baseline_status=baseline_status,
            reflection=r
            )

            # 🔴 ROUTE AFTER CONTEXT SET
            st.session_state.page = "insight_chatbot"
            st.rerun()




    


def render_dashboard():
    st.title("📊 Mental Health Intelligence Dashboard")

    test_label = st.selectbox(
        "Select Test",
        list(TESTS.keys()),
        key="dashboard_test_selector"
    )

    test_name = TESTS[test_label]
    df = load_data(test_name)

    if df.empty:
        st.info("No data available for this test.")
        return

    df["timestamp"] = pd.to_datetime(df["timestamp"])

    daily = resample_df(df.copy(), "daily")
    weekly = resample_df(df.copy(), "weekly")
    yearly = resample_df(df.copy(), "yearly")

    render_view(daily, "daily", "Daily (Day-by-Day)", test_name)
    render_view(weekly, "weekly", "Weekly Overview", test_name)
    render_view(yearly, "yearly", "Yearly / Long-Term View", test_name)

