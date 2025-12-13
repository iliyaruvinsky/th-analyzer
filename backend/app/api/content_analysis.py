"""
Content Analysis API Endpoints

Provides endpoints for the intelligent Content Analyzer pipeline.
Supports both single alert analysis and batch processing with
configurable report levels (summary/full LLM-generated).
"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from enum import Enum
import os
import uuid
import logging
from datetime import datetime

from app.core.database import get_db
from app.core.config import settings
from app.services.content_analyzer import ContentAnalyzer
from app.services.content_analyzer.artifact_reader import ArtifactReader
from app.services.content_analyzer.report_generator import ReportGenerator
from app.models.finding import Finding
from app.models.focus_area import FocusArea
from app.models.risk_assessment import RiskAssessment
from app.models.money_loss import MoneyLossCalculation
from app.models.data_source import DataSource, DataSourceType, FileFormat
# Dashboard models for integrated pipeline
from app.models.alert_instance import AlertInstance
from app.models.alert_analysis import AlertAnalysis
from app.models.critical_discovery import CriticalDiscovery
from app.models.key_finding import KeyFinding
from app.models.action_item import ActionItem

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/content-analysis", tags=["Content Analysis"])


# ============================================================================
# Enums and Constants
# ============================================================================

class ReportLevel(str, Enum):
    """Report generation level."""
    SUMMARY = "summary"  # Quick metrics extraction, no LLM (low cost)
    FULL = "full"        # Complete LLM-generated report (higher cost)


# In-memory batch job storage (for production, use Redis or database)
_batch_jobs: Dict[str, Dict[str, Any]] = {}


# Request/Response Models
class AnalyzeTextRequest(BaseModel):
    """Request to analyze text content directly."""
    alert_id: str
    alert_name: str
    code: Optional[str] = None
    explanation: Optional[str] = None
    metadata: Optional[str] = None
    summary: Optional[str] = None
    use_llm: bool = True


class AnalyzeDirectoryRequest(BaseModel):
    """Request to analyze a directory with artifact files."""
    directory_path: str
    use_llm: bool = True
    report_level: ReportLevel = ReportLevel.FULL  # full or summary


class AnalyzeBatchRequest(BaseModel):
    """Request to analyze multiple alert directories."""
    directory_paths: List[str]
    report_level: ReportLevel = ReportLevel.FULL


class ScanFoldersRequest(BaseModel):
    """Request to scan for alert folders."""
    root_path: str = "docs/skywind-4c-alerts-output"


class ScanFoldersResponse(BaseModel):
    """Response with discovered alert folders."""
    folders: List[Dict[str, Any]]
    total: int


class BatchJobResponse(BaseModel):
    """Response after starting a batch job."""
    job_id: str
    total_alerts: int
    status: str
    message: str


class BatchStatusResponse(BaseModel):
    """Response with batch job status."""
    job_id: str
    status: str  # pending, processing, completed, failed
    total: int
    processed: int
    successful: int
    failed: int
    results: List[Dict[str, Any]]
    started_at: Optional[str]
    completed_at: Optional[str]


class FindingResponse(BaseModel):
    """Response containing a single finding."""
    alert_id: str
    alert_name: str
    focus_area: str
    focus_area_confidence: float
    classification_reasoning: str
    title: str
    description: str
    business_impact: str
    what_happened: str
    business_risk: str
    affected_areas: List[str]
    total_count: int
    monetary_amount: float
    currency: str
    key_metrics: Dict[str, Any]
    notable_items: List[Dict[str, Any]]
    severity: str
    severity_reasoning: str
    risk_score: int
    risk_level: str
    risk_factors: List[str]
    money_loss_estimate: float
    money_loss_confidence: float
    recommended_actions: List[str]
    analyzed_at: str
    analysis_version: str


class FeedbackRequest(BaseModel):
    """Request to provide feedback on a finding."""
    alert_id: str
    finding_id: Optional[int] = None
    is_correct: bool
    correct_focus_area: Optional[str] = None
    feedback_notes: str
    correct_severity: Optional[str] = None


class FeedbackResponse(BaseModel):
    """Response after submitting feedback."""
    status: str
    message: str


# Global analyzer instance (lazy initialization)
_analyzer_instance: Optional[ContentAnalyzer] = None


def get_content_analyzer() -> ContentAnalyzer:
    """Get or create the ContentAnalyzer instance."""
    global _analyzer_instance

    if _analyzer_instance is None:
        # Get configuration from settings
        llm_provider = getattr(settings, 'LLM_PROVIDER', 'openai')
        api_key = None

        if llm_provider == 'anthropic':
            api_key = getattr(settings, 'ANTHROPIC_API_KEY', None)
        else:
            api_key = getattr(settings, 'OPENAI_API_KEY', None)

        use_llm = api_key is not None

        _analyzer_instance = ContentAnalyzer(
            llm_provider=llm_provider,
            api_key=api_key,
            use_llm=use_llm
        )

        logger.info(f"ContentAnalyzer initialized: LLM={use_llm}, provider={llm_provider}")

    return _analyzer_instance


@router.post("/analyze", response_model=FindingResponse)
async def analyze_content(
    request: AnalyzeTextRequest,
    db: Session = Depends(get_db)
):
    """
    Analyze alert content and return findings.

    This endpoint accepts alert artifacts directly (Code, Explanation, Metadata, Summary)
    and returns a detailed finding with classification, scoring, and recommendations.

    Use this for testing the analyzer with specific content.
    """
    try:
        analyzer = get_content_analyzer()

        # Create artifacts from request
        artifact_reader = ArtifactReader()
        artifacts = artifact_reader.read_from_content(
            alert_id=request.alert_id,
            alert_name=request.alert_name,
            code=request.code,
            explanation=request.explanation,
            metadata=request.metadata,
            summary=request.summary
        )

        # Temporarily override LLM setting if requested
        original_use_llm = analyzer.use_llm
        if not request.use_llm:
            analyzer.use_llm = False

        try:
            finding = analyzer.analyze_alert(artifacts, include_raw=True)
        finally:
            analyzer.use_llm = original_use_llm

        return FindingResponse(**finding.to_dict())

    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@router.post("/analyze-directory", response_model=FindingResponse)
async def analyze_directory(
    request: AnalyzeDirectoryRequest,
    db: Session = Depends(get_db)
):
    """
    Analyze alert from a directory containing artifact files.

    The directory should contain files named:
    - Code_*.txt
    - Explanation_*.txt
    - Metadata_*.txt
    - Summary_*.txt (or .csv, .xlsx)
    """
    try:
        if not os.path.exists(request.directory_path):
            raise HTTPException(status_code=404, detail=f"Directory not found: {request.directory_path}")

        analyzer = get_content_analyzer()

        # Temporarily override LLM setting if requested
        original_use_llm = analyzer.use_llm
        if not request.use_llm:
            analyzer.use_llm = False

        try:
            finding = analyzer.analyze_from_directory(request.directory_path, include_raw=True)
        finally:
            analyzer.use_llm = original_use_llm

        return FindingResponse(**finding.to_dict())

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


class SavedFindingResponse(BaseModel):
    """Response after saving a finding to database."""
    finding_id: int
    message: str
    focus_area: str
    severity: str
    risk_score: int
    money_loss_estimate: float
    markdown_path: Optional[str] = None
    report_level: str = "summary"


@router.post("/analyze-and-save", response_model=SavedFindingResponse)
async def analyze_and_save(
    request: AnalyzeDirectoryRequest,
    db: Session = Depends(get_db)
):
    """
    Analyze alert from directory AND save to database + generate markdown report.

    This endpoint:
    1. Runs the Content Analyzer on the artifact files
    2. Saves the finding to the database
    3. Creates associated RiskAssessment and MoneyLossCalculation records
    4. Generates markdown report (full LLM or summary based on report_level)
    5. Saves markdown to docs/analysis/ folder

    Report Levels:
    - "summary": Quick metrics extraction, no LLM (low cost)
    - "full": Complete LLM-generated Key Findings report (higher cost)

    The saved finding will appear in the Dashboard.
    """
    try:
        if not os.path.exists(request.directory_path):
            raise HTTPException(status_code=404, detail=f"Directory not found: {request.directory_path}")

        analyzer = get_content_analyzer()
        artifact_reader = ArtifactReader()

        # Read artifacts first (needed for both analysis and report generation)
        artifacts = artifact_reader.read_from_directory(request.directory_path)

        # Determine if we should use LLM based on request
        use_llm_for_analysis = request.use_llm and request.report_level == ReportLevel.FULL

        # Override LLM setting
        original_use_llm = analyzer.use_llm
        analyzer.use_llm = use_llm_for_analysis

        try:
            content_finding = analyzer.analyze_alert(artifacts, include_raw=True)
        finally:
            analyzer.use_llm = original_use_llm

        # Get or create the focus area
        focus_area = db.query(FocusArea).filter(FocusArea.code == content_finding.focus_area).first()
        if not focus_area:
            focus_area = FocusArea(
                code=content_finding.focus_area,
                name=content_finding.focus_area.replace("_", " ").title(),
                description=f"Auto-created for {content_finding.focus_area}"
            )
            db.add(focus_area)
            db.flush()

        # Get or create a data source for this artifact directory
        data_source = db.query(DataSource).filter(
            DataSource.original_filename == request.directory_path
        ).first()
        if not data_source:
            dir_name = os.path.basename(request.directory_path.rstrip('/\\'))
            data_source = DataSource(
                filename=f"artifacts_{dir_name}",
                original_filename=request.directory_path,
                file_format=FileFormat.JSON,
                data_type=DataSourceType.ALERT,
                file_path=request.directory_path,
                file_size=0,
                status="processed"
            )
            db.add(data_source)
            db.flush()

        # Generate markdown report
        markdown_path = None
        markdown_report = None
        try:
            report_generator = ReportGenerator()
            markdown_report = report_generator.generate_report(
                artifacts=artifacts,
                content_finding=content_finding,
                report_level=request.report_level.value
            )

            # Save markdown to file
            markdown_path = report_generator.save_report(
                report=markdown_report,
                alert_id=content_finding.alert_id,
                alert_name=content_finding.alert_name,
                module=_extract_module_from_path(request.directory_path)
            )
            logger.info(f"Generated markdown report: {markdown_path}")
        except Exception as e:
            logger.warning(f"Failed to generate markdown report: {e}")
            # Continue without markdown - don't fail the whole request

        # Create the Finding with new report storage fields
        finding = Finding(
            data_source_id=data_source.id,
            focus_area_id=focus_area.id,
            title=content_finding.title,
            description=content_finding.description[:4000] if content_finding.description else None,
            severity=content_finding.severity,
            classification_confidence=content_finding.focus_area_confidence,
            status="new",
            # New fields for content analysis pipeline
            source_alert_id=content_finding.alert_id,
            source_alert_name=content_finding.alert_name,
            source_module=_extract_module_from_path(request.directory_path),
            source_directory=request.directory_path,
            markdown_report=markdown_report,
            report_path=markdown_path,
            report_level=request.report_level.value,
            key_findings_json={
                "risk_score": content_finding.risk_score,
                "money_loss_estimate": content_finding.money_loss_estimate,
                "focus_area": content_finding.focus_area,
                "severity": content_finding.severity,
                "total_count": content_finding.total_count,
                "monetary_amount": content_finding.monetary_amount,
                "currency": content_finding.currency,
                "key_metrics": content_finding.key_metrics,
            },
            analysis_status="completed",
            analyzed_at=datetime.utcnow()
        )
        db.add(finding)
        db.flush()

        # Create RiskAssessment
        risk_assessment = RiskAssessment(
            finding_id=finding.id,
            risk_score=content_finding.risk_score,
            risk_level=content_finding.risk_level,
            risk_category=content_finding.focus_area,
            risk_description=content_finding.severity_reasoning,
            risk_factors=content_finding.risk_factors,
            potential_impact=content_finding.business_impact
        )
        db.add(risk_assessment)

        # Create MoneyLossCalculation
        money_loss = MoneyLossCalculation(
            finding_id=finding.id,
            estimated_loss=content_finding.money_loss_estimate,
            confidence_score=content_finding.money_loss_confidence,
            calculation_method="content_analyzer",
            final_estimate=content_finding.money_loss_estimate,
            reasoning=f"Estimated from {content_finding.alert_name} analysis"
        )
        db.add(money_loss)

        # Populate Alert Dashboard tables for unified visualization
        dashboard_result = _populate_dashboard_tables(
            db=db,
            content_finding=content_finding,
            directory_path=request.directory_path,
            finding_id=finding.id
        )
        logger.info(f"Dashboard integration: {dashboard_result}")

        db.commit()

        # Build success message with dashboard info
        dashboard_msg = ""
        if dashboard_result.get("alert_analysis_id"):
            dashboard_msg = f" Dashboard populated: {dashboard_result.get('critical_discoveries', 0)} discoveries, {dashboard_result.get('action_items', 0)} action items."

        return SavedFindingResponse(
            finding_id=finding.id,
            message=f"Finding saved successfully for alert: {content_finding.alert_name}.{dashboard_msg}",
            focus_area=content_finding.focus_area,
            severity=content_finding.severity,
            risk_score=content_finding.risk_score,
            money_loss_estimate=content_finding.money_loss_estimate,
            markdown_path=markdown_path,
            report_level=request.report_level.value
        )

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Analysis and save failed: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis and save failed: {str(e)}")


def _extract_module_from_path(directory_path: str) -> str:
    """Extract module code (FI, MM, SD, etc.) from directory path."""
    path_parts = directory_path.replace("\\", "/").split("/")
    # Look for known module codes in path
    modules = ["FI", "MM", "SD", "MD", "PUR", "HR", "PP", "QM"]
    for part in path_parts:
        if part.upper() in modules:
            return part.upper()
    return "GENERAL"


def _populate_dashboard_tables(
    db: Session,
    content_finding,
    directory_path: str,
    finding_id: int
) -> dict:
    """
    Populate the Alert Dashboard tables from content analysis results.

    Creates:
    - AlertInstance (or reuses existing)
    - AlertAnalysis (linked to AlertInstance)
    - CriticalDiscovery records (from notable_items)
    - KeyFinding records
    - ActionItem records (for high-risk findings)

    Returns dict with created record IDs.
    """
    try:
        module = _extract_module_from_path(directory_path)

        # Map focus area to severity
        severity_map = {
            "BUSINESS_PROTECTION": "HIGH",
            "ACCESS_GOVERNANCE": "HIGH",
            "BUSINESS_CONTROL": "MEDIUM",
            "TECHNICAL_CONTROL": "MEDIUM",
            "JOBS_CONTROL": "LOW",
            "S4HANA_EXCELLENCE": "MEDIUM"
        }

        # Map risk_score to fraud_indicator
        def get_fraud_indicator(risk_score: int, severity: str) -> str:
            if risk_score >= 80 or severity == "CRITICAL":
                return "INVESTIGATE"
            elif risk_score >= 60 or severity == "HIGH":
                return "MONITOR"
            else:
                return "NONE"

        # Validate content_finding before proceeding
        from app.services.content_analyzer.analyzer import ContentAnalyzer
        analyzer = ContentAnalyzer(use_llm=False)
        is_valid, validation_warnings = analyzer._validate_content_finding(content_finding)
        
        if validation_warnings:
            logger.warning(f"Validation warnings for alert {content_finding.alert_id}: {', '.join(validation_warnings)}")
        
        # 1. Create or get AlertInstance
        alert_instance = db.query(AlertInstance).filter(
            AlertInstance.alert_id == content_finding.alert_id
        ).first()

        if not alert_instance:
            # Validate required fields with defaults
            alert_id = content_finding.alert_id or f"UNKNOWN_{datetime.utcnow().timestamp()}"
            alert_name = content_finding.alert_name or "Unnamed Alert"
            focus_area = content_finding.focus_area or "BUSINESS_CONTROL"
            
            # Ensure business_purpose is not None
            business_purpose = (
                content_finding.business_impact or 
                (content_finding.description[:500] if content_finding.description else None) or
                f"Alert: {alert_name}"
            )
            
            # Ensure parameters is a dict, not None
            parameters = {
                "directory_path": directory_path,
                "module": module
            }
            
            alert_instance = AlertInstance(
                alert_id=alert_id,
                alert_name=alert_name,
                focus_area=focus_area,
                subcategory=module,
                parameters=parameters,
                business_purpose=business_purpose
            )
            db.add(alert_instance)
            db.flush()
            logger.info(f"Created AlertInstance: {alert_instance.alert_id}")

        # 2. Create AlertAnalysis
        # Validate and set defaults for required fields
        severity = content_finding.severity.upper() if content_finding.severity else "MEDIUM"
        risk_score = content_finding.risk_score if content_finding.risk_score is not None else 50
        
        fraud_indicator = get_fraud_indicator(risk_score, severity)

        # Convert money_loss_estimate to proper decimal
        financial_impact = content_finding.money_loss_estimate or 0.0

        # Cap records_affected to PostgreSQL Integer max (2,147,483,647)
        # Ensure records_affected is >= 0
        records_affected = content_finding.total_count if content_finding.total_count is not None else 0
        if records_affected < 0:
            logger.warning(f"records_affected is negative ({records_affected}), setting to 0")
            records_affected = 0
        if records_affected > 2147483647:
            logger.warning(f"records_affected exceeds max INT ({records_affected}), capping to 2147483647")
            records_affected = 2147483647  # Cap to max INT value

        # Ensure raw_summary_data is a dict, not None
        raw_summary_data = {
            "key_metrics": content_finding.key_metrics if content_finding.key_metrics else {},
            "risk_factors": content_finding.risk_factors if content_finding.risk_factors else [],
            "recommended_actions": content_finding.recommended_actions if content_finding.recommended_actions else [],
            "finding_id": finding_id
        }

        alert_analysis = AlertAnalysis(
            alert_instance_id=alert_instance.id,
            analysis_type="QUANTI",  # Quantitative analysis
            execution_date=datetime.utcnow().date(),
            records_affected=records_affected,
            severity=severity,
            risk_score=risk_score,
            fraud_indicator=fraud_indicator,
            financial_impact_usd=financial_impact,
            local_currency=content_finding.currency or "USD",
            report_path=directory_path,
            raw_summary_data=raw_summary_data,
            created_by="content_analyzer_pipeline"
        )
        db.add(alert_analysis)
        db.flush()
        logger.info(f"Created AlertAnalysis: {alert_analysis.id}")

        # 3. Create CriticalDiscovery records from notable_items
        discovery_count = 0
        if hasattr(content_finding, 'notable_items') and content_finding.notable_items:
            for idx, item in enumerate(content_finding.notable_items[:5], 1):  # Max 5 discoveries
                # Handle both dict and object notable items
                if isinstance(item, dict):
                    title = item.get('title', item.get('entity', f'Discovery {idx}'))
                    description = item.get('description', item.get('details', str(item)))
                    entity = item.get('entity', item.get('id', ''))
                    amount = item.get('amount', item.get('value', 0))
                    percentage = item.get('percentage', 0)
                else:
                    title = getattr(item, 'title', f'Discovery {idx}')
                    description = getattr(item, 'description', str(item))
                    entity = getattr(item, 'entity', '')
                    amount = getattr(item, 'amount', 0)
                    percentage = getattr(item, 'percentage', 0)

                discovery = CriticalDiscovery(
                    alert_analysis_id=alert_analysis.id,
                    discovery_order=idx,
                    title=str(title)[:255],
                    description=str(description)[:2000],
                    affected_entity=str(entity)[:255] if entity else None,
                    metric_value=float(amount) if amount else None,
                    percentage_of_total=float(percentage) if percentage else None,
                    is_fraud_indicator=(fraud_indicator == "INVESTIGATE")
                )
                db.add(discovery)
                discovery_count += 1

        # If no notable items, create one from the main finding
        # This ensures at least one CriticalDiscovery per analysis
        if discovery_count == 0:
            # Try to get title from various sources
            title = (
                content_finding.title or 
                content_finding.alert_name or 
                "Alert Analysis Finding"
            )
            
            # Try to get description from various sources
            description = (
                content_finding.description or 
                content_finding.business_impact or 
                content_finding.what_happened or
                f"Analysis of alert: {content_finding.alert_name}"
            )
            
            discovery = CriticalDiscovery(
                alert_analysis_id=alert_analysis.id,
                discovery_order=1,
                title=title[:255],
                description=description[:2000],
                metric_value=float(financial_impact) if financial_impact else None,
                is_fraud_indicator=(fraud_indicator == "INVESTIGATE")
            )
            db.add(discovery)
            discovery_count = 1
            logger.info(f"Created default CriticalDiscovery from main finding (no notable_items available)")

        if discovery_count == 0:
            logger.error(f"Failed to create any CriticalDiscovery records for alert_analysis {alert_analysis.id}")
            raise ValueError("At least one CriticalDiscovery must be created per analysis")

        logger.info(f"Created {discovery_count} CriticalDiscovery records")

        # 4. Create KeyFinding records
        key_finding_count = 0

        # First key finding: main business impact
        if content_finding.business_impact:
            kf = KeyFinding(
                alert_analysis_id=alert_analysis.id,
                finding_rank=1,
                finding_text=content_finding.business_impact[:2000],
                finding_category="Impact",
                financial_impact_usd=financial_impact
            )
            db.add(kf)
            key_finding_count += 1

        # Second key finding: risk description
        if hasattr(content_finding, 'severity_reasoning') and content_finding.severity_reasoning:
            kf = KeyFinding(
                alert_analysis_id=alert_analysis.id,
                finding_rank=2,
                finding_text=content_finding.severity_reasoning[:2000],
                finding_category="Risk"
            )
            db.add(kf)
            key_finding_count += 1

        # Third key finding from risk_factors
        if hasattr(content_finding, 'risk_factors') and content_finding.risk_factors:
            factors_text = "; ".join(content_finding.risk_factors[:3])
            kf = KeyFinding(
                alert_analysis_id=alert_analysis.id,
                finding_rank=3,
                finding_text=f"Risk Factors: {factors_text}"[:2000],
                finding_category="Concentration"
            )
            db.add(kf)
            key_finding_count += 1

        logger.info(f"Created {key_finding_count} KeyFinding records")

        # 5. Create ActionItem records for high-risk findings
        action_count = 0
        if fraud_indicator == "INVESTIGATE" or severity in ["CRITICAL", "HIGH"]:
            # Immediate action for investigation
            action = ActionItem(
                alert_analysis_id=alert_analysis.id,
                action_type="IMMEDIATE",
                priority=1,
                title=f"Investigate {content_finding.alert_name}",
                description=f"High-risk alert detected with {severity} severity and risk score {content_finding.risk_score}. Review findings and determine if fraudulent activity occurred.",
                status="OPEN"
            )
            db.add(action)
            action_count += 1

        # Short-term action from recommended_actions
        if hasattr(content_finding, 'recommended_actions') and content_finding.recommended_actions:
            for idx, rec_action in enumerate(content_finding.recommended_actions[:2], 1):
                action = ActionItem(
                    alert_analysis_id=alert_analysis.id,
                    action_type="SHORT_TERM",
                    priority=2 + idx,
                    title=str(rec_action)[:255],
                    description=f"Recommended action from analysis: {rec_action}",
                    status="OPEN"
                )
                db.add(action)
                action_count += 1

        logger.info(f"Created {action_count} ActionItem records")

        return {
            "alert_instance_id": alert_instance.id,
            "alert_analysis_id": alert_analysis.id,
            "critical_discoveries": discovery_count,
            "key_findings": key_finding_count,
            "action_items": action_count
        }

    except Exception as e:
        logger.error(f"Failed to populate dashboard tables: {e}")
        # Don't fail the whole request - dashboard population is supplementary
        return {
            "error": str(e),
            "alert_instance_id": None,
            "alert_analysis_id": None
        }


@router.post("/analyze-sample/{sample_name}", response_model=FindingResponse)
async def analyze_sample(
    sample_name: str,
    use_llm: bool = True,
    db: Session = Depends(get_db)
):
    """
    Analyze a sample alert from the docs/skywind-4c-alerts-output directory.

    Provide the folder name (e.g., "200025_001373 - Comparison of monthly purchase volume by vendor")
    """
    try:
        # Look for the sample in known locations
        base_paths = [
            "/app/docs/skywind-4c-alerts-output/FI",
            "/app/docs/skywind-4c-alerts-output/MM",
            "docs/skywind-4c-alerts-output/FI",
            "docs/skywind-4c-alerts-output/MM",
        ]

        sample_path = None
        for base in base_paths:
            potential_path = os.path.join(base, sample_name)
            if os.path.exists(potential_path):
                sample_path = potential_path
                break

            # Also try partial matching
            if os.path.exists(base):
                for folder in os.listdir(base):
                    if sample_name in folder:
                        sample_path = os.path.join(base, folder)
                        break

            if sample_path:
                break

        if not sample_path:
            raise HTTPException(
                status_code=404,
                detail=f"Sample not found: {sample_name}. Check docs/skywind-4c-alerts-output/"
            )

        analyzer = get_content_analyzer()

        # Temporarily override LLM setting
        original_use_llm = analyzer.use_llm
        if not use_llm:
            analyzer.use_llm = False

        try:
            finding = analyzer.analyze_from_directory(sample_path, include_raw=True)
        finally:
            analyzer.use_llm = original_use_llm

        return FindingResponse(**finding.to_dict())

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@router.get("/samples")
async def list_samples():
    """
    List available sample alerts for testing.
    """
    samples = []
    base_paths = [
        ("/app/docs/skywind-4c-alerts-output/FI", "FI"),
        ("/app/docs/skywind-4c-alerts-output/MM", "MM"),
        ("docs/skywind-4c-alerts-output/FI", "FI"),
        ("docs/skywind-4c-alerts-output/MM", "MM"),
    ]

    for base_path, module in base_paths:
        if os.path.exists(base_path):
            for folder in os.listdir(base_path):
                full_path = os.path.join(base_path, folder)
                if os.path.isdir(full_path):
                    # List files in the folder
                    files = os.listdir(full_path) if os.path.exists(full_path) else []
                    samples.append({
                        "name": folder,
                        "module": module,
                        "path": full_path,
                        "files": files
                    })

    return {"samples": samples, "total": len(samples)}


@router.post("/feedback", response_model=FeedbackResponse)
async def submit_feedback(
    request: FeedbackRequest,
    db: Session = Depends(get_db)
):
    """
    Submit feedback on a finding for iterative improvement.

    This feedback will be used to improve the analyzer's accuracy over time.
    """
    try:
        # TODO: Store feedback in database for learning
        # For now, just log it
        logger.info(
            f"Feedback received for alert {request.alert_id}: "
            f"correct={request.is_correct}, "
            f"correct_focus_area={request.correct_focus_area}, "
            f"notes={request.feedback_notes}"
        )

        # In future: store in feedback table, use for prompt refinement

        return FeedbackResponse(
            status="received",
            message="Feedback recorded successfully. Thank you for helping improve the analyzer."
        )

    except Exception as e:
        logger.error(f"Feedback submission failed: {e}")
        raise HTTPException(status_code=500, detail=f"Feedback submission failed: {str(e)}")


@router.get("/status")
async def get_analyzer_status():
    """
    Get the current status of the Content Analyzer.
    """
    try:
        analyzer = get_content_analyzer()

        return {
            "status": "active",
            "use_llm": analyzer.use_llm,
            "llm_provider": analyzer.llm_classifier.llm_provider if analyzer.llm_classifier else None,
            "context_loaded": analyzer._context_loaded,
            "version": "1.0.0"
        }

    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }


# ============================================================================
# New Pipeline Endpoints
# ============================================================================

@router.post("/scan-folders", response_model=ScanFoldersResponse)
async def scan_folders(request: ScanFoldersRequest):
    """
    Scan for alert folders in a directory structure.

    Discovers 4C alert folders containing artifact files (Code_*, Explanation_*, etc.)
    Returns a list of folders ready for processing with analyze-batch.

    Default scans: docs/skywind-4c-alerts-output
    """
    try:
        folders = []
        root_path = request.root_path

        # Handle both absolute and relative paths
        if not os.path.isabs(root_path):
            # Try Docker path first, then local
            docker_path = f"/app/{root_path}"
            if os.path.exists(docker_path):
                root_path = docker_path
            elif not os.path.exists(root_path):
                raise HTTPException(status_code=404, detail=f"Path not found: {root_path}")

        if not os.path.exists(root_path):
            raise HTTPException(status_code=404, detail=f"Path not found: {root_path}")

        # Walk the directory tree to find alert folders
        for dirpath, dirnames, filenames in os.walk(root_path):
            # Check if this folder contains 4C artifacts
            has_code = any(f.lower().startswith("code_") for f in filenames)
            has_summary = any(f.lower().startswith("summary_") for f in filenames)
            has_explanation = any(f.lower().startswith("explanation_") for f in filenames)
            has_metadata = any(f.lower().startswith("metadata") for f in filenames)

            # Need at least Summary + one other artifact
            artifact_count = sum([has_code, has_summary, has_explanation, has_metadata])
            if has_summary and artifact_count >= 2:
                # Extract alert info from folder name
                folder_name = os.path.basename(dirpath)
                # Try to parse alert ID from folder name (e.g., "200025_001373 - Alert Name")
                import re
                alert_match = re.match(r'^(\d+_\d+)\s*-\s*(.+)$', folder_name)

                if alert_match:
                    alert_id = alert_match.group(1)
                    alert_name = alert_match.group(2)
                else:
                    alert_id = folder_name
                    alert_name = folder_name

                # Determine module from path
                module = _extract_module_from_path(dirpath)

                folders.append({
                    "path": dirpath,
                    "folder_name": folder_name,
                    "alert_id": alert_id,
                    "alert_name": alert_name,
                    "module": module,
                    "artifacts": {
                        "code": has_code,
                        "explanation": has_explanation,
                        "metadata": has_metadata,
                        "summary": has_summary
                    },
                    "files": filenames
                })

        return ScanFoldersResponse(
            folders=folders,
            total=len(folders)
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Scan folders failed: {e}")
        raise HTTPException(status_code=500, detail=f"Scan folders failed: {str(e)}")


@router.post("/analyze-batch", response_model=BatchJobResponse)
async def analyze_batch(
    request: AnalyzeBatchRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Start batch processing of multiple alert directories.

    Creates a background job to process all specified directories.
    Use batch-status/{job_id} to monitor progress.

    Args:
        directory_paths: List of paths to alert directories
        report_level: "summary" (no LLM) or "full" (LLM-generated)
    """
    try:
        job_id = str(uuid.uuid4())

        # Initialize job tracking
        _batch_jobs[job_id] = {
            "job_id": job_id,
            "status": "pending",
            "total": len(request.directory_paths),
            "processed": 0,
            "successful": 0,
            "failed": 0,
            "results": [],
            "started_at": datetime.utcnow().isoformat(),
            "completed_at": None,
            "report_level": request.report_level.value
        }

        # Start background processing
        background_tasks.add_task(
            _process_batch_job,
            job_id,
            request.directory_paths,
            request.report_level.value
        )

        return BatchJobResponse(
            job_id=job_id,
            total_alerts=len(request.directory_paths),
            status="pending",
            message=f"Batch job started. Processing {len(request.directory_paths)} alerts with {request.report_level.value} report level."
        )

    except Exception as e:
        logger.error(f"Failed to start batch job: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to start batch job: {str(e)}")


async def _process_batch_job(job_id: str, directory_paths: List[str], report_level: str):
    """Background task to process batch of alerts."""
    from app.core.database import SessionLocal

    job = _batch_jobs.get(job_id)
    if not job:
        return

    job["status"] = "processing"

    # Create a new database session for background task
    db = SessionLocal()

    try:
        analyzer = get_content_analyzer()
        artifact_reader = ArtifactReader()
        report_generator = ReportGenerator()

        use_llm = report_level == "full"
        original_use_llm = analyzer.use_llm
        analyzer.use_llm = use_llm

        for idx, directory_path in enumerate(directory_paths):
            result = {
                "path": directory_path,
                "status": "pending",
                "finding_id": None,
                "markdown_path": None,
                "error": None
            }

            try:
                if not os.path.exists(directory_path):
                    result["status"] = "failed"
                    result["error"] = f"Directory not found: {directory_path}"
                    job["failed"] += 1
                else:
                    # Read and analyze
                    artifacts = artifact_reader.read_from_directory(directory_path)
                    content_finding = analyzer.analyze_alert(artifacts, include_raw=False)

                    # Get or create focus area
                    focus_area = db.query(FocusArea).filter(
                        FocusArea.code == content_finding.focus_area
                    ).first()
                    if not focus_area:
                        focus_area = FocusArea(
                            code=content_finding.focus_area,
                            name=content_finding.focus_area.replace("_", " ").title(),
                            description=f"Auto-created for {content_finding.focus_area}"
                        )
                        db.add(focus_area)
                        db.flush()

                    # Get or create data source
                    data_source = db.query(DataSource).filter(
                        DataSource.original_filename == directory_path
                    ).first()
                    if not data_source:
                        dir_name = os.path.basename(directory_path.rstrip('/\\'))
                        data_source = DataSource(
                            filename=f"artifacts_{dir_name}",
                            original_filename=directory_path,
                            file_format=FileFormat.JSON,
                            data_type=DataSourceType.ALERT,
                            file_path=directory_path,
                            file_size=0,
                            status="processed"
                        )
                        db.add(data_source)
                        db.flush()

                    # Generate markdown report
                    markdown_path = None
                    try:
                        markdown_report = report_generator.generate_report(
                            artifacts=artifacts,
                            content_finding=content_finding,
                            report_level=report_level
                        )
                        markdown_path = report_generator.save_report(
                            report=markdown_report,
                            alert_id=content_finding.alert_id,
                            alert_name=content_finding.alert_name,
                            module=_extract_module_from_path(directory_path)
                        )
                    except Exception as e:
                        logger.warning(f"Failed to generate markdown for {directory_path}: {e}")

                    # Create finding
                    finding = Finding(
                        data_source_id=data_source.id,
                        focus_area_id=focus_area.id,
                        title=content_finding.title,
                        description=content_finding.description[:4000] if content_finding.description else None,
                        severity=content_finding.severity,
                        classification_confidence=content_finding.focus_area_confidence,
                        status="new"
                    )
                    db.add(finding)
                    db.flush()

                    # Create RiskAssessment
                    risk_assessment = RiskAssessment(
                        finding_id=finding.id,
                        risk_score=content_finding.risk_score,
                        risk_level=content_finding.risk_level,
                        risk_category=content_finding.focus_area,
                        risk_description=content_finding.severity_reasoning,
                        risk_factors=content_finding.risk_factors,
                        potential_impact=content_finding.business_impact
                    )
                    db.add(risk_assessment)

                    # Create MoneyLossCalculation
                    money_loss = MoneyLossCalculation(
                        finding_id=finding.id,
                        estimated_loss=content_finding.money_loss_estimate,
                        confidence_score=content_finding.money_loss_confidence,
                        calculation_method="content_analyzer",
                        final_estimate=content_finding.money_loss_estimate,
                        reasoning=f"Batch processed: {content_finding.alert_name}"
                    )
                    db.add(money_loss)

                    # Populate Alert Dashboard tables for batch processing
                    dashboard_result = _populate_dashboard_tables(
                        db=db,
                        content_finding=content_finding,
                        directory_path=directory_path,
                        finding_id=finding.id
                    )

                    db.commit()

                    result["status"] = "success"
                    result["finding_id"] = finding.id
                    result["markdown_path"] = markdown_path
                    result["alert_name"] = content_finding.alert_name
                    result["focus_area"] = content_finding.focus_area
                    result["severity"] = content_finding.severity
                    result["dashboard"] = dashboard_result
                    job["successful"] += 1

            except Exception as e:
                db.rollback()
                result["status"] = "failed"
                result["error"] = str(e)
                job["failed"] += 1
                logger.error(f"Failed to process {directory_path}: {e}")

            job["results"].append(result)
            job["processed"] = idx + 1

        # Restore LLM setting
        analyzer.use_llm = original_use_llm

        job["status"] = "completed"
        job["completed_at"] = datetime.utcnow().isoformat()

    except Exception as e:
        job["status"] = "failed"
        job["completed_at"] = datetime.utcnow().isoformat()
        logger.error(f"Batch job {job_id} failed: {e}")
    finally:
        db.close()


@router.get("/batch-status/{job_id}", response_model=BatchStatusResponse)
async def get_batch_status(job_id: str):
    """
    Get the status of a batch processing job.

    Returns progress information and results for each processed alert.
    """
    job = _batch_jobs.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail=f"Job not found: {job_id}")

    return BatchStatusResponse(
        job_id=job["job_id"],
        status=job["status"],
        total=job["total"],
        processed=job["processed"],
        successful=job["successful"],
        failed=job["failed"],
        results=job["results"],
        started_at=job["started_at"],
        completed_at=job["completed_at"]
    )


@router.get("/batch-jobs")
async def list_batch_jobs():
    """
    List all batch jobs (for debugging/monitoring).
    """
    jobs = []
    for job_id, job in _batch_jobs.items():
        jobs.append({
            "job_id": job_id,
            "status": job["status"],
            "total": job["total"],
            "processed": job["processed"],
            "successful": job["successful"],
            "failed": job["failed"],
            "started_at": job["started_at"],
            "completed_at": job["completed_at"]
        })
    return {"jobs": jobs, "total": len(jobs)}
