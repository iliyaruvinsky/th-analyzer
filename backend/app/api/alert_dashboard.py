
"""
Alert Dashboard API - Endpoints for alert analysis dashboard and EI vocabulary.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, desc
from typing import Optional, List
from decimal import Decimal
from datetime import datetime

from app.core.database import get_db
from app.models import (
    Client, SourceSystem, ExceptionIndicator, EIVocabulary,
    AlertInstance, AlertAnalysis, CriticalDiscovery, KeyFinding,
    ConcentrationMetric, ActionItem
)
from app.schemas.alert_dashboard import (
    # Client
    ClientCreate, ClientResponse,
    # Source System
    SourceSystemCreate, SourceSystemResponse,
    # Exception Indicator
    ExceptionIndicatorCreate, ExceptionIndicatorResponse,
    # EI Vocabulary
    EIVocabularyCreate, EIVocabularyResponse, EIWithVocabularyResponse,
    # Alert Instance
    AlertInstanceCreate, AlertInstanceResponse,
    # Alert Analysis
    AlertAnalysisCreate, AlertAnalysisResponse, AlertAnalysisWithDetails,
    # Critical Discovery
    CriticalDiscoveryCreate, CriticalDiscoveryResponse,
    # Key Finding
    KeyFindingCreate, KeyFindingResponse,
    # Concentration Metric
    ConcentrationMetricCreate, ConcentrationMetricResponse,
    # Action Item
    ActionItemCreate, ActionItemUpdate, ActionItemResponse,
    # Dashboard
    DashboardKPIsResponse, CriticalDiscoveryDrilldown
)
from app.schemas.maintenance import DeleteResponse
from app.utils.audit_logger import audit_log
import logging

router = APIRouter(prefix="/alert-dashboard", tags=["alert-dashboard"])
logger = logging.getLogger(__name__)


# =============================================================================
# Dashboard KPI Endpoints
# =============================================================================

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
    ).order_by(
        desc(AlertAnalysis.financial_impact_usd),
        desc(AlertAnalysis.created_at)  # Secondary sort by creation date (newest first for same financial impact)
    ).limit(limit).all()

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


@router.get("/action-queue", response_model=List[ActionItemResponse])
async def get_action_queue(
    status: str = Query("OPEN", description="Filter by status"),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db)
):
    """
    Get action items requiring investigation.

    Returns action items filtered by status for the action queue.
    """
    query = db.query(ActionItem)

    if status:
        query = query.filter(ActionItem.status == status)

    items = query.order_by(
        ActionItem.priority.asc(),
        ActionItem.created_at.desc()
    ).limit(limit).all()

    return [ActionItemResponse.model_validate(item) for item in items]


# =============================================================================
# Client Endpoints
# =============================================================================

@router.post("/clients", response_model=ClientResponse)
async def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    """Create a new client."""
    existing = db.query(Client).filter(Client.code == client.code).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"Client with code '{client.code}' already exists")

    db_client = Client(**client.model_dump())
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return ClientResponse.model_validate(db_client)


@router.get("/clients", response_model=List[ClientResponse])
async def list_clients(db: Session = Depends(get_db)):
    """List all clients."""
    clients = db.query(Client).order_by(Client.name).all()
    return [ClientResponse.model_validate(c) for c in clients]


@router.get("/clients/{client_id}", response_model=ClientResponse)
async def get_client(client_id: int, db: Session = Depends(get_db)):
    """Get a client by ID."""
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return ClientResponse.model_validate(client)


# =============================================================================
# Source System Endpoints
# =============================================================================

@router.post("/source-systems", response_model=SourceSystemResponse)
async def create_source_system(source_system: SourceSystemCreate, db: Session = Depends(get_db)):
    """Create a new source system."""
    db_system = SourceSystem(**source_system.model_dump())
    db.add(db_system)
    db.commit()
    db.refresh(db_system)
    return SourceSystemResponse.model_validate(db_system)


@router.get("/source-systems", response_model=List[SourceSystemResponse])
async def list_source_systems(
    client_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """List source systems, optionally filtered by client."""
    query = db.query(SourceSystem)
    if client_id:
        query = query.filter(SourceSystem.client_id == client_id)
    systems = query.order_by(SourceSystem.code).all()
    return [SourceSystemResponse.model_validate(s) for s in systems]


# =============================================================================
# Exception Indicator Endpoints
# =============================================================================

@router.post("/exception-indicators", response_model=ExceptionIndicatorResponse)
async def create_exception_indicator(
    ei: ExceptionIndicatorCreate,
    db: Session = Depends(get_db)
):
    """Create a new Exception Indicator."""
    existing = db.query(ExceptionIndicator).filter(ExceptionIndicator.ei_id == ei.ei_id).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"EI '{ei.ei_id}' already exists")

    db_ei = ExceptionIndicator(**ei.model_dump())
    db.add(db_ei)
    db.commit()
    db.refresh(db_ei)
    return ExceptionIndicatorResponse.model_validate(db_ei)


@router.get("/exception-indicators", response_model=List[ExceptionIndicatorResponse])
async def list_exception_indicators(
    module: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """List Exception Indicators, optionally filtered by module."""
    query = db.query(ExceptionIndicator)
    if module:
        query = query.filter(ExceptionIndicator.module == module)
    eis = query.order_by(ExceptionIndicator.ei_id).all()
    return [ExceptionIndicatorResponse.model_validate(ei) for ei in eis]


@router.get("/exception-indicators/{ei_id}", response_model=EIWithVocabularyResponse)
async def get_exception_indicator(ei_id: int, db: Session = Depends(get_db)):
    """Get an Exception Indicator with its vocabulary."""
    ei = db.query(ExceptionIndicator).options(
        joinedload(ExceptionIndicator.vocabulary)
    ).filter(ExceptionIndicator.id == ei_id).first()

    if not ei:
        raise HTTPException(status_code=404, detail="Exception Indicator not found")

    return EIWithVocabularyResponse.model_validate(ei)


# =============================================================================
# EI Vocabulary Endpoints
# =============================================================================

@router.post("/ei-vocabulary", response_model=EIVocabularyResponse)
async def create_or_update_ei_vocabulary(
    vocabulary: EIVocabularyCreate,
    db: Session = Depends(get_db)
):
    """
    Create or update EI vocabulary entry.

    If vocabulary exists for the EI, increments version and updates.
    """
    existing = db.query(EIVocabulary).filter(EIVocabulary.ei_id == vocabulary.ei_id).first()

    if existing:
        # Update existing vocabulary
        for key, value in vocabulary.model_dump(exclude={'ei_id'}).items():
            setattr(existing, key, value)
        existing.version += 1
        existing.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(existing)
        return EIVocabularyResponse.model_validate(existing)
    else:
        # Create new vocabulary
        db_vocab = EIVocabulary(**vocabulary.model_dump())
        db.add(db_vocab)
        db.commit()
        db.refresh(db_vocab)
        return EIVocabularyResponse.model_validate(db_vocab)


@router.get("/ei-vocabulary", response_model=List[EIVocabularyResponse])
async def list_ei_vocabulary(db: Session = Depends(get_db)):
    """List all EI vocabulary entries."""
    vocabs = db.query(EIVocabulary).order_by(EIVocabulary.ei_id).all()
    return [EIVocabularyResponse.model_validate(v) for v in vocabs]


@router.get("/ei-vocabulary/{ei_id}", response_model=EIVocabularyResponse)
async def get_ei_vocabulary(ei_id: int, db: Session = Depends(get_db)):
    """Get vocabulary for a specific EI."""
    vocab = db.query(EIVocabulary).filter(EIVocabulary.ei_id == ei_id).first()
    if not vocab:
        raise HTTPException(status_code=404, detail="EI Vocabulary not found")
    return EIVocabularyResponse.model_validate(vocab)


# =============================================================================
# Alert Instance Endpoints
# =============================================================================

@router.post("/alert-instances", response_model=AlertInstanceResponse)
async def create_alert_instance(
    alert_instance: AlertInstanceCreate,
    db: Session = Depends(get_db)
):
    """Create a new alert instance."""
    existing = db.query(AlertInstance).filter(AlertInstance.alert_id == alert_instance.alert_id).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"Alert '{alert_instance.alert_id}' already exists")

    db_alert = AlertInstance(**alert_instance.model_dump())
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    return AlertInstanceResponse.model_validate(db_alert)


@router.get("/alert-instances", response_model=List[AlertInstanceResponse])
async def list_alert_instances(
    focus_area: Optional[str] = None,
    ei_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """List alert instances with optional filtering."""
    query = db.query(AlertInstance)

    if focus_area:
        query = query.filter(AlertInstance.focus_area == focus_area)
    if ei_id:
        query = query.filter(AlertInstance.ei_id == ei_id)

    alerts = query.order_by(AlertInstance.alert_id).offset(skip).limit(limit).all()
    return [AlertInstanceResponse.model_validate(a) for a in alerts]


@router.get("/alert-instances/{alert_id}", response_model=AlertInstanceResponse)
async def get_alert_instance(alert_id: str, db: Session = Depends(get_db)):
    """Get an alert instance by alert_id."""
    alert = db.query(AlertInstance).filter(AlertInstance.alert_id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert instance not found")
    return AlertInstanceResponse.model_validate(alert)


# =============================================================================
# Alert Analysis Endpoints
# =============================================================================

@router.post("/analyses", response_model=AlertAnalysisResponse)
async def save_alert_analysis(
    analysis: AlertAnalysisCreate,
    db: Session = Depends(get_db)
):
    """
    Save analysis results from LLM processing.

    This endpoint receives parsed analysis data and persists it for dashboard display.
    """
    db_analysis = AlertAnalysis(**analysis.model_dump())
    db.add(db_analysis)
    db.commit()
    db.refresh(db_analysis)
    return AlertAnalysisResponse.model_validate(db_analysis)


@router.get("/analyses", response_model=List[AlertAnalysisResponse])
async def list_analyses(
    focus_area: Optional[str] = None,
    severity: Optional[str] = None,
    analysis_type: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """List alert analyses with filtering."""
    query = db.query(AlertAnalysis)

    if severity:
        query = query.filter(AlertAnalysis.severity == severity)
    if analysis_type:
        query = query.filter(AlertAnalysis.analysis_type == analysis_type)
    if focus_area:
        query = query.join(AlertInstance).filter(AlertInstance.focus_area == focus_area)

    analyses = query.order_by(desc(AlertAnalysis.execution_date)).offset(skip).limit(limit).all()
    return [AlertAnalysisResponse.model_validate(a) for a in analyses]


@router.get("/analyses/{analysis_id}", response_model=AlertAnalysisWithDetails)
async def get_analysis_details(analysis_id: int, db: Session = Depends(get_db)):
    """Get full analysis with all child records."""
    analysis = db.query(AlertAnalysis).options(
        joinedload(AlertAnalysis.critical_discoveries),
        joinedload(AlertAnalysis.key_findings),
        joinedload(AlertAnalysis.concentration_metrics),
        joinedload(AlertAnalysis.action_items),
        joinedload(AlertAnalysis.alert_instance)
    ).filter(AlertAnalysis.id == analysis_id).first()

    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")

    return AlertAnalysisWithDetails.model_validate(analysis)


# =============================================================================
# Critical Discovery Endpoints
# =============================================================================

@router.post("/critical-discoveries", response_model=CriticalDiscoveryResponse)
async def create_critical_discovery(
    discovery: CriticalDiscoveryCreate,
    db: Session = Depends(get_db)
):
    """Create a critical discovery."""
    db_discovery = CriticalDiscovery(**discovery.model_dump())
    db.add(db_discovery)
    db.commit()
    db.refresh(db_discovery)
    return CriticalDiscoveryResponse.model_validate(db_discovery)


@router.post("/critical-discoveries/bulk", response_model=List[CriticalDiscoveryResponse])
async def create_critical_discoveries_bulk(
    discoveries: List[CriticalDiscoveryCreate],
    db: Session = Depends(get_db)
):
    """Create multiple critical discoveries at once."""
    db_discoveries = [CriticalDiscovery(**d.model_dump()) for d in discoveries]
    db.add_all(db_discoveries)
    db.commit()
    for d in db_discoveries:
        db.refresh(d)
    return [CriticalDiscoveryResponse.model_validate(d) for d in db_discoveries]


# =============================================================================
# Key Finding Endpoints
# =============================================================================

@router.post("/key-findings", response_model=KeyFindingResponse)
async def create_key_finding(
    finding: KeyFindingCreate,
    db: Session = Depends(get_db)
):
    """Create a key finding."""
    db_finding = KeyFinding(**finding.model_dump())
    db.add(db_finding)
    db.commit()
    db.refresh(db_finding)
    return KeyFindingResponse.model_validate(db_finding)


@router.post("/key-findings/bulk", response_model=List[KeyFindingResponse])
async def create_key_findings_bulk(
    findings: List[KeyFindingCreate],
    db: Session = Depends(get_db)
):
    """Create multiple key findings at once."""
    db_findings = [KeyFinding(**f.model_dump()) for f in findings]
    db.add_all(db_findings)
    db.commit()
    for f in db_findings:
        db.refresh(f)
    return [KeyFindingResponse.model_validate(f) for f in db_findings]


# =============================================================================
# Concentration Metric Endpoints
# =============================================================================

@router.post("/concentration-metrics", response_model=ConcentrationMetricResponse)
async def create_concentration_metric(
    metric: ConcentrationMetricCreate,
    db: Session = Depends(get_db)
):
    """Create a concentration metric."""
    db_metric = ConcentrationMetric(**metric.model_dump())
    db.add(db_metric)
    db.commit()
    db.refresh(db_metric)
    return ConcentrationMetricResponse.model_validate(db_metric)


@router.post("/concentration-metrics/bulk", response_model=List[ConcentrationMetricResponse])
async def create_concentration_metrics_bulk(
    metrics: List[ConcentrationMetricCreate],
    db: Session = Depends(get_db)
):
    """Create multiple concentration metrics at once."""
    db_metrics = [ConcentrationMetric(**m.model_dump()) for m in metrics]
    db.add_all(db_metrics)
    db.commit()
    for m in db_metrics:
        db.refresh(m)
    return [ConcentrationMetricResponse.model_validate(m) for m in db_metrics]


# =============================================================================
# Action Item Endpoints
# =============================================================================

@router.post("/action-items", response_model=ActionItemResponse)
async def create_action_item(
    action_item: ActionItemCreate,
    db: Session = Depends(get_db)
):
    """Create an action item."""
    db_item = ActionItem(**action_item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return ActionItemResponse.model_validate(db_item)


@router.patch("/action-items/{item_id}", response_model=ActionItemResponse)
async def update_action_item(
    item_id: int,
    update: ActionItemUpdate,
    db: Session = Depends(get_db)
):
    """Update an action item (e.g., change status, assign, resolve)."""
    item = db.query(ActionItem).filter(ActionItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Action item not found")

    update_data = update.model_dump(exclude_unset=True)

    # Handle resolution
    if update_data.get('status') in ['REMEDIATED', 'FALSE_POSITIVE']:
        update_data['resolved_at'] = datetime.utcnow()

    for key, value in update_data.items():
        setattr(item, key, value)

    db.commit()
    db.refresh(item)
    return ActionItemResponse.model_validate(item)


@router.post("/action-items/bulk", response_model=List[ActionItemResponse])
async def create_action_items_bulk(
    action_items: List[ActionItemCreate],
    db: Session = Depends(get_db)
):
    """Create multiple action items at once."""
    db_items = [ActionItem(**a.model_dump()) for a in action_items]
    db.add_all(db_items)
    db.commit()
    for item in db_items:
        db.refresh(item)
    return [ActionItemResponse.model_validate(item) for item in db_items]


# =============================================================================
# Deletion Endpoints
# =============================================================================

@router.delete("/analyses/{analysis_id}", response_model=DeleteResponse)
async def delete_alert_analysis(
    analysis_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a single alert analysis and all related data.
    
    Cascades to:
    - CriticalDiscoveries
    - KeyFindings
    - ConcentrationMetrics
    - ActionItems
    """
    analysis = db.query(AlertAnalysis).filter(AlertAnalysis.id == analysis_id).first()
    if not analysis:
        raise HTTPException(status_code=404, detail=f"Alert analysis {analysis_id} not found")
    
    try:
        # Count related records before deletion
        discovery_count = len(analysis.critical_discoveries)
        key_finding_count = len(analysis.key_findings)
        concentration_count = len(analysis.concentration_metrics)
        action_item_count = len(analysis.action_items)
        
        alert_instance = analysis.alert_instance
        alert_id = alert_instance.alert_id if alert_instance else "UNKNOWN"
        alert_name = alert_instance.alert_name if alert_instance else "Unknown Alert"
        
        # Delete the analysis (cascade deletes will handle children)
        db.delete(analysis)
        db.commit()
        
        # Audit log
        audit_log(
            db=db,
            action="delete",
            entity_type="alert_analysis",
            entity_id=analysis_id,
            description=f"Deleted alert analysis {analysis_id} for alert {alert_id}: {alert_name}",
            details={
                "alert_id": alert_id,
                "alert_name": alert_name,
                "discoveries_deleted": discovery_count,
                "key_findings_deleted": key_finding_count,
                "concentration_metrics_deleted": concentration_count,
                "action_items_deleted": action_item_count
            },
            status="success"
        )
        
        return DeleteResponse(
            success=True,
            message=f"Alert analysis {analysis_id} and all related data deleted successfully",
            deleted_records={
                "alert_analysis": 1,
                "critical_discoveries": discovery_count,
                "key_findings": key_finding_count,
                "concentration_metrics": concentration_count,
                "action_items": action_item_count
            }
        )
        
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting alert analysis {analysis_id}: {str(e)}")
        
        audit_log(
            db=db,
            action="delete",
            entity_type="alert_analysis",
            entity_id=analysis_id,
            description=f"Failed to delete alert analysis {analysis_id}",
            status="error",
            error_message=str(e)
        )
        
        raise HTTPException(
            status_code=500,
            detail=f"Error deleting alert analysis: {str(e)}"
        )


@router.delete("/alert-instances/by-alert-id/{alert_id}", response_model=DeleteResponse)
async def delete_alert_instance_by_alert_id(
    alert_id: str,
    db: Session = Depends(get_db)
):
    """
    Delete an alert instance by alert_id (e.g., "200025_001444") and all its analyses.
    
    Cascades to:
    - All AlertAnalyses for this instance
    - All CriticalDiscoveries, KeyFindings, ConcentrationMetrics, ActionItems
    """
    alert_instance = db.query(AlertInstance).filter(AlertInstance.alert_id == alert_id).first()
    if not alert_instance:
        raise HTTPException(status_code=404, detail=f"Alert instance with alert_id '{alert_id}' not found")
    
    alert_instance_id = alert_instance.id
    return await _delete_alert_instance_internal(alert_instance_id, alert_instance, db)


@router.delete("/alert-instances/{alert_instance_id}", response_model=DeleteResponse)
async def delete_alert_instance(
    alert_instance_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete an alert instance and all its analyses.
    
    Cascades to:
    - All AlertAnalyses for this instance
    - All CriticalDiscoveries, KeyFindings, ConcentrationMetrics, ActionItems
    """
    alert_instance = db.query(AlertInstance).filter(AlertInstance.id == alert_instance_id).first()
    if not alert_instance:
        raise HTTPException(status_code=404, detail=f"Alert instance {alert_instance_id} not found")
    
    return await _delete_alert_instance_internal(alert_instance_id, alert_instance, db)


def _delete_alert_instance_internal(
    alert_instance_id: int,
    alert_instance: AlertInstance,
    db: Session
) -> DeleteResponse:
    """
    Internal function to delete an alert instance.
    """
    
    try:
        # Count related records before deletion
        analyses = alert_instance.analyses
        analysis_count = len(analyses)
        
        total_discoveries = sum(len(a.critical_discoveries) for a in analyses)
        total_key_findings = sum(len(a.key_findings) for a in analyses)
        total_concentration = sum(len(a.concentration_metrics) for a in analyses)
        total_action_items = sum(len(a.action_items) for a in analyses)
        
        alert_id = alert_instance.alert_id
        alert_name = alert_instance.alert_name
        
        # Delete the instance (cascade deletes will handle all analyses and their children)
        db.delete(alert_instance)
        db.commit()
        
        # Audit log
        audit_log(
            db=db,
            action="delete",
            entity_type="alert_instance",
            entity_id=alert_instance_id,
            description=f"Deleted alert instance {alert_instance_id}: {alert_id} - {alert_name}",
            details={
                "alert_id": alert_id,
                "alert_name": alert_name,
                "analyses_deleted": analysis_count,
                "discoveries_deleted": total_discoveries,
                "key_findings_deleted": total_key_findings,
                "concentration_metrics_deleted": total_concentration,
                "action_items_deleted": total_action_items
            },
            status="success"
        )
        
        return DeleteResponse(
            success=True,
            message=f"Alert instance {alert_instance_id} ({alert_id}) and all related data deleted successfully",
            deleted_records={
                "alert_instance": 1,
                "alert_analyses": analysis_count,
                "critical_discoveries": total_discoveries,
                "key_findings": total_key_findings,
                "concentration_metrics": total_concentration,
                "action_items": total_action_items
            }
        )
        
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting alert instance {alert_instance_id}: {str(e)}")
        
        audit_log(
            db=db,
            action="delete",
            entity_type="alert_instance",
            entity_id=alert_instance_id,
            description=f"Failed to delete alert instance {alert_instance_id}",
            status="error",
            error_message=str(e)
        )
        
        raise HTTPException(
            status_code=500,
            detail=f"Error deleting alert instance: {str(e)}"
        )


@router.delete("/alert-instances", response_model=DeleteResponse)
async def delete_all_alert_instances(
    confirm: bool = Query(False, description="Must be True to confirm deletion"),
    db: Session = Depends(get_db)
):
    """
    Delete ALL alert instances and all related data.
    
    WARNING: This is a destructive operation that will delete:
    - All AlertInstances
    - All AlertAnalyses
    - All CriticalDiscoveries
    - All KeyFindings
    - All ConcentrationMetrics
    - All ActionItems
    
    Requires confirm=true query parameter.
    """
    if not confirm:
        raise HTTPException(
            status_code=400,
            detail="Must set confirm=true to delete all alert instances"
        )
    
    try:
        # Count all records before deletion
        all_instances = db.query(AlertInstance).all()
        instance_count = len(all_instances)
        
        total_analyses = 0
        total_discoveries = 0
        total_key_findings = 0
        total_concentration = 0
        total_action_items = 0
        
        for instance in all_instances:
            analyses = instance.analyses
            total_analyses += len(analyses)
            for analysis in analyses:
                total_discoveries += len(analysis.critical_discoveries)
                total_key_findings += len(analysis.key_findings)
                total_concentration += len(analysis.concentration_metrics)
                total_action_items += len(analysis.action_items)
        
        # Delete all instances (cascade deletes will handle everything)
        db.query(AlertInstance).delete()
        db.commit()
        
        # Audit log
        audit_log(
            db=db,
            action="delete_all",
            entity_type="alert_instance",
            description="Deleted all alert instances and related data",
            details={
                "alert_instances_deleted": instance_count,
                "alert_analyses_deleted": total_analyses,
                "critical_discoveries_deleted": total_discoveries,
                "key_findings_deleted": total_key_findings,
                "concentration_metrics_deleted": total_concentration,
                "action_items_deleted": total_action_items
            },
            status="success"
        )
        
        return DeleteResponse(
            success=True,
            message="All alert instances and related data deleted successfully",
            deleted_records={
                "alert_instances": instance_count,
                "alert_analyses": total_analyses,
                "critical_discoveries": total_discoveries,
                "key_findings": total_key_findings,
                "concentration_metrics": total_concentration,
                "action_items": total_action_items
            }
        )
        
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting all alert instances: {str(e)}")
        
        audit_log(
            db=db,
            action="delete_all",
            entity_type="alert_instance",
            description="Failed to delete all alert instances",
            status="error",
            error_message=str(e)
        )
        
        raise HTTPException(
            status_code=500,
            detail=f"Error deleting all alert instances: {str(e)}"
        )


@router.delete("/discoveries/{discovery_id}", response_model=DeleteResponse)
async def delete_critical_discovery(
    discovery_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a single critical discovery.
    
    This removes only the discovery record, not the entire analysis.
    Use this when you want to remove a specific discovery without deleting
    the whole alert analysis.
    """
    discovery = db.query(CriticalDiscovery).filter(CriticalDiscovery.id == discovery_id).first()
    if not discovery:
        raise HTTPException(status_code=404, detail=f"Critical discovery {discovery_id} not found")
    
    try:
        analysis_id = discovery.alert_analysis_id
        title = discovery.title
        
        # Delete the discovery
        db.delete(discovery)
        db.commit()
        
        # Audit log
        audit_log(
            db=db,
            action="delete",
            entity_type="critical_discovery",
            entity_id=discovery_id,
            description=f"Deleted critical discovery {discovery_id}: {title}",
            details={
                "discovery_id": discovery_id,
                "title": title,
                "alert_analysis_id": analysis_id
            },
            status="success"
        )
        
        return DeleteResponse(
            success=True,
            message=f"Critical discovery {discovery_id} deleted successfully",
            deleted_records={
                "critical_discovery": 1
            }
        )
        
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting critical discovery {discovery_id}: {str(e)}")
        
        audit_log(
            db=db,
            action="delete",
            entity_type="critical_discovery",
            entity_id=discovery_id,
            description=f"Failed to delete critical discovery {discovery_id}",
            status="error",
            error_message=str(e)
        )
        
        raise HTTPException(
            status_code=500,
            detail=f"Error deleting critical discovery: {str(e)}"
        )
