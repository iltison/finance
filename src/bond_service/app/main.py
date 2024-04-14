import logging
import sys

import uvicorn

from main_service.app.config import get_web_config
from main_service.app.controllers.web_api.app import (
    production_application_factory,
)

app = production_application_factory()


def get_logger():
    # TODO: доделать
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=logging.INFO,
    )


def run():
    get_logger()
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
