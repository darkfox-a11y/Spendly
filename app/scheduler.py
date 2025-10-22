# app/scheduler.py

# Import AsyncIOScheduler instead of BackgroundScheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.services.due_subscriptions import get_due_subscriptions
from app.services.email_service import send_due_reminder
from app.db.database import SessionLocal
from app.db.models import User
from datetime import datetime
import traceback
import asyncio # Import asyncio

# Keep the detailed check_due_subscriptions function for now
def check_due_subscriptions():
    """
    Runs automatically to check for upcoming or overdue subscriptions
    and sends reminder emails to users.
    """
    print(f"[{datetime.now()}] 👉 JOB START: check_due_subscriptions")
    db = None
    try:
        # Use a context manager for the DB session in an async context
        # Although this function itself isn't async, using SessionLocal directly is okay here
        db = SessionLocal()
        print(f"[{datetime.now()}]    DB session created.")
        users = db.query(User).all()
        print(f"[{datetime.now()}]    Found {len(users)} users.")

        if not users:
             print(f"[{datetime.now()}]    No users found in the database. Skipping checks.")

        for user in users:
            print(f"[{datetime.now()}]    Checking user {user.id} ({user.email})...")
            result = get_due_subscriptions(db, user.id)
            if result.get("due_soon") or result.get("overdue"):
                print(f"[{datetime.now()}]    User {user.id} has due/overdue subs. Attempting email...")
                # Assuming send_due_reminder is synchronous
                send_due_reminder(user.email, result)
            else:
                print(f"[{datetime.now()}]    User {user.id} has no due/overdue subs.")

    except Exception as e:
        print(f"[{datetime.now()}] 💥 ERROR in check_due_subscriptions: {e}")
        print(traceback.format_exc())
    finally:
        if db:
            db.close()
            print(f"[{datetime.now()}]    DB session closed.")
        print(f"[{datetime.now()}] 🏁 JOB END: check_due_subscriptions")

# Use a global scheduler instance for AsyncIOScheduler
scheduler = AsyncIOScheduler(timezone="UTC")

def start_scheduler():
    """Initialize and start the background scheduler."""
    global scheduler
    # Add the job (make sure it's not added multiple times if reloader runs this)
    if not scheduler.get_job("due_sub_checker"):
        scheduler.add_job(check_due_subscriptions, "interval", minutes=1, id="due_sub_checker")
        print("➕ Job added to scheduler.")
    else:
         print("Job already exists in scheduler.")

    # Start the scheduler if it's not already running
    if not scheduler.running:
        try:
            scheduler.start()
            print("⏰ AsyncIOScheduler started successfully.")
        except Exception as e:
             print(f"❌ Failed to start AsyncIOScheduler: {e}")
    else:
        print("⏰ AsyncIOScheduler is already running.")

def shutdown_scheduler():
    """Shutdown the scheduler."""
    global scheduler
    if scheduler.running:
        scheduler.shutdown()
        print("🛑 AsyncIOScheduler shut down.")