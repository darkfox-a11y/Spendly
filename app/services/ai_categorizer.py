# app/services/ai_categorizer.py
from groq import Groq
from app.core.config import settings

# ✅ Preferred models (top one tried first)
PREFERRED_MODELS = [
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
    "gemma2-9b-it",
]

def _pick_available_model(client: Groq) -> str:
    """Check which preferred model exists in your Groq account."""
    try:
        available = {m.id for m in client.models.list().data}
        for m in PREFERRED_MODELS:
            if m in available:
                print(f"✅ Using Groq model: {m}")
                return m
    except Exception as e:
        print(f"⚠️ Could not fetch models list: {e}")
    print(f"⚙️ Defaulting to first preferred model: {PREFERRED_MODELS[0]}")
    return PREFERRED_MODELS[0]

def predict_category(name: str, description: str | None = None) -> str:
    client = Groq(api_key=settings.GROQ_API_KEY)
    model = _pick_available_model(client)

    prompt = f"""
    You are a precise service categorizer.
    Given the name and description of a product, subscription, or company,
    describe what type of service it provides in 2–4 words 
    (e.g., "Credit Card Provider", "Streaming Platform", "Payment Gateway").
    Name: {name}
    Description: {description or 'N/A'}
    Respond with only the service type.
    """

    try:
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are an expert at identifying services."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
            max_tokens=12,
        )
        return (resp.choices[0].message.content or "").strip() or "Other"
    except Exception as e:
        print(f"[Groq fallback error] {e}")
        return "Other"
