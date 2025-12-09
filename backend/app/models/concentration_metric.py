"""
Concentration Metric Model - Concentration data by dimension.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric, Index
from sqlalchemy.orm import relationship

from app.core.database import Base


class ConcentrationMetric(Base):
    """
    Concentration Metric - Concentration analysis by dimension.

    Tracks how values are distributed across different dimensions:
    - By Sales Organization (SALES_ORG)
    - By Customer (CUSTOMER)
    - By Region (REGION)
    - By Company Code (COMPANY_CODE)
    """
    __tablename__ = "concentration_metrics"

    id = Column(Integer, primary_key=True, index=True)
    alert_analysis_id = Column(Integer, ForeignKey("alert_analyses.id"), nullable=False, index=True)

    # Dimension identification
    dimension_type = Column(String(50), nullable=False, index=True)  # SALES_ORG, CUSTOMER, REGION
    dimension_code = Column(String(50), nullable=False)  # e.g., "TZ01", "2008812"
    dimension_name = Column(String(255))  # e.g., "Tanzania", "CHARTWELL ROOFING"

    # Metrics
    record_count = Column(Integer)  # Number of records
    value_local = Column(Numeric(18, 2))  # Value in local currency
    value_usd = Column(Numeric(18, 2))  # Value in USD
    percentage_of_total = Column(Numeric(5, 2))  # Concentration percentage
    rank = Column(Integer)  # Rank by value

    created_at = Column(DateTime, default=datetime.utcnow)

    # Index for dimension queries
    __table_args__ = (
        Index('idx_concentration_type_code', 'dimension_type', 'dimension_code'),
    )

    # Relationships
    alert_analysis = relationship("AlertAnalysis", back_populates="concentration_metrics")

    def __repr__(self):
        return f"<ConcentrationMetric(type='{self.dimension_type}', code='{self.dimension_code}', pct={self.percentage_of_total}%)>"
