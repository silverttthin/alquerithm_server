from fastapi import FastAPI
from comment_domain.comment_routes import router as comment_router
from post_domain.post_routes import router as post_router
from user_domain.user_routes import router as user_router

app = FastAPI()

# 라우터 등록
app.include_router(comment_router, prefix="/comments", tags=["comments"])
app.include_router(post_router, prefix="/posts", tags=["posts"])
app.include_router(user_router, prefix="/users", tags=["users"])