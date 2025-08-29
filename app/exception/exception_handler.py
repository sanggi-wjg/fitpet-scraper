import logging

from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.enum.error_code_enum import ErrorCodeEnum
from app.exception.exceptions import FitpetScraperException

logger = logging.getLogger(__name__)


async def global_exception_handler(request: Request, exc: Exception):
    content = {
        "code": ErrorCodeEnum.INTERNAL_SERVER_ERROR.value,
        "message": "Internal server error",
        "detail": request.url.path,
    }
    logger.error(f"Internal server error: {content}")

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=content,
    )


async def fitpet_scraper_exception_handler(request: Request, exc: FitpetScraperException):
    content = {
        "code": exc.error_code.value,
        "message": exc.message,
        "detail": request.url.path,
    }
    logger.warning(content)

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=content,
    )
