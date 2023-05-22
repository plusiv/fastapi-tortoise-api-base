from fastapi import APIRouter
from api.routers.v1.endpoints import login, users 

router = APIRouter()
router.include_router(login.router, tags=['User'])
router.include_router(users.router, prefix='/users', tags=['User'])

