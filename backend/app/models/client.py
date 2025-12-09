"""
Client Model - Represents the company whose SAP systems we monitor.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship

from app.core.database import Base


class Client(Base):
    """
    Client entity representing a company whose SAP systems are monitored.

    Example: Safal Group - Africa's leading building solutions provider.
    Each THA campaign runs against a specific client.
    """
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(20), unique=True, nullable=False, index=True)  # e.g., "SAFAL"
    name = Column(String(255), nullable=False)  # e.g., "Safal Group"
    description = Column(Text)  # Business description
    website = Column(String(255))  # Company website
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    source_systems = relationship("SourceSystem", back_populates="client", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Client(code='{self.code}', name='{self.name}')>"
