from fastapi import APIRouter, Body, Depends, HTTPException
from database import comment_collection, post_collection
from comment_domain.comment_model import CommentModel
from auth import get_current_user
from user_domain.user_model import UserModel

router = APIRouter()


# 댓글 작성 엔드포인트
@router.post("/posts/{post_id}/comments", response_description="Add comment to a post", response_model=CommentModel)
async def add_comment(post_id: str, comment: CommentModel = Body(...),
                      current_user: UserModel = Depends(get_current_user)):
    # 댓글 작성자의 ID와 게시글 ID 설정
    comment.post_id = post_id
    comment.author_id = str(current_user.id)
    # 새 댓글 데이터베이스에 삽입
    new_comment = await comment_collection.insert_one(comment.model_dump(by_alias=True, exclude=["id"]))
    # 삽입된 댓글 반환
    created_comment = await comment_collection.find_one({"_id": new_comment.inserted_id})

    # 게시글에 댓글 추가
    await post_collection.update_one({"_id": post_id}, {"$push": {"comments": created_comment}})
    return created_comment


# 댓글 추천 엔드포인트
@router.post("/comments/{comment_id}/like", response_description="Increase comment likes")
async def like_comment(comment_id: str, current_user: UserModel = Depends(get_current_user)):
    # 댓글 조회
    comment = await comment_collection.find_one({"_id": comment_id})
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    # 이미 추천했는지 확인
    if "liked_by" not in comment:
        comment["liked_by"] = []

    if current_user.id in comment["liked_by"]:
        raise HTTPException(status_code=400, detail="You have already liked this comment")

    # 추천 수 증가 및 추천자 목록에 추가
    await comment_collection.update_one(
        {"_id": comment_id},
        {"$inc": {"likes": 1}, "$push": {"liked_by": current_user.id}}
    )
    updated_comment = await comment_collection.find_one({"_id": comment_id})
    return updated_comment
