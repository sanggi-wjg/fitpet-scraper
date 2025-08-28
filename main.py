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
    args = parser.parse_args()

    if args.create_tables:
        create_tables()

    if args.scrape_naver_shopping:
        from app.tasks.tasks import scrape_naver_shopping_task
        scrape_naver_shopping_task()


if __name__ == "__main__":
    main()
