AI Calling Agent 🤖📞

A multilingual AI-powered voice calling agent that conducts automated feedback calls in Hindi, English, and Hinglish — built to automate customer/client feedback collection through natural, human-like phone conversations.

🚀 Overview

This project automates outbound feedback calls using an LLM-driven conversational engine integrated with real-time voice infrastructure. The agent calls contacts from a Google Sheet, conducts a natural feedback conversation, generates a summary, and logs the results back to Google Sheets automatically — no manual follow-up needed.

✨ Key Features
Multilingual conversations — handles Hindi, English, and Hinglish naturally
Real-time voice calls — powered by Vapi (primary) with Twilio as backup telephony
Fast LLM inference — uses Groq as a cloud fallback, with local Ollama (phi3) support for offline/dev use
Automated contact pipeline — reads pending contacts from Google Sheets, places calls automatically, and updates their status (Pending → In Progress → Called)
Webhook-driven call handling — FastAPI backend listens for Vapi events (call start, live transcript, call end) in real time
Auto-generated feedback summaries — conversation transcripts are summarized and logged to a "Feedback" sheet after each call
Built-in safety filter — profanity filtering on the conversational layer
Local testing utilities — scripts to test Twilio connectivity and local Ollama inference independently
🛠️ Tech Stack
Component	Technology
Voice/Telephony	Vapi (primary), Twilio (backup)
LLM Inference	Groq (cloud), Ollama / phi3 (local)
Backend	FastAPI
Data Storage	Google Sheets (via gspread)
Language	Python
📂 Project Structure
├── server.py               # FastAPI server — handles Vapi webhooks, call lifecycle events
├── ai_brain.py              # Conversational logic, system prompt, LLM interaction, safety filter
├── config.py                # Loads all API keys/config from environment variables
├── make_calls.py            # Polls Google Sheets for new contacts and auto-triggers calls
├── google_sheets.py         # Google Sheets integration — read contacts, update status, save feedback
├── Test_twlio_phone.py      # Standalone script to test Twilio connectivity
├── test_ollama.py           # Standalone script to test local Ollama inference
├── requirements.txt         # Python dependencies
├── SETUP.md                 # Step-by-step setup guide
├── start_all.bat            # Windows script to launch the full stack
└── .env.example             # Environment variable template
⚙️ Setup
Clone the repository
bash
   git clone https://github.com/GodxCR7/Ai-calling-agent.git
   cd Ai-calling-agent
Install dependencies
bash
   pip install -r requirements.txt
Configure environment variables
bash
   cp .env.example .env
   # Fill in your Vapi, Twilio, Groq, and Deepgram keys
Add a Google Cloud service account credentials.json to the project root (required for Google Sheets access)
Set up your Google Sheet with a Contacts sheet (Name, Phone Number, Status columns) and a Feedback sheet
Run the project
bash
   # Windows
   start_all.bat

   # Or manually
   python server.py
   python make_calls.py

See SETUP.md for full step-by-step instructions.

📊 How It Works
make_calls.py polls the Google Sheet every 60 seconds for contacts with an empty Status
Once a new contact is found, it waits ~2 minutes, then triggers a call via Vapi
server.py receives real-time webhook events from Vapi as the call progresses (start, live transcript, end)
ai_brain.py drives the conversation — generating natural, multilingual responses in real time
When the call ends, the full conversation is summarized and saved to a local file
The contact's status is updated to Called, and the feedback summary is appended to the Feedback sheet
📝 Notes

This project was built as part of an AI/ML automation internship, focused on solving real-world feedback collection challenges through conversational AI and end-to-end workflow automation.

👤 Author

Pratik Nayak
GitHub: @GodxCR7
