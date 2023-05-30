# -*- coding: utf-8 -*-
from fastapi import APIRouter
from app.routers.v1.endpoints import login, users, email, sms

router = APIRouter()
router.include_router(login.router, tags=["User"])
router.include_router(users.router, prefix="/users", tags=["User"])
router.include_router(email.router, prefix="/email", tags=["Emails"])
router.include_router(sms.router, prefix="/sms", tags=["SMS"])
