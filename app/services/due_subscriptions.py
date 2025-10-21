# app/services/due_subscriptions.py

from datetime import date, timedelta
from sqlalchemy.orm import Session
from app.db.models import Subscription


def get_due_subscriptions(db: Session, user_id: int) -> dict:
    """
    Fetch all subscriptions that are either due soon (within 7 days)
    or already overdue for the given user.

    Returns:
        {
            "due_soon": [ {name, renewal_date, price, category}, ... ],
            "overdue":  [ {name, renewal_date, price, category}, ... ]
        }
    """
    today = date.today()
    upcoming_threshold = today + timedelta(days=7)

    # Fetch all user subscriptions
    subscriptions = (
        db.query(Subscription)
        .filter(Subscription.owner_id == user_id)
        .all()
    )

    due_soon, overdue = [], []

    for sub in subscriptions:
        try:
            renewal = sub.renewal_date
            # Handle possible string-type dates (if not converted properly)
            if isinstance(renewal, str):
                renewal = date.fromisoformat(renewal)
        except Exception:
            continue  # Skip malformed dates safely

        sub_info = {
            "name": sub.name,
            "renewal_date": renewal.strftime("%Y-%m-%d"),
            "price": float(sub.price),
            "category": sub.category,
        }

        if today <= renewal <= upcoming_threshold:
            due_soon.append(sub_info)
        elif renewal < today:
            overdue.append(sub_info)

    return {"due_soon": due_soon, "overdue": overdue}
