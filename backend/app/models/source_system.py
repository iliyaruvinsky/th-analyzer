"""
Source System Model - Represents SAP source systems being monitored.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from app.core.database import Base


class SourceSystem(Base):
    """
    SAP source system being monitored.

    Examples:
    - PS4 (Production S/4HANA)
    - ECP (ECC Production)
    - BIP (BI Production)
    """
    __tablename__ = "source_systems"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False, index=True)
    code = Column(String(20), nullable=False)  # e.g., "PS4"
    name = Column(String(100), nullable=False)  # e.g., "Production S4"
    system_type = Column(String(50))  # ECC, S/4HANA, BW, CRM
    environment = Column(String(20))  # DEV, QA, PROD
    created_at = Column(DateTime, default=datetime.utcnow)

    # Unique constraint: one code per client
    __table_args__ = (
        UniqueConstraint('client_id', 'code', name='uq_source_system_client_code'),
    )

    # Relationships
    client = relationship("Client", back_populates="source_systems")
    alert_instances = relationship("AlertInstance", back_populates="source_system", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<SourceSystem(code='{self.code}', name='{self.name}', type='{self.system_type}')>"
