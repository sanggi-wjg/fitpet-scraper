LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            # "format": "%(asctime)s [%(levelname)-8s] %(name)-20s | %(funcName)s:%(lineno)d | %(message)s",
            "format": "%(asctime)s [%(levelname)s] %(name)s.%(funcName)s:%(lineno)d | %(message)s",
        },
    },
    "handlers": {
        "stream": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "level": "INFO",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "default",
            "level": "INFO",
            "filename": "app.log",
            "maxBytes": 1024 * 1024,  # 1MB
            "backupCount": 100,
            "encoding": "UTF-8",
        },
    },
    "loggers": {
        "": {
            "level": "INFO",
            "handlers": ["stream", "file"],
            "propagate": False,
        },
        "httpx": {
            "level": "WARNING",
            "handlers": ["stream"],
            "propagate": False,
        },
        "sqlalchemy.engine": {
            "level": "INFO",
            "handlers": ["stream", "file"],
            "propagate": False,
        },
        "celery": {
            "level": "INFO",
            "handlers": ["stream", "file"],
            "propagate": False,
        },
        "celery.task": {
            "level": "INFO",
            "handlers": ["stream", "file"],
            "propagate": False,
        },
    },
}
