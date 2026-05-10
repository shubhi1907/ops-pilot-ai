from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.session import get_db
from models.ticket import Ticket

router = APIRouter()

@router.get("/analytics")
def get_analytics(db: Session = Depends(get_db)):
    tickets = db.query(Ticket).all()

    total = len(tickets)
    high_priority = sum(1 for t in tickets if t.priority == "High")
    escalations = sum(1 for t in tickets if t.should_escalate == "yes")

    return {
        "total_tickets": total,
        "high_priority_tickets": high_priority,
        "escalations": escalations
    }