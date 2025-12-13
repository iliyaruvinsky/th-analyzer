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
from .artifact_reader import ArtifactReader, AlertArtifacts, SummaryData
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
        
        # Store focus area for use in fallback analysis
        self._last_classification_focus_area = classification.focus_area

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
        # Pass alert_name for type-based severity determination
        # Pass metadata for BACKDAYS normalization
        # Check metadata file first, then Code file for BACKDAYS
        metadata_dict = self._parse_metadata(artifacts.metadata) if artifacts.metadata else {}
        if "BACKDAYS" not in metadata_dict and artifacts.code:
            code_params = self._parse_metadata(artifacts.code)
            if "BACKDAYS" in code_params:
                metadata_dict["BACKDAYS"] = code_params["BACKDAYS"]

        combined_score = self.scoring_engine.calculate_score(
            focus_area=classification.focus_area,
            qualitative_data=analysis.qualitative_analysis,
            quantitative_data=analysis.quantitative_analysis,
            severity=analysis.severity,
            alert_name=artifacts.alert_name,
            metadata=metadata_dict
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
            affected_areas=analysis.qualitative_analysis.get("affected_areas", []) if analysis.qualitative_analysis.get("affected_areas") is not None else [],

            # Quantitative analysis
            total_count=combined_score.quantitative.total_count,
            monetary_amount=combined_score.quantitative.monetary_amount,
            currency=combined_score.quantitative.currency,
            key_metrics=combined_score.quantitative.key_metrics if combined_score.quantitative.key_metrics is not None else {},
            notable_items=combined_score.quantitative.notable_items if combined_score.quantitative.notable_items is not None else [],

            # Scoring - use severity from scoring engine (alert-type based) not fallback analysis
            severity=combined_score.qualitative.severity.value,
            severity_reasoning=combined_score.qualitative.severity_reasoning or analysis.severity_reasoning,
            risk_score=combined_score.risk_score,
            risk_level=combined_score.risk_level.value,
            risk_factors=combined_score.risk_factors if combined_score.risk_factors is not None else [],

            # Money loss
            money_loss_estimate=combined_score.money_loss_estimate,
            money_loss_confidence=combined_score.money_loss_confidence,

            # Recommendations
            recommended_actions=analysis.recommended_actions if analysis.recommended_actions is not None else [],
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

    def _parse_metadata(self, metadata_text: str) -> Dict[str, Any]:
        """
        Parse metadata text to extract key parameters like BACKDAYS.

        Args:
            metadata_text: Raw metadata text from Metadata_* file

        Returns:
            Dictionary with extracted parameters
        """
        import re

        result = {"raw_metadata": metadata_text}

        if not metadata_text:
            return result

        # Extract BACKDAYS parameter
        backdays_match = re.search(r'BACKDAYS\s*[=:]\s*(\d+)', metadata_text, re.IGNORECASE)
        if backdays_match:
            result["BACKDAYS"] = int(backdays_match.group(1))

        # Extract REPET_BACKDAYS (used in repetitive alerts)
        repet_match = re.search(r'REPET_BACKDAYS\s*[=:]\s*(\d+)', metadata_text, re.IGNORECASE)
        if repet_match:
            result["REPET_BACKDAYS"] = int(repet_match.group(1))

        # Extract other common parameters
        param_patterns = [
            (r'DURATION\s*[=:]\s*(\d+)', "DURATION"),
            (r'THRESHOLD\s*[=:]\s*([\d.]+)', "THRESHOLD"),
            (r'AMOUNT\s*[=:]\s*([\d,.]+)', "AMOUNT"),
        ]

        for pattern, key in param_patterns:
            match = re.search(pattern, metadata_text, re.IGNORECASE)
            if match:
                try:
                    result[key] = float(match.group(1).replace(',', ''))
                except ValueError:
                    pass

        return result

    def _fallback_classification(self, artifacts: AlertArtifacts) -> tuple:
        """Fallback classification when LLM is not available."""
        # Always use the LLMClassifier's weighted pattern matching
        # This works without an API key - it's the analyze_without_llm method
        classifier = LLMClassifier()  # No API key needed for pattern-based
        return classifier.analyze_without_llm(artifacts)

    def _extract_what_happened(self, explanation: Optional[str], alert_name: str) -> str:
        """Extract 'what_happened' from explanation file (first paragraph)."""
        if not explanation:
            return f"Alert triggered: {alert_name}"
        
        # Try to extract first paragraph or first few sentences
        lines = explanation.split('\n')
        first_paragraph = lines[0].strip() if lines else ""
        
        # If first line is too short, try to get more context
        if len(first_paragraph) < 50 and len(lines) > 1:
            first_paragraph = ' '.join(lines[:3]).strip()[:500]
        
        # Fallback to alert name if still empty
        return first_paragraph or f"Alert triggered: {alert_name}"

    def _extract_business_risk(self, explanation: Optional[str], alert_name: str) -> str:
        """Extract business risk indicators from explanation."""
        if not explanation:
            return "Requires review"
        
        explanation_lower = explanation.lower()
        
        # Look for risk indicators
        if any(word in explanation_lower for word in ["fraud", "theft", "unauthorized", "breach"]):
            return "Potential security or fraud risk - immediate review required"
        elif any(word in explanation_lower for word in ["revenue", "loss", "unbilled", "negative"]):
            return "Potential revenue or financial impact - prompt review recommended"
        elif any(word in explanation_lower for word in ["bottleneck", "stuck", "blocked", "delay"]):
            return "Process disruption - operational review needed"
        elif any(word in explanation_lower for word in ["violation", "compliance", "sod"]):
            return "Compliance concern - audit review needed"
        else:
            return "Requires review to assess business impact"

    def _extract_affected_areas(self, summary_data: Optional[SummaryData]) -> List[str]:
        """Identify affected areas from summary data columns."""
        affected_areas = []
        
        if not summary_data or not summary_data.columns:
            return affected_areas
        
        # Look for common entity columns
        entity_keywords = ["org", "organization", "entity", "customer", "vendor", "company", "division"]
        
        for col in summary_data.columns:
            col_name_lower = col.name.lower()
            for keyword in entity_keywords:
                if keyword in col_name_lower:
                    affected_areas.append(col.name)
                    break
        
        return affected_areas[:5]  # Limit to top 5

    def _extract_notable_items(self, summary_data, max_items: int = 5) -> List[Dict[str, Any]]:
        """Extract notable items from summary_data (top items by amount/value)."""
        notable_items = []
        
        if not summary_data or not summary_data.sample_rows:
            return notable_items
        
        # Try to find amount/value columns
        amount_columns = []
        entity_columns = []
        
        # Import ColumnType locally to avoid circular imports
        from app.services.content_analyzer.artifact_reader import ColumnType
        
        for col in summary_data.columns:
            col_name_lower = col.name.lower()
            if col.column_type in [ColumnType.CURRENCY, ColumnType.NUMERIC]:
                if any(keyword in col_name_lower for keyword in ["amount", "value", "total", "sum", "price"]):
                    amount_columns.append(col.name)
            elif any(keyword in col_name_lower for keyword in ["entity", "vendor", "customer", "org", "id"]):
                entity_columns.append(col.name)
        
        # Extract items with amounts
        items_with_amounts = []
        for row in summary_data.sample_rows:
            item = {}
            amount = 0.0
            
            # Get amount from first amount column found
            for amt_col in amount_columns:
                if amt_col in row:
                    try:
                        amount = float(row[amt_col]) if row[amt_col] else 0.0
                        item["amount"] = amount
                        break
                    except (ValueError, TypeError):
                        pass
            
            # Get entity identifier
            for ent_col in entity_columns:
                if ent_col in row and row[ent_col]:
                    item["entity"] = str(row[ent_col])
                    break
            
            # Include other relevant fields
            for key, value in row.items():
                if key not in amount_columns and value:
                    item[key] = str(value)[:100]  # Truncate long values
            
            if amount > 0 or item.get("entity"):
                items_with_amounts.append((item, amount))
        
        # Sort by amount (descending) and take top N
        items_with_amounts.sort(key=lambda x: x[1], reverse=True)
        
        total_amount = summary_data.total_amount or 0.0
        
        for item, amount in items_with_amounts[:max_items]:
            notable_item = {
                "title": item.get("entity", item.get("title", "Item")),
                "description": f"Amount: {amount:,.2f}" if amount > 0 else "Item flagged",
                "amount": amount,
                "percentage_of_total": (amount / total_amount * 100) if total_amount > 0 else 0.0
            }
            notable_items.append(notable_item)
        
        return notable_items

    def _detect_concentration_patterns(self, summary_data: SummaryData) -> List[str]:
        """
        Detect concentration patterns (>50% by entity).
        
        Returns list of concentration violation descriptions.
        """
        violations = []
        
        if not summary_data or not summary_data.sample_rows:
            return violations
        
        # Find entity and amount columns
        amount_columns = []
        entity_columns = []
        
        from app.services.content_analyzer.artifact_reader import ColumnType
        
        for col in summary_data.columns:
            col_name_lower = col.name.lower()
            if col.column_type in [ColumnType.CURRENCY, ColumnType.NUMERIC]:
                if any(keyword in col_name_lower for keyword in ["amount", "value", "total", "sum", "price"]):
                    amount_columns.append(col.name)
            elif any(keyword in col_name_lower for keyword in ["entity", "vendor", "customer", "org", "company"]):
                entity_columns.append(col.name)
        
        if not amount_columns or not entity_columns:
            return violations
        
        # Group by entity and calculate totals
        entity_totals = {}
        total_amount = summary_data.total_amount or 0.0
        
        for row in summary_data.sample_rows:
            entity = None
            amount = 0.0
            
            # Get entity identifier
            for ent_col in entity_columns:
                if ent_col in row and row[ent_col]:
                    entity = str(row[ent_col])
                    break
            
            # Get amount
            for amt_col in amount_columns:
                if amt_col in row:
                    try:
                        amount = float(row[amt_col]) if row[amt_col] else 0.0
                        break
                    except (ValueError, TypeError):
                        pass
            
            if entity and amount > 0:
                if entity not in entity_totals:
                    entity_totals[entity] = 0.0
                entity_totals[entity] += amount
        
        # Check for >50% concentrations
        if total_amount > 0:
            for entity, entity_total in entity_totals.items():
                percentage = (entity_total / total_amount) * 100
                if percentage > 50:
                    violations.append(f"{entity}: {percentage:.1f}% of total ({entity_total:,.2f})")
        
        return violations[:5]  # Limit to top 5

    def _detect_threshold_violations(
        self, 
        summary_data: Optional[SummaryData], 
        total_count: int, 
        monetary_amount: float
    ) -> List[str]:
        """
        Detect threshold violations (concentrations, anomalies, high counts/amounts).
        
        Returns list of threshold violation descriptions.
        """
        violations = []
        
        # High count threshold
        if total_count >= 1000:
            violations.append(f"High volume: {total_count:,} records")
        elif total_count >= 500:
            violations.append(f"Elevated volume: {total_count:,} records")
        
        # High monetary amount threshold
        if monetary_amount >= 1000000:
            violations.append(f"High financial exposure: ${monetary_amount:,.2f}")
        elif monetary_amount >= 100000:
            violations.append(f"Significant financial exposure: ${monetary_amount:,.2f}")
        
        # Concentration violations from summary_data
        if summary_data:
            concentration_violations = self._detect_concentration_patterns(summary_data)
            violations.extend(concentration_violations)
        
        return violations

    def _calculate_key_metrics(self, summary_data: Optional[SummaryData]) -> Dict[str, Any]:
        """Calculate key metrics from summary data."""
        metrics = {}
        
        if not summary_data:
            return metrics
        
        # Basic metrics
        if summary_data.row_count is not None:
            metrics["total_records"] = summary_data.row_count
        
        if summary_data.total_amount is not None:
            metrics["total_amount"] = summary_data.total_amount
            if summary_data.currency:
                metrics["currency"] = summary_data.currency
        
        if summary_data.total_count is not None:
            metrics["total_count"] = summary_data.total_count
        
        # Calculate averages if we have both amount and count
        if summary_data.total_amount and summary_data.row_count and summary_data.row_count > 0:
            metrics["average_amount"] = summary_data.total_amount / summary_data.row_count
        
        # Extract metrics from key metric columns
        for col in summary_data.columns:
            if col.is_key_metric:
                if col.total is not None:
                    metrics[f"{col.name}_total"] = col.total
                if col.avg_value is not None:
                    metrics[f"{col.name}_average"] = col.avg_value
                if col.max_value is not None:
                    metrics[f"{col.name}_max"] = col.max_value
        
        return metrics

    def _fallback_analysis(self, artifacts: AlertArtifacts) -> AnalysisResult:
        """Fallback analysis when LLM is not available."""
        # IMPORTANT: Quantitative data (counts, monetary amounts) comes ONLY from Summary_* file
        # The other 3 files (Code, Explanation, Metadata) provide CONTEXT only:
        # - Code_* = technical implementation
        # - Explanation_* = business meaning (may contain template/example numbers - DO NOT USE)
        # - Metadata_* = parameters like BACKDAYS

        # Use structured data if available, otherwise fall back to text extraction
        if artifacts.summary_data:
            # Use structured summary data
            summary_data = artifacts.summary_data
            total_count = summary_data.row_count or 0
            monetary_amount = summary_data.total_amount or 0.0
            
            # Extract notable items
            notable_items = self._extract_notable_items(summary_data, max_items=5)
            
            # Calculate key metrics
            key_metrics = self._calculate_key_metrics(summary_data)
            
            # Extract affected areas
            affected_areas = self._extract_affected_areas(summary_data)
            
            # Detect threshold violations (includes concentration patterns)
            threshold_violations = self._detect_threshold_violations(summary_data, total_count, monetary_amount)
        else:
            # Fall back to text extraction
            all_counts = []
            all_monetary = []
            
            if artifacts.summary:
                metrics = self.scoring_engine.extract_metrics_from_text(artifacts.summary)
                all_counts.extend(metrics.get("counts", []))
                all_monetary.extend(metrics.get("monetary_values", []))
            
            total_count = max(all_counts) if all_counts else 0
            monetary_amount = max((m["amount"] for m in all_monetary), default=0.0)
            notable_items = []
            key_metrics = {}
            affected_areas = []
            threshold_violations = []

        # Extract qualitative analysis from explanation
        what_happened = self._extract_what_happened(artifacts.explanation, artifacts.alert_name)
        business_risk = self._extract_business_risk(artifacts.explanation, artifacts.alert_name)
        
        # Determine severity using scoring engine
        # Get focus area from classification result (stored during analyze_alert)
        # If not available, try to classify from alert name
        focus_area = getattr(self, '_last_classification_focus_area', None)
        if not focus_area:
            # Try simple classification from alert name
            alert_lower = artifacts.alert_name.lower()
            if any(word in alert_lower for word in ["fraud", "security", "unauthorized", "vendor.*bank"]):
                focus_area = "BUSINESS_PROTECTION"
            elif any(word in alert_lower for word in ["bottleneck", "unbilled", "stuck", "delay"]):
                focus_area = "BUSINESS_CONTROL"
            else:
                focus_area = "BUSINESS_CONTROL"  # Default
        
        severity_level, severity_reasoning = self.scoring_engine.determine_severity_from_alert_type(
            alert_name=artifacts.alert_name,
            focus_area=focus_area,
            explanation=artifacts.explanation or "",
            code_summary=artifacts.code_summary or ""
        )
        
        # Enhance severity reasoning with quantitative factors and threshold violations
        reasoning_parts = []
        if total_count > 0:
            reasoning_parts.append(f"{total_count:,} records")
        if monetary_amount > 0:
            reasoning_parts.append(f"${monetary_amount:,.2f}")
        if threshold_violations:
            reasoning_parts.append(f"{len(threshold_violations)} threshold violation(s)")
        
        if reasoning_parts:
            severity_reasoning += f" - Quantitative factors: {', '.join(reasoning_parts)}"
        
        # Generate recommended actions based on severity
        recommended_actions = []
        if severity_level.value == "Critical":
            recommended_actions = [
                "Immediate review required - critical issue detected",
                "Notify stakeholders immediately",
                "Investigate root cause"
            ]
        elif severity_level.value == "High":
            recommended_actions = [
                "Prompt review required - high priority issue",
                "Verify data accuracy",
                "Assess business impact"
            ]
        elif severity_level.value == "Medium":
            recommended_actions = [
                "Review alert details",
                "Verify data accuracy",
                "Document findings"
            ]
        else:
            recommended_actions = [
                "Monitor for trends",
                "Review periodically"
            ]

        return AnalysisResult(
            findings_summary=artifacts.explanation or f"Alert: {artifacts.alert_name}",
            qualitative_analysis={
                "what_happened": what_happened,
                "business_risk": business_risk,
                "affected_areas": affected_areas
            },
            quantitative_analysis={
                "total_count": total_count,
                "monetary_amount": monetary_amount,
                "key_metrics": key_metrics,
                "notable_items": notable_items,
                "threshold_violations": threshold_violations
            },
            severity=severity_level.value,
            severity_reasoning=severity_reasoning,
            recommended_actions=recommended_actions
        )

    def _fallback_risk_score(self, analysis: AnalysisResult) -> RiskScore:
        """Fallback risk scoring when LLM is not available."""
        # Severity scores per BUSINESS_PROTECTION.md
        severity_scores = {
            "Critical": 90,
            "High": 75,
            "Medium": 60,
            "Low": 50
        }
        base_score = severity_scores.get(analysis.severity, 60)

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

    def _validate_content_finding(self, content_finding: ContentFinding) -> tuple[bool, list[str]]:
        """
        Validate that a ContentFinding has all required fields populated.
        
        This function checks:
        - AlertInstance required fields: alert_id, alert_name, focus_area, business_purpose
        - AlertAnalysis required fields: severity, risk_score, records_affected (total_count)
        - CriticalDiscovery creation: at least one notable_item or description available
        
        Returns:
            Tuple of (is_valid, list_of_warnings)
        """
        warnings = []
        
        # Validate AlertInstance fields
        if not content_finding.alert_id:
            warnings.append("AlertInstance.alert_id is missing")
        elif not isinstance(content_finding.alert_id, str) or len(content_finding.alert_id.strip()) == 0:
            warnings.append(f"AlertInstance.alert_id is invalid: {content_finding.alert_id}")
        
        if not content_finding.alert_name:
            warnings.append("AlertInstance.alert_name is missing")
        elif not isinstance(content_finding.alert_name, str) or len(content_finding.alert_name.strip()) == 0:
            warnings.append(f"AlertInstance.alert_name is invalid: {content_finding.alert_name}")
        
        if not content_finding.focus_area:
            warnings.append("AlertInstance.focus_area is missing")
        elif not isinstance(content_finding.focus_area, str) or len(content_finding.focus_area.strip()) == 0:
            warnings.append(f"AlertInstance.focus_area is invalid: {content_finding.focus_area}")
        
        # Validate business_purpose (can come from business_impact, description, or alert_name)
        has_business_purpose = bool(
            content_finding.business_impact or 
            content_finding.description or 
            content_finding.alert_name
        )
        if not has_business_purpose:
            warnings.append("AlertInstance.business_purpose cannot be derived (no business_impact, description, or alert_name)")
        
        # Validate AlertAnalysis fields
        if not content_finding.severity:
            warnings.append("AlertAnalysis.severity is missing")
        elif content_finding.severity.upper() not in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
            warnings.append(f"AlertAnalysis.severity is invalid: {content_finding.severity}")
        
        if content_finding.risk_score is None:
            warnings.append("AlertAnalysis.risk_score is missing")
        elif not isinstance(content_finding.risk_score, (int, float)):
            warnings.append(f"AlertAnalysis.risk_score is not numeric: {content_finding.risk_score}")
        elif content_finding.risk_score < 0 or content_finding.risk_score > 100:
            warnings.append(f"AlertAnalysis.risk_score is out of range (0-100): {content_finding.risk_score}")
        
        # Validate records_affected (total_count)
        if content_finding.total_count is None:
            warnings.append("AlertAnalysis.records_affected (total_count) is missing")
        elif not isinstance(content_finding.total_count, (int, float)):
            warnings.append(f"AlertAnalysis.records_affected (total_count) is not numeric: {content_finding.total_count}")
        elif content_finding.total_count < 0:
            warnings.append(f"AlertAnalysis.records_affected (total_count) is negative: {content_finding.total_count}")
        
        # Validate CriticalDiscovery creation requirement
        # At least one notable_item or description/business_impact must be available
        has_notable_items = bool(content_finding.notable_items and len(content_finding.notable_items) > 0)
        has_description = bool(content_finding.description or content_finding.business_impact)
        has_title = bool(content_finding.title)
        if not has_notable_items and not has_description and not has_title:
            warnings.append("CriticalDiscovery creation: No notable_items, description, business_impact, or title available")
        
        # Validate JSON fields are dicts, not None
        if content_finding.key_metrics is None:
            warnings.append("key_metrics is None (should be dict)")
        elif not isinstance(content_finding.key_metrics, dict):
            warnings.append(f"key_metrics is not a dict: {type(content_finding.key_metrics)}")
        
        if content_finding.notable_items is None:
            warnings.append("notable_items is None (should be list)")
        elif not isinstance(content_finding.notable_items, list):
            warnings.append(f"notable_items is not a list: {type(content_finding.notable_items)}")
        
        if content_finding.risk_factors is None:
            warnings.append("risk_factors is None (should be list)")
        elif not isinstance(content_finding.risk_factors, list):
            warnings.append(f"risk_factors is not a list: {type(content_finding.risk_factors)}")
        
        if content_finding.recommended_actions is None:
            warnings.append("recommended_actions is None (should be list)")
        elif not isinstance(content_finding.recommended_actions, list):
            warnings.append(f"recommended_actions is not a list: {type(content_finding.recommended_actions)}")
        
        # Log warnings if any
        if warnings:
            logger.warning(f"ContentFinding validation warnings for alert {content_finding.alert_id}: {', '.join(warnings)}")
        
        is_valid = len(warnings) == 0
        return is_valid, warnings

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
