from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.auth_service import get_current_user
from app.services.ai_cost_intelligence import generate_cost_insights
from app.db.models import User

router = APIRouter(prefix="/ai", tags=["AI Intelligence"])

@router.get("/cost-summary")
def ai_cost_summary(
    db: Session = Depends(get_db),
    current_user:User=Depends(get_current_user)
):
    return generate_cost_insights(db, current_user.id)
