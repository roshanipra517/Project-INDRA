import truststore

# Fix SSL certificate issue on Windows
truststore.inject_into_ssl()

import os
from dotenv import load_dotenv
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

# Load .env
load_dotenv()

# Get Twilio credentials
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_phone = os.getenv("TWILIO_PHONE_NUMBER")
my_phone = os.getenv("PATROL_PHONE_NUMBER")

# Check configuration
if not all([account_sid, auth_token, twilio_phone, my_phone]):
    print("ERROR: Twilio configuration is incomplete.")
    exit()

# Create Twilio client
client = Client(account_sid, auth_token)

try:
    # Send SMS
    message = client.messages.create(
        body="[MHA CYBER COMMAND] 🚨 ALERT: Imminent Cash-Out at ATM-PUNE-001. Dispatching nearest unit.",
        from_=twilio_phone,
        to=my_phone
    )

    print("SMS sent successfully!")
    print("Message SID:", message.sid)
    print("Status:", message.status)

except TwilioRestException as e:
    print("TWILIO ERROR")
    print("Error Code:", e.code)
    print("Error Message:", e.msg)
    print("HTTP Status:", e.status)