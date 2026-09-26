AI Calling Agent
An automated voice-based feedback collection system that calls contacts and conducts natural, multilingual conversations using an AI model.

This workflow helps businesses automate customer/client feedback collection by calling contacts, gathering their responses, and logging structured feedback automatically — reducing manual follow-up effort.

Overview
The system reads pending contacts from a Google Sheet, places outbound calls to them, conducts a natural feedback conversation using an AI model, and logs the results automatically.

Outcomes include:

Feedback is collected and summarized after each call
Contact status is automatically updated as calls progress
Results are logged to Google Sheets for review
The system triggers calls via Vapi, drives the conversation using an LLM, and handles real-time call events through webhooks.

Workflow Logic
The automation follows this logic:

Contact Polling

Checks Google Sheets every 60 seconds for new contacts with no status
Call Trigger

Waits ~2 minutes, then places an outbound call via Vapi
Webhook Event Handling

FastAPI server listens for real-time call events (start, live transcript, end)
AI Conversation

LLM drives a natural, multilingual (Hindi/English/Hinglish) feedback conversation
Built-in profanity/safety filter applied to responses
Feedback Summary

Conversation transcript is summarized once the call ends
Update & Store

Contact status updated to "Called"
Feedback summary appended to the Google Sheet
Features
Multilingual voice conversations (Hindi, English, Hinglish)
Automated outbound calling pipeline
Real-time webhook-driven call handling
AI-generated feedback summaries
Automated status tracking and data logging in Google Sheets
Local + cloud LLM support (Ollama for offline, Groq for fast cloud inference)
Twilio backup telephony support
Built-in safety/profanity filter
Tech Stack
Vapi – Primary voice/telephony platform
Twilio – Backup telephony integration
Groq – Cloud LLM inference
Ollama (phi3) – Local LLM inference
FastAPI – Backend server for webhook handling
Google Sheets – Contact and feedback data storage
Python – Core language
Workflow Structure
Main components used in the system:

server.py – FastAPI server, handles Vapi webhooks and call lifecycle events
ai_brain.py – Conversational logic, system prompt, LLM interaction, safety filter
config.py – Loads API keys/configuration from environment variables
make_calls.py – Polls Google Sheets and auto-triggers calls
google_sheets.py – Reads contacts, updates status, saves feedback
Test_twlio_phone.py – Standalone Twilio connectivity test
test_ollama.py – Standalone local Ollama inference test
Use Case
This automation can be used by:

Businesses conducting post-service feedback calls
Sales/support teams following up with customers
Event or service-based companies collecting client feedback
Any workflow needing automated, conversational outbound calling
It helps reduce manual calling effort and automates structured feedback collection.

How to Use
Clone the repository

git clone https://github.com/GodxCR7/Ai-calling-agent.git
cd Ai-calling-agent
Install dependencies

pip install -r requirements.txt
Configure environment variables

cp .env.example .env
Fill in your Vapi, Twilio, Groq, and Deepgram keys

Add your Google Cloud service account credentials.json to the project root

Set up your Google Sheet with a Contacts sheet (Name, Phone Number, Status) and a Feedback sheet

Run the project

# Windows
start_all.bat

# Or manually
python server.py
python make_calls.py
See SETUP.md for full step-by-step instructions.

Future Improvements
Add retry logic for failed/missed calls
Support additional languages beyond Hindi/English/Hinglish
Build a dashboard for call analytics and feedback trends
Add authentication to webhook endpoints
Store call recordings alongside transcripts
Author
Pratik Nayak MCA Graduate | AI/ML Automation Enthusiast

Focused on building conversational AI and automation systems that reduce manual work and improve operational efficiency.
