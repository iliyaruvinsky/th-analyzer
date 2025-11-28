"""
Scoring Engine for Treasure Hunt Analyzer

Implements qualitative and quantitative scoring for findings.
Combines LLM analysis with rule-based calculations for comprehensive risk assessment.

Scoring Philosophy:
- Alerts are NOT confirmations of fraud/bad events - they expose POSSIBILITIES
- Severity reflects urgency of review, potential harm if ignored, and type of risk
- Risk types: Cybersecurity breach, Possible fraud, Compliance (SoD), Process deviation
- Factor 1: Alert Nature (base score by severity)
- Factor 2: Count (normalized by BACKDAYS when available)
- Factor 3: Monetary amounts involved
- Factor 4: Focus area multiplier
- Factor 5: Quantities/patterns involved
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

    # Base scores by severity (Updated per user requirements)
    # CRITICAL: Cybersecurity breach, direct theft pattern, full access grant - IMMEDIATE review
    # HIGH: Possible fraud/theft, SoD+fraud combo, sensitive transactions - PROMPT review
    # MEDIUM: Pure SoD violations, process deviations - may be acceptable but needs documentation
    # LOW: Tracking/housekeeping items - awareness/trend monitoring
    SEVERITY_BASE_SCORES = {
        SeverityLevel.CRITICAL: 90,  # Was 85
        SeverityLevel.HIGH: 75,      # Was 65
        SeverityLevel.MEDIUM: 60,    # Was 45
        SeverityLevel.LOW: 50,       # Was 25
    }

    # Alert type to severity mapping for BUSINESS_PROTECTION focus area
    # These patterns help determine severity based on alert name/type
    BUSINESS_PROTECTION_ALERT_SEVERITY = {
        # CRITICAL: Cybersecurity breach, direct theft mechanism, full access grant
        "CRITICAL": [
            "debug",                           # DEBUG system updates - bypasses all controls
            "sap_all", "sap_new",              # Critical authorization grants
            "po for one-time vendor",          # Direct theft pattern
            "purchase order for one-time",     # Direct theft pattern
            "unauthorized transaction",        # Security bypass
            "dialog user by unauthorized",     # User master manipulation
            "activating transaction",          # Unauthorized transaction execution
        ],
        # HIGH: Possible fraud/theft, SoD+fraud combo, sensitive transactions, rarely used vendors
        "HIGH": [
            "vendor bank.*changed.*reversed",  # Classic fraud pattern
            "vendor bank.*revert",             # Classic fraud pattern
            "modified vendor bank",            # Bank modification alert
            "vendor.*credentials.*multiple",   # Suspicious pattern
            "suspicious material",             # Possible theft
            "alternative payee",               # Payment redirection
            "account payable fraud",           # Possible fraud
            "inventory variance",              # Possible theft
            "inventory count.*differ",         # Possible theft
            "login.*password.*not.*sso",       # SSO bypass
            "rarely used vendor",              # Silent vendor with rare transactions = fraud indicator
            "rarely used vendors",             # Plural form
            "ruv ",                            # Rarely Used Vendor abbreviation
            "sensitive transaction",           # WHO/WHY/HOW needed
            "sod.*fraud",                      # SoD + fraud combination = HIGH
            "segregation.*fraud",              # SoD + fraud combination = HIGH
        ],
        # MEDIUM: Pure SoD violations, process deviations
        "MEDIUM": [
            "approved by creator",             # Pure SoD - may be OK in thin-staffed orgs
            "parked.*posted.*same user",       # Pure SoD
            "gr/ir.*altered.*same user",       # Pure SoD
            "retroactive",                     # Process deviation
            "payment terms mismatch",          # Process error
            "exceptional posting",             # Anomaly
            "over delivery tolerance",         # Control bypass potential
        ],
        # LOW: Tracking/housekeeping
        "LOW": [
            "one-time vendor created",         # Track for later
            "credit limit changed",            # Business decision
            "inactive vendor.*no balance",     # Housekeeping
            "inactive vendor$",                # Housekeeping (without high balance)
        ],
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
        self._compiled_alert_patterns = self._compile_alert_patterns()

    def _compile_alert_patterns(self) -> Dict[str, List[re.Pattern]]:
        """Pre-compile regex patterns for alert severity matching."""
        compiled = {}
        for severity, patterns in self.BUSINESS_PROTECTION_ALERT_SEVERITY.items():
            compiled[severity] = [re.compile(p, re.IGNORECASE) for p in patterns]
        return compiled

    def determine_severity_from_alert_type(
        self,
        alert_name: str,
        focus_area: str,
        explanation: str = "",
        code_summary: str = ""
    ) -> Tuple[SeverityLevel, str]:
        """
        Determine severity based on alert type/name for a given focus area.

        This implements Factor 1 (Alert Nature) of the scoring methodology.
        Different alert types have inherent severity levels based on:
        - Type of risk (cybersecurity vs fraud vs SoD vs process deviation)
        - Urgency of review required
        - Potential harm if ignored

        Args:
            alert_name: The name/title of the alert
            focus_area: The classified focus area
            explanation: Optional explanation text for additional context
            code_summary: Optional code summary for additional context

        Returns:
            Tuple of (SeverityLevel, reasoning string)
        """
        combined_text = f"{alert_name} {explanation} {code_summary}".lower()

        # For BUSINESS_PROTECTION, use specific alert-type mapping
        if focus_area == "BUSINESS_PROTECTION":
            for severity_name, patterns in self._compiled_alert_patterns.items():
                for pattern in patterns:
                    if pattern.search(combined_text):
                        severity_level = getattr(SeverityLevel, severity_name)
                        reasoning = f"Alert type matches {severity_name} pattern: {pattern.pattern}"
                        return severity_level, reasoning

        # Check for specific high-risk indicators across all focus areas
        high_risk_indicators = [
            ("fraud", SeverityLevel.HIGH, "Fraud indicator detected"),
            ("theft", SeverityLevel.HIGH, "Theft indicator detected"),
            ("cyber", SeverityLevel.HIGH, "Cybersecurity concern"),
            ("unauthorized", SeverityLevel.HIGH, "Unauthorized activity"),
            ("sap_all", SeverityLevel.CRITICAL, "Critical authorization grant"),
            ("debug", SeverityLevel.CRITICAL, "Debug mode security risk"),
        ]

        for indicator, severity, reason in high_risk_indicators:
            if indicator in combined_text:
                return severity, reason

        # Default based on focus area
        focus_area_defaults = {
            "BUSINESS_PROTECTION": (SeverityLevel.HIGH, "Default for Business Protection alerts"),
            "ACCESS_GOVERNANCE": (SeverityLevel.MEDIUM, "Default for Access Governance - SoD review needed"),
            "BUSINESS_CONTROL": (SeverityLevel.MEDIUM, "Default for Business Control - process review needed"),
            "TECHNICAL_CONTROL": (SeverityLevel.MEDIUM, "Default for Technical Control - system review needed"),
            "JOBS_CONTROL": (SeverityLevel.LOW, "Default for Jobs Control - operational monitoring"),
        }

        return focus_area_defaults.get(
            focus_area,
            (SeverityLevel.MEDIUM, "Default severity")
        )

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
        severity: str = "Medium",
        alert_name: str = "",
        metadata: Optional[Dict[str, Any]] = None
    ) -> CombinedScore:
        """
        Calculate combined score from qualitative and quantitative data.

        Scoring factors:
        - Factor 1: Alert Nature (base score by severity)
        - Factor 2: Count (normalized by BACKDAYS when available)
        - Factor 3: Monetary amounts involved
        - Factor 4: Focus area multiplier
        - Factor 5: Quantities/patterns involved

        Args:
            focus_area: The focus area classification
            qualitative_data: Qualitative analysis from LLM
            quantitative_data: Quantitative analysis from LLM
            severity: Severity level string (can be overridden by alert type)
            alert_name: Alert name for type-based severity determination
            metadata: Optional metadata dict containing BACKDAYS and other parameters

        Returns:
            CombinedScore with detailed breakdown
        """
        metadata = metadata or {}

        # Determine severity from alert type if available (Factor 1: Alert Nature)
        if alert_name and focus_area:
            severity_level, severity_reasoning = self.determine_severity_from_alert_type(
                alert_name=alert_name,
                focus_area=focus_area,
                explanation=qualitative_data.get("what_happened", ""),
                code_summary=""
            )
            # Update qualitative data with determined severity reasoning
            qualitative_data["severity_reasoning"] = severity_reasoning
        else:
            # Parse severity from provided string
            severity_level = self._parse_severity(severity)

        # Build qualitative score
        qualitative = self._build_qualitative_score(qualitative_data, severity_level)

        # Build quantitative score
        quantitative = self._build_quantitative_score(quantitative_data)

        # Extract BACKDAYS for count normalization (Factor 2)
        backdays = self._extract_backdays(metadata)

        # Calculate risk score with all factors
        scoring_breakdown, risk_score = self._calculate_risk_score(
            focus_area, severity_level, quantitative, backdays
        )

        # Determine risk level
        risk_level = self._score_to_risk_level(risk_score)

        # Calculate money loss estimate
        money_loss, money_loss_confidence = self._estimate_money_loss(
            focus_area, quantitative, qualitative
        )

        # Compile risk factors
        risk_factors = self._compile_risk_factors(
            focus_area, qualitative, quantitative, backdays
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

    def _extract_backdays(self, metadata: Dict[str, Any]) -> Optional[int]:
        """
        Extract BACKDAYS parameter from metadata.

        BACKDAYS represents history depth: BACKDAYS=1 means yesterday+today.
        Used to normalize counts for meaningful risk assessment.
        Example: 1,943 vendors in 1 day vs 1,943 vendors in 30 days = VERY different risk

        Args:
            metadata: Metadata dictionary potentially containing BACKDAYS

        Returns:
            BACKDAYS value as integer, or None if not found
        """
        if not metadata:
            return None

        # Try different possible keys for BACKDAYS
        for key in ["BACKDAYS", "backdays", "BackDays", "back_days"]:
            if key in metadata:
                try:
                    return int(metadata[key])
                except (ValueError, TypeError):
                    pass

        # Try to find in raw metadata string
        if "raw_metadata" in metadata:
            raw = str(metadata["raw_metadata"])
            match = re.search(r'BACKDAYS\s*[=:]\s*(\d+)', raw, re.IGNORECASE)
            if match:
                return int(match.group(1))

        return None

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
        quantitative: QuantitativeScore,
        backdays: Optional[int] = None
    ) -> Tuple[Dict[str, int], int]:
        """
        Calculate risk score with breakdown.

        Factors:
        - Factor 1: Base score from severity (determined by alert type)
        - Factor 2: Count adjustment (normalized by BACKDAYS)
        - Factor 3: Money adjustment
        - Factor 4: Focus area multiplier
        - Factor 5: Quantity/pattern adjustment

        Returns:
            Tuple of (scoring_breakdown dict, final_score int)
        """
        breakdown = {}

        # Factor 1: Base score from severity (Alert Nature)
        base_score = self.SEVERITY_BASE_SCORES[severity]
        breakdown["factor1_severity_base"] = base_score

        # Factor 2: Count adjustment (normalized by BACKDAYS)
        raw_count = quantitative.total_count
        normalized_count = raw_count

        if backdays and backdays > 0:
            # Normalize count by BACKDAYS for meaningful comparison
            # Higher daily rate = higher risk
            normalized_count = raw_count / backdays
            breakdown["raw_count"] = raw_count
            breakdown["backdays"] = backdays
            breakdown["normalized_count_per_day"] = round(normalized_count, 2)

        count_adj = self._calculate_count_adjustment(normalized_count, backdays)
        breakdown["factor2_count_adjustment"] = count_adj

        # Factor 3: Money adjustment
        money_adj = self._calculate_money_adjustment(quantitative.monetary_amount)
        breakdown["factor3_money_adjustment"] = money_adj

        # Factor 4: Focus area multiplier
        multiplier = self.FOCUS_AREA_MULTIPLIERS.get(focus_area, 1.0)
        breakdown["factor4_focus_area_multiplier"] = int(multiplier * 100)

        # Factor 5: Quantity/pattern adjustment (concentration, frequency patterns)
        quantity_adj = self._calculate_quantity_adjustment(quantitative, backdays)
        breakdown["factor5_quantity_adjustment"] = quantity_adj

        # Calculate final score
        raw_score = (base_score + count_adj + money_adj + quantity_adj) * multiplier
        final_score = max(0, min(100, int(raw_score)))
        breakdown["final_score"] = final_score

        return breakdown, final_score

    def _calculate_count_adjustment(
        self,
        normalized_count: float,
        backdays: Optional[int] = None
    ) -> int:
        """
        Calculate count-based score adjustment.

        When BACKDAYS is available, use normalized daily rate thresholds.
        When not available, use raw count thresholds.

        Args:
            normalized_count: Count (normalized by BACKDAYS if available)
            backdays: BACKDAYS value if available

        Returns:
            Score adjustment points
        """
        if backdays and backdays > 0:
            # Use daily rate thresholds
            # These thresholds represent concerning daily volumes
            if normalized_count >= 100:      # 100+ items per day = critical
                return 15
            elif normalized_count >= 50:     # 50+ items per day = high
                return 10
            elif normalized_count >= 10:     # 10+ items per day = medium
                return 5
            elif normalized_count >= 1:      # 1+ items per day = low
                return 2
        else:
            # Use raw count thresholds (legacy behavior)
            if normalized_count >= self.COUNT_THRESHOLDS["critical"]:
                return 15
            elif normalized_count >= self.COUNT_THRESHOLDS["high"]:
                return 10
            elif normalized_count >= self.COUNT_THRESHOLDS["medium"]:
                return 5

        return 0

    def _calculate_money_adjustment(self, monetary_amount: float) -> int:
        """
        Calculate money-based score adjustment.

        Args:
            monetary_amount: Total monetary exposure

        Returns:
            Score adjustment points
        """
        if monetary_amount >= self.MONEY_THRESHOLDS["critical"]:  # $1M+
            return 20
        elif monetary_amount >= self.MONEY_THRESHOLDS["high"]:    # $100K+
            return 15
        elif monetary_amount >= self.MONEY_THRESHOLDS["medium"]:  # $10K+
            return 10
        elif monetary_amount >= self.MONEY_THRESHOLDS["low"]:     # $1K+
            return 5
        return 0

    def _calculate_quantity_adjustment(
        self,
        quantitative: QuantitativeScore,
        backdays: Optional[int] = None
    ) -> int:
        """
        Calculate Factor 5: Quantity/pattern-based adjustment.

        Considers:
        - Concentration patterns (e.g., high-value items in small count)
        - Notable items that exceed thresholds
        - Threshold violations

        Args:
            quantitative: Quantitative score data
            backdays: BACKDAYS value if available

        Returns:
            Score adjustment points
        """
        adjustment = 0

        # Check for notable high-value items
        notable_count = len(quantitative.notable_items)
        if notable_count > 0:
            if notable_count >= 5:
                adjustment += 5
            elif notable_count >= 2:
                adjustment += 3

        # Check for threshold violations
        violations_count = len(quantitative.threshold_violations)
        if violations_count > 0:
            if violations_count >= 3:
                adjustment += 5
            else:
                adjustment += violations_count * 2

        # Concentration pattern: high money relative to count
        if quantitative.total_count > 0 and quantitative.monetary_amount > 0:
            avg_per_item = quantitative.monetary_amount / quantitative.total_count
            if avg_per_item >= 100000:      # $100K+ average per item = high concentration
                adjustment += 5
            elif avg_per_item >= 10000:     # $10K+ average per item = medium concentration
                adjustment += 3

        return min(adjustment, 15)  # Cap Factor 5 at 15 points

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
        quantitative: QuantitativeScore,
        backdays: Optional[int] = None
    ) -> List[str]:
        """Compile list of risk factors with context."""
        factors = []

        # Severity factor with reasoning
        if qualitative.severity in [SeverityLevel.CRITICAL, SeverityLevel.HIGH]:
            severity_desc = f"{qualitative.severity.value} severity"
            if qualitative.severity_reasoning:
                severity_desc += f" - {qualitative.severity_reasoning}"
            factors.append(severity_desc)

        # Count factor with BACKDAYS context
        if quantitative.total_count > 0:
            if backdays and backdays > 0:
                daily_rate = quantitative.total_count / backdays
                factors.append(
                    f"Volume: {quantitative.total_count:,} items over {backdays} day(s) "
                    f"({daily_rate:.1f}/day)"
                )
            elif quantitative.total_count > 100:
                factors.append(f"High volume: {quantitative.total_count:,} items")

        # Money factor
        if quantitative.monetary_amount > 10000:
            factors.append(f"Financial exposure: ${quantitative.monetary_amount:,.2f}")

        # Focus area specific factors
        focus_area_factors = {
            "BUSINESS_PROTECTION": "Possible fraud/security event - stakeholder review required",
            "BUSINESS_CONTROL": "Business process anomaly - review recommended",
            "ACCESS_GOVERNANCE": "Compliance/authorization concern - audit trail needed",
            "TECHNICAL_CONTROL": "System stability indicator - technical review needed",
            "JOBS_CONTROL": "Operational pattern - monitoring recommended",
        }
        if focus_area in focus_area_factors:
            factors.append(focus_area_factors[focus_area])

        # Threshold violations
        for violation in quantitative.threshold_violations[:3]:
            factors.append(f"Threshold exceeded: {violation}")

        # Notable items
        if len(quantitative.notable_items) > 0:
            factors.append(f"{len(quantitative.notable_items)} notable items requiring attention")

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
