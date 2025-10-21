# app/test_email_trigger.py
from app.services.email_service import send_due_reminder

# Replace this with your test email ID (can be your own Gmail)
TEST_RECIPIENT = "neeradahire2004@gmail.com"

# Mock subscription data to simulate due and overdue reminders
mock_due_data = {
    "due_soon": [
        {
            "name": "Netflix",
            "renewal_date": "2025-10-24",
            "price": 499.00,
            "category": "Entertainment"
        },
        {
            "name": "Canva",
            "renewal_date": "2025-10-25",
            "price": 299.00,
            "category": "Design"
        }
    ],
    "overdue": [
        {
            "name": "Spotify",
            "renewal_date": "2025-10-15",
            "price": 199.00,
            "category": "Music"
        }
    ]
}

print("📬 Triggering test email send...")

try:
    send_due_reminder(TEST_RECIPIENT, mock_due_data)
    print(f"✅ Test email sent successfully to {TEST_RECIPIENT}")
except Exception as e:
    print(f"❌ Failed to send test email: {e}")
