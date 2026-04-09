import os
from dotenv import load_dotenv
load_dotenv()
# Vapi AI
VAPI_API_KEY = os.getenv("VAPI_API_KEY")
VAPI_PHONE_NUMBER = os.getenv("VAPI_PHONE_NUMBER")
# Twilio (Backup)
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
# Deepgram
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
# OpenAI (not used)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# Ollama
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "phi3")
# Google Sheets
GOOGLE_CREDENTIALS_FILE = os.getenv("GOOGLE_SHEETS_CREDENTIALS", "credentials.json")
# Retelly (not used - keeping for reference)
RETELLY_API_KEY = os.getenv("RETELLY_API_KEY")