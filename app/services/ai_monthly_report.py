from datetime import datetime, timedelta
from decimal import Decimal
from sqlalchemy.orm import Session
from groq import Groq
from app.db.models import Subscription, User
from app.core.config import settings

client = Groq(api_key=settings.GROQ_API_KEY)


def generate_monthly_report(db: Session, user_id: int):
    """Generate an AI-driven monthly finance summary comparing current and previous months."""
    
    today = datetime.utcnow()
    first_day = today.replace(day=1)
    last_month_end = first_day - timedelta(days=1)
    last_month_start = last_month_end.replace(day=1)

    # 🔹 Get current and previous month subscriptions
    current_month_spend = db.query(Subscription).filter(
        Subscription.owner_id == user_id,
        Subscription.renewal_date >= first_day
    ).all()

    previous_month_spend = db.query(Subscription).filter(
        Subscription.owner_id == user_id,
        Subscription.renewal_date >= last_month_start,
        Subscription.renewal_date <= last_month_end
    ).all()

    # 🔹 Compute totals
    total_spent = sum([float(sub.price) for sub in current_month_spend])
    previous_spent = sum([float(sub.price) for sub in previous_month_spend])
    change_percent = (
        ((total_spent - previous_spent) / previous_spent * 100)
        if previous_spent > 0 else 0
    )

    # 🔹 Category breakdowns
    category_spend_current = {}
    category_spend_previous = {}

    for sub in current_month_spend:
        category_spend_current[sub.category] = category_spend_current.get(sub.category, 0) + float(sub.price)
    for sub in previous_month_spend:
        category_spend_previous[sub.category] = category_spend_previous.get(sub.category, 0) + float(sub.price)

    # 🔹 Category growth analysis
    category_growth = {}
    for category, current_value in category_spend_current.items():
        prev_value = category_spend_previous.get(category, 0)
        if prev_value > 0:
            category_growth[category] = ((current_value - prev_value) / prev_value) * 100
        elif current_value > 0:
            category_growth[category] = 100  # new category appeared this month

    top_growth_category = (
        max(category_growth, key=category_growth.get)
        if category_growth else None
    )

    # 🔹 Top 3 subscriptions
    top_subscriptions = sorted(
        current_month_spend,
        key=lambda s: float(s.price),
        reverse=True
    )[:3]

    top_subscriptions_list = [
        {"name": sub.name, "category": sub.category, "price": float(sub.price)}
        for sub in top_subscriptions
    ]

    # 🔹 Prompt for AI summary
    prompt = f"""
    Generate a financial summary comparing this month to last month.
    Current month total: ${total_spent:.2f}
    Previous month total: ${previous_spent:.2f}
    Change: {change_percent:.2f}%
    Category breakdown: {category_spend_current}
    Top 3 subscriptions: {top_subscriptions_list}
    Category that increased most: {top_growth_category if top_growth_category else "None"}
    Provide 3-5 concise sentences in friendly and analytical tone.
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a financial AI assistant that summarizes user spending patterns."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=220,
        temperature=0.7
    )

    ai_summary = response.choices[0].message.content.strip()

    # 🔹 Final output
    return {
        "month": today.strftime("%B %Y"),
        "total_spent": total_spent,
        "previous_spent": previous_spent,
        "change_percent": round(change_percent, 2),
        "category_breakdown": category_spend_current,
        "top_subscriptions": top_subscriptions_list,
        "top_growth_category": top_growth_category,
        "ai_summary": ai_summary
    }
