from decimal import Decimal
from typing import List

from pydantic import BaseModel, Field, field_validator

from app.util.util_string import clean_html_tags


class NaverShoppingApiResponse(BaseModel):
    class Item(BaseModel):
        title: str
        link: str
        image: str
        lprice: Decimal
        hprice: Decimal | None = Field(default=None)
        mall_name: str = Field(alias="mallName")
        product_id: str = Field(alias="productId")
        product_type: str = Field(alias="productType")
        brand: str
        maker: str
        category1: str
        category2: str
        category3: str
        category4: str

        @field_validator("title", mode="before")
        @classmethod
        def convert_title(cls, value: str) -> str:
            return clean_html_tags(value)

        @field_validator("lprice", mode="before")
        @classmethod
        def convert_lprice(cls, value: str) -> Decimal:
            return Decimal(value)

        @field_validator("hprice", mode="before")
        @classmethod
        def convert_hprice(cls, value: str) -> Decimal | None:
            if not value:
                return None
            return Decimal(value)

        @property
        def is_mall_name_naver(self) -> bool:
            return self.mall_name == "네이버"

    last_build_date: str = Field(alias="lastBuildDate")
    total: int
    start: int
    display: int
    items: List[Item]

    def has_items(self) -> bool:
        return len(self.items) > 0
