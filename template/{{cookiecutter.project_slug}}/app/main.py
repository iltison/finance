import uvicorn

from app.configs.config import get_web_config
from app.controllers.rest_api.app import production_application_factory

app = production_application_factory()


def run():
    web_config = get_web_config()
    uvicorn.run(
        app,
        host=web_config.host,
        port=web_config.port,
        log_level=web_config.log_level,
        lifespan="on",
    )


if __name__ == "__main__":
    run()
