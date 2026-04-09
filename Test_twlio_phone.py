# Download the helper library from https://www.twilio.com/docs/python/install
from dotenv import load_dotenv
load_dotenv()
import os
from twilio.rest import Client

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
client = Client(account_sid, auth_token)

call = client.calls.create(
    url="https://overdeep-nonflirtatiously-kym.ngrok-free.app/answer",
    to="+919606295698",
    from_="+16812992087",
)

print(f"Call initiated! SID: {call.sid}")