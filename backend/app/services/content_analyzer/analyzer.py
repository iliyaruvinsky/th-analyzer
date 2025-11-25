"""
Content Analyzer - Main Orchestrator

This is the main entry point for content analysis in THA.
It orchestrates the context loading, artifact reading, LLM classification,
and scoring to produce comprehensive findings.
"""

import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field, asdict
from datetime import datetime

from .context_loader import ContextLoader, get_context_loader
from .artifact_reader import ArtifactReader, AlertArtifacts
from .llm_classifier import LLMClassifier, ClassificationResult, AnalysisResult, RiskScore
from .scoring_engine import ScoringEngine, CombinedScore, SeverityLevel, RiskLevel

logger = logging.getLogger(__name__)


@dataclass
class ContentFinding:
    """
    A complete finding produced by the Content Analyzer.

    This represents a single issue/finding extracted from an alert,
    with full classification, analysis, and scoring.
    """
    # Identification
    alert_id: str
    alert_name: str

    # Classification
    focus_area: str
    focus_area_confidence: float
    classification_reasoning: str

    # Finding details
    title: str
    description: str
    business_impact: str

    # Qualitative analysis
    what_happened: str
    business_risk: str
    affected_areas: List[str]

    # Quantitative analysis
    total_count: int
    monetary_amount: float
    currency: str
    key_metrics: Dict[str, Any]
    notable_items: List[Dict[str, Any]]

    # Scoring
    severity: str
    severity_reasoning: str
    risk_score: int
    risk_level: str
    risk_factors: List[str]

    # Money loss
    money_loss_estimate: float
    money_loss_confidence: float

    # Recommendations
    recommended_actions: List[str]

    # Metadata
    analyzed_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    analysis_version: str = "1.0.0"

    # Raw data for debugging/feedback
    raw_analysis: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API responses."""
        return asdict(self)


class ContentAnalyzer:
    """
    Main Content Analyzer for Treasure Hunt Analyzer.

    This class orchestrates the full analysis pipeline:
    1. Load contextual knowledge (TH principles)
    2. Read alert artifacts (Code, Explanation, Metadata, Summary)
    3. Classify into focus area using LLM
    4. Analyze summary data for findings
    5. Score findings (qualitative + quantitative)
    6. Generate human-readable descriptions

    Usage:
        analyzer = ContentAnalyzer(llm_provider="openai", api_key="...")
        findings = analyzer.analyze_alert(artifacts)
    """

    def __init__(
        self,
        llm_provider: str = "openai",
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        use_llm: bool = True,
        context_loader: Optional[ContextLoader] = None
    ):
        """
        Initialize the Content Analyzer.

        Args:
            llm_provider: "openai" or "anthropic"
            api_key: API key for LLM provider
            model: Specific model to use
            use_llm: Whether to use LLM (if False, uses pattern-based fallback)
            context_loader: Optional custom context loader
        """
        self.use_llm = use_llm
        self.context_loader = context_loader or get_context_loader()
        self.artifact_reader = ArtifactReader()
        self.scoring_engine = ScoringEngine()

        if use_llm:
            self.llm_classifier = LLMClassifier(
                llm_provider=llm_provider,
                api_key=api_key,
                model=model,
                context_loader=self.context_loader
            )
        else:
            self.llm_classifier = None

        # Load context on initialization
        self._context_loaded = False

    def _ensure_context_loaded(self):
        """Ensure TH context is loaded."""
        if not self._context_loaded:
            self.context_loader.load_all_context()
            self._context_loaded = True

    def analyze_alert(
        self,
        artifacts: AlertArtifacts,
        include_raw: bool = False
    ) -> ContentFinding:
        """
        Analyze a single alert and produce a finding.

        Args:
            artifacts: The alert artifacts to analyze
            include_raw: Whether to include raw LLM responses

        Returns:
            ContentFinding with full analysis
        """
        self._ensure_context_loaded()

        logger.info(f"Analyzing alert: {artifacts.alert_name} ({artifacts.alert_id})")

        # Step 1: Classify into focus area
        if self.use_llm and self.llm_classifier:
            classification = self.llm_classifier.classify_focus_area(artifacts)
        else:
            focus_area, confidence, reasoning = self._fallback_classification(artifacts)
            classification = ClassificationResult(
                focus_area=focus_area,
                confidence=confidence,
                reasoning=reasoning
            )

        logger.info(f"Classified as: {classification.focus_area} (confidence: {classification.confidence})")

        # Step 2: Analyze summary data
        if self.use_llm and self.llm_classifier:
            analysis = self.llm_classifier.analyze_summary(artifacts, classification.focus_area)
        else:
            analysis = self._fallback_analysis(artifacts)

        # Step 3: Calculate risk score
        if self.use_llm and self.llm_classifier:
            risk = self.llm_classifier.calculate_risk_score(
                artifacts, classification.focus_area, analysis
            )
        else:
            risk = self._fallback_risk_score(analysis)

        # Step 4: Generate finding description
        if self.use_llm and self.llm_classifier:
            description = self.llm_classifier.generate_finding_description(
                artifacts, classification.focus_area, analysis
            )
        else:
            description = self._fallback_description(artifacts, analysis)

        # Step 5: Calculate combined score
        combined_score = self.scoring_engine.calculate_score(
            focus_area=classification.focus_area,
            qualitative_data=analysis.qualitative_analysis,
            quantitative_data=analysis.quantitative_analysis,
            severity=analysis.severity
        )

        # Build the finding
        finding = ContentFinding(
            # Identification
            alert_id=artifacts.alert_id,
            alert_name=artifacts.alert_name,

            # Classification
            focus_area=classification.focus_area,
            focus_area_confidence=classification.confidence,
            classification_reasoning=classification.reasoning,

            # Finding details
            title=description.get("title", artifacts.alert_name),
            description=description.get("description", analysis.findings_summary),
            business_impact=description.get("business_impact", ""),

            # Qualitative analysis
            what_happened=analysis.qualitative_analysis.get("what_happened", ""),
            business_risk=analysis.qualitative_analysis.get("business_risk", ""),
            affected_areas=analysis.qualitative_analysis.get("affected_areas", []),

            # Quantitative analysis
            total_count=combined_score.quantitative.total_count,
            monetary_amount=combined_score.quantitative.monetary_amount,
            currency=combined_score.quantitative.currency,
            key_metrics=combined_score.quantitative.key_metrics,
            notable_items=combined_score.quantitative.notable_items,

            # Scoring
            severity=analysis.severity,
            severity_reasoning=analysis.severity_reasoning,
            risk_score=combined_score.risk_score,
            risk_level=combined_score.risk_level.value,
            risk_factors=combined_score.risk_factors,

            # Money loss
            money_loss_estimate=combined_score.money_loss_estimate,
            money_loss_confidence=combined_score.money_loss_confidence,

            # Recommendations
            recommended_actions=analysis.recommended_actions,
        )

        # Include raw data if requested
        if include_raw:
            finding.raw_analysis = {
                "classification": asdict(classification) if hasattr(classification, '__dataclass_fields__') else vars(classification),
                "analysis": asdict(analysis) if hasattr(analysis, '__dataclass_fields__') else vars(analysis),
                "risk": asdict(risk) if hasattr(risk, '__dataclass_fields__') else vars(risk),
                "scoring_breakdown": combined_score.scoring_breakdown
            }

        logger.info(f"Analysis complete. Risk score: {finding.risk_score}, Focus area: {finding.focus_area}")

        return finding

    def analyze_from_directory(
        self,
        directory_path: str,
        include_raw: bool = False
    ) -> ContentFinding:
        """
        Analyze an alert from a directory containing artifact files.

        Args:
            directory_path: Path to directory with Code/Explanation/Metadata/Summary files
            include_raw: Whether to include raw LLM responses

        Returns:
            ContentFinding with full analysis
        """
        artifacts = self.artifact_reader.read_from_directory(directory_path)
        return self.analyze_alert(artifacts, include_raw=include_raw)

    def analyze_multiple(
        self,
        artifacts_list: List[AlertArtifacts],
        include_raw: bool = False
    ) -> List[ContentFinding]:
        """
        Analyze multiple alerts.

        Args:
            artifacts_list: List of AlertArtifacts to analyze
            include_raw: Whether to include raw LLM responses

        Returns:
            List of ContentFinding objects
        """
        findings = []
        for artifacts in artifacts_list:
            try:
                finding = self.analyze_alert(artifacts, include_raw=include_raw)
                findings.append(finding)
            except Exception as e:
                logger.error(f"Failed to analyze {artifacts.alert_name}: {e}")
                # Create a minimal finding for failed analyses
                findings.append(self._create_error_finding(artifacts, str(e)))

        return findings

    def _fallback_classification(self, artifacts: AlertArtifacts) -> tuple:
        """Fallback classification when LLM is not available."""
        if self.llm_classifier:
            return self.llm_classifier.analyze_without_llm(artifacts)

        # Simple keyword-based classification
        text = f"{artifacts.alert_name} {artifacts.explanation or ''}"
        text_lower = text.lower()

        if any(kw in text_lower for kw in ["fraud", "security", "unauthorized", "suspicious"]):
            return "BUSINESS_PROTECTION", 0.6, "Keyword match: security/fraud terms"
        elif any(kw in text_lower for kw in ["sod", "segregation", "access", "privilege", "authorization"]):
            return "ACCESS_GOVERNANCE", 0.6, "Keyword match: access/governance terms"
        elif any(kw in text_lower for kw in ["job", "batch", "background", "scheduled"]):
            return "JOBS_CONTROL", 0.6, "Keyword match: job-related terms"
        elif any(kw in text_lower for kw in ["dump", "memory", "cpu", "system", "error"]):
            return "TECHNICAL_CONTROL", 0.6, "Keyword match: technical terms"
        else:
            return "BUSINESS_CONTROL", 0.4, "Default classification"

    def _fallback_analysis(self, artifacts: AlertArtifacts) -> AnalysisResult:
        """Fallback analysis when LLM is not available."""
        # Extract metrics from summary if available
        metrics = {}
        if artifacts.summary:
            metrics = self.scoring_engine.extract_metrics_from_text(artifacts.summary)

        total_count = max(metrics.get("counts", [0]))
        monetary = metrics.get("monetary_values", [])
        monetary_amount = monetary[0]["amount"] if monetary else 0.0

        return AnalysisResult(
            findings_summary=artifacts.explanation or f"Alert: {artifacts.alert_name}",
            qualitative_analysis={
                "what_happened": f"Alert triggered: {artifacts.alert_name}",
                "business_risk": "Requires review",
                "affected_areas": []
            },
            quantitative_analysis={
                "total_count": total_count,
                "key_metrics": {},
                "notable_items": []
            },
            severity="Medium",
            severity_reasoning="Default severity - manual review recommended",
            recommended_actions=["Review alert details", "Verify data accuracy"]
        )

    def _fallback_risk_score(self, analysis: AnalysisResult) -> RiskScore:
        """Fallback risk scoring when LLM is not available."""
        severity_scores = {
            "Critical": 80,
            "High": 60,
            "Medium": 40,
            "Low": 20
        }
        base_score = severity_scores.get(analysis.severity, 40)

        return RiskScore(
            risk_score=base_score,
            risk_level=analysis.severity,
            risk_factors=["Automated assessment"],
            potential_financial_impact={}
        )

    def _fallback_description(
        self,
        artifacts: AlertArtifacts,
        analysis: AnalysisResult
    ) -> Dict[str, str]:
        """Fallback description generation when LLM is not available."""
        return {
            "title": artifacts.alert_name,
            "description": analysis.findings_summary,
            "business_impact": "Review required to assess business impact",
            "technical_details": artifacts.code_summary or ""
        }

    def _create_error_finding(self, artifacts: AlertArtifacts, error: str) -> ContentFinding:
        """Create a finding for failed analyses."""
        return ContentFinding(
            alert_id=artifacts.alert_id,
            alert_name=artifacts.alert_name,
            focus_area="BUSINESS_CONTROL",
            focus_area_confidence=0.0,
            classification_reasoning=f"Analysis failed: {error}",
            title=f"Error analyzing: {artifacts.alert_name}",
            description=f"Analysis failed with error: {error}",
            business_impact="Unable to assess - manual review required",
            what_happened="Analysis error occurred",
            business_risk="Unknown",
            affected_areas=[],
            total_count=0,
            monetary_amount=0.0,
            currency="USD",
            key_metrics={},
            notable_items=[],
            severity="Medium",
            severity_reasoning="Default severity due to analysis error",
            risk_score=50,
            risk_level="Medium",
            risk_factors=["Analysis failed - manual review required"],
            money_loss_estimate=0.0,
            money_loss_confidence=0.0,
            recommended_actions=["Manual review required", "Check alert data integrity"]
        )


def create_content_analyzer(
    llm_provider: Optional[str] = None,
    api_key: Optional[str] = None,
    use_llm: bool = True
) -> ContentAnalyzer:
    """
    Factory function to create a ContentAnalyzer with configuration.

    Automatically reads configuration from environment if not provided.

    Args:
        llm_provider: "openai" or "anthropic" (default: from env)
        api_key: API key (default: from env)
        use_llm: Whether to use LLM

    Returns:
        Configured ContentAnalyzer instance
    """
    import os

    # Get provider from env if not specified
    if llm_provider is None:
        llm_provider = os.environ.get("LLM_PROVIDER", "openai")

    # Get API key from env if not specified
    if api_key is None:
        if llm_provider == "anthropic":
            api_key = os.environ.get("ANTHROPIC_API_KEY")
        else:
            api_key = os.environ.get("OPENAI_API_KEY")

    # Disable LLM if no API key available
    if not api_key:
        logger.warning("No API key found, disabling LLM-based analysis")
        use_llm = False

    return ContentAnalyzer(
        llm_provider=llm_provider,
        api_key=api_key,
        use_llm=use_llm
    )
