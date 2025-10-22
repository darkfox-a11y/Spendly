# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.core.rate_limiter import limiter
from app.routers import auth, budget, subscriptions, ai
from app.scheduler import start_scheduler, shutdown_scheduler
from contextlib import asynccontextmanager
import asyncio

# --- DB SETUP ---
from app.db.database import engine, Base
Base.metadata.create_all(bind=engine)
# ---------------------------


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Starting up Spendly backend...")
    # Wait until event loop is running
    await asyncio.sleep(0.1)
    start_scheduler()
    print("✅ Scheduler started inside lifespan.")
    yield
    shutdown_scheduler()
    print("👋 Application shutdown. Scheduler stopped.")


app = FastAPI(
    title="Spendly Backend",
    description="AI-powered subscription and budget tracker.",
    version="1.0.0",
    lifespan=lifespan,   # ✅ Register lifespan so scheduler starts automatically
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
@app.get("/")
def read_root():
    return {"message": "Welcome to the Spendly Backend API!"}