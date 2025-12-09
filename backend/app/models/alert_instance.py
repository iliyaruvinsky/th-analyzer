"""
Alert Instance Model - Specific alert configurations (EI + parameters).
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship

from app.core.database import Base


class AlertInstance(Base):
    """
    Alert Instance - A specific alert configuration.

    An alert is an EI with specified parameters.
    Example: Alert 200025_001455 = EI SW_10_01_ORD_VAL_TOT with BACKDAYS=365, VBTYP=H
    """
    __tablename__ = "alert_instances"

    id = Column(Integer, primary_key=True, index=True)
    alert_id = Column(String(50), unique=True, nullable=False, index=True)  # 200025_001455
    alert_name = Column(String(255), nullable=False)  # "Monthly returns value by Payer and Sales organization"

    # Relationships to parent entities
    ei_id = Column(Integer, ForeignKey("exception_indicators.id"), index=True)
    source_system_id = Column(Integer, ForeignKey("source_systems.id"), index=True)

    # Classification
    focus_area = Column(String(50), nullable=False, index=True)  # BUSINESS_PROTECTION, etc.
    subcategory = Column(String(100))  # SD Alerts, FI Alerts

    # Configuration from Metadata
    parameters = Column(JSON)  # Alert parameters from Metadata_*.xlsx
    business_purpose = Column(Text)  # From Explanation artifact

    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    exception_indicator = relationship("ExceptionIndicator", back_populates="alert_instances")
    source_system = relationship("SourceSystem", back_populates="alert_instances")
    analyses = relationship("AlertAnalysis", back_populates="alert_instance", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<AlertInstance(alert_id='{self.alert_id}', name='{self.alert_name[:50]}...')>"
