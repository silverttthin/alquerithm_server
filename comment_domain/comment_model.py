from pydantic import BaseModel, BeforeValidator, Field
from typing import Annotated, Optional

pyObjectId = Annotated[str, BeforeValidator(str)]


class CommentModel(BaseModel):
    id: Optional[pyObjectId] = Field(alias="_id", default=None)
    content: str
    post_id: Optional[pyObjectId] = Field(alias="post_id", default=None)
    author_id: Optional[pyObjectId] = Field(alias="author_id", default=None)
