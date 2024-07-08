from fastapi import FastAPI, Body

# DB 가져오기
from database import user_collection
from database import post_collection
from database import comment_collection

from models import PostModel


app = FastAPI()


@app.post(
    "/posts/",
    response_description="Add new post",
    response_model=PostModel
)
async def create_post(post: PostModel = Body(...)):
    new_post = await post_collection.insert_one(post.model_dump(by_alias=True, exclude=["id"]))

    created_post = await post_collection.find_one({"_id": new_post.inserted_id})
    return created_post


