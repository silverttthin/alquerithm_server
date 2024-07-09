from datetime import timedelta
from typing import List

from fastapi import APIRouter, Body, HTTPException, Depends
from auth import manager, authenticate_user
from user_domain.user_model import UserModel, UserLoginModel
from database import user_collection
from user_domain.user_service import get_3_tags, get_solved_list, get_solved_problems_today  # user_service.py 파일의 함수 임포트

router = APIRouter()



# 사용자 등록 엔드포인트
@router.post("/register", response_model=UserModel)
async def create_user(user: UserModel = Body(...)):
    # crawling 정보들 모델에 박아넣기 - top, bottom tag
    top_3_tags, bottom_3_tags = await get_3_tags(user.boj_username)
    user.most_tags = top_3_tags
    user.least_tags = bottom_3_tags

    # solved_list
    solved_list = await get_solved_list(user.boj_username)
    user.solved_list = solved_list

    # todays
    todays = await get_solved_problems_today(user.boj_username)
    user.today_solved = todays

    # 새 사용자 데이터베이스에 삽입
    new_user = await user_collection.insert_one(user.model_dump(by_alias=True, exclude=["id"]))
    # 삽입된 사용자 반환
    created_user = await user_collection.find_one({"_id": new_user.inserted_id})
    return created_user

# 로그인 엔드포인트
@router.post("/login")
async def login(data: UserLoginModel = Body(...)):
    # 사용자 인증
    user = await authenticate_user(data.username, data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    # 액세스 토큰 생성
    access_token = manager.create_access_token(data={"sub": user.username}, expires_delta=timedelta(hours=1000))
    return {"access_token": access_token, "token_type": "bearer"}


# 사용자 목록 조회 엔드포인트
@router.get("/", response_model=List[UserModel])
async def get_users():
    users = await user_collection.find().to_list(length=None)
    return users