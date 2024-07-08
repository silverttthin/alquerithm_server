from motor.motor_asyncio import AsyncIOMotorClient

MONGO_DETAILS = "mongodb+srv://sco3o17:1q2w3e4r@cluster0.al5hilk.mongodb.net/"

client = AsyncIOMotorClient(MONGO_DETAILS)
post_database = client.Post
user_database = client.User
comment_database = client.Commnet

user_collection = user_database.get_collection("user")
post_collection = post_database.get_collection("post")
comment_collection = comment_database.get_collection("comment")


