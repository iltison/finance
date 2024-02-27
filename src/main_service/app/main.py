import uvicorn

from main_service.app.config import get_web_config
from main_service.app.controllers.web_api.app import app

if __name__ == "__main__":
    web_config = get_web_config()

    uvicorn.run(
        app,
        host=web_config.host,
        port=web_config.port,
        log_level=web_config.log_level,
        lifespan="on",
    )
