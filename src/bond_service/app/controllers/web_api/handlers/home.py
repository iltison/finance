from fastapi import APIRouter

from app.controllers.web_api.schemas.home import HomeResponse

home_router = APIRouter()


@home_router.get("/")
async def get_home() -> HomeResponse:
    return HomeResponse(ok=True)
