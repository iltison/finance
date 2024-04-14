from app.controllers.web_api.schemas.home import HomeResponse
from fastapi import APIRouter

home_router = APIRouter()


@home_router.get("/")
async def get_home() -> HomeResponse:
    return HomeResponse(ok=True)
