from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.verification import (
    EmailVerificationRequest, 
    EmailVerificationVerify, 
    EmailVerificationResponse,
    EmailVerificationStatus
)
from app.core.email_service import email_service
from app.core.crud import get_user_by_email
from app.core.truemail_validator import truemail_validator
import re

router = APIRouter()

def is_valid_email_domain(email: str) -> bool:
    """Real email validation using truemail-like validation"""
    try:
        return truemail_validator.is_email_valid(email)
    except Exception as e:
        print(f"Email validation error: {e}")
        return False

@router.post("/send-verification", response_model=EmailVerificationResponse)
def send_email_verification(
    request: EmailVerificationRequest, 
    db: Session = Depends(get_db)
):
    """Send email verification code"""
    email = request.email.lower()
    
    # Check if email is valid using real validation
    if not is_valid_email_domain(email):
        raise HTTPException(
            status_code=400,
            detail="Email address is invalid or not deliverable. Please check your email address and try again."
        )
    
    # Check if user already exists
    existing_user = get_user_by_email(db, email)
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    # Create verification record
    verification_code = email_service.create_verification_record(db, email)
    
    # Send verification email
    success = email_service.send_verification_email(email, verification_code)
    
    if not success:
        raise HTTPException(
            status_code=500,
            detail="Failed to send verification email. Please try again."
        )
    
    return EmailVerificationResponse(
        message="Verification code sent to your email",
        expires_in_minutes=10
    )

@router.post("/verify-email")
def verify_email_code(
    request: EmailVerificationVerify, 
    db: Session = Depends(get_db)
):
    """Verify email code"""
    email = request.email.lower()
    code = request.verification_code.strip()
    
    if not code or len(code) != 6 or not code.isdigit():
        raise HTTPException(
            status_code=400,
            detail="Invalid verification code format"
        )
    
    # Verify the code
    is_valid = email_service.verify_code(db, email, code)
    
    if not is_valid:
        raise HTTPException(
            status_code=400,
            detail="Invalid or expired verification code"
        )
    
    return {"message": "Email verified successfully", "verified": True}

@router.get("/verification-status/{email}", response_model=EmailVerificationStatus)
def get_verification_status(email: str, db: Session = Depends(get_db)):
    """Get email verification status"""
    email = email.lower()
    is_verified = email_service.is_email_verified(db, email)
    
    return EmailVerificationStatus(
        email=email,
        is_verified=is_verified
    )

@router.post("/validate-email")
def validate_email_detailed(request: EmailVerificationRequest):
    """Detailed email validation for debugging"""
    email = request.email.lower()
    
    try:
        result = truemail_validator.validate_email_address(email)
        return {
            "email": email,
            "validation_result": result,
            "is_valid": truemail_validator.is_email_valid(email)
        }
    except Exception as e:
        return {
            "email": email,
            "error": str(e),
            "is_valid": False
        }