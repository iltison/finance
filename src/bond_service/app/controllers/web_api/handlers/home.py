import structlog
from fastapi import APIRouter

from app.controllers.web_api.schemas.home import HomeResponse

home_router = APIRouter()

logger = structlog.get_logger(__name__)


@home_router.get("/")
async def get_home() -> HomeResponse:
    logger.info("get home")
    return HomeResponse(ok=True)
