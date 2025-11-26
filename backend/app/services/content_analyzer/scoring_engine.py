"""
Scoring Engine for Treasure Hunt Analyzer

Implements qualitative and quantitative scoring for findings.
Combines LLM analysis with rule-based calculations for comprehensive risk assessment.
"""

import re
import logging
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum

logger = logging.getLogger(__name__)


class SeverityLevel(Enum):
    """Severity levels for findings."""
    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


class RiskLevel(Enum):
    """Risk levels based on score."""
    CRITICAL = "Critical"  # 76-100
    HIGH = "High"          # 51-75
    MEDIUM = "Medium"      # 26-50
    LOW = "Low"            # 0-25


@dataclass
class QualitativeScore:
    """Qualitative analysis result."""
    what_happened: str
    business_risk: str
    affected_areas: List[str]
    severity: SeverityLevel
    severity_reasoning: str


@dataclass
class QuantitativeScore:
    """Quantitative analysis result."""
    total_count: int
    monetary_amount: float
    currency: str
    key_metrics: Dict[str, Any]
    notable_items: List[Dict[str, Any]]
    threshold_violations: List[str]


@dataclass
class CombinedScore:
    """Combined qualitative and quantitative score."""
    risk_score: int  # 0-100
    risk_level: RiskLevel
    qualitative: QualitativeScore
    quantitative: QuantitativeScore
    money_loss_estimate: float
    money_loss_confidence: float
    risk_factors: List[str]
    scoring_breakdown: Dict[str, int]


class ScoringEngine:
    """
    Engine for scoring findings based on qualitative and quantitative analysis.

    Scoring Methodology:
    - Base score from severity (25-100)
    - Adjustments for quantitative factors (+/- 20)
    - Adjustments for focus area specific risks (+/- 15)
    - Final score capped at 0-100
    """

    # Base scores by severity
    SEVERITY_BASE_SCORES = {
        SeverityLevel.CRITICAL: 85,
        SeverityLevel.HIGH: 65,
        SeverityLevel.MEDIUM: 45,
        SeverityLevel.LOW: 25,
    }

    # Focus area risk multipliers
    FOCUS_AREA_MULTIPLIERS = {
        "BUSINESS_PROTECTION": 1.2,  # Higher risk - fraud/security
        "BUSINESS_CONTROL": 1.0,     # Standard business risk
        "ACCESS_GOVERNANCE": 1.15,   # Compliance risk
        "TECHNICAL_CONTROL": 0.9,    # Technical issues
        "JOBS_CONTROL": 0.85,        # Operational issues
    }

    # Thresholds for quantitative scoring adjustments
    COUNT_THRESHOLDS = {
        "critical": 1000,  # +15 points
        "high": 500,       # +10 points
        "medium": 100,     # +5 points
        "low": 10,         # +0 points
    }

    MONEY_THRESHOLDS = {
        "critical": 1000000,  # +20 points for $1M+
        "high": 100000,       # +15 points for $100K+
        "medium": 10000,      # +10 points for $10K+
        "low": 1000,          # +5 points for $1K+
    }

    def __init__(self):
        self._currency_patterns = self._build_currency_patterns()

    def _build_currency_patterns(self) -> List[Tuple[str, str]]:
        """Build regex patterns for extracting monetary values."""
        return [
            (r'\$\s*([\d,]+(?:\.\d{2})?)\s*([KkMmBb])?', 'USD'),
            (r'USD\s*([\d,]+(?:\.\d{2})?)\s*([KkMmBb])?', 'USD'),
            (r'EUR\s*([\d,]+(?:\.\d{2})?)\s*([KkMmBb])?', 'EUR'),
            (r'([\d,]+(?:\.\d{2})?)\s*(?:dollars?|USD)', 'USD'),
        ]

    def calculate_score(
        self,
        focus_area: str,
        qualitative_data: Dict[str, Any],
        quantitative_data: Dict[str, Any],
        severity: str = "Medium"
    ) -> CombinedScore:
        """
        Calculate combined score from qualitative and quantitative data.

        Args:
            focus_area: The focus area classification
            qualitative_data: Qualitative analysis from LLM
            quantitative_data: Quantitative analysis from LLM
            severity: Severity level string

        Returns:
            CombinedScore with detailed breakdown
        """
        # Parse severity
        severity_level = self._parse_severity(severity)

        # Build qualitative score
        qualitative = self._build_qualitative_score(qualitative_data, severity_level)

        # Build quantitative score
        quantitative = self._build_quantitative_score(quantitative_data)

        # Calculate risk score
        scoring_breakdown, risk_score = self._calculate_risk_score(
            focus_area, severity_level, quantitative
        )

        # Determine risk level
        risk_level = self._score_to_risk_level(risk_score)

        # Calculate money loss estimate
        money_loss, money_loss_confidence = self._estimate_money_loss(
            focus_area, quantitative, qualitative
        )

        # Compile risk factors
        risk_factors = self._compile_risk_factors(
            focus_area, qualitative, quantitative
        )

        return CombinedScore(
            risk_score=risk_score,
            risk_level=risk_level,
            qualitative=qualitative,
            quantitative=quantitative,
            money_loss_estimate=money_loss,
            money_loss_confidence=money_loss_confidence,
            risk_factors=risk_factors,
            scoring_breakdown=scoring_breakdown
        )

    def _parse_severity(self, severity: str) -> SeverityLevel:
        """Parse severity string to enum."""
        severity_map = {
            "critical": SeverityLevel.CRITICAL,
            "high": SeverityLevel.HIGH,
            "medium": SeverityLevel.MEDIUM,
            "low": SeverityLevel.LOW,
        }
        return severity_map.get(severity.lower(), SeverityLevel.MEDIUM)

    def _build_qualitative_score(
        self,
        data: Dict[str, Any],
        severity: SeverityLevel
    ) -> QualitativeScore:
        """Build qualitative score from LLM analysis data."""
        return QualitativeScore(
            what_happened=data.get("what_happened", "Event detected"),
            business_risk=data.get("business_risk", "Potential business impact"),
            affected_areas=data.get("affected_areas", []),
            severity=severity,
            severity_reasoning=data.get("severity_reasoning", "")
        )

    def _build_quantitative_score(self, data: Dict[str, Any]) -> QuantitativeScore:
        """Build quantitative score from LLM analysis data."""
        # Extract monetary values
        key_metrics = data.get("key_metrics", {})
        monetary_amount = 0.0
        currency = "USD"

        # Try to find monetary amount in various places
        if "monetary_amount" in data:
            monetary_amount = float(data["monetary_amount"])
        elif "total_amount" in key_metrics:
            monetary_amount = self._parse_monetary_value(str(key_metrics["total_amount"]))

        # Look for monetary values in notable items
        notable_items = data.get("notable_items", [])
        for item in notable_items:
            value = item.get("value", "")
            if isinstance(value, str) and '$' in value:
                parsed = self._parse_monetary_value(value)
                if parsed > monetary_amount:
                    monetary_amount = parsed

        return QuantitativeScore(
            total_count=int(data.get("total_count", 0)),
            monetary_amount=monetary_amount,
            currency=currency,
            key_metrics=key_metrics,
            notable_items=notable_items,
            threshold_violations=data.get("threshold_violations", [])
        )

    def _parse_monetary_value(self, value: str) -> float:
        """Parse monetary value from string."""
        if not value:
            return 0.0

        # Remove currency symbols and commas
        clean_value = re.sub(r'[$,€£]', '', str(value))

        # Handle K/M/B suffixes
        multipliers = {'k': 1000, 'm': 1000000, 'b': 1000000000}

        match = re.search(r'([\d.]+)\s*([KkMmBb])?', clean_value)
        if match:
            number = float(match.group(1))
            suffix = match.group(2)
            if suffix:
                number *= multipliers.get(suffix.lower(), 1)
            return number

        try:
            return float(clean_value)
        except ValueError:
            return 0.0

    def _calculate_risk_score(
        self,
        focus_area: str,
        severity: SeverityLevel,
        quantitative: QuantitativeScore
    ) -> Tuple[Dict[str, int], int]:
        """
        Calculate risk score with breakdown.

        Returns:
            Tuple of (scoring_breakdown dict, final_score int)
        """
        breakdown = {}

        # Base score from severity
        base_score = self.SEVERITY_BASE_SCORES[severity]
        breakdown["severity_base"] = base_score

        # Count adjustment
        count_adj = 0
        if quantitative.total_count >= self.COUNT_THRESHOLDS["critical"]:
            count_adj = 15
        elif quantitative.total_count >= self.COUNT_THRESHOLDS["high"]:
            count_adj = 10
        elif quantitative.total_count >= self.COUNT_THRESHOLDS["medium"]:
            count_adj = 5
        breakdown["count_adjustment"] = count_adj

        # Money adjustment
        money_adj = 0
        if quantitative.monetary_amount >= self.MONEY_THRESHOLDS["critical"]:
            money_adj = 20
        elif quantitative.monetary_amount >= self.MONEY_THRESHOLDS["high"]:
            money_adj = 15
        elif quantitative.monetary_amount >= self.MONEY_THRESHOLDS["medium"]:
            money_adj = 10
        elif quantitative.monetary_amount >= self.MONEY_THRESHOLDS["low"]:
            money_adj = 5
        breakdown["money_adjustment"] = money_adj

        # Focus area multiplier
        multiplier = self.FOCUS_AREA_MULTIPLIERS.get(focus_area, 1.0)
        breakdown["focus_area_multiplier"] = int(multiplier * 100)

        # Calculate final score
        raw_score = (base_score + count_adj + money_adj) * multiplier
        final_score = max(0, min(100, int(raw_score)))
        breakdown["final_score"] = final_score

        return breakdown, final_score

    def _score_to_risk_level(self, score: int) -> RiskLevel:
        """Convert numeric score to risk level."""
        if score >= 76:
            return RiskLevel.CRITICAL
        elif score >= 51:
            return RiskLevel.HIGH
        elif score >= 26:
            return RiskLevel.MEDIUM
        return RiskLevel.LOW

    def _estimate_money_loss(
        self,
        focus_area: str,
        quantitative: QuantitativeScore,
        qualitative: QualitativeScore
    ) -> Tuple[float, float]:
        """
        Estimate potential money loss.

        Returns:
            Tuple of (estimated_loss, confidence)
        """
        # If we have a direct monetary amount, use it
        if quantitative.monetary_amount > 0:
            return quantitative.monetary_amount, 0.8

        # Otherwise estimate based on count and focus area
        base_estimate_per_item = {
            "BUSINESS_PROTECTION": 5000,   # Fraud items tend to be high value
            "BUSINESS_CONTROL": 1000,      # Process delays cost money
            "ACCESS_GOVERNANCE": 2000,     # Compliance issues
            "TECHNICAL_CONTROL": 500,      # Tech issues
            "JOBS_CONTROL": 200,           # Job issues
        }

        base = base_estimate_per_item.get(focus_area, 1000)
        count = max(1, quantitative.total_count)

        # Adjust for severity
        severity_multiplier = {
            SeverityLevel.CRITICAL: 2.0,
            SeverityLevel.HIGH: 1.5,
            SeverityLevel.MEDIUM: 1.0,
            SeverityLevel.LOW: 0.5,
        }
        multiplier = severity_multiplier.get(qualitative.severity, 1.0)

        estimate = base * count * multiplier

        # Lower confidence for estimates without direct monetary data
        confidence = 0.4 if quantitative.monetary_amount == 0 else 0.7

        return estimate, confidence

    def _compile_risk_factors(
        self,
        focus_area: str,
        qualitative: QualitativeScore,
        quantitative: QuantitativeScore
    ) -> List[str]:
        """Compile list of risk factors."""
        factors = []

        # Severity factor
        if qualitative.severity in [SeverityLevel.CRITICAL, SeverityLevel.HIGH]:
            factors.append(f"{qualitative.severity.value} severity level")

        # Count factor
        if quantitative.total_count > 100:
            factors.append(f"High volume: {quantitative.total_count} items")

        # Money factor
        if quantitative.monetary_amount > 10000:
            factors.append(f"Financial exposure: ${quantitative.monetary_amount:,.2f}")

        # Focus area specific factors
        focus_area_factors = {
            "BUSINESS_PROTECTION": "Potential fraud or security breach",
            "BUSINESS_CONTROL": "Business process inefficiency",
            "ACCESS_GOVERNANCE": "Compliance/authorization risk",
            "TECHNICAL_CONTROL": "System stability concern",
            "JOBS_CONTROL": "Operational performance issue",
        }
        if focus_area in focus_area_factors:
            factors.append(focus_area_factors[focus_area])

        # Threshold violations
        for violation in quantitative.threshold_violations[:3]:
            factors.append(f"Threshold exceeded: {violation}")

        return factors

    def extract_metrics_from_text(self, text: str) -> Dict[str, Any]:
        """
        Extract quantitative metrics from raw text.

        Useful for processing Summary files directly.

        Args:
            text: Raw text to analyze

        Returns:
            Dictionary of extracted metrics
        """
        metrics = {
            "counts": [],
            "monetary_values": [],
            "percentages": [],
            "dates": [],
        }

        # Extract counts (handle comma-separated numbers like 1,943)
        count_patterns = [
            r'([\d,]+)\s+(?:records?|items?|entries|rows?|vendors?|customers?|users?)',
            r'(?:total|count|found)\s*[:\-]?\s*([\d,]+)',
        ]
        for pattern in count_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for m in matches:
                # Remove commas before converting to int
                clean_num = m.replace(',', '')
                if clean_num.isdigit():
                    metrics["counts"].append(int(clean_num))

        # Extract monetary values
        for pattern, currency in self._currency_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                if isinstance(match, tuple):
                    value = self._parse_monetary_value(f"{match[0]}{match[1] if len(match) > 1 else ''}")
                else:
                    value = self._parse_monetary_value(match)
                if value > 0:
                    metrics["monetary_values"].append({"amount": value, "currency": currency})

        # Extract percentages
        pct_matches = re.findall(r'(\d+(?:\.\d+)?)\s*%', text)
        metrics["percentages"] = [float(p) for p in pct_matches]

        return metrics
