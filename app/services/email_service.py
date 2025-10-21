import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings

def send_due_reminder(recipient_email: str, result: dict):
    """Send an email reminder listing due and overdue subscriptions."""
    sender_email = settings.SMTP_EMAIL
    sender_pass = settings.SMTP_PASSWORD

    subject = "🔔 Spendly – Upcoming & Overdue Subscriptions"

    # Build message body
    due_list = "\n".join([f"• {s['name']} on {s['renewal_date']}" for s in result["due_soon"]])
    overdue_list = "\n".join([f"• {s['name']} (due {s['renewal_date']})" for s in result["overdue"]])
    body = f"""Hi there 👋,

Here’s your current subscription status:

📅 Due Soon:
{due_list or 'None'}

⚠️ Overdue:
{overdue_list or 'None'}

Keep track and avoid surprise renewals 💸

— Spendly Smart Assistant
"""

    # Craft MIME message
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_pass)
            server.send_message(msg)
        print(f"✅ Reminder email sent to {recipient_email}")
    except Exception as e:
        print(f"❌ Failed to send email to {recipient_email}: {e}")
