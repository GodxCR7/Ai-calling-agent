import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
# Path to your credentials file
CREDENTIALS_FILE = "credentials.json"
def get_google_sheets_client():
    """Authenticate and return the Google Sheets client."""
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    credentials = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=scope)
    client = gspread.authorize(credentials)
    return client
def get_contacts():
    """Read contacts from the 'Contacts' sheet."""
    client = get_google_sheets_client()
    
    try:
        spreadsheet = client.open("AI Calling Agent")
        contacts_sheet = spreadsheet.worksheet("Contacts")
    except gspread.SpreadsheetNotFound:
        print("Spreadsheet 'AI Calling Agent' not found!")
        return []
    
    # Get all records from Contacts sheet
    records = contacts_sheet.get_all_records()
    return records
def update_contact_status(row_number, status):
    """Update the Status column in Contacts sheet."""
    client = get_google_sheets_client()
    spreadsheet = client.open("AI Calling Agent")
    contacts_sheet = spreadsheet.worksheet("Contacts")
    
    # Assuming column C (3) is Status
    contacts_sheet.update_cell(row_number, 3, status)
def save_feedback(name, phone, feedback_summary):
    """Save the feedback to the 'Feedback' sheet."""
    client = get_google_sheets_client()
    
    try:
        spreadsheet = client.open("AI Calling Agent")
        feedback_sheet = spreadsheet.worksheet("Feedback")
    except gspread.SpreadsheetNotFound:
        print("Spreadsheet 'AI Calling Agent' not found!")
        return
    
    # Append a new row with feedback
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    feedback_sheet.append_row([name, phone, feedback_summary, timestamp])
    print(f"Feedback saved for {name}")
# Test the connection
if __name__ == "__main__":
    print("Testing Google Sheets connection...")
    try:
        contacts = get_contacts()
        print(f"Found {len(contacts)} contacts!")
        for contact in contacts:
            print(contact)
    except Exception as e:
        print(f"Error: {e}")