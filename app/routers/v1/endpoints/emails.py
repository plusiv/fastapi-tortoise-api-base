# -*- coding: utf-8 -*-
from app.pydantic_models.messages import SentEmailPydantic
from app.routers.v1.dependencies import current_user
from app.core import email

from fastapi import APIRouter, HTTPException, status


router = APIRouter()


@router.post("/test", response_model=SentEmailPydantic)
async def send_test_email(current_user: current_user, email_destination: str):
    sent_email = await email.send_wellcome(
        first_name=current_user.first_name,
        email_to=email_destination,
        user_id=current_user.id,
    )

    if not sent_email.sent_at:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to send email.",
        )

    return sent_email
