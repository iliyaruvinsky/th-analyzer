# AlertSummary KPI Backend - Code References

**Feature:** 01-alert-summary-backend  
**Last Updated:** 2025-12-12

---

## Code Locations

### API Endpoint

**File:** `backend/app/api/alert_dashboard.py`

**Endpoint Function:**

```50:130:backend/app/api/alert_dashboard.py
@router.get("/kpis", response_model=DashboardKPIsResponse)
async def get_dashboard_kpis(db: Session = Depends(get_db)):
    """
    Get all dashboard KPI metrics.

    Returns summary cards data including:
    - Total critical discoveries
    - Alerts analyzed
    - Financial exposure (USD)
    - Average risk score
    - Distribution by severity, focus area, and module
    - Open action items count
    """
    # Critical discoveries count
    total_critical_discoveries = db.query(func.count(CriticalDiscovery.id)).scalar() or 0

    # Alerts analyzed count
    total_alerts_analyzed = db.query(func.count(AlertAnalysis.id)).scalar() or 0

    # Total financial exposure
    total_exposure = db.query(func.sum(AlertAnalysis.financial_impact_usd)).scalar()
    total_financial_exposure_usd = Decimal(total_exposure) if total_exposure else Decimal("0.00")

    # Average risk score
    avg_risk = db.query(func.avg(AlertAnalysis.risk_score)).scalar()
    avg_risk_score = float(avg_risk) if avg_risk else 0.0

    # Alerts by severity
    severity_counts = db.query(
        AlertAnalysis.severity,
        func.count(AlertAnalysis.id)
    ).group_by(AlertAnalysis.severity).all()
    alerts_by_severity = {
        "CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0
    }
    for severity, count in severity_counts:
        if severity in alerts_by_severity:
            alerts_by_severity[severity] = count

    # Alerts by focus area (through alert_instance relationship)
    # Start from AlertAnalysis and join to AlertInstance to get proper counts
    focus_area_counts = db.query(
        AlertInstance.focus_area,
        func.count(AlertAnalysis.id)
    ).select_from(AlertAnalysis).join(
        AlertInstance, AlertAnalysis.alert_instance_id == AlertInstance.id
    ).group_by(AlertInstance.focus_area).all()
    alerts_by_focus_area = {fa: count for fa, count in focus_area_counts}

    # Alerts by module (from alert_instance.subcategory which stores module extracted from path)
    # Start from AlertAnalysis and join to AlertInstance for proper aggregation
    module_counts = db.query(
        AlertInstance.subcategory,
        func.count(AlertAnalysis.id)
    ).select_from(AlertAnalysis).join(
        AlertInstance, AlertAnalysis.alert_instance_id == AlertInstance.id
    ).filter(AlertInstance.subcategory.isnot(None)
    ).group_by(AlertInstance.subcategory).all()
    alerts_by_module = {module: count for module, count in module_counts if module}

    # Open investigations (INVESTIGATE fraud indicators)
    open_investigations = db.query(func.count(AlertAnalysis.id)).filter(
        AlertAnalysis.fraud_indicator == "INVESTIGATE"
    ).scalar() or 0

    # Open action items
    open_action_items = db.query(func.count(ActionItem.id)).filter(
        ActionItem.status == "OPEN"
    ).scalar() or 0

    return DashboardKPIsResponse(
        total_critical_discoveries=total_critical_discoveries,
        total_alerts_analyzed=total_alerts_analyzed,
        total_financial_exposure_usd=total_financial_exposure_usd,
        avg_risk_score=avg_risk_score,
        alerts_by_severity=alerts_by_severity,
        alerts_by_focus_area=alerts_by_focus_area,
        alerts_by_module=alerts_by_module,
        open_investigations=open_investigations,
        open_action_items=open_action_items
    )
```

### Schema Definition

**File:** `backend/app/schemas/alert_dashboard.py`

**Response Schema:**

```302:320:backend/app/schemas/alert_dashboard.py
class DashboardKPIsResponse(BaseModel):
    """Main KPI summary for dashboard top row."""
    # Critical Discovery KPI Card
    total_critical_discoveries: int = Field(..., description="Total critical discoveries count")
    total_alerts_analyzed: int = Field(..., description="Number of alerts analyzed")
    total_financial_exposure_usd: Decimal = Field(..., description="Total USD exposure")

    # Risk metrics
    avg_risk_score: float = Field(..., description="Average risk score (0-100)")

    # Distribution breakdowns
    alerts_by_severity: Dict[str, int] = Field(..., description="{CRITICAL: n, HIGH: n, MEDIUM: n, LOW: n}")
    alerts_by_focus_area: Dict[str, int] = Field(..., description="Distribution by focus area")
    alerts_by_module: Dict[str, int] = Field(..., description="Distribution by SAP module")

    # Action queue metrics
    open_investigations: int = Field(..., description="Count of INVESTIGATE items")
    open_action_items: int = Field(..., description="Total open action items")
```

### Database Models Used

- `CriticalDiscovery` - `backend/app/models/critical_discovery.py`
- `AlertAnalysis` - `backend/app/models/alert_analysis.py`
- `AlertInstance` - `backend/app/models/alert_instance.py`
- `ActionItem` - `backend/app/models/action_item.py`

---

## Related Code

### Frontend Usage

**Should be used by:** `frontend/src/pages/alert-discoveries/features/alert-summary/AlertSummary.tsx`

**Current Issue:** Frontend aggregates data client-side instead of using this endpoint.

---

## Dependencies

- SQLAlchemy ORM for database queries
- FastAPI for endpoint routing
- Pydantic for response validation
