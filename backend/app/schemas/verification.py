from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class EmailVerificationRequest(BaseModel):
    email: EmailStr

class EmailVerificationVerify(BaseModel):
    email: EmailStr
    verification_code: str

class EmailVerificationResponse(BaseModel):
    message: str
    expires_in_minutes: int = 10

class EmailVerificationStatus(BaseModel):
    email: str
    is_verified: bool
    expires_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True