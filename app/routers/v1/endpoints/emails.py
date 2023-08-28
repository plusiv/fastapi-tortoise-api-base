# -*- coding: utf-8 -*-
from fastapi import APIRouter, BackgroundTasks

from app.core import email
from app.routers.v1.dependencies import current_user

router = APIRouter()


@router.post("/test")
async def send_test_email(
    current_user: current_user,
    email_destination: str,
    background_tasks: BackgroundTasks,
):
    # Send email in the background
    background_tasks.add_task(
        email.send_wellcome,
        first_name=current_user.first_name,
        email_to=email_destination,
        user_id=current_user.id,
    )
    return {"message": "Notification sent in the background"}
