# 💸 Spendly — AI-Powered Subscription & Budget Tracker

> **Smart financial management made simple.**  
> Track subscriptions, manage budgets, get AI-powered spending insights, and receive automatic due reminders — all in one platform.

---

## 🧠 Overview

**Spendly** is a full-stack **FastAPI-based** backend service that helps users:
- Register and authenticate securely (JWT-based)
- Track all their **subscriptions** (price, category, renewal date)
- Manage monthly **budgets**
- Get **AI-generated spending summaries**
- Receive **email reminders** for upcoming renewals
- Access everything securely through a **Dockerized, production-ready API**

---

## 🚀 Features

| Category | Description |
|-----------|--------------|
| 🔐 **Authentication** | JWT-based register, login, and token management |
| 📦 **Subscriptions CRUD** | Add, update, delete, and search subscriptions by name |
| 💰 **Budget Tracking** | Define monthly limits and track spending in real-time |
| 🧾 **AI Cost Intelligence** | Summarizes your monthly spending and gives personalized suggestions using LLM (Groq API) |
| 🧠 **AI Monthly Insights** | Generates detailed financial reports at the end of each month |
| 📧 **Email Reminders** | Automatic reminders for subscriptions nearing renewal dates |
| ⏱ **Rate Limiting** | Prevents abuse of API endpoints (via `slowapi`) |
| 🔒 **HTTPS & CORS** | Secure communication for production use |
| 🐳 **Dockerized** | Complete backend setup with PostgreSQL via Docker Compose |
| ⚙️ **Modular Architecture** | Clear separation of routers, services, schemas, and database models |

---

## 🏗️ Architecture

spendly/
├── app/
│ ├── core/ # config, security, and rate limiter setup
│ ├── db/ # database connection & models
│ ├── routers/ # FastAPI routers (auth, budget, subscriptions, ai)
│ ├── schemas/ # Pydantic validation models
│ ├── services/ # Business logic (auth, ai, budget, due reminders)
│ ├── scheduler/ # APScheduler jobs (daily due-check emails)
│ ├── main.py # FastAPI entrypoint
│ └── init.py
│
├── .env # Environment variables (API keys, DB, SMTP)
├── requirements.txt # All dependencies
├── Dockerfile # FastAPI container definition
├── docker-compose.yml # Multi-container setup (backend + PostgreSQL)
└── README.md

yaml
Copy code

---

## ⚙️ Tech Stack

| Component | Tech |
|------------|------|
| **Backend Framework** | FastAPI |
| **Database** | PostgreSQL (SQLAlchemy ORM) |
| **Task Scheduler** | APScheduler |
| **Email Service** | SMTP (Gmail) |
| **AI Models** | Groq API (Llama 3) |
| **Auth** | JWT + OAuth2 |
| **Containerization** | Docker, Docker Compose |
| **ORM** | SQLAlchemy |
| **Validation** | Pydantic v2 |
| **Rate Limiting** | SlowAPI |
| **HTTPS + CORS** | Starlette Middleware |

---

🧩 Key API Endpoints
Method	Endpoint	Description
POST	/auth/register	Register a new user
POST	/auth/login	Login and get JWT token
GET	/auth/me	Get current user info
POST	/subscriptions/	Create a subscription
GET	/subscriptions/	Get all subscriptions for user
DELETE	/subscriptions/{id}	Delete a subscription
GET	/budget/	Get user budget
POST	/budget/	Create a budget
PUT	/budget/	Update existing budget
GET	/ai/cost-summary	AI-powered monthly expense summary
GET	/ai/monthly-insight	AI-generated full spending report
GET	/due/reminders	Upcoming or overdue subscriptions

🧠 AI Features (Groq LLM)
Cost Intelligence Engine:
Analyzes your spending patterns across subscriptions and categories.
Returns actionable insights such as:

"You’ve overspent by 35% this month. Consider reducing entertainment costs."

AI Monthly Insights:
Generates natural-language summaries for your monthly expenses.

📧 Email Reminder System
Daily scheduled task using APScheduler

Automatically checks subscriptions due within the next 3 days

Sends personalized reminder emails via Gmail SMTP

🧱 Example Usage Flow
Register → /auth/register

Login → get JWT token

Create a Budget → /budget/

Add Subscriptions → /subscriptions/

Get AI Summary → /ai/cost-summary

Check Due Renewals → /due/reminders

Automatic Email Alerts → Sent daily at 9 AM

🔮 Future Improvements
💬 Conversational AI Assistant (“Ask Spendly”)

📊 React dashboard with charts (Vite + Tailwind)

📱 Push notifications via Firebase

🧩 Stripe integration for subscription auto-pay

👨‍💻 Developer Setup (without Docker)
bash
Copy code
# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Run the app
uvicorn app.main:app --reload
