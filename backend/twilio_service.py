import os
from dotenv import load_dotenv
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

load_dotenv()


def send_dispatch_sms(target_atm_id: str):

    # Demo mode: used because Twilio Trial blocks custom SMS templates
    demo_mode = os.getenv("DEMO_MODE", "true").lower() == "true"

    message_body = (
        f"🚨 MHA CRITICAL ALERT: Cash-out predicted at "
        f"{target_atm_id}. Execute interception immediately."
    )

    if demo_mode:
        print("\n========== DEMO SMS ==========")
        print("TO: Patrol Unit")
        print("MESSAGE:", message_body)
        print("===============================\n")

        return {
            "success": True,
            "mode": "demo",
            "message": message_body
        }

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

    try:
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            body=message_body,
            from_=twilio_phone,
            to=patrol_phone
        )

        return {
            "success": True,
            "mode": "twilio",
            "message_sid": message.sid,
            "status": message.status
        }

    except TwilioRestException as e:
        print("TWILIO ERROR:", e)

        raise RuntimeError(
            f"Twilio SMS failed: {e}"
        )