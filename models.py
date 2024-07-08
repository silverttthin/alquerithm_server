from pydantic import BaseModel, BeforeValidator, Field, ConfigDict
from typing import Annotated, List, Optional

pyObjectId = Annotated[str, BeforeValidator(str)]


class PostModel(BaseModel):
    id: Optional[pyObjectId] = Field(alias="_id", default=None)
    title: str
    content: str
    result: str
    author_id: str
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "title": "1000",
                "content": "1000번 문제 루비급 아님?",
                "result": "질문",
                "author_id": "123"
            }
        },
    )


class PostCollection(BaseModel):
    posts: List[PostModel]