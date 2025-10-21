# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.scheduler import start_scheduler
from app.core.rate_limiter import limiter
from app.routers import auth, budget, subscriptions, ai

app = FastAPI(
    title="Spendly Backend",
    description="AI-powered subscription and budget tracker.",
    version="1.0.0",
)

# Rate limiter setup
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router)
app.include_router(budget.router)
app.include_router(subscriptions.router)
app.include_router(ai.router)

# ✅ Start scheduler when FastAPI starts
@app.on_event("startup")
def start_background_tasks():
    start_scheduler()
