import logging
import sys

import uvicorn

from main_service.app.config import get_web_config
from main_service.app.controllers.web_api.app import application_factory


def get_logger():
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=logging.INFO,
    )


def start_service():
    get_logger()
    web_config = get_web_config()

    uvicorn.run(
        application_factory(),
        host=web_config.host,
        port=web_config.port,
        log_level=web_config.log_level,
    )


if __name__ == "__main__":
    start_service()
