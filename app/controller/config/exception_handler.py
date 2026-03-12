import logging
from datetime import UTC, datetime

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.exception.exceptions import FitpetScraperException


logger = logging.getLogger(__name__)


def register_exception_handlers(app: FastAPI) -> None:

    @app.exception_handler(Exception)
    async def exception_handler(request: Request, e: Exception):
        logger.exception(e)

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "status": f"{status.HTTP_500_INTERNAL_SERVER_ERROR} INTERNAL_SERVER_ERROR",
                "error": "Internal Server Error, please contact the administrator.",
                "path": request.url.path,
                "requestedAt": datetime.now(UTC.utc).isoformat(),
            },
        )

    @app.exception_handler(FitpetScraperException)
    def fitpet_scraper_exception_handler(request: Request, exc: FitpetScraperException):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "status": f"{status.HTTP_400_BAD_REQUEST} BAD_REQUEST",
                "error": exc.message,
                "path": request.url.path,
                "requestedAt": datetime.now(UTC.utc).isoformat(),
            },
        )
