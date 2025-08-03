import smtplib
import ssl
import secrets
import string
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
from sqlalchemy.orm import Session
from app.models.verification import EmailVerification
from app.core.crud import get_user_by_email
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from email_config import *

class EmailService:
    def __init__(self):
        # Load configuration from email_config.py
        self.smtp_server = SMTP_SERVER
        self.smtp_port = SMTP_PORT
        self.email_address = EMAIL_ADDRESS
        self.email_password = EMAIL_PASSWORD
        self.use_real_email = ENABLE_EMAIL_SENDING
    
    def generate_verification_code(self, length: int = 6) -> str:
        """Generate a random verification code"""
        return ''.join(secrets.choice(string.digits) for _ in range(length))
    
    def send_verification_email(self, email: str, verification_code: str) -> bool:
        """Send verification email (simulated for demo)"""
        if not self.use_real_email:
            # For demo purposes, just log the verification code
            print(f"\n{'='*50}")
            print(f"📧 EMAIL VERIFICATION CODE")
            print(f"{'='*50}")
            print(f"📧 To: {email}")
            print(f"🔑 Verification Code: {verification_code}")
            print(f"⏰ Expires in: 10 minutes")
            print(f"💡 Copy this code to complete registration")
            print(f"{'='*50}\n")
            return True
        
        try:
            # Create message
            message = MIMEMultipart("alternative")
            message["Subject"] = EMAIL_SUBJECT
            message["From"] = self.email_address
            message["To"] = email
            
            # Use template from config
            html_content = EMAIL_TEMPLATE.format(verification_code=verification_code)
            part = MIMEText(html_content, "html")
            message.attach(part)
            
            # Send email
            context = ssl.create_default_context()
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.email_address, self.email_password)
                server.sendmail(self.email_address, email, message.as_string())
            
            print(f"✅ Email sent successfully!")
            print(f"   From: {self.email_address}")
            print(f"   To: {email}")
            print(f"   Code: {verification_code}")
            return True
        except Exception as e:
            print(f"❌ Failed to send email!")
            print(f"   From: {self.email_address}")
            print(f"   To: {email}")
            print(f"   Error: {e}")
            return False
    
    def create_verification_record(self, db: Session, email: str) -> str:
        """Create a new verification record and return the code"""
        verification_code = self.generate_verification_code()
        expires_at = datetime.utcnow() + timedelta(minutes=10)
        
        # Remove any existing unverified codes for this email
        db.query(EmailVerification).filter(
            EmailVerification.email == email,
            EmailVerification.is_used == False
        ).delete()
        
        # Create new verification record
        verification = EmailVerification(
            email=email,
            verification_code=verification_code,
            expires_at=expires_at
        )
        db.add(verification)
        db.commit()
        
        return verification_code
    
    def verify_code(self, db: Session, email: str, code: str) -> bool:
        """Verify the email code"""
        verification = db.query(EmailVerification).filter(
            EmailVerification.email == email,
            EmailVerification.verification_code == code,
            EmailVerification.is_used == False,
            EmailVerification.expires_at > datetime.utcnow()
        ).first()
        
        if verification:
            verification.is_used = True
            db.commit()
            return True
        
        return False
    
    def is_email_verified(self, db: Session, email: str) -> bool:
        """Check if email has been verified"""
        # Check if user exists and has verified email
        user = get_user_by_email(db, email)
        if user:
            return True  # User exists, so email was verified during registration
            
        # Check for recent verification
        verification = db.query(EmailVerification).filter(
            EmailVerification.email == email,
            EmailVerification.is_used == True
        ).order_by(EmailVerification.created_at.desc()).first()
        
        return verification is not None

# Global email service instance
email_service = EmailService()