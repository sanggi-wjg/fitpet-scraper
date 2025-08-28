from pydantic import BaseModel, ConfigDict


class KeywordModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    word: str
