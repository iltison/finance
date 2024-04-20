import logging.config

import structlog


def configure_logger():
    time_stamper = structlog.processors.TimeStamper(fmt="iso")
    config = {
        "version": 1,
        "disable_existing_loggers": True,
        "formatters": {
            "colored": {
                "()": structlog.stdlib.ProcessorFormatter,
                "processors": [
                    time_stamper,
                    structlog.stdlib.add_log_level,
                    structlog.stdlib.add_logger_name,
                    structlog.contextvars.merge_contextvars,
                    structlog.processors.CallsiteParameterAdder(
                        {
                            structlog.processors.CallsiteParameter.MODULE,
                            structlog.processors.CallsiteParameter.FUNC_NAME,
                            structlog.processors.CallsiteParameter.THREAD,
                            structlog.processors.CallsiteParameter.THREAD_NAME,
                            structlog.processors.CallsiteParameter.PROCESS,
                            structlog.processors.CallsiteParameter.PROCESS_NAME,
                        }
                    ),
                    structlog.stdlib.ExtraAdder(),
                    structlog.dev.ConsoleRenderer(colors=True),
                ],
            },
        },
        "handlers": {
            "default": {
                "class": "logging.StreamHandler",
                "formatter": "colored",
                "level": "DEBUG",
            },
        },
        "loggers": {
            "default": {"handlers": ["default"]},
            "root": {"handlers": ["default"], "level": "DEBUG"},
            "uvicorn.access": {"handlers": ["default"]},
            "uvicorn.error": {"handlers": ["default"]},
        },
    }
    logging.config.dictConfig(config)
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.StackInfoRenderer(),
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )
    return config
