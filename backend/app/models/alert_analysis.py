"""
Alert Analysis Model - Analysis results for each alert execution.
"""
from datetime import datetime, date
from decimal import Decimal
from sqlalchemy import Column, Integer, String, Text, DateTime, Date, ForeignKey, JSON, Numeric, Index
from sqlalchemy.orm import relationship

from app.core.database import Base


class AlertAnalysis(Base):
    """
    Alert Analysis - Results from analyzing an alert.

    Stores the complete analysis output including:
    - Severity and risk classification
    - Financial impact calculations
    - Links to detailed findings (critical discoveries, key findings, etc.)
    """
    __tablename__ = "alert_analyses"

    id = Column(Integer, primary_key=True, index=True)
    alert_instance_id = Column(Integer, ForeignKey("alert_instances.id"), nullable=False, index=True)

    # Analysis metadata
    analysis_type = Column(String(20), nullable=False, index=True)  # QUANTI, QUALI, HYBRID
    execution_date = Column(Date, nullable=False, index=True)  # When alert was executed
    period_start = Column(Date)  # Analysis period start
    period_end = Column(Date)  # Analysis period end

    # Volume metrics
    records_affected = Column(Integer)  # Number of records flagged
    unique_entities = Column(Integer)  # Unique customers/vendors/etc.

    # Risk classification
    severity = Column(String(20), nullable=False, index=True)  # CRITICAL, HIGH, MEDIUM, LOW
    risk_score = Column(Integer)  # 0-100
    fraud_indicator = Column(String(50))  # CONFIRMED, INVESTIGATE, MONITOR, NONE

    # Financial impact
    financial_impact_local = Column(Numeric(18, 2))  # Amount in local currency
    financial_impact_usd = Column(Numeric(18, 2))  # Amount in USD
    local_currency = Column(String(10))  # Currency code (KES, ZAR, TZS)
    exchange_rate = Column(Numeric(10, 4))  # Rate used for conversion

    # Report reference
    report_path = Column(String(500))  # Path to full MD report
    raw_summary_data = Column(JSON)  # Parsed Summary artifact data

    # Audit fields
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(String(100))  # LLM/User who created

    # Indexes for dashboard queries
    __table_args__ = (
        Index('idx_alert_analyses_severity_date', 'severity', 'execution_date'),
        Index('idx_alert_analyses_type_date', 'analysis_type', 'execution_date'),
    )

    # Relationships
    alert_instance = relationship("AlertInstance", back_populates="analyses")
    critical_discoveries = relationship("CriticalDiscovery", back_populates="alert_analysis", cascade="all, delete-orphan")
    key_findings = relationship("KeyFinding", back_populates="alert_analysis", cascade="all, delete-orphan")
    concentration_metrics = relationship("ConcentrationMetric", back_populates="alert_analysis", cascade="all, delete-orphan")
    action_items = relationship("ActionItem", back_populates="alert_analysis", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<AlertAnalysis(id={self.id}, severity='{self.severity}', risk_score={self.risk_score})>"
