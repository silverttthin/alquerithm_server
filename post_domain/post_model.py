from pydantic import BaseModel, BeforeValidator, Field
from typing import Annotated, List, Optional
from comment_domain.comment_model import CommentModel

pyObjectId = Annotated[str, BeforeValidator(str)]


class PostModel(BaseModel):
    id: Optional[pyObjectId] = Field(alias="_id", default=None)
    problemNum: str
    codeURL: str
    content: str
    result: str
    author_id: Optional[pyObjectId] = Field(alias="author_id", default=None)
    comments: List[CommentModel] = []


class PostCollection(BaseModel):
    posts: List[PostModel]
