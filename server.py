from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
import subprocess
import os
from dotenv import load_dotenv
from vapi import Vapi
load_dotenv()
from config import VAPI_API_KEY, VAPI_PHONE_NUMBER
from ai_brain import chat_with_ai, ai_brain_instance
from google_sheets import save_feedback, get_contacts
import json
app = FastAPI()
vapi_client = Vapi(token=VAPI_API_KEY)
active_calls = {}
@app.get("/")
def home():
    return {"message": "Vapi AI Calling Agent is running!", "vapi_phone": VAPI_PHONE_NUMBER}
@app.post("/vapi-webhook")
async def vapi_webhook(request: Request):
    try:
        body = await request.body()
        data = json.loads(body)
    except:
        return JSONResponse({"status": "ok"})
    
    event_type = data.get("type")
    print(f" Webhook event: {event_type}")
    
    if event_type == "conversation-started":
        call_id = data.get("call", {}).get("id")
        customer = data.get("call", {}).get("customer", {})
        customer_number = customer.get("number", "Unknown")
        if call_id:
            active_calls[call_id] = {
                "stage": "started",
                "conversation": [],
                "summary": "",
                "customer_number": customer_number
            }
            print(f" Call started: {call_id}")
    
    elif event_type == "conversation-ended":
        call_id = data.get("call", {}).get("id")
        if call_id and call_id in active_calls:
            conv_history = active_calls[call_id]["conversation"]
            customer_number = active_calls[call_id].get("customer_number", "Unknown")
            
            if conv_history:
                summary = generate_feedback_summary(conv_history)
            else:
                summary = "No conversation recorded"
            
            active_calls[call_id]["summary"] = summary
            
            # Save to text file
            with open(f"feedback_{call_id}.txt", "w") as f:
                f.write(f"Conversation: {' | '.join(conv_history)}\nSummary: {summary}\nPhone: {customer_number}")
            
            # Find contact name and save to Google Sheets
            contacts = get_contacts()
            contact_name = "Unknown"
            for c in contacts:
                if c.get("Phone Number") == customer_number:
                    contact_name = c.get("Name", "Unknown")
                    break
            
            save_feedback(contact_name, customer_number, summary)
            print(f"✓ Feedback saved to Google Sheets for {contact_name}")
            
            print(f" Call ended - saved feedback to feedback_{call_id}.txt")
            print(f" Summary: {summary}")
            del active_calls[call_id]
        
        ai_brain_instance.reset_conversation()
    
    elif event_type == "voice-activity":
        call_id = data.get("call", {}).get("id")
        transcript = data.get("message", {}).get("transcript", {})
        
        if transcript and call_id in active_calls:
            role = transcript.get("role", "unknown")
            text = transcript.get("text", "")
            
            if text and role != "unknown":
                active_calls[call_id]["conversation"].append(f"{role}: {text}")
                print(f" Transcript ({role}): {text[:60]}...")
    
    return JSONResponse({"status": "ok"})
def generate_feedback_summary(conv_history):
    """Generate a summary from the conversation history"""
    if not conv_history:
        return "No feedback collected"
    
    conversation_text = "\n".join(conv_history)
    
    summary_prompt = f"""Based on this conversation, provide a brief 1-2 sentence summary of the feedback:
{conversation_text}
Summary:"""
    
    try:
        result = subprocess.run(
            ["ollama", "run", "phi3", summary_prompt],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=20
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()[:200]
    except:
        pass
    
    return f"Feedback collected from {len(conv_history)} exchanges"
@app.post("/vapi-webhook/chat/completions")
@app.post("/v1/chat/completions")
async def vapi_llm_endpoint(request: Request):
    try:
        body = await request.body()
        data = json.loads(body)
        
        messages = data.get("messages", [])
        print(f" Received {len(messages)} messages from Vapi")
        
        ai_brain_instance.reset_conversation()
        latest_user_message = ""
        
        for msg in messages:
            role = msg.get("role", "")
            content = msg.get("content", "")
            if role == "user":
                ai_brain_instance.conversation_history.append({"role": "user", "content": content})
                latest_user_message = content
                print(f" User: {content[:50]}...")
            elif role == "assistant":
                ai_brain_instance.conversation_history.append({"role": "assistant", "content": content})
        
        # Call the real AI (Ollama or Groq fallback)
        print(" Calling AI brain...")
        ai_response = chat_with_ai(latest_user_message)
        
        print(f" AI Response: {ai_response[:80]}...")
        
        return JSONResponse({
            "choices": [{
                "message": {
                    "role": "assistant",
                    "content": ai_response
                },
                "finish_reason": "stop"
            }]
        })
        
    except Exception as e:
        print(f" Error in LLM endpoint: {e}")
        import traceback
        traceback.print_exc()
        return JSONResponse({"error": {"message": str(e)}}, status_code=500)
@app.post("/start-call")
async def start_call(request: Request):
    data = await request.json()
    phone = data.get("phone")
    
    try:
        phone = str(phone)
        if not phone.startswith('+'):
            phone = '+' + phone
        
        call = vapi_client.calls.create(
            phone_number_id="46d10882-d970-47d5-a929-703b2d3a7fd0",
            assistant_id="7763eebc-0b58-45af-84d1-62945cb64f12",
            customer={"number": phone}
        )
        
        print(f" Call started! ID: {call.id}")
        return JSONResponse({"status": "success", "call_id": call.id})
        
    except Exception as e:
        print(f"Error: {e}")
        return JSONResponse({"status": "error", "message": str(e)})
if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=5000, reload=True)