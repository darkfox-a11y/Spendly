from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.auth_service import get_current_user
from app.services.ai_cost_intelligence import generate_cost_insights
from app.db.models import User
from app.services.ai_monthly_report import generate_monthly_report

router = APIRouter(prefix="/ai", tags=["AI Intelligence"])

@router.get("/cost-summary")
def ai_cost_summary(
    db: Session = Depends(get_db),
    current_user:User=Depends(get_current_user)
):
    return generate_cost_insights(db, current_user.id)

@router.get("/monthly-report", status_code=status.HTTP_200_OK)
def ai_monthly_report(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    """Generate an AI-driven monthly finance summary comparing current and previous months."""
    return generate_monthly_report(db, current_user.id)
