from pydantic import BaseModel, BeforeValidator, Field
from typing import Annotated, List, Optional

pyObjectId = Annotated[str, BeforeValidator(str)]


class CommentModel(BaseModel):
    id: Optional[pyObjectId] = Field(alias="_id", default=None)
    content: str
    likes: int
    post_id: Optional[pyObjectId] = Field(alias="post_id", default=None) # 이 댓글이 달린 게시글 정보
    author_id: Optional[pyObjectId] = Field(alias="author_id", default=None) # 이 댓글을 쓴 놈 정보


class PostModel(BaseModel):
    id: Optional[pyObjectId] = Field(alias="_id", default=None)
    problemNum: str
    codeURL: str
    content: str
    result: str
    author_id: Optional[pyObjectId] = Field(alias="author_id", default=None)
    comments: List[CommentModel] = []


class UserModel(BaseModel):
    id: Optional[pyObjectId] = Field(alias="_id", default=None)
    username: str
    tags: List[str]
    alias_num: int

    my_posts: List[PostModel] = []
    commented_posts: List[CommentModel] = []
    # boormark는 좀 나중에


class PostCollection(BaseModel):
    posts: List[PostModel]



