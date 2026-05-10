from fastapi import FastAPI

from routers import ticket_router
from routers import analytics_router

from db.database import Base, engine

# ✅ Create DB tables
Base.metadata.create_all(bind=engine)

# ✅ Create app FIRST
app = FastAPI(title="OpsPilot AI")

# ✅ THEN include routers
app.include_router(ticket_router.router)
app.include_router(analytics_router.router)


@app.get("/")
def home():
    return {"message": "OpsPilot AI is running"}