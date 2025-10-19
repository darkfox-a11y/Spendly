# app/main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.routers import subscriptions

# Routers
from app.routers import auth,budget,subscriptions

# -----------------------------
# Initialize FastAPI
# -----------------------------
app = FastAPI(
    title="Spendly Backend",
    description="AI-powered subscription and budget tracker.",
    version="1.0.0",
)

# -----------------------------
# Force HTTPS Middleware
# -----------------------------
# Redirects all plain HTTP requests to HTTPS automatically
app.add_middleware(HTTPSRedirectMiddleware)

# -----------------------------
# Rate Limiter Setup
# -----------------------------
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# -----------------------------
# CORS Middleware
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # to be later restricted in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Include Routers
# -----------------------------
app.include_router(auth.router)
app.include_router(subscriptions.router)
app.include_router(budget.router)

