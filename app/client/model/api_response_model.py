import datetime
from decimal import Decimal

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
    items: list[Item]

    def has_items(self) -> bool:
        return len(self.items) > 0


class PetFriendsProductDetailApiResponse(BaseModel):
    class ProductDetailValue(BaseModel):
        product_id: int
        meta_product_name: str
        product_group1_name: str
        product_group2_name: str
        product_group3_name: str
        top_image_path: str | None
        top_image_name: str | None
        video_url: str | None
        pb_code: str
        brand_name: str
        product_type: str
        created_at: datetime.datetime
        updated_at: datetime.datetime | None
        first_open_date: datetime.datetime | None
        top_image_url: str
        product_badge_image_url: str
        review_count: int
        total_review_rating: float
        product_name: str
        minimum_price: str
        selling_price: Decimal
        discount_apply_price: Decimal
        discount_rate: int | None
        review_rating_average: float
        delivery_type_code: str

        @field_validator("selling_price", mode="before")
        @classmethod
        def convert_selling_price(cls, value: str) -> Decimal:
            return Decimal(value)

        @field_validator("discount_apply_price", mode="before")
        @classmethod
        def convert_discount_apply_price(cls, value: str) -> Decimal:
            return Decimal(value)

    class ProductDetail(BaseModel):
        status: str
        value: "PetFriendsProductDetailApiResponse.ProductDetailValue"

    class Data(BaseModel):
        product_detail: "PetFriendsProductDetailApiResponse.ProductDetail"

    status: str
    data: Data
