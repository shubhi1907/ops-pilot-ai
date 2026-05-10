from sqlalchemy import Column, Integer, String, Text
from db.database import Base


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)

    email = Column(Text)

    category = Column(String)
    priority = Column(String)
    department = Column(String)
    should_escalate = Column(String)
    response = Column(Text)
    confidence_score = Column(String)    
    risk_score = Column(String)

    # ✅ Approval / Governance
    approval_status = Column(String, default="pending")
    approved_by = Column(String)
    approved_at = Column(String)
    rejection_reason = Column(Text)

    # ✅ Workflow lifecycle
    status = Column(String, default="created")
    created_at = Column(String)
    updated_at = Column(String)