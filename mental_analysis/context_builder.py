from mental_analysis.logic.storage import load_data

def build_insight_context(
    test,
    view,
    trend,
    confidence,
    baseline_status,
    reflection
):
    return {
        "test": test,
        "view": view,
        "trend": trend,
        "confidence": confidence,
        "baseline_status": baseline_status,
        "reflection": reflection
    }


def build_chat_context(tool):
    df = load_data(tool)

    if df.empty or len(df) < 2:
        return {
            "summary": "Limited data available for analysis."
        }

    recent = df.tail(3)
    trend = "increasing" if recent["score"].iloc[-1] > recent["score"].iloc[0] else "stable or decreasing"

    return {
        "data_points": len(df),
        "recent_scores": recent["score"].tolist(),
        "recent_trend": trend
    }
