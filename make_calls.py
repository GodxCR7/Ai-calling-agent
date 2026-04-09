import os
import time
from datetime import datetime
import requests
from google_sheets import get_contacts, update_contact_status, save_feedback
SERVER_URL = "http://localhost:5000"
last_checked_rows = {}
def get_feedback(call_id):
    """Read saved feedback from file"""
    try:
        filename = f"feedback_{call_id}.txt"
        if os.path.exists(filename):
            with open(filename, "r") as f:
                content = f.read()
            # Extract summary (last line after "Summary: ")
            lines = content.split("\n")
            for line in lines:
                if line.startswith("Summary: "):
                    return line.replace("Summary: ", "")
            return content[:200]  # Return first 200 chars if no summary
    except:
        pass
    return "Call completed"
def make_vapi_call(phone, name):
    try:
        phone = str(phone)
        if not phone.startswith('+'):
            phone = '+' + phone
        
        response = requests.post(
            f"{SERVER_URL}/start-call",
            json={"phone": phone, "name": name},
            timeout=30
        )
        return response.json()
    except Exception as e:
        print(f"Error making Vapi call: {e}")
        return {"status": "error"}
def check_and_call():
    print(f"[{datetime.now()}] Checking for new contacts...")
    
    try:
        contacts = get_contacts()
        
        for index, contact in enumerate(contacts):
            status = contact.get('Status', '')
            phone = contact.get('Phone Number', '')
            name = contact.get('Name', '')
            
            if status == 'Called' or not phone:
                continue
            
            phone = str(phone)
            if not phone.startswith('+'):
                phone = '+' + phone
            
            row_key = f"{name}_{phone}"
            
            if row_key not in last_checked_rows:
                update_contact_status(index + 2, "In Progress")
                last_checked_rows[row_key] = {"time": datetime.now(), "call_id": None}
                print(f"Found new contact: {name} - {phone}")
                print(f"Will call {name} in 2 minutes...")
            
            else:
                time_since = (datetime.now() - last_checked_rows[row_key]["time"]).total_seconds()
                
                if time_since >= 120:
                    print(f"Calling {name} now...")
                    result = make_vapi_call(phone, name)
                    
                    if result.get("status") == "success":
                        call_id = result.get("call_id")
                        last_checked_rows[row_key]["call_id"] = call_id
                        
                        # Wait a bit for conversation to complete
                        time.sleep(15)
                        
                        # Get actual feedback
                        feedback = get_feedback(call_id)
                        
                        update_contact_status(index + 2, "Called")
                        save_feedback(name, phone, feedback)
                        print(f"Feedback saved for {name}: {feedback[:50]}...")
                        
                        del last_checked_rows[row_key]
                    else:
                        print(f"Call failed for {name}")
                        
    except Exception as e:
        print(f"Error checking contacts: {e}")
if __name__ == "__main__":
    print("Vapi AI Calling Agent - Auto Mode")
    print(f"Server: {SERVER_URL}")
    print("Press Ctrl+C to stop")
    print("-" * 50)
    
    while True:
        check_and_call()
        time.sleep(60)