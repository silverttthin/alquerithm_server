from pydantic import BaseModel, Field, BeforeValidator
from typing import List, Optional, Annotated
from post_domain.post_model import PostModel
from comment_domain.comment_model import CommentModel

pyObjectId = Annotated[str, BeforeValidator(str)]


class UserModel(BaseModel):
    id: Optional[pyObjectId] = Field(alias="_id", default=None)
    username: str
    password: str
    boj_username: str

    #----crawling fields-------------------ㄱ
    most_tags: List[str] = []
    least_tags: List[str] = []
    alias_num: int = 3
    solved_list: List[str] = []
    #ㄴ--------------------------------------

    my_posts: List[PostModel] = []
    commented_posts: List[CommentModel] = []

class UserLoginModel(BaseModel):
    username: str
    password: str