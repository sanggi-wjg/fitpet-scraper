from functools import lru_cache


@lru_cache
def logging_config():
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "()": "uvicorn.logging.DefaultFormatter",
                "fmt": "%(levelprefix)s %(message)s",
                "use_colors": None,
            },
            "access": {
                "()": "uvicorn.logging.AccessFormatter",
                "fmt": '%(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s',  # noqa: E501
            },
            "standard": {
                "format": "%(asctime)s [%(levelname)s] %(name)s.%(funcName)s:%(lineno)d | %(message)s",
            },
        },
        "handlers": {
            "default": {
                "level": "INFO",
                "formatter": "default",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            },
            "access": {
                "formatter": "access",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            },
            "standard": {
                "level": "DEBUG",
                "formatter": "standard",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            },
        },
        "loggers": {
            "": {
                "level": "INFO",
                "handlers": ["standard"],
                "propagate": False,
            },
            "uvicorn": {
                "handlers": ["default"],
                "level": "INFO",
                "propagate": False,
            },
            "uvicorn.access": {
                "handlers": ["access"],
                "level": "INFO",
                "propagate": False,
            },
            "uvicorn.error": {
                "level": "INFO",
            },
            # "httpx": {
            #     "level": "WARNING",
            #     "handlers": ["standard"],
            #     "propagate": False,
            # },
            # "sqlalchemy.engine": {
            #     "level": "DEBUG",
            #     "handlers": ["standard"],
            #     "propagate": False,
            # },
            # "celery": {
            #     "level": "INFO",
            #     "handlers": ["standard"],
            #     "propagate": False,
            # },
            # "celery.task": {
            #     "level": "INFO",
            #     "handlers": ["standard"],
            #     "propagate": False,
            # },
        },
    }


# def log_exception_handler(exc_type, exc_value, exc_traceback):
#     if issubclass(exc_type, KeyboardInterrupt):
#         sys.__excepthook__(exc_type, exc_value, exc_traceback)
#         return
#
#     logger = logging.getLogger(__name__)
#     logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))
