from typing import Dict, Optional
from app.models.finding import Finding
from app.models.issue_type import IssueType


class RiskScorer:
    """Calculate risk scores for findings"""
    
    # Base risk scores by severity (per BUSINESS_PROTECTION.md)
    SEVERITY_SCORES = {
        "Critical": 90,
        "High": 75,
        "Medium": 60,
        "Low": 50,
    }
    
    # Risk multipliers by issue type
    ISSUE_TYPE_MULTIPLIERS = {
        "FRAUD_DETECTION": 1.2,
        "SOD_VIOLATION": 1.3,
        "CYBERSECURITY_THREAT": 1.4,
        "UNAUTHORIZED_ACCESS": 1.3,
        "MATERIAL_CONVERSION_FRAUD": 1.5,
        "VENDOR_PAYMENT_DIVERSION": 1.4,
        "SELF_APPROVAL": 1.2,
        "PROCESS_BOTTLENECK": 0.9,
        "LONG_SESSION": 0.8,
    }
    
    def calculate_risk_score(self, finding: Finding, 
                            issue_type: Optional[IssueType] = None) -> Dict[str, any]:
        """
        Calculate risk score for a finding
        
        Returns:
            Dict with risk_score, risk_level, risk_category
        """
        # Start with base score from severity
        base_score = self.SEVERITY_SCORES.get(finding.severity, 50)
        
        # Apply issue type multiplier
        multiplier = 1.0
        if issue_type and issue_type.code in self.ISSUE_TYPE_MULTIPLIERS:
            multiplier = self.ISSUE_TYPE_MULTIPLIERS[issue_type.code]
        
        # Apply classification confidence
        confidence_multiplier = finding.classification_confidence or 0.7
        adjusted_multiplier = 1.0 + (multiplier - 1.0) * confidence_multiplier
        
        # Calculate final score
        risk_score = int(base_score * adjusted_multiplier)
        risk_score = min(100, max(0, risk_score))  # Clamp to 0-100
        
        # Determine risk level
        if risk_score >= 80:
            risk_level = "Critical"
            risk_category = "Security" if issue_type and "FRAUD" in issue_type.code else "Compliance"
        elif risk_score >= 60:
            risk_level = "High"
            risk_category = "Security" if issue_type and "FRAUD" in issue_type.code else "Operational"
        elif risk_score >= 40:
            risk_level = "Medium"
            risk_category = "Operational"
        else:
            risk_level = "Low"
            risk_category = "Operational"
        
        return {
            "risk_score": risk_score,
            "risk_level": risk_level,
            "risk_category": risk_category,
            "base_score": base_score,
            "multiplier": adjusted_multiplier
        }

