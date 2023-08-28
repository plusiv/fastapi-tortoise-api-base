# -*- coding: utf-8 -*-
from fastapi import APIRouter

from app.routers.v1.endpoints import emails, login, sms, todos, users

router = APIRouter()
router.include_router(login.router, tags=["User"])
router.include_router(users.router, prefix="/users", tags=["User"])
router.include_router(todos.router, prefix="/todos", tags=["To Dos"])
router.include_router(emails.router, prefix="/emails", tags=["Emails"])
router.include_router(sms.router, prefix="/sms", tags=["SMS"])
