import logging.config
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class LoggingConfig:
    level: str = "INFO"  # 루트 로거 레벨
    uvicorn_level: str = "INFO"
    apscheduler_level: str = "WARNING"
    sqlalchemy_level: str = "WARNING"
    format: str = "%(asctime)s.%(msecs)03d [%(levelname)-8s] %(name)s | " "%(funcName)s:%(lineno)d — %(message)s"
    date_format: str = "%Y-%m-%d %H:%M:%S"


def setup_logging():
    logging_config = LoggingConfig()

    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "format": logging_config.format,
                    "datefmt": logging_config.date_format,
                },
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                    "stream": "ext://sys.stdout",
                },
            },
            "root": {
                "level": logging_config.level,
                "handlers": ["console"],
            },
            "loggers": {
                "uvicorn": {
                    "level": logging_config.uvicorn_level,
                    "handlers": ["console"],
                    "propagate": False,
                },
                "uvicorn.error": {
                    "level": logging_config.uvicorn_level,
                    "handlers": ["console"],
                    "propagate": False,
                },
                "uvicorn.access": {
                    "level": logging_config.uvicorn_level,
                    "handlers": ["console"],
                    "propagate": False,
                },
                "apscheduler": {
                    "level": logging_config.apscheduler_level,
                    "handlers": ["console"],
                    "propagate": False,
                },
                "sqlalchemy.engine": {
                    "level": logging_config.sqlalchemy_level,
                    "handlers": ["console"],
                    "propagate": False,
                },
            },
        }
    )
