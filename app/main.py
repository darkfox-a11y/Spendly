# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

# Routers
from app.routers import auth, budget, subscriptions,ai

# Rate limiter
from app.core.rate_limiter import limiter

# -----------------------------
# Initialize FastAPI
# -----------------------------
app = FastAPI(
    title="Spendly Backend",
    description="AI-powered subscription and budget tracker.",
    version="1.0.0",
)

# -----------------------------
# Force HTTPS Middleware (COMMENT OUT FOR DEVELOPMENT)
# -----------------------------
# Only enable this in production with proper SSL certificates
# app.add_middleware(HTTPSRedirectMiddleware)

# -----------------------------
# Rate Limiter Setup
# -----------------------------
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# -----------------------------
# CORS Middleware
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Restrict in production
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
app.include_router(ai.router)


# -----------------------------
# Root Endpoint
# -----------------------------
@app.get("/")
def read_root():
    return {
        "message": "Welcome to Spendly API",
        "version": "1.0.0",
        "docs": "/docs"
    }