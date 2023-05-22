from fastapi import APIRouter
from api.routers.v1.endpoints import login, users 

api_router = APIRouter()
api_router.include_router(login.router, tags=['User'])
api_router.include_router(login.router, prefix='/users', tags=['User'])

