"""
Exception Indicator Models - EI definitions and vocabulary catalog.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship

from app.core.database import Base


class ExceptionIndicator(Base):
    """
    Exception Indicator (EI) - Base ABAP function for alerts.

    Each EI can serve as the base for multiple alerts.
    The same EI with different parameters creates different alerts.

    Example: SW_10_01_ORD_VAL_TOT -> /SKN/F_SW_10_01_ORD_VAL_TOT
    """
    __tablename__ = "exception_indicators"

    id = Column(Integer, primary_key=True, index=True)
    ei_id = Column(String(50), unique=True, nullable=False, index=True)  # SW_10_01_ORD_VAL_TOT
    function_name = Column(String(100))  # /SKN/F_SW_10_01_ORD_VAL_TOT
    module = Column(String(10), nullable=False, index=True)  # FI, SD, MM, MD, PUR
    category = Column(String(50))  # Applications, Master Data, Access Control
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    vocabulary = relationship("EIVocabulary", back_populates="exception_indicator", uselist=False, cascade="all, delete-orphan")
    alert_instances = relationship("AlertInstance", back_populates="exception_indicator")

    def __repr__(self):
        return f"<ExceptionIndicator(ei_id='{self.ei_id}', module='{self.module}')>"


class EIVocabulary(Base):
    """
    EI Vocabulary - LLM-generated interpretations of EI ABAP code.

    This catalog stores what the LLM learned from analyzing each EI's code,
    enabling faster and more consistent analysis of alerts based on that EI.
    """
    __tablename__ = "ei_vocabulary"

    id = Column(Integer, primary_key=True, index=True)
    ei_id = Column(Integer, ForeignKey("exception_indicators.id"), unique=True, nullable=False)

    # Data extraction from ABAP code
    source_tables = Column(JSON)  # ["VBAK", "VBAP", "KNC1"] - Tables queried
    key_fields = Column(JSON)  # {"NETWR": "Net Value", "KUNNR": "Customer"} - Field meanings
    data_selection_logic = Column(Text)  # Parsed SELECT/WHERE interpretation
    aggregation_logic = Column(Text)  # How data is grouped (by customer, by period, etc.)
    threshold_fields = Column(JSON)  # Parameters controlling flagging (TOT_NETWR_FR, etc.)

    # Risk interpretation
    risk_patterns = Column(JSON)  # Known red flag patterns this EI can detect
    interpretation_notes = Column(Text)  # LLM-generated analysis summary

    # Additional code requirements
    external_functions_needed = Column(JSON)  # List of called functions requiring additional code

    # Versioning
    version = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    exception_indicator = relationship("ExceptionIndicator", back_populates="vocabulary")

    def __repr__(self):
        return f"<EIVocabulary(ei_id={self.ei_id}, version={self.version})>"
