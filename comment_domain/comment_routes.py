from bson import ObjectId
from fastapi import APIRouter, Body, Depends, HTTPException
from database import comment_collection, post_collection
from comment_domain.comment_model import CommentModel
from auth import get_current_user
from user_domain.user_model import UserModel

router = APIRouter()

# 댓글 작성 엔드포인트
@router.post("/{post_id}/", response_model=CommentModel)
async def add_comment(post_id: str, comment: CommentModel = Body(...),
                      current_user: UserModel = Depends(get_current_user)):
    # 댓글 작성자의 ID와 게시글 ID 설정
    comment.post_id = post_id
    comment.author_id = str(current_user.id)

    # 새 댓글 데이터베이스에 삽입
    new_comment = await comment_collection.insert_one(comment.model_dump(by_alias=True, exclude=["id"]))
    # 삽입된 댓글 반환
    created_comment = await comment_collection.find_one({"_id": new_comment.inserted_id})

    # 댓글의 JSON 객체를 게시글의 comments 배열에 추가
    if created_comment:
        created_comment_model = CommentModel(**created_comment)
        await post_collection.update_one(
            {"_id": ObjectId(post_id)},
            {"$push": {"comments": created_comment_model.model_dump(by_alias=True)}}
        )
    return created_comment_model