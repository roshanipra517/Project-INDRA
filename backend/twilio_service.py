import os

from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()


def send_dispatch_sms(target_atm_id: str):
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    twilio_phone = os.getenv("TWILIO_PHONE_NUMBER")
    patrol_phone = os.getenv("PATROL_PHONE_NUMBER")

    if not all([
        account_sid,
        auth_token,
        twilio_phone,
        patrol_phone
    ]):
        raise RuntimeError("Twilio configuration is incomplete")

    client = Client(account_sid, auth_token)

    message_body = (
        f"[MHA CYBER COMMAND] 🚨 ALERT: "
        f"Imminent Cash-Out at {target_atm_id}. "
        f"Dispatching nearest unit."
    )

    message = client.messages.create(
        body=message_body,
        from_=twilio_phone,
        to=patrol_phone
    )

    return message.sid