import json
import os
from datetime import datetime


REMINDER_FILE = "reminders.json"


def load_reminders():
    """
    Load existing reminders from reminders.json.
    """

    if not os.path.exists(REMINDER_FILE):
        return []

    try:
        with open(
            REMINDER_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except (json.JSONDecodeError, FileNotFoundError):

        return []


def save_reminder(
    sender,
    subject,
    thread_id,
    reminder_date
):
    """
    Save a new follow-up reminder.
    """

    reminders = load_reminders()

    reminder = {
        "sender": sender,
        "subject": subject,
        "thread_id": thread_id,
        "reminder_date": reminder_date,
        "status": "Pending",
        "created_at": datetime.now().isoformat()
    }

    reminders.append(reminder)

    with open(
        REMINDER_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            reminders,
            file,
            indent=4
        )

    print("📌 Follow-up reminder saved.")


def get_due_reminders():
    """
    Return reminders that are due today.
    """

    reminders = load_reminders()

    today = datetime.now().strftime(
        "%Y-%m-%d"
    )

    due_reminders = []

    for reminder in reminders:

        if (
            reminder.get("reminder_date", "")
            <= today
            and reminder.get("status") == "Pending"
        ):

            due_reminders.append(
                reminder
            )

    return due_reminders


def complete_reminder(thread_id):
    """
    Mark a reminder as completed using its thread ID.
    """

    reminders = load_reminders()

    updated = False

    for reminder in reminders:

        if reminder.get("thread_id") == thread_id:

            reminder["status"] = "Completed"

            reminder["completed_at"] = (
                datetime.now().isoformat()
            )

            updated = True

    if updated:

        with open(
            REMINDER_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                reminders,
                file,
                indent=4
            )

        print(
            "✅ Follow-up reminder marked as completed."
        )

    else:

        print(
            "ℹ️ No matching reminder found."
        )