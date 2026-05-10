from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from ai.agents import (
    classification_agent,
    decision_agent,
    response_agent
)
from ai.vector_service import add_document, search_similar

from db.session import get_db
from models.ticket import Ticket
from models.request_models import EmailRequest

router = APIRouter()


# =========================================
# PROCESS EMAIL
# =========================================

@router.post("/process-email")
def process_email(request: EmailRequest, db: Session = Depends(get_db)):

    # 1. AI decision
    # 1. Classification agent
    classification = classification_agent(request.email)

    # 2. Decision agent
    decision = decision_agent(
        request.email,
        classification
    )

    if decision is None:
        decision = {
            "category": "Other",
            "priority": "Medium",
            "department": "Support",
            "should_escalate": "no",
            "confidence_score": 0.5
        }

    # 2. Extract fields
    category = decision.get("category", "Other")
    priority = decision.get("priority", "Medium")
    department = decision.get("department", "Support")
    should_escalate = decision.get("should_escalate", "no")
    confidence = decision.get("confidence_score", 0.5)
    risk_score = decision.get("risk_score", 0.3)

    # 3. Search memory
    similar_issues = search_similar(request.email)

    # 4. Generate response
    response_text = response_agent(
        request.email,
        category,
        similar_issues
    )

    # 5. Timestamp
    now = str(datetime.utcnow())

    # 6. Create ticket
    ticket = Ticket(
        email=request.email,
        category=category,
        priority=priority,
        department=department,
        should_escalate=should_escalate,
        response=response_text,
        confidence_score=str(confidence),
        risk_score=str(risk_score),
        approval_status="pending",
        status="created",
        created_at=now,
        updated_at=now
    )

    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    # 7. Store memory
    add_document(request.email)

    # 8. Escalation logic
    escalation_message = None

    if str(should_escalate).lower() == "yes":
        escalation_message = f"⚠️ Escalation triggered for ticket {ticket.id}"

    return {
        "ticket_id": ticket.id,
        "category": category,
        "priority": priority,
        "department": department,
        "should_escalate": should_escalate,
        "confidence_score": confidence,
        "risk_score": risk_score,
        "response": response_text,
        "escalation": escalation_message
    }


# =========================================
# APPROVE TICKET
# =========================================

@router.post("/approve-ticket/{ticket_id}")
def approve_ticket(ticket_id: int, db: Session = Depends(get_db)):

    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()

    if not ticket:
        return {"error": f"Ticket {ticket_id} not found"}

    ticket.approval_status = "approved"
    ticket.status = "approved"
    ticket.approved_by = "manager_1"
    ticket.approved_at = str(datetime.utcnow())
    ticket.updated_at = str(datetime.utcnow())

    db.commit()

    return {"message": f"Ticket {ticket_id} approved"}


# =========================================
# REJECT TICKET
# =========================================

@router.post("/reject-ticket/{ticket_id}")
def reject_ticket(ticket_id: int, reason: str, db: Session = Depends(get_db)):

    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()

    if not ticket:
        return {"error": f"Ticket {ticket_id} not found"}

    ticket.approval_status = "rejected"
    ticket.status = "rejected"
    ticket.rejection_reason = reason
    ticket.updated_at = str(datetime.utcnow())

    db.commit()

    return {"message": f"Ticket {ticket_id} rejected"}


# =========================================
# GET TICKET TIMELINE
# =========================================

@router.get("/ticket/{ticket_id}")
def get_ticket(ticket_id: int, db: Session = Depends(get_db)):

    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()

    if not ticket:
        return {"error": f"Ticket {ticket_id} not found"}

    return {
        "id": ticket.id,
        "status": ticket.status,
        "created_at": ticket.created_at,
        "updated_at": ticket.updated_at,
        "approval_status": ticket.approval_status,
        "approved_at": ticket.approved_at,
        "rejection_reason": ticket.rejection_reason
    }