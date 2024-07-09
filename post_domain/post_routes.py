from fastapi import APIRouter, Body, Depends, HTTPException
from database import post_collection
from post_domain.post_model import PostModel, PostCollection
from auth import get_current_user
from user_domain.user_model import UserModel

router = APIRouter()


# 게시글 작성 엔드포인트
@router.post("/", response_description="Add new post", response_model=PostModel)
async def create_post(post: PostModel = Body(...), current_user: UserModel = Depends(get_current_user)):
    # 1. 현 유저의 ID값을 author_id 필드값으로 넣기
    post.author_id = str(current_user.id)
    # 2. 새 게시글 디비에 넣기
    new_post = await post_collection.insert_one(post.model_dump(by_alias=True, exclude=["id"]))

    # 삽입된 게시글 반환
    created_post = await post_collection.find_one({"_id": new_post.inserted_id})
    return created_post


# 게시글 조회 엔드포인트
@router.get("/", response_model=PostCollection)
async def get_posts():
    # 모든 게시글 조회
    posts = await post_collection.find().to_list(length=None)
    return PostCollection(posts=posts)

