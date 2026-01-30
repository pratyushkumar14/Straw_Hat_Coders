import streamlit as st
from mental_analysis.llm.hf_client import get_llm_insight

def render_insight_chatbot():
    st.title("🧠 Understanding Your Results")

    context = st.session_state.get("insight_context")

    if context is None:
        st.warning("No reflection context found.")
        return

    # LLM call only once
    if "insight_response" not in st.session_state:
        with st.spinner("Generating insight…"):
            st.session_state.insight_response = get_llm_insight(
                test=context["test"],
                view=context["view"],
                trend=context["trend"],
                confidence=context["confidence"],
                baseline_status=context["baseline_status"]
            )

    st.write(st.session_state.insight_response)

    st.markdown("### Reflect further")
    user_text = st.text_input("Your thoughts (optional)")

    if user_text:
        st.write("Thank you for sharing. Reflection helps awareness.")

    if st.button("⬅ Back to Dashboard"):
        st.session_state.page = "dashboard"
        st.session_state.insight_response = None
        st.session_state.insight_context = None
        st.rerun()
