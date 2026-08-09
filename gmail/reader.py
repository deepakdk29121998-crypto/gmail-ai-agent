import base64
import re

from googleapiclient.discovery import build
from gmail.auth import authenticate


def get_latest_email():
    """
    Fetch up to 10 inbox emails that have not been
    processed by the AI agent.

    Returns:
        list of email dictionaries
    """

    creds = authenticate()

    service = build(
        "gmail",
        "v1",
        credentials=creds
    )


    # ========================================================
    # GET INBOX EMAILS
    # ========================================================

    results = service.users().messages().list(
        userId="me",
        maxResults=10,
        labelIds=["INBOX"]
    ).execute()

    messages = results.get(
        "messages",
        []
    )


    if not messages:

        return []


    # ========================================================
    # FIND AI-PROCESSED LABEL
    # ========================================================

    labels_response = service.users().labels().list(
        userId="me"
    ).execute()

    labels = labels_response.get(
        "labels",
        []
    )


    processed_label_id = None


    for label in labels:

        if label["name"] == "AI-Processed":

            processed_label_id = label["id"]

            break


    # ========================================================
    # PROCESS EMAILS
    # ========================================================

    emails = []


    for msg in messages:

        # ----------------------------------------------------
        # Get message metadata
        # ----------------------------------------------------

        message_metadata = service.users().messages().get(
            userId="me",
            id=msg["id"],
            format="metadata"
        ).execute()


        message_labels = message_metadata.get(
            "labelIds",
            []
        )


        # ----------------------------------------------------
        # Skip already processed emails
        # ----------------------------------------------------

        if (
            processed_label_id
            and processed_label_id in message_labels
        ):

            continue


        # ----------------------------------------------------
        # Get complete email
        # ----------------------------------------------------

        message = service.users().messages().get(
            userId="me",
            id=msg["id"],
            format="full"
        ).execute()


        message_id = msg["id"]

        thread_id = message.get(
            "threadId"
        )


        payload = message.get(
            "payload",
            {}
        )


        headers = payload.get(
            "headers",
            []
        )


        # ----------------------------------------------------
        # Extract sender and subject
        # ----------------------------------------------------

        sender = ""
        subject = ""


        for header in headers:

            if header["name"].lower() == "from":

                sender = header["value"]


            elif header["name"].lower() == "subject":

                subject = header["value"]


        # ----------------------------------------------------
        # Extract email address from sender
        # ----------------------------------------------------

        match = re.search(
            r"<(.+?)>",
            sender
        )


        if match:

            sender = match.group(1)


        # ----------------------------------------------------
        # Extract email body
        # ----------------------------------------------------

        body = ""


        if "parts" in payload:

            for part in payload["parts"]:

                if part.get("mimeType") == "text/plain":

                    data = part.get(
                        "body",
                        {}
                    ).get("data")


                    if data:

                        body = base64.urlsafe_b64decode(
                            data
                        ).decode(
                            "utf-8",
                            errors="ignore"
                        )

                    break


        else:

            data = payload.get(
                "body",
                {}
            ).get("data")


            if data:

                body = base64.urlsafe_b64decode(
                    data
                ).decode(
                    "utf-8",
                    errors="ignore"
                )


        # ----------------------------------------------------
        # Store email
        # ----------------------------------------------------

        emails.append({

            "message_id": message_id,

            "sender": sender,

            "subject": subject,

            "body": body,

            "thread_id": thread_id

        })


    return emails


def add_label(
    message_id,
    label_name
):
    """
    Add a Gmail label to an email.
    Creates the label if it does not already exist.
    """

    creds = authenticate()

    service = build(
        "gmail",
        "v1",
        credentials=creds
    )


    # ========================================================
    # FIND EXISTING LABEL
    # ========================================================

    labels_response = service.users().labels().list(
        userId="me"
    ).execute()


    labels = labels_response.get(
        "labels",
        []
    )


    label_id = None


    for label in labels:

        if label["name"].lower() == label_name.lower():

            label_id = label["id"]

            break


    # ========================================================
    # CREATE LABEL IF NEEDED
    # ========================================================

    if not label_id:

        label_body = {
            "name": label_name
        }


        created_label = service.users().labels().create(
            userId="me",
            body=label_body
        ).execute()


        label_id = created_label["id"]


        print(
            f"🏷️ Created Gmail label: {label_name}"
        )


    # ========================================================
    # APPLY LABEL
    # ========================================================

    service.users().messages().modify(
        userId="me",
        id=message_id,
        body={
            "addLabelIds": [
                label_id
            ]
        }
    ).execute()


    print(
        f"🏷️ Label added: {label_name}"
    )