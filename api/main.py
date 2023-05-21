from api.database.settings import TORTOISE_ORM
from api.routers.v1.api import api_router as api_v1
from fastapi import FastAPI
from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise

app = FastAPI()
app.include_router(api_v1, prefix="/api/v1")

# Health Check
@app.get("/ping", tags=["Health Check"])
async def ping():
    return "pong"

register_tortoise(
    app=app,
    config=TORTOISE_ORM,
    add_exception_handlers=True,
)

