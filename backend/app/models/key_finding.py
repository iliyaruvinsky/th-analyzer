"""
Key Finding Model - Top N findings from each analysis.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import relationship

from app.core.database import Base


class KeyFinding(Base):
    """
    Key Finding - Top findings from an alert analysis.

    Typically the top 3 findings that summarize the most important discoveries.
    """
    __tablename__ = "key_findings"

    id = Column(Integer, primary_key=True, index=True)
    alert_analysis_id = Column(Integer, ForeignKey("alert_analyses.id"), nullable=False, index=True)

    # Finding details
    finding_rank = Column(Integer, nullable=False)  # 1, 2, 3
    finding_text = Column(Text, nullable=False)  # Finding description
    finding_category = Column(String(50))  # Concentration, Anomaly, Data Quality, Process Gap

    # Financial impact if applicable
    financial_impact_usd = Column(Numeric(18, 2))

    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    alert_analysis = relationship("AlertAnalysis", back_populates="key_findings")

    def __repr__(self):
        return f"<KeyFinding(rank={self.finding_rank}, category='{self.finding_category}')>"
