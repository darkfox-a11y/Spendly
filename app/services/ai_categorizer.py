from openai import OpenAI
from app.core.config import settings
import requests

def predict_category(name: str, description: str | None = None) -> str:
    """
    Predicts a category for a subscription using the free Groq API (Mixtral-8x7B).
    Falls back to rule-based classification if API fails.
    """
    name_lower = name.lower()

    # 🔹 Rule-based local fallback first
    if any(k in name_lower for k in ["netflix", "spotify", "youtube", "prime"]):
        return "Entertainment"
    if any(k in name_lower for k in ["adobe", "microsoft", "notion", "canva", "slack"]):
        return "Productivity"
    if any(k in name_lower for k in ["chatgpt", "openai", "bard", "claude", "copilot"]):
        return "AI Tools"
    if any(k in name_lower for k in ["aws", "azure", "gcp", "cloud"]):
        return "Cloud Services"
    if any(k in name_lower for k in ["udemy", "coursera", "skillshare", "khan"]):
        return "Education"
    if any(k in name_lower for k in ["groww", "zerodha", "stripe", "razorpay"]):
        return "Finance"

    # 🔹 Try Groq API (same syntax as OpenAI)
    if not settings.GROQ_API_KEY:
        return "Other"

    try:
        client = OpenAI(
            base_url="https://api.groq.com/openai/v1",
            api_key=settings.GROQ_API_KEY
        )

        prompt = f"""
        Classify this subscription into one of:
        Entertainment, Productivity, AI Tools, Education, Finance, Cloud Services, Other.
        Name: {name}
        Description: {description or 'N/A'}
        Respond with only the category name.
        """

        response = client.chat.completions.create(
            model="mixtral-8x7b",
            messages=[
                {"role": "system", "content": "You are a precise subscription categorizer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=10,
        )

        category = response.choices[0].message.content.strip()
        return category or "Other"

    except Exception as e:
        print(f"[Groq Fallback Error]: {e}")
        return "Other"
