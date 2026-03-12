from sqlalchemy import select
from sqlalchemy.orm import Session

from app.entity.sitemap_source import SitemapSource


class SitemapSourceRepository:

    def __init__(self, session: Session):
        self.session = session

    def find_all(self) -> list[SitemapSource]:
        stmt = select(SitemapSource).order_by(SitemapSource.id)
        return list(self.session.scalars(stmt))
