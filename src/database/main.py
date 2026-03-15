from pymongo import MongoClient
from dotenv import load_dotenv
from motor import motor_asyncio
import os
from ..models.post import post_model
from fastapi import HTTPException
from bson import ObjectId
from typing import Dict, Any
from ..common.jsonParser import replace_image_name_to_url_in_post

class DataBase:

    def __init__(self):

        load_dotenv()

        db_host = os.getenv("DB_HOST")
        db_port = os.getenv("DB_PORT")
        db_user = os.getenv("DB_USER")
        db_password = os.getenv("DB_PASSWORD")
        db_name = os.getenv("DB_NAME")

        db_url = f"mongodb://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}?authSource=admin"

        self.client = motor_asyncio.AsyncIOMotorClient(db_url)
        self.db = self.client[db_name]
        self.posts = self.db['posts']

    async def get_all_posts(self):

        try:

            result = await self.posts.find().to_list()

            for post in result:

                post["_id"] = str(post["_id"])
            
            return result
        
        except Exception as e:

            return HTTPException(status_code=400, detail=str(e))

    async def get_posts_by_user_id(self, user_id : str, limit = 10):

        try:

            result = await self.posts.find({"user_id": user_id}).to_list(length=limit)

            for post in result:

                post["_id"] = str(post["_id"])

            return result
        
        except Exception as e:

            return HTTPException(status_code=400, detail=str(e))
        
    async def get_post_by_post_id(self, post_id : str):

        try:

            result = await self.posts.find_one({"_id": ObjectId(post_id)})

            result["_id"] = str(result["_id"])

            return result
        
        except Exception as e:

            return HTTPException(status_code=400, detail=str(e))
        
    async def create_post(self, post : post_model, user_id : str):

        try:

            post_id = ObjectId()

            json_post = post.model_dump()
            json_post["views"] = 0
            json_post["_id"] = post_id
            json_post["post"] = replace_image_name_to_url_in_post(post, post_id)

            await self.posts.insert_one(json_post)

            return post_id
        
        except Exception as e:

            return HTTPException(status_code=400, detail=str(e))
        
    async def delete_post(self, post_id : str, user_id : str):

        try:

            post = await self.posts.find_one({"_id": ObjectId(post_id)})

            if post["user_id"] == user_id:

                await self.posts.delete_one({"_id": ObjectId(post_id)})

            else:

                return HTTPException(status_code=401, detail="You can't delete not yours post")
            
        except Exception as e:

            return HTTPException(status_code=400, detail=str(e))
        
    async def update_post(self, post_id : str, user_id : str, new_content : post_model):

        try:

            post = await self.posts.find_one({"_id": ObjectId(post_id)})

            if post["user_id"] == user_id:

                await self.posts.update_one({"_id": ObjectId(post_id)}, {"$set": new_content.model_dump()})

            else:

                return HTTPException(status_code=401, detail="You can't update not yours post")
        
        except Exception as e:

            return HTTPException(status_code=400, detail=str(e))
        

    async def update_views_counter_by_post_id(self, post_id : str):

        try:

            await self.posts.update_one({"_id": ObjectId(post_id)}, {"$inc": {"views": 1}})

        except Exception as e:

            return HTTPException(status_code=400, detail=str(e))