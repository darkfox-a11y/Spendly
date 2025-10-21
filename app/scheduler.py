# app/scheduler.py

from apscheduler.schedulers.background import BackgroundScheduler
from app.services.due_subscriptions import get_due_subscriptions
from app.services.email_service import send_due_reminder
from app.db.database import SessionLocal
from app.db.models import User
from datetime import datetime


def check_due_subscriptions():
    """
    Runs automatically every day to check for upcoming or overdue subscriptions
    and sends reminder emails to users.
    """
    print(f"[{datetime.now()}] 🔎 Checking due subscriptions...")
    db = SessionLocal()
    users = db.query(User).all()

    for user in users:
        result = get_due_subscriptions(db, user.id)
        if result["due_soon"] or result["overdue"]:
            send_due_reminder(user.email, result)

    db.close()


def start_scheduler():
    """Initialize and start the background scheduler."""
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_due_subscriptions, "cron", hour=9,minute=0)  # every day at 9 AM
    scheduler.start()
    print("⏰ APScheduler started successfully")
