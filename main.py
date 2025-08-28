import argparse
import logging.config

from app.config.database import create_tables
from app.config.log import LOGGING_CONFIG

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description="FitpetScraper CLI")
    parser.add_argument("-c", "--create-tables", action="store_true", help="Create database tables.")
    parser.add_argument("-sn", "--scrape-naver-shopping", action="store_true", help="Scrape naver shopping.")
    parser.add_argument("-k", "--create-keyword", type=str, help="Create keywords.")
    args = parser.parse_args()

    if args.create_tables:
        create_tables()

    elif args.scrape_naver_shopping:
        from app.tasks.tasks import scrape_naver_shopping_task
        scrape_naver_shopping_task()

    elif args.create_keyword:
        from app.service.keyword_service import KeywordService
        keyword_service = KeywordService()
        keyword_service.create_keyword(args.create_keyword)


if __name__ == "__main__":
    main()
