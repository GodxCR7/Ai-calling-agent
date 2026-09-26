# 🤖 AI Calling Agent

An automated **AI-powered voice calling system** that places outbound calls, conducts natural multilingual conversations, collects customer feedback, and automatically stores structured results.

The system is designed to help businesses automate customer/client feedback collection by replacing repetitive manual follow-up calls with an intelligent conversational AI workflow.

---

## 📌 Overview

The AI Calling Agent automates the complete feedback collection process:

1. Reads pending contacts from **Google Sheets**
2. Automatically triggers outbound calls using **Vapi**
3. Conducts a natural conversation using an **LLM**
4. Supports **Hindi, English, and Hinglish**
5. Processes real-time call events through **FastAPI webhooks**
6. Summarizes the conversation using AI
7. Updates the contact's calling status
8. Stores the generated feedback summary back into **Google Sheets**

This creates an end-to-end automated pipeline for conversational customer feedback collection.

---

## 🏗️ Workflow Architecture

```text
┌─────────────────────┐
│    Google Sheets    │
│                     │
│ Name                │
│ Phone Number        │
│ Status              │
└──────────┬──────────┘
           │
           │ Poll every 60 seconds
           ▼
┌─────────────────────┐
│    make_calls.py    │
│                     │
│ Find pending calls  │
└──────────┬──────────┘
           │
           │ Trigger outbound call
           ▼
┌─────────────────────┐
│        Vapi         │
│                     │
│ Voice Call Engine   │
└──────────┬──────────┘
           │
           │ Real-time events
           ▼
┌─────────────────────┐
│      FastAPI        │
│      server.py      │
│                     │
│ Webhook Handler     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│     AI Brain        │
│    ai_brain.py      │
│                     │
│ LLM Conversation    │
│ Safety Filter       │
│ Feedback Processing │
└──────────┬──────────┘
           │
           │ Call completed
           ▼
┌─────────────────────┐
│   Feedback Summary  │
│                     │
│ AI-generated        │
│ conversation        │
│ summary             │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│    Google Sheets    │
│                     │
│ Status → Called     │
│ Feedback → Saved    │
└─────────────────────┘
```

---

## ✨ Features

- Multilingual voice conversations (Hindi, English, Hinglish)
- Automated outbound calling pipeline
- Real-time webhook-driven call handling
- AI-generated feedback summaries
- Automated status tracking and data logging in Google Sheets
- Local + cloud LLM support (Ollama for offline, Groq for fast cloud inference)
- Twilio backup telephony support
- Built-in safety/profanity filter

---

## 🛠️ Tech Stack

- **Vapi** – Primary voice/telephony platform
- **Twilio** – Backup telephony integration
- **Groq** – Cloud LLM inference
- **Ollama (phi3)** – Local LLM inference
- **FastAPI** – Backend server for webhook handling
- **Google Sheets** – Contact and feedback data storage
- **Python** – Core language

---

## 📂 Workflow Structure

Main components used in the system:

- `server.py` – FastAPI server, handles Vapi webhooks and call lifecycle events
- `ai_brain.py` – Conversational logic, system prompt, LLM interaction, safety filter
- `config.py` – Loads API keys/configuration from environment variables
- `make_calls.py` – Polls Google Sheets and auto-triggers calls
- `google_sheets.py` – Reads contacts, updates status, saves feedback
- `Test_twlio_phone.py` – Standalone Twilio connectivity test
- `test_ollama.py` – Standalone local Ollama inference test

---

## 🎯 Use Case

This automation can be used by:

- Businesses conducting post-service feedback calls
- Sales/support teams following up with customers
- Event or service-based companies collecting client feedback
- Any workflow needing automated, conversational outbound calling

It helps reduce manual calling effort and automates structured feedback collection.

---

## 🚀 How to Use

1. Clone the repository
```bash
   git clone https://github.com/GodxCR7/Ai-calling-agent.git
   cd Ai-calling-agent
```

2. Install dependencies
```bash
   pip install -r requirements.txt
```

3. Configure environment variables
```bash
   cp .env.example .env
```
   Fill in your Vapi, Twilio, Groq, and Deepgram keys

4. Add your Google Cloud service account `credentials.json` to the project root

5. Set up your Google Sheet with a Contacts sheet (Name, Phone Number, Status) and a Feedback sheet

6. Run the project
```bash
   # Windows
   start_all.bat

   # Or manually
   python server.py
   python make_calls.py
```

---

## 🔮 Future Improvements

- Add retry logic for failed/missed calls
- Support additional languages beyond Hindi/English/Hinglish
- Build a dashboard for call analytics and feedback trends
- Add authentication to webhook endpoints
- Store call recordings alongside transcripts

---

## 👤 Author

**Pratik Nayak**
MCA Graduate | AI/ML Automation Enthusiast

Focused on building conversational AI and automation systems that reduce manual work and improve operational efficiency.
