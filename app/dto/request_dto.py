from pydantic import BaseModel, Field


class CreateKeywordRequestDto(BaseModel):
    word: str = Field(description="추가할 키워드", min_length=1, max_length=255)
