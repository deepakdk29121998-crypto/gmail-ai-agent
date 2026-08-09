import os
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

Format:

{{
  "importance":"High | Medium | Low",
  "category":"Interview | Client | Bank | Personal | Promotion | Newsletter | Other",
  "summary":"Short summary",
  "needs_reply":true,
  "reply":"Professional email reply"
}}
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )

    return response.text