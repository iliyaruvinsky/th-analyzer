"""
Pydantic schemas for Alert Analysis Dashboard.
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from decimal import Decimal


# =============================================================================
# Client Schemas
# =============================================================================

class ClientBase(BaseModel):
    code: str = Field(..., max_length=20, description="Client code (e.g., SAFAL)")
    name: str = Field(..., max_length=255, description="Client name")
    description: Optional[str] = None
    website: Optional[str] = None


class ClientCreate(ClientBase):
    pass


class ClientResponse(ClientBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# =============================================================================
# Source System Schemas
# =============================================================================

class SourceSystemBase(BaseModel):
    code: str = Field(..., max_length=20, description="System code (e.g., PS4)")
    name: str = Field(..., max_length=100, description="System name")
    system_type: Optional[str] = Field(None, max_length=50, description="ECC, S/4HANA, BW")
    environment: Optional[str] = Field(None, max_length=20, description="DEV, QA, PROD")


class SourceSystemCreate(SourceSystemBase):
    client_id: int


class SourceSystemResponse(SourceSystemBase):
    id: int
    client_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# =============================================================================
# Exception Indicator Schemas
# =============================================================================

class ExceptionIndicatorBase(BaseModel):
    ei_id: str = Field(..., max_length=50, description="EI identifier (e.g., SW_10_01_ORD_VAL_TOT)")
    function_name: Optional[str] = Field(None, max_length=100, description="ABAP function name")
    module: str = Field(..., max_length=10, description="Module (FI, SD, MM, MD, PUR)")
    category: Optional[str] = Field(None, max_length=50, description="Applications, Master Data, Access Control")


class ExceptionIndicatorCreate(ExceptionIndicatorBase):
    pass


class ExceptionIndicatorResponse(ExceptionIndicatorBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# =============================================================================
# EI Vocabulary Schemas
# =============================================================================

class EIVocabularyBase(BaseModel):
    source_tables: Optional[List[str]] = Field(None, description="Tables queried by EI")
    key_fields: Optional[Dict[str, str]] = Field(None, description="Field meanings")
    data_selection_logic: Optional[str] = Field(None, description="Parsed SELECT/WHERE interpretation")
    aggregation_logic: Optional[str] = Field(None, description="How data is grouped")
    threshold_fields: Optional[Dict[str, Any]] = Field(None, description="Parameters controlling flagging")
    risk_patterns: Optional[List[str]] = Field(None, description="Known red flag patterns")
    interpretation_notes: Optional[str] = Field(None, description="LLM-generated analysis summary")
    external_functions_needed: Optional[List[str]] = Field(None, description="Called functions requiring additional code")


class EIVocabularyCreate(EIVocabularyBase):
    ei_id: int


class EIVocabularyResponse(EIVocabularyBase):
    id: int
    ei_id: int
    version: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class EIWithVocabularyResponse(ExceptionIndicatorResponse):
    vocabulary: Optional[EIVocabularyResponse] = None


# =============================================================================
# Alert Instance Schemas
# =============================================================================

class AlertInstanceBase(BaseModel):
    alert_id: str = Field(..., max_length=50, description="Alert identifier (e.g., 200025_001455)")
    alert_name: str = Field(..., max_length=255, description="Alert name")
    focus_area: str = Field(..., max_length=50, description="Focus area classification")
    subcategory: Optional[str] = Field(None, max_length=100)
    parameters: Optional[Dict[str, Any]] = Field(None, description="Alert parameters from Metadata")
    business_purpose: Optional[str] = Field(None, description="From Explanation artifact")


class AlertInstanceCreate(AlertInstanceBase):
    ei_id: Optional[int] = None
    source_system_id: Optional[int] = None


class AlertInstanceResponse(AlertInstanceBase):
    id: int
    ei_id: Optional[int] = None
    source_system_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True


# =============================================================================
# Alert Analysis Schemas
# =============================================================================

class AlertAnalysisBase(BaseModel):
    analysis_type: str = Field(..., max_length=20, description="QUANTI, QUALI, HYBRID")
    execution_date: date = Field(..., description="When alert was executed")
    period_start: Optional[date] = None
    period_end: Optional[date] = None
    records_affected: Optional[int] = None
    unique_entities: Optional[int] = None
    severity: str = Field(..., max_length=20, description="CRITICAL, HIGH, MEDIUM, LOW")
    risk_score: Optional[int] = Field(None, ge=0, le=100)
    fraud_indicator: Optional[str] = Field(None, max_length=50, description="CONFIRMED, INVESTIGATE, MONITOR, NONE")
    financial_impact_local: Optional[Decimal] = None
    financial_impact_usd: Optional[Decimal] = None
    local_currency: Optional[str] = Field(None, max_length=10)
    exchange_rate: Optional[Decimal] = None
    report_path: Optional[str] = Field(None, max_length=500)
    raw_summary_data: Optional[Dict[str, Any]] = None


class AlertAnalysisCreate(AlertAnalysisBase):
    alert_instance_id: int
    created_by: Optional[str] = None


class AlertAnalysisResponse(AlertAnalysisBase):
    id: int
    alert_instance_id: int
    created_at: datetime
    created_by: Optional[str] = None

    class Config:
        from_attributes = True


# =============================================================================
# Critical Discovery Schemas
# =============================================================================

class CriticalDiscoveryBase(BaseModel):
    discovery_order: int = Field(1, description="Order in the analysis")
    title: str = Field(..., max_length=255, description="Short title")
    description: str = Field(..., description="Full discovery text")
    affected_entity: Optional[str] = Field(None, max_length=255, description="Entity name")
    affected_entity_id: Optional[str] = Field(None, max_length=50, description="Entity ID")
    metric_value: Optional[Decimal] = None
    metric_unit: Optional[str] = Field(None, max_length=50)
    percentage_of_total: Optional[Decimal] = None
    is_fraud_indicator: bool = False


class CriticalDiscoveryCreate(CriticalDiscoveryBase):
    alert_analysis_id: int


class CriticalDiscoveryResponse(CriticalDiscoveryBase):
    id: int
    alert_analysis_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# =============================================================================
# Key Finding Schemas
# =============================================================================

class KeyFindingBase(BaseModel):
    finding_rank: int = Field(..., ge=1, description="Rank (1, 2, 3)")
    finding_text: str = Field(..., description="Finding description")
    finding_category: Optional[str] = Field(None, max_length=50, description="Concentration, Anomaly, Data Quality, Process Gap")
    financial_impact_usd: Optional[Decimal] = None


class KeyFindingCreate(KeyFindingBase):
    alert_analysis_id: int


class KeyFindingResponse(KeyFindingBase):
    id: int
    alert_analysis_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# =============================================================================
# Concentration Metric Schemas
# =============================================================================

class ConcentrationMetricBase(BaseModel):
    dimension_type: str = Field(..., max_length=50, description="SALES_ORG, CUSTOMER, REGION")
    dimension_code: str = Field(..., max_length=50)
    dimension_name: Optional[str] = Field(None, max_length=255)
    record_count: Optional[int] = None
    value_local: Optional[Decimal] = None
    value_usd: Optional[Decimal] = None
    percentage_of_total: Optional[Decimal] = None
    rank: Optional[int] = None


class ConcentrationMetricCreate(ConcentrationMetricBase):
    alert_analysis_id: int


class ConcentrationMetricResponse(ConcentrationMetricBase):
    id: int
    alert_analysis_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# =============================================================================
# Action Item Schemas
# =============================================================================

class ActionItemBase(BaseModel):
    action_type: str = Field(..., max_length=50, description="IMMEDIATE, SHORT_TERM, PROCESS_IMPROVEMENT")
    priority: Optional[int] = Field(None, ge=1, le=5)
    title: str = Field(..., max_length=255)
    description: Optional[str] = None
    status: str = Field("OPEN", max_length=30, description="OPEN, IN_REVIEW, REMEDIATED, FALSE_POSITIVE")
    assigned_to: Optional[str] = Field(None, max_length=100)
    due_date: Optional[date] = None


class ActionItemCreate(ActionItemBase):
    alert_analysis_id: int


class ActionItemUpdate(BaseModel):
    status: Optional[str] = Field(None, max_length=30)
    assigned_to: Optional[str] = Field(None, max_length=100)
    due_date: Optional[date] = None
    resolution_notes: Optional[str] = None


class ActionItemResponse(ActionItemBase):
    id: int
    alert_analysis_id: int
    resolution_notes: Optional[str] = None
    resolved_at: Optional[datetime] = None
    resolved_by: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


# =============================================================================
# Dashboard KPI Schemas
# =============================================================================

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


class AlertAnalysisWithDetails(AlertAnalysisResponse):
    """Full analysis with nested child objects."""
    critical_discoveries: List[CriticalDiscoveryResponse] = []
    key_findings: List[KeyFindingResponse] = []
    concentration_metrics: List[ConcentrationMetricResponse] = []
    action_items: List[ActionItemResponse] = []
    alert_instance: Optional[AlertInstanceResponse] = None


class TrendDataPoint(BaseModel):
    """Single data point for trend analysis."""
    period: str = Field(..., description="Period label (e.g., '2024-01', 'Q1 2024')")
    alerts_analyzed: int
    critical_discoveries: int
    financial_exposure_usd: Decimal
    avg_risk_score: float


class TrendAnalysisResponse(BaseModel):
    """Trend data for time-series visualization."""
    period_type: str = Field(..., description="MONTHLY, QUARTERLY, YEARLY")
    data_points: List[TrendDataPoint]
    comparison_message: Optional[str] = Field(None, description="Comparison note (e.g., '+15% vs prior period')")
