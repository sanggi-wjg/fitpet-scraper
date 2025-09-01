from logging.config import dictConfig

import uvicorn
from fastapi import Depends, FastAPI
from starlette import status

from app.config.database import create_tables
from app.config.log import logging_config
from app.dto.request_dto import CreateKeywordRequestDto
from app.enum.channel_enum import ChannelEnum
from app.exception.exception_handler import fitpet_scraper_exception_handler, global_exception_handler
from app.exception.exceptions import UnsupportedChannelException, KeywordAlreadyExistsException, FitpetScraperException
from app.service.keyword_service import KeywordService, get_keyword_service
from app.task.tasks import scrape_naver_shopping_task

dictConfig(logging_config())
create_tables()

app = FastAPI()
app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(FitpetScraperException, fitpet_scraper_exception_handler)
app.add_exception_handler(KeywordAlreadyExistsException, fitpet_scraper_exception_handler)
app.add_exception_handler(UnsupportedChannelException, fitpet_scraper_exception_handler)


@app.get("/", status_code=status.HTTP_200_OK)
async def root():
    return {"message": "Hello World"}


@app.get("/api/v1/keywords", status_code=status.HTTP_200_OK)
async def get_keywords(
    keyword: KeywordService = Depends(get_keyword_service),
):
    return keyword.get_available_keywords()


@app.post("/api/v1/keywords", status_code=status.HTTP_201_CREATED)
async def create_keyword_endpoint(
    request_dto: CreateKeywordRequestDto,
    keyword_service: KeywordService = Depends(get_keyword_service),
):
    keyword_service.create_keyword(request_dto.word)
    return {"message": f"{request_dto.word} created successfully"}


@app.post("/api/v1/scrape/{channel}", status_code=status.HTTP_202_ACCEPTED)
async def scrape_endpoint(
    channel: ChannelEnum,
):
    if channel == ChannelEnum.NAVER_SHOPPING:
        scrape_naver_shopping_task.delay()
    else:
        raise UnsupportedChannelException(channel)
    return {"message": "Scraping started in background"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        port=8000,
        reload=False,
        reload_delay=3,
        use_colors=True,
    )
