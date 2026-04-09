import subprocess
import os
from importlib import import_module
from dotenv import load_dotenv
load_dotenv()
import groq
profanity = None
try:
    profanity = import_module("better_profanity").profanity
    profanity.load_censor_words()
    SAFETY_FILTER = True
    print("Safety filter enabled!")
except ImportError:
    SAFETY_FILTER = False
    print("Safety filter not available - skipping")
class AIBrain:
    def __init__(self):
        self.model = os.getenv("OLLAMA_MODEL", "phi3")
        self.conversation_history = []
        
        # Groq setup
        groq_api_key = os.getenv("GROQ_API_KEY")
        self.use_groq = bool(groq_api_key)
        if self.use_groq:
            self.groq_client = groq.Groq(api_key=groq_api_key)
            print("Groq fallback enabled!")
        
        self.system_prompt = """You are Pratik, a professional feedback collection agent from Fydo, an Indian event management company.
YOUR JOB:
- Call event managers to collect feedback about Fydo's event services
- Have a natural, friendly conversation
- Ask about their experience with recent events they attended or organized
- Get honest feedback to help improve services
CONVERSATION RULES:
1. Start with a greeting: "Hello, I am Pratik from Fydo. How was your experience with our event services?"
2. Listen to their response carefully
3. Ask follow-up questions like:
   - "What did you like most?"
   - "Was there anything that could be improved?"
   - "Would you recommend our services to others?"
4. Keep responses VERY SHORT (1 sentence only)
5. Be polite, professional, and genuine
IMPORTANT RULES:
- NEVER use profanity or inappropriate language
- If they seem busy, offer to call back at a better time
- If they don't want to talk, thank them politely and end
- Never argue or get defensive
- Always end the conversation graciously
Your responses should be conversational and natural."""
    def think(self, user_message: str) -> str:
        self.conversation_history.append({"role": "user", "content": user_message})
        
        full_prompt = f"{self.system_prompt}\n\n"
        
        for msg in self.conversation_history:
            role_label = "Human" if msg["role"] == "user" else "Pratik"
            full_prompt += f"{role_label}: {msg['content']}\n"
        
        full_prompt += "\nPratik's response (keep it VERY short, 1 sentence):"
        
        ai_response = None
        
        # Try Ollama first (local) - increased timeout to 30s
        try:
            result = subprocess.run(
                ["ollama", "run", self.model, full_prompt],
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace',
                timeout=30
            )
            if result.returncode == 0 and result.stdout.strip():
                ai_response = result.stdout.strip()
                print("Using Ollama (local)")
        except Exception as e:
            print(f"Ollama error: {e}")
        
        # Fallback to Groq if Ollama failed - using llama-3.1-8b-instant
        if not ai_response and self.use_groq:
            try:
                chat_completion = self.groq_client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "user", "content": full_prompt}]
                )
                ai_response = chat_completion.choices[0].message.content
                print("Using Groq (cloud fallback)")
            except Exception as e:
                print(f"Groq error: {e}")
        
        if not ai_response:
            return "Sure, I'd love to hear your thoughts."
        
        # Process response
        if SAFETY_FILTER:
            ai_response = profanity.censor(ai_response)
        
        first_period = ai_response.find('.')
        first_newline = ai_response.find('\n')
        
        if first_period != -1 and (first_newline == -1 or first_period < first_newline):
            ai_response = ai_response[:first_period + 1]
        elif first_newline != -1:
            ai_response = ai_response[:first_newline]
        
        ai_response = ai_response.strip()
        if len(ai_response) > 150:
            ai_response = ai_response[:150].rsplit(' ', 1)[0] + "."
        
        self.conversation_history.append({"role": "assistant", "content": ai_response})
        return ai_response
    def reset_conversation(self):
        self.conversation_history = []
ai_brain_instance = AIBrain()
def chat_with_ai(user_message: str) -> str:
    return ai_brain_instance.think(user_message)
if __name__ == "__main__":
    print("Testing AI Brain...")
    response = chat_with_ai("Hi")
    print(f"AI Response: {response}")