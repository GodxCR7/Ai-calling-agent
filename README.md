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
