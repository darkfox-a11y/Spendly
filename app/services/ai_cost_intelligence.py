# app/services/ai_cost_intelligence.py
from sqlalchemy.orm import Session
from app.db.models import Subscription, Budget
from app.core.config import settings
from groq import Groq

client = Groq(api_key=settings.GROQ_API_KEY)


def generate_cost_insights(db: Session, user_id: int):
    """Generate AI-powered cost insights for a user."""
    budget = db.query(Budget).filter(Budget.user_id == user_id).first()
    subscriptions = db.query(Subscription).filter(Subscription.owner_id == user_id).all()

    if not budget or not subscriptions:
        return {"error": "No budget or subscriptions found for this user."}

    total_spent = sum([float(s.price) for s in subscriptions])
    remaining = float(budget.monthly_limit) - total_spent

    # Spend by category
    category_spend = {}
    for s in subscriptions:
        category_spend[s.category] = category_spend.get(s.category, 0.0) + float(s.price)

    # Prepare text for LLM
    summary_text = (
        f"Monthly limit: {budget.monthly_limit}. "
        f"Total spent: {total_spent}. Remaining: {remaining}. "
        f"Spending by category: {category_spend}."
    )

    # 🔮 AI insight generation
    prompt = f"""
    You are Spendly, an AI financial assistant.
    Analyze the following user spending data and provide a short, friendly 4-sentence insight.

    {summary_text}

    Mention:
    - Overspending categories
    - Saving suggestions
    - Any pattern you observe
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=180,
    )

    ai_message = response.choices[0].message.content.strip()

    return {
        "total_spent": total_spent,
        "remaining": remaining,
        "category_spend": category_spend,
        "ai_summary": ai_message,
    }
