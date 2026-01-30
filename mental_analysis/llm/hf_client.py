from gradio_client import Client

client = Client("Priyanshu292004/mental-health-insight-llm")

VIEW_MAP = {
    "daily": "Daily",
    "weekly": "Weekly",
    "yearly": "Yearly"
}

def get_llm_insight(test, view, trend, confidence, baseline_status):
    return client.predict(
        test=test,
        view=VIEW_MAP[view],
        trend=trend,
        confidence=confidence,
        baseline_status=baseline_status,
        api_name="/generate_insight"
    )
