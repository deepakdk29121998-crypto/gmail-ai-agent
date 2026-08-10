import os
import json
from dotenv import load_dotenv
from google import genai

# Load the .env file
load_dotenv()

# Create Gemini client
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def ask_gemini(subject, body):

    prompt = f"""
You are an AI Email Assistant.

Analyze the email below.

Subject:
{subject}

Body:
{body}

Return ONLY a valid JSON object.
Do not use Markdown code fences.
Do not include ```json.
Do not include any explanation before or after the JSON.

Format:

{{
    "importance": "High | Medium | Low",
    "category": "Interview | Client | Bank | Personal | Promotion | Newsletter | Other",
    "summary": "Short summary",
    "needs_reply": true,
    "reply": "Professional email reply"
}}
"""

    try:

        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt
        )

        text = response.text.strip()

        # Remove Markdown code fences if Gemini adds them
        if text.startswith("```json"):
            text = text[7:]

        elif text.startswith("```"):
            text = text[3:]

        if text.endswith("```"):
            text = text[:-3]

        text = text.strip()

        # Validate that the response is valid JSON
        json.loads(text)

        return text

    except Exception as e:

        error_message = str(e)

        # Handle Gemini quota errors
        if "429" in error_message or "RESOURCE_EXHAUSTED" in error_message:

            print("\n⚠️ Gemini API quota has been exhausted.")
            print("Please wait for the quota to reset or check your Gemini API usage.")
            print("⏭️ Skipping this email...\n")

            raise RuntimeError(
                "Gemini API quota exhausted."
            )

        # Handle other Gemini API errors
        print("\n⚠️ Gemini API error.")
        print("Reason:", error_message)
        print("⏭️ Skipping this email...\n")

        raise