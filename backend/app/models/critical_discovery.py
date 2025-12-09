"""
Critical Discovery Model - Individual critical findings from analysis.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Numeric, Boolean

from sqlalchemy.orm import relationship

from app.core.database import Base


class CriticalDiscovery(Base):
    """
    Critical Discovery - The most important finding from an alert analysis.

    These are the high-signal findings that require immediate attention.
    Example: "OTC account with 153 returns (74% of volume) through generic customer"
    """
    __tablename__ = "critical_discoveries"

    id = Column(Integer, primary_key=True, index=True)
    alert_analysis_id = Column(Integer, ForeignKey("alert_analyses.id"), nullable=False, index=True)

    # Discovery details
    discovery_order = Column(Integer, default=1)  # Order in the analysis (1st, 2nd, etc.)
    title = Column(String(255), nullable=False)  # Short title
    description = Column(Text, nullable=False)  # Full discovery text

    # Affected entity
    affected_entity = Column(String(255))  # Customer/Vendor/Account name
    affected_entity_id = Column(String(50))  # Entity ID (e.g., customer number)

    # Metrics
    metric_value = Column(Numeric(18, 2))  # Numeric value (e.g., 153 returns)
    metric_unit = Column(String(50))  # Unit (e.g., "returns", "USD", "%")
    percentage_of_total = Column(Numeric(5, 2))  # Percentage representation

    # Risk flag
    is_fraud_indicator = Column(Boolean, default=False)  # Is this a fraud red flag?

    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    alert_analysis = relationship("AlertAnalysis", back_populates="critical_discoveries")

    def __repr__(self):
        return f"<CriticalDiscovery(title='{self.title[:50]}...', fraud={self.is_fraud_indicator})>"
