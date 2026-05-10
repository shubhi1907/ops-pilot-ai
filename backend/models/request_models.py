from pydantic import BaseModel

class EmailRequest(BaseModel):
    email: str