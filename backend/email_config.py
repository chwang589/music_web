# Email Configuration
# To enable real email sending:
# 1. Set ENABLE_EMAIL_SENDING = True
# 2. Configure your Gmail account below
# 3. Use an "App Password" for Gmail (not your regular password)
# 4. Enable 2-step verification on Gmail and generate an app password

ENABLE_EMAIL_SENDING = True  # Set to True to send real emails

# Gmail Configuration (example)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = "wphtlip@gmail.com"  # Replace with your Gmail
EMAIL_PASSWORD = "nmlf wfjr bsbr ifqh"    # Replace with your Gmail app password

# Email Templates
EMAIL_SUBJECT = "Music Web - Email Verification Code"
EMAIL_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
    <div style="background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 30px; border-radius: 10px 10px 0 0; text-align: center;">
        <h1 style="margin: 0; font-size: 28px;">🎵 Music Web</h1>
        <p style="margin: 10px 0 0 0; font-size: 16px;">Email Verification</p>
    </div>
    
    <div style="background: #f8f9fa; padding: 30px; border-radius: 0 0 10px 10px;">
        <h2 style="color: #667eea; margin-top: 0;">Verification Code</h2>
        <p>Thank you for registering with Music Web! Please use the verification code below to complete your registration:</p>
        
        <div style="background: white; padding: 20px; margin: 20px 0; border-radius: 8px; text-align: center; border: 2px solid #667eea;">
            <h1 style="color: #667eea; font-size: 36px; margin: 0; letter-spacing: 8px; font-family: 'Courier New', monospace;">{verification_code}</h1>
        </div>
        
        <p><strong>⏰ This code will expire in 10 minutes.</strong></p>
        
        <p>If you didn't request this verification, you can safely ignore this email.</p>
        
        <hr style="border: none; border-top: 1px solid #e9ecef; margin: 30px 0;">
        
        <p style="color: #6c757d; font-size: 12px; text-align: center;">
            This is an automated message from Music Web. Please do not reply to this email.
        </p>
    </div>
</body>
</html>
"""