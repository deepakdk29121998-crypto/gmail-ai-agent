# 🤖 Gmail AI Email Assistant

An AI-powered Gmail assistant that intelligently analyzes incoming emails, identifies important messages, categorizes them, generates professional reply drafts, applies Gmail labels, and manages follow-up reminders — while keeping the user in control of sending emails.

---

## 🚀 Project Overview

The Gmail AI Email Assistant combines the **Gmail API, Google Gemini AI, Python, OAuth 2.0, and automation** to reduce the time spent manually reviewing and responding to emails.

The system can:

- Read recent Gmail messages
- Analyze email importance
- Categorize emails
- Generate concise summaries
- Determine whether a reply is required
- Generate professional reply drafts
- Apply Gmail labels automatically
- Create follow-up reminders
- Ask for human approval before sending
- Reply inside the original Gmail conversation thread
- Track completed follow-ups
- Handle AI/API errors safely

---

## ✨ Key Features

### 📧 Gmail Integration
- Gmail API integration
- OAuth 2.0 authentication
- Read recent emails
- Extract sender, subject, body, thread ID and message ID

### 🧠 AI Email Analysis
Gemini analyzes each email and determines:

- Importance: High / Medium / Low
- Email category
- Email summary
- Whether a response is required
- Suggested professional response

### 🏷️ Automatic Gmail Labels

The assistant automatically applies labels such as:

- `AI-Processed`
- Email category labels
- `AI-High-Priority`
- `AI-Medium-Priority`

### ✍️ AI Reply Generation

For emails requiring a response, Gemini generates a professional reply draft.

The system **does not automatically send the response**.

The user must approve it first.

### 👤 Human-in-the-Loop Approval

Before sending an AI-generated reply:

```text
AI generates reply
        ↓
User reviews reply
        ↓
User selects Y / N
        ↓
Send only after approval