from pymongo import MongoClient
from dotenv import load_dotenv
from motor import motor_asyncio
import os

class dataBase:

    def __init__(self):

        load_dotenv()

        db_host = os.getenv("DB_HOST")
        db_port = os.getenv("DB_PORT")

        self.client = motor_asyncio.AsyncIOMotorClient(f"mongodb://{db_host}:{db_port}")
        self.db = self.client["news"]
        self.posts = self.db['posts']

    async def getPostsByAuthorId(self, authorId : int, limit = 10):

        result = await self.posts.find({"user_id": authorId}).to_list(length=limit)

        for post in result:

            post["_id"] = str(post["_id"])

        return result