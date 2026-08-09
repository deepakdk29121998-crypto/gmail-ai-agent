import json
from datetime import datetime, timedelta

from gmail.reader import get_latest_email, add_label
from gmail.sender import send_email
from ai.classifier import ask_gemini
from reminders import (
    save_reminder,
    get_due_reminders,
    complete_reminder
)


print("📧 Reading latest Gmail emails...\n")


# ============================================================
# CHECK FOR DUE FOLLOW-UP REMINDERS
# ============================================================

due_reminders = get_due_reminders()

if due_reminders:

    print("\n========== 📌 Due Follow-Ups ==========")

    for reminder in due_reminders:

        print("\n📩 From:", reminder["sender"])
        print("📌 Subject:", reminder["subject"])
        print("📅 Due Date:", reminder["reminder_date"])
        print("🔔 Status:", reminder["status"])

    print("\n=======================================\n")

else:

    print("📌 No follow-up reminders are due today.\n")


# ============================================================
# GET EMAILS
# ============================================================

emails = get_latest_email()

if not emails:

    print("❌ No emails found.")
    exit()


# ============================================================
# PROCESS EACH EMAIL
# ============================================================

for email in emails:

    sender = email["sender"]
    subject = email["subject"]
    body = email["body"]
    thread_id = email["thread_id"]
    message_id = email["message_id"]

    print("\n========================================")
    print("📩 From:", sender)
    print("📌 Subject:", subject)
    print("========================================")


    # ========================================================
    # AI ANALYSIS
    # ========================================================

    print("\n🤖 AI is analyzing the email...\n")

    try:

        response = ask_gemini(
            subject,
            body
        )

    except Exception as e:

        print("\n⚠️ Gemini API error.")
        print("Reason:", e)
        print("⏭️ Skipping this email and continuing...\n")

        continue


    # ========================================================
    # PARSE AI RESPONSE
    # ========================================================

    try:

        result = json.loads(response)

        required_fields = [
            "importance",
            "category",
            "summary",
            "needs_reply",
            "reply"
        ]

        missing_fields = [
            field
            for field in required_fields
            if field not in result
        ]

        if missing_fields:

            print(
                "❌ AI response is missing required fields:"
            )

            print(missing_fields)

            continue


        # ====================================================
        # VALIDATE IMPORTANCE
        # ====================================================

        valid_importance = [
            "high",
            "medium",
            "low"
        ]

        if result["importance"].lower() not in valid_importance:

            print(
                "❌ Invalid importance value:",
                result["importance"]
            )

            continue


        # ====================================================
        # VALIDATE NEEDS_REPLY
        # ====================================================

        if not isinstance(
            result["needs_reply"],
            bool
        ):

            print(
                "❌ Invalid needs_reply value:",
                result["needs_reply"]
            )

            continue


    except json.JSONDecodeError:

        print("❌ AI returned invalid JSON:")
        print(response)

        continue


    except Exception as e:

        print("❌ Error processing AI response:")
        print(e)

        continue


    # ========================================================
    # DISPLAY AI ANALYSIS
    # ========================================================

    print("\n========== AI Analysis ==========")

    print(
        "Importance :",
        result["importance"]
    )

    print(
        "Category   :",
        result["category"]
    )

    print(
        "Summary    :",
        result["summary"]
    )

    print(
        "Needs Reply:",
        result["needs_reply"]
    )

    print(
        "\n✅ AI analysis completed successfully."
    )

    print(
        "🏷️ Applying Gmail labels..."
    )


    # ========================================================
    # MARK EMAIL AS AI PROCESSED
    # ========================================================

    add_label(
        message_id,
        "AI-Processed"
    )

    print(
        "✅ AI-Processed label added."
    )


    # ========================================================
    # ADD CATEGORY LABEL
    # ========================================================

    category = result["category"]

    add_label(
        message_id,
        category
    )

    print(
        "🏷️ Category label added:",
        category
    )


    # ========================================================
    # CHECK IMPORTANCE
    # ========================================================

    importance = result["importance"].lower()

    if importance == "low":

        print(
            "\n⏭️ Low-importance email."
        )

        print(
            "No reply will be generated."
        )

        print(
            "Moving to the next email...\n"
        )

        continue


    # ========================================================
    # ADD PRIORITY LABEL
    # ========================================================

    if importance == "high":

        add_label(
            message_id,
            "AI-High-Priority"
        )

        print(
            "🔴 High-priority label added."
        )

    elif importance == "medium":

        add_label(
            message_id,
            "AI-Medium-Priority"
        )

        print(
            "🟡 Medium-priority label added."
        )


    # ========================================================
    # CREATE FOLLOW-UP REMINDER
    # ========================================================

    if result["needs_reply"]:

        reminder_date = (
            datetime.now() + timedelta(days=1)
        ).strftime("%Y-%m-%d")

        save_reminder(
            sender,
            subject,
            thread_id,
            reminder_date
        )

        print(
            "📅 Follow-up reminder created:",
            reminder_date
        )


    # ========================================================
    # CHECK WHETHER REPLY IS REQUIRED
    # ========================================================

    if not result["needs_reply"]:

        print(
            "\n⏭️ This email does not require a reply."
        )

        print(
            "Skipping reply approval...\n"
        )

        continue


    # ========================================================
    # DISPLAY GENERATED REPLY
    # ========================================================

    print(
        "\n========== Draft Reply ==========\n"
    )

    print(
        result["reply"]
    )


    # ========================================================
    # ASK PERMISSION BEFORE SENDING
    # ========================================================

    choice = input(
        "\nDo you want to send this reply? (Y/N): "
    ).strip().lower()


    if choice == "y":

        send_email(
            sender,
            "Re: " + subject,
            result["reply"],
            thread_id
        )

        complete_reminder(
            thread_id
        )

        print(
            "\n✅ Reply sent successfully to:",
            sender
        )

    else:

        print(
            "\n❌ Reply cancelled."
        )


# ============================================================
# FINISHED
# ============================================================

print(
    "\n========================================"
)

print(
    "🎉 Finished processing all emails."
)

print(
    "========================================"
)