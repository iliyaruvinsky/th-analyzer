"""
Content Analysis API Endpoints

Provides endpoints for the new intelligent Content Analyzer.
These endpoints allow testing and iterating on the analysis logic.
"""

from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
import os
import logging

from app.core.database import get_db
from app.core.config import settings
from app.services.content_analyzer import ContentAnalyzer, create_content_analyzer
from app.services.content_analyzer.artifact_reader import ArtifactReader, AlertArtifacts

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/content-analysis", tags=["Content Analysis"])


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
