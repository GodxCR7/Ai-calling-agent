#  AI Calling Agent - Setup Guide

## FIRST READ THE COMPLETE DOCUMENTATION

## What You Need (Get from Pratik on WhatsApp)

- `.env` file
- `credentials.json` file

## Steps to Run

### 1. Place the files

- Drop `.env` and `credentials.json` into the project root folder

### 2. Install dependencies

```cmd
pip install -r requirements.txt
```

### 3. Add yourself to Google Sheet

- Open the shared Google Sheet (link shared on WhatsApp)
- Go to **Contacts** sheet
- Add a new row: your **Name**, **Phone Number** (with country code e.g. 91XXXXXXXXXX), leave **Status** empty

### 4. Update start_all.bat

- Open `start_all.bat`
- Change the `cd` path to your own project folder path

### 5. Run the project

- Double-click `start_all.bat`
- Wait \~2 minutes
- You will receive a call from the AI agent!

### 6. Check feedback

- Open the **Feedback** sheet in Google Sheets
- Your feedback summary will appear there after the call ends

---
