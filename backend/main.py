from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel, Field

from auth import verify_jwt_token
from twilio_service import send_dispatch_sms


app = FastAPI(title="Project INDRA API")


# ==============================
# Request Model
# ==============================

class DispatchRequest(BaseModel):
    target_atm_id: str = Field(
        min_length=1,
        max_length=50
    )


# ==============================
# Health Check
# ==============================

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "message": "INDRA backend is running"
    }


# ==============================
# JWT Protected Test
# ==============================

@app.get("/protected-test")
def protected_test(
    user=Depends(verify_jwt_token)
):
    return {
        "message": "JWT authentication successful",
        "user": user
    }


# ==============================
# Secure Dispatch API
# ==============================

@app.post("/api/dispatch")
def dispatch_alert(
    request: DispatchRequest,
    user=Depends(verify_jwt_token)
):

    try:
        # Send SMS / Demo Alert
        sms_result = send_dispatch_sms(
            request.target_atm_id
        )

    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

    # Successful response
    return {
        "status": "success",
        "message": "Dispatch alert sent",
        "target_atm_id": request.target_atm_id,
        "requested_by": user["user_id"],
        "dispatch": sms_result
    }