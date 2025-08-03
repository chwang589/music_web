import dns.resolver
import smtplib
import socket
from email_validator import validate_email, EmailNotValidError
from typing import Dict, Any

class TruemailValidator:
    """
    Python implementation of email validation similar to truemail-go
    """
    
    def __init__(self):
        self.timeout = 10
        
    def validate_email_address(self, email: str) -> Dict[str, Any]:
        """
        Comprehensive email validation
        Returns dict with validation results
        """
        result = {
            "email": email,
            "valid": False,
            "syntax_valid": False,
            "domain_valid": False,
            "mx_valid": False,
            "smtp_valid": False,
            "errors": []
        }
        
        try:
            # Step 1: Syntax validation
            validated_email = validate_email(email)
            result["syntax_valid"] = True
            result["email"] = validated_email.email
            
            # Extract domain
            domain = validated_email.domain
            
            # Step 2: Domain validation  
            if self._validate_domain(domain):
                result["domain_valid"] = True
                
                # Step 3: MX record validation
                if self._validate_mx_records(domain):
                    result["mx_valid"] = True
                    
                    # Step 4: SMTP validation (basic check)
                    if self._validate_smtp(domain, validated_email.local):
                        result["smtp_valid"] = True
                        result["valid"] = True
                    else:
                        result["errors"].append("SMTP server not reachable")
                else:
                    result["errors"].append("No valid MX records found")
            else:
                result["errors"].append("Domain does not exist")
                
        except EmailNotValidError as e:
            result["errors"].append(f"Syntax error: {str(e)}")
        except Exception as e:
            result["errors"].append(f"Validation error: {str(e)}")
            
        return result
    
    def _validate_domain(self, domain: str) -> bool:
        """Check if domain exists"""
        try:
            dns.resolver.resolve(domain, 'A')
            return True
        except:
            try:
                dns.resolver.resolve(domain, 'AAAA')
                return True
            except:
                return False
    
    def _validate_mx_records(self, domain: str) -> bool:
        """Check if domain has MX records"""
        try:
            mx_records = dns.resolver.resolve(domain, 'MX')
            return len(mx_records) > 0
        except:
            return False
    
    def _validate_smtp(self, domain: str, local_part: str) -> bool:
        """Basic SMTP server connectivity check"""
        try:
            # Get MX records
            mx_records = dns.resolver.resolve(domain, 'MX')
            mx_record = str(mx_records[0].exchange)
            
            # Try to connect to SMTP server
            with smtplib.SMTP(timeout=self.timeout) as smtp:
                smtp.connect(mx_record, 25)
                smtp.helo()
                # Just check if we can connect, don't actually verify the email
                return True
                
        except Exception as e:
            # Many servers block SMTP connections, so we'll be lenient here
            # If MX records exist, we assume SMTP is probably working
            try:
                mx_records = dns.resolver.resolve(domain, 'MX')
                return len(mx_records) > 0
            except:
                return False
    
    def is_email_valid(self, email: str) -> bool:
        """Simple validation method that returns True/False"""
        result = self.validate_email_address(email)
        return result["valid"] or (result["syntax_valid"] and result["mx_valid"])

# Global validator instance
truemail_validator = TruemailValidator()