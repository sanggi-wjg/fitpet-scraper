from logging.config import dictConfig

import uvicorn
from fastapi import Depends, FastAPI, HTTPException

from app.config.database import create_tables
from app.config.log import LOGGING_CONFIG
from app.dto.request_dto import CreateKeywordRequestDto
from app.enum.channel_enum import ChannelEnum
from app.exception.exception_handler import fitpet_scraper_exception_handler, global_exception_handler
from app.exception.exceptions import UnsupportedChannelException, KeywordAlreadyExistsException, FitpetScraperException
from app.service.keyword_service import KeywordService, get_keyword_service
from app.tasks.tasks import scrape_naver_shopping_task

dictConfig(LOGGING_CONFIG)

app = FastAPI()
app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(FitpetScraperException, fitpet_scraper_exception_handler)
app.add_exception_handler(KeywordAlreadyExistsException, fitpet_scraper_exception_handler)
app.add_exception_handler(UnsupportedChannelException, fitpet_scraper_exception_handler)


@app.post("/api/v1/keywords")
async def create_keyword_endpoint(
    request_dto: CreateKeywordRequestDto,
    keyword_service: KeywordService = Depends(get_keyword_service),
):
    result = keyword_service.create_keyword(request_dto.word)
    if not result:
        raise HTTPException(status_code=400, detail=f"{request_dto.word} 이미 존재합니다.")
    return {"message": f"{request_dto.word} created successfully"}


@app.post("/init/create-table")
async def create_tables_endpoint():
    create_tables()
    return {"message": "Tables created successfully"}


@app.post("/api/v1/scrape/{channel}")
async def scrape_endpoint(channel: ChannelEnum):
    if channel == ChannelEnum.NAVER_SHOPPING:
        scrape_naver_shopping_task()
    else:
        raise UnsupportedChannelException(channel)
    return {"message": "Scraping started successfully"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        port=8000,
        reload=True,
        reload_delay=3,
        use_colors=True,
    )
