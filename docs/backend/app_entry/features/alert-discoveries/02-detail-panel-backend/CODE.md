# Detail Panel Backend - Code References

**Feature:** 02-detail-panel-backend  
**Last Updated:** 2025-12-12

---

## Code Locations

### API Endpoint

**File:** `backend/app/api/alert_dashboard.py`

**Endpoint Function:**

```133:198:backend/app/api/alert_dashboard.py
@router.get("/critical-discoveries", response_model=List[CriticalDiscoveryDrilldown])
async def get_critical_discoveries_drilldown(
    db: Session = Depends(get_db),
    limit: int = Query(10, ge=1, le=100)
):
    """
    Get critical discoveries grouped by alert for drill-down view.

    Returns alerts with their critical discoveries and concentration metrics for detailed investigation.
    """
    # Get analyses with critical discoveries
    analyses = db.query(AlertAnalysis).options(
        joinedload(AlertAnalysis.critical_discoveries),
        joinedload(AlertAnalysis.concentration_metrics),
        joinedload(AlertAnalysis.key_findings),
        joinedload(AlertAnalysis.alert_instance).joinedload(AlertInstance.exception_indicator)
    ).filter(
        AlertAnalysis.critical_discoveries.any()
    ).order_by(desc(AlertAnalysis.financial_impact_usd)).limit(limit).all()

    result = []
    for analysis in analyses:
        alert_instance = analysis.alert_instance
        ei = alert_instance.exception_indicator if alert_instance else None

        # Module comes from EI if linked, otherwise from subcategory (extracted from path)
        module = "N/A"
        if ei and ei.module:
            module = ei.module
        elif alert_instance and alert_instance.subcategory:
            module = alert_instance.subcategory

        drilldown = CriticalDiscoveryDrilldown(
            alert_id=alert_instance.alert_id if alert_instance else "UNKNOWN",
            alert_name=alert_instance.alert_name if alert_instance else "Unknown Alert",
            module=module,
            focus_area=alert_instance.focus_area if alert_instance else "N/A",
            severity=analysis.severity,
            discovery_count=len(analysis.critical_discoveries),
            financial_impact_usd=analysis.financial_impact_usd,
            discoveries=[
                CriticalDiscoveryResponse.model_validate(d)
                for d in analysis.critical_discoveries
            ],
            concentration_metrics=[
                ConcentrationMetricResponse.model_validate(m)
                for m in analysis.concentration_metrics
            ],
            key_findings=[
                KeyFindingResponse.model_validate(f)
                for f in analysis.key_findings
            ],
            # Summary data from AlertAnalysis
            records_affected=analysis.records_affected,
            unique_entities=analysis.unique_entities,
            period_start=analysis.period_start,
            period_end=analysis.period_end,
            risk_score=analysis.risk_score,
            raw_summary_data=analysis.raw_summary_data,
            # Alert configuration from AlertInstance
            business_purpose=alert_instance.business_purpose if alert_instance else None,
            parameters=alert_instance.parameters if alert_instance else None
        )
        result.append(drilldown)

    return result
```

### Schema Definition

**File:** `backend/app/schemas/alert_dashboard.py`

**Response Schema:**

```322:344:backend/app/schemas/alert_dashboard.py
class CriticalDiscoveryDrilldown(BaseModel):
    """Critical discovery grouped by alert for drill-down view."""
    alert_id: str
    alert_name: str
    module: str
    focus_area: str
    severity: str
    discovery_count: int
    financial_impact_usd: Optional[Decimal] = None
    discoveries: List[CriticalDiscoveryResponse]
    concentration_metrics: List[ConcentrationMetricResponse] = []
    key_findings: List[KeyFindingResponse] = []
    # Summary Data fields from AlertAnalysis
    records_affected: Optional[int] = None
    unique_entities: Optional[int] = None
    period_start: Optional[date] = None
    period_end: Optional[date] = None
    risk_score: Optional[int] = None
    raw_summary_data: Optional[Dict[str, Any]] = None
    # Alert configuration from AlertInstance
    business_purpose: Optional[str] = None  # From Explanation_* file
    parameters: Optional[Dict[str, Any]] = None  # From Metadata_* file
```

---

## Related Code

### Frontend Usage

**Used by:** `frontend/src/pages/alert-discoveries/features/detail-panel/DiscoveryDetailPanel.tsx`

### Database Models

- `AlertAnalysis` - `backend/app/models/alert_analysis.py`
- `AlertInstance` - `backend/app/models/alert_instance.py`
- `CriticalDiscovery` - `backend/app/models/critical_discovery.py`
- `ConcentrationMetric` - `backend/app/models/concentration_metric.py`
- `KeyFinding` - `backend/app/models/key_finding.py`
