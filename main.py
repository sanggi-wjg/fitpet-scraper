from contextlib import asynccontextmanager
from logging.config import dictConfig

import uvicorn
from fastapi import FastAPI, BackgroundTasks, Depends
from sqlalchemy.orm import Session
from starlette import status

from app.controller.config.exception_handler import register_exception_handlers
from app.controller.dto.request_dto import CreateKeywordRequestDto
from app.core.background_scheduler import scheduler
from app.core.database import engine, get_db
from app.core.log import logging_config
from app.enum.channel_enum import ChannelEnum
from app.exception.exception_handler import global_exception_handler
from app.exception.exceptions import UnsupportedChannelException
from app.service.keyword_service import KeywordService
from app.task.scrape_tasks import scrape_naver_shopping_task

dictConfig(logging_config())


@asynccontextmanager
async def lifespan(_app: FastAPI):
    scheduler.start()
    yield
    scheduler.shutdown(wait=True)
    engine.dispose()


app = FastAPI()
register_exception_handlers(app)


@app.get("/", status_code=status.HTTP_200_OK, tags=["Root"])
async def root():
    return {"message": "Hello World"}


@app.get("/health", status_code=status.HTTP_200_OK, tags=["Health"])
async def health_check():
    return {"status": "healthy"}


@app.get(
    "/api/v1/keywords",
    status_code=status.HTTP_200_OK,
    tags=["Keyword"],
)
async def get_keywords(
    db: Session = Depends(get_db),
):
    service = KeywordService(db)
    return service.get_keywords()


@app.post(
    "/api/v1/keywords",
    status_code=status.HTTP_201_CREATED,
    tags=["Keyword"],
)
async def create_keyword_endpoint(
    request_dto: CreateKeywordRequestDto,
    db: Session = Depends(get_db),
):
    service = KeywordService(db)
    service.create_keyword(request_dto.word)
    return {"message": f"{request_dto.word} created successfully"}


@app.post(
    "/api/v1/scrape/{channel}",
    status_code=status.HTTP_202_ACCEPTED,
    tags=["Scrape"],
)
async def scrape_endpoint(
    channel: ChannelEnum,
    background_tasks: BackgroundTasks,
):
    if channel == ChannelEnum.NAVER_SHOPPING:
        background_tasks.add_task(scrape_naver_shopping_task)
    else:
        raise UnsupportedChannelException(channel)
    return {"message": "Scraping started in background"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        port=8010,
        reload=False,
        access_log=True,
        use_colors=True,
    )
