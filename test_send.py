from gmail.sender import send_email

to_email = "aravind1996babu@gmail.com"   # Replace with your email
subject = "Test Email from Gmail AI Agent"

message = """
Hello,

This is a test email sent from my Gmail AI Agent using the Gmail API.

Regards,
Deepak's AI Agent
"""

send_email(to_email, subject, message)