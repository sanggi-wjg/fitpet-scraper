from sqlalchemy.orm import Session


class ScrapedProductDetailRepository:

    def __init__(self, session: Session):
        self.session = session
