from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, cast
from sqlalchemy.types import Float

from app.core.database import get_db
from app.models.finding import Finding
from app.models.risk_assessment import RiskAssessment
from app.models.money_loss import MoneyLossCalculation
from app.models.analysis_run import AnalysisRun
from app.schemas.dashboard import KPISummaryResponse

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/kpis", response_model=KPISummaryResponse)
async def get_kpi_summary(db: Session = Depends(get_db)):
    """
    Get summary KPIs for the dashboard.
    """
    total_findings = db.query(func.count(Finding.id)).scalar() or 0
    
    # Use average risk score, not sum
    avg_risk_score_query = db.query(func.avg(RiskAssessment.risk_score)).scalar()
    total_risk_score = float(avg_risk_score_query) if avg_risk_score_query is not None else 0.0

    total_money_loss_query = db.query(func.sum(MoneyLossCalculation.estimated_loss)).scalar()
    total_money_loss = float(total_money_loss_query) if total_money_loss_query is not None else 0.0

    analysis_runs = db.query(func.count(AnalysisRun.id)).scalar() or 0
    
    return KPISummaryResponse(
        total_findings=total_findings,
        total_risk_score=total_risk_score,
        total_money_loss=total_money_loss,
        analysis_runs=analysis_runs
    )
