from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel, Field
from twilio.base.exceptions import TwilioRestException

from auth import verify_jwt_token
from twilio_service import send_dispatch_sms


app = FastAPI(title="Project INDRA API")


class DispatchRequest(BaseModel):
    target_atm_id: str = Field(
        min_length=1,
        max_length=50
    )


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "message": "INDRA backend is running"
    }


@app.get("/protected-test")
def protected_test(user=Depends(verify_jwt_token)):
    return {
        "message": "JWT authentication successful",
        "user": user
    }


@app.post("/api/dispatch")
def dispatch_alert(
    request: DispatchRequest,
    user=Depends(verify_jwt_token)
):

    try:
        message_sid = send_dispatch_sms(
            request.target_atm_id
        )

    except RuntimeError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="SMS service is not configured"
        )

    except TwilioRestException:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="SMS dispatch failed"
        )

    return {
        "status": "success",
        "message": "Dispatch alert sent",
        "target_atm_id": request.target_atm_id,
        "requested_by": user["user_id"],
        "twilio_message_sid": message_sid
    }