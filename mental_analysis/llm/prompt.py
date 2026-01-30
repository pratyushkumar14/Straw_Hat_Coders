SYSTEM_PROMPT = """
You are a mental health insight assistant.
Your role is to explain trends from mental health screening data.
Do NOT diagnose, treat, or provide medical advice.
Use neutral, supportive, and informational language.
Focus on trends, confidence, and awareness.
"""

def build_user_prompt(context: dict):
    return f"""
Test: {context['test']}
Time Range: {context['period']}
Trend: {context['trend']}
Confidence: {context['confidence']}

Explain what the user is seeing in simple language.
Also provide 2 gentle reflection questions.
"""
