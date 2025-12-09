"""
Action Item Model - Items requiring investigation or follow-up.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Date, ForeignKey, Index
from sqlalchemy.orm import relationship

from app.core.database import Base


class ActionItem(Base):
    """
    Action Item - Investigation or follow-up tasks from analysis.

    Tracks action items with status for workflow management:
    - OPEN: Needs attention
    - IN_REVIEW: Being investigated
    - REMEDIATED: Issue resolved
    - FALSE_POSITIVE: Not a real issue
    """
    __tablename__ = "action_items"

    id = Column(Integer, primary_key=True, index=True)
    alert_analysis_id = Column(Integer, ForeignKey("alert_analyses.id"), nullable=False, index=True)

    # Action details
    action_type = Column(String(50), nullable=False)  # IMMEDIATE, SHORT_TERM, PROCESS_IMPROVEMENT
    priority = Column(Integer)  # 1-5 (1=Highest)
    title = Column(String(255), nullable=False)  # Action title
    description = Column(Text)  # Full action description

    # Status tracking
    status = Column(String(30), default="OPEN", index=True)  # OPEN, IN_REVIEW, REMEDIATED, FALSE_POSITIVE
    assigned_to = Column(String(100))  # Assignee
    due_date = Column(Date)  # Target completion date

    # Resolution
    resolution_notes = Column(Text)  # Notes on resolution
    resolved_at = Column(DateTime)  # When resolved
    resolved_by = Column(String(100))  # Who resolved

    created_at = Column(DateTime, default=datetime.utcnow)

    # Indexes for action queue queries
    __table_args__ = (
        Index('idx_action_items_status_priority', 'status', 'priority'),
        Index('idx_action_items_type_status', 'action_type', 'status'),
    )

    # Relationships
    alert_analysis = relationship("AlertAnalysis", back_populates="action_items")

    def __repr__(self):
        return f"<ActionItem(title='{self.title[:50]}...', status='{self.status}')>"
