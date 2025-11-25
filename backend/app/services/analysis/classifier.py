from typing import Dict, List, Optional, Tuple
from sqlalchemy.orm import Session
from app.models.focus_area import FocusArea
from app.models.issue_type import IssueType
import re


class FocusAreaClassifier:
    """Classify alerts/reports into one of the 6 focus areas"""
    
    # Keywords and patterns for each focus area
    # Extended patterns to match real-world Skywind 4C alerts
    FOCUS_AREA_PATTERNS = {
        "BUSINESS_PROTECTION": [
            r"fraud",
            r"cybersecurity",
            r"security.*breach",
            r"unauthorized.*access",
            r"material.*conversion",
            r"vendor.*payment.*diversion",
            r"backdated.*purchase",
            r"one.*time.*vendor",
            r"retroactiv",  # Retroactively created documents = potential fraud
            r"duplicate.*payment",
            r"suspicious",
            r"irregular",
            r"manipulation",
            r"falsif",
        ],
        "BUSINESS_CONTROL": [
            r"bottleneck",
            r"stuck.*order",
            r"unbilled.*delivery",
            r"incomplete.*service",
            r"data.*exchange.*failure",
            r"process.*observability",
            r"business.*anomal",
            r"waiting.*approval",  # PO/PR waiting for approval
            r"pending.*approval",
            r"approval.*delay",
            r"negative.*profit",  # Negative profit deals
            r"profit.*deal",
            r"margin",
            r"pricing.*issue",
            r"purchase.*order",
            r"sales.*order",
            r"delivery.*block",
            r"blocked.*order",
            r"overdue",
            r"delay",
            r"pur\s+po",  # PUR PO pattern
            r"goods.*receipt",
        ],
        "ACCESS_GOVERNANCE": [
            r"segregation.*duties",
            r"sod.*violation",
            r"authorization",
            r"user.*access",
            r"long.*time.*logged",
            r"session.*duration",
            r"self.*approval",
            r"access.*review",
            r"user.*activity",
            r"privilege",
            r"permission",
            r"role.*assign",
            r"critical.*transaction",
        ],
        "TECHNICAL_CONTROL": [
            r"system.*dump",
            r"lock.*conflict",
            r"resource.*exhaustion",
            r"update.*request.*failure",
            r"configuration.*drift",
            r"infrastructure",
            r"technical.*anomal",
            r"runtime.*error",
            r"abap.*dump",
            r"short.*dump",
            r"performance.*issue",
            r"memory",
            r"cpu.*usage",
        ],
        "JOBS_CONTROL": [
            r"job.*performance",
            r"long.*running.*job",
            r"job.*failure",
            r"background.*job",
            r"resource.*utilization",
            r"job.*overlap",
            r"batch.*process",
            r"scheduled.*task",
        ],
        "S4HANA_EXCELLENCE": [
            r"s4.*hana",
            r"post.*migration",
            r"post.*go.*live",
            r"fiori.*interface",
            r"universal.*journal",
            r"migration.*safeguard",
            r"hana.*performance",
            r"cds.*view",
        ],
    }

    # Default focus area when no patterns match
    DEFAULT_FOCUS_AREA = "BUSINESS_CONTROL"
    
    def __init__(self, db: Session):
        self.db = db
        self._focus_areas = None
        self._load_focus_areas()
    
    def _load_focus_areas(self):
        """Load focus areas from database"""
        self._focus_areas = {
            fa.code: fa for fa in self.db.query(FocusArea).all()
        }
    
    def classify(self, alert_name: Optional[str] = None, 
                 report_type: Optional[str] = None,
                 data: Optional[Dict] = None) -> Tuple[Optional[FocusArea], float]:
        """
        Classify into a focus area
        
        Returns:
            Tuple of (FocusArea, confidence_score)
        """
        text_to_analyze = ""
        
        # Build text from available sources
        if alert_name:
            text_to_analyze += f" {alert_name.lower()}"
        
        if report_type:
            text_to_analyze += f" {report_type.lower()}"
        
        if data:
            # Extract relevant fields from data
            for key, value in data.items():
                if isinstance(value, str) and len(value) < 200:  # Avoid very long text
                    text_to_analyze += f" {value.lower()}"
        
        if not text_to_analyze:
            return None, 0.0
        
        # Score each focus area
        scores = {}
        for focus_code, patterns in self.FOCUS_AREA_PATTERNS.items():
            score = 0.0
            matches = 0
            
            for pattern in patterns:
                if re.search(pattern, text_to_analyze, re.IGNORECASE):
                    matches += 1
                    score += 1.0 / len(patterns)  # Weight by pattern count
            
            # Normalize score
            if matches > 0:
                score = min(1.0, score * (matches / len(patterns)))
            
            scores[focus_code] = score
        
        # Get focus area with highest score
        if not scores or max(scores.values()) == 0:
            # Return default focus area with low confidence instead of None
            # This ensures findings are always created for uploaded data
            default_fa = self._focus_areas.get(self.DEFAULT_FOCUS_AREA)
            if default_fa:
                return default_fa, 0.3  # Low confidence for default classification
            return None, 0.0

        best_focus_code = max(scores, key=scores.get)
        confidence = scores[best_focus_code]
        
        focus_area = self._focus_areas.get(best_focus_code)
        
        return focus_area, confidence


class IssueTypeClassifier:
    """Classify findings into specific issue types"""
    
    def __init__(self, db: Session):
        self.db = db
        self._issue_types = None
        self._load_issue_types()
    
    def _load_issue_types(self):
        """Load issue types from database"""
        self._issue_types = {
            it.code: it for it in self.db.query(IssueType).all()
        }
    
    def classify(self, focus_area: FocusArea,
                 alert_name: Optional[str] = None,
                 report_type: Optional[str] = None,
                 data: Optional[Dict] = None) -> Tuple[Optional[IssueType], float]:
        """
        Classify into an issue type within a focus area
        
        Returns:
            Tuple of (IssueType, confidence_score)
        """
        # Get issue types for this focus area
        issue_types = [
            it for it in self._issue_types.values()
            if it.focus_area_id == focus_area.id
        ]
        
        if not issue_types:
            return None, 0.0
        
        text_to_analyze = ""
        if alert_name:
            text_to_analyze += f" {alert_name.lower()}"
        if report_type:
            text_to_analyze += f" {report_type.lower()}"
        if data:
            for key, value in data.items():
                if isinstance(value, str) and len(value) < 200:
                    text_to_analyze += f" {value.lower()}"
        
        # Score each issue type
        scores = {}
        for issue_type in issue_types:
            score = 0.0
            
            # Check if issue type code or name appears in text
            if issue_type.code.lower() in text_to_analyze:
                score += 0.5
            if issue_type.name.lower() in text_to_analyze:
                score += 0.3
            if issue_type.description and issue_type.description.lower() in text_to_analyze:
                score += 0.2
            
            # Pattern matching for specific issue types
            if issue_type.code == "LONG_SESSION" and ("24" in text_to_analyze or "hour" in text_to_analyze):
                score += 0.5
            if issue_type.code == "SOD_VIOLATION" and ("violation" in text_to_analyze or "conflict" in text_to_analyze):
                score += 0.5
            if issue_type.code == "FRAUD_DETECTION" and "fraud" in text_to_analyze:
                score += 0.5
            
            scores[issue_type.code] = min(1.0, score)
        
        if not scores or max(scores.values()) == 0:
            # Return default issue type for focus area if available
            default_issue = issue_types[0] if issue_types else None
            return default_issue, 0.3
        
        best_issue_code = max(scores, key=scores.get)
        confidence = scores[best_issue_code]
        
        issue_type = self._issue_types.get(best_issue_code)
        
        return issue_type, confidence

