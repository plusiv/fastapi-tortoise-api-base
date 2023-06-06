# -*- coding: utf-8 -*-
from app.pydantic_models.messages import SentSMSPydantic
from app.routers.v1.dependencies import current_user
from app.core import sms

from fastapi import APIRouter, HTTPException, status


router = APIRouter()


@router.post("/test", response_model=SentSMSPydantic)
async def send_test_sms(current_user: current_user, number_destination: str):
    sent_sms = await sms.send_sms(
        number_destination, f"A test from {current_user.first_name}"
    )

    if not sent_sms.sent_at:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to send sms.",
        )

    return sent_sms
