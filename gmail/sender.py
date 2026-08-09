import base64
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from gmail.auth import authenticate


def send_email(to, subject, message, thread_id=None):

    creds = authenticate()

    service = build("gmail", "v1", credentials=creds)

    email = MIMEText(message)

    email["to"] = to
    email["subject"] = subject

    raw = base64.urlsafe_b64encode(
        email.as_bytes()
    ).decode()

    body = {
        "raw": raw
    }

    # If thread_id is available, send as a reply
    if thread_id:
        body["threadId"] = thread_id

    service.users().messages().send(
        userId="me",
        body=body
    ).execute()

    print("✅ Email Sent Successfully")