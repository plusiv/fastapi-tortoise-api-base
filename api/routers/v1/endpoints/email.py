from api.pydantic_models.message import SentEmailPydantic
from api.routers.v1.dependencies import current_user
from api.core import email

from fastapi import APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from typing import Annotated


router = APIRouter()

@router.post("/test", response_model=SentEmailPydantic)
async def send_test_email(current_user: current_user, email_destination: str):
    sent_email = await email.send_wellcome(current_user.first_name, email_to=email_destination)

    if not sent_email.sent_at:
        raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Unable to send email.",
                )
    
    return sent_email

