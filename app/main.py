from fastapi import FastAPI
from app.routers import auth , subscriptions,budget

app = FastAPI(title = "Budget Management API")

app.include_router(auth.router)
app.include_router(subscriptions.router)
app.include_router(budget.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Budget Management API"}
