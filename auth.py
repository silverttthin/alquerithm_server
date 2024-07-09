import logging

from fastapi import Depends, HTTPException, status
from fastapi_login import LoginManager
from user_domain.user_model import UserModel
from database import user_collection

# 비밀 키 설정
SECRET = "your-secret-key"
# LoginManager 객체 생성
manager = LoginManager(SECRET, token_url="/users/login")


# 사용자 로더 함수: 사용자 이름을 통해 사용자 객체를 반환
@manager.user_loader()
async def load_user(username: str):
    logging.info(f"Loading user: {username}")
    user = await user_collection.find_one({"username": username})
    if user:
        return UserModel(**user)
    return None


# 사용자 인증 함수: 사용자 이름과 비밀번호를 확인하여 인증된 사용자 객체를 반환
async def authenticate_user(username: str, password: str):
    logging.info(f"Authenticating user: {username}")
    user = await load_user(username)
    if not user or user.password != password:
        return False
    return user


# 현재 로그인된 사용자 반환 함수
async def get_current_user(user=Depends(manager)):
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    logging.info(f"Authenticated user! : {user.username}")
    return user
