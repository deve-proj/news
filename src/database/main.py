from pymongo import MongoClient
from dotenv import load_dotenv
from motor import motor_asyncio
import os
from ..models.post_model import post_model
from fastapi import HTTPException
from bson import ObjectId
from typing import Dict, Any
from ..utils.jsonParser import replace_image_name_to_url_in_post
from datetime import datetime

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
        self.comments = self.db['comments']

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

            await self.update_views_counter_by_post_id(result["_id"])

            result["_id"] = str(result["_id"])

            return result
        
        except:

            raise HTTPException(status_code=400, detail="There isn't post with this id")
        
    async def create_post(self, post : post_model, user_id : str):

        try:

            post_id = ObjectId()

            json_post = post.model_dump()
            json_post = replace_image_name_to_url_in_post(post, post_id)
            print(json_post)
            json_post["views"] = 0
            json_post["_id"] = post_id
            json_post["datetime"] = datetime.now()

            await self.posts.insert_one(json_post)

            return post_id
        
        except Exception as e:

            return HTTPException(status_code=400, detail=str(e))
        
    async def delete_post(self, post_id : str, user_id : str):

        try:

            await self.posts.delete_one({"_id": ObjectId(post_id)})

        except Exception as e:

            return HTTPException(status_code=405, detail=str(e))
        
    async def update_post(self, post_id : str, new_content : post_model):

        try:

            post_data = new_content.model_dump()

            post_data["post"] = replace_image_name_to_url_in_post(new_content, post_id)

            await self.posts.update_one({"_id": ObjectId(post_id)}, {"$set": post_data})
            
        except Exception as e:

            return HTTPException(status_code=400, detail=str(e))
        

    async def update_views_counter_by_post_id(self, post_id : str):

        try:

            await self.posts.update_one({"_id": ObjectId(post_id)}, {"$inc": {"views": 1}})

        except Exception as e:

            return HTTPException(status_code=400, detail=str(e))
        
    async def add_comment(self, post_id, message):

        try:

            comment_id = (await self.comments.insert_one(message)).inserted_id

            await self.posts.update_one({'_id': ObjectId(post_id)}, {"$push": {"comments": comment_id}})

        except Exception as e:

            return HTTPException(status_code=400, detail=str(e))
        
    async def reply_to_comment(self, comment_id, message):

        try:

            reply_id = (await self.comments.insert_one(message)).inserted_id

            await self.comments.update_one({'_id': ObjectId(comment_id)}, {"$push": {"replies": reply_id}})

        except Exception as e:

            return HTTPException(status_code=400, detail=str(e))
        
    async def get_comments(self, post_id):

        try:

            result = []

            comment_ids = (await self.posts.find_one({'_id': ObjectId(post_id)})).get('comments', [])

            for comment_id in comment_ids:
                
                comment = await self.comments.find_one({'_id': comment_id, 'parent_id': None})

                comment['_id'] = str(comment['_id'])

                result.append(comment)

            return result

        except Exception as e:

            return HTTPException(status_code=400, detail=str(e))
        
    async def like(self, post_id : str):

        try:

            await self.posts.update_one({"_id": ObjectId(post_id)}, {"$inc": {"likes": 1}})

        except Exception as e:

            return HTTPException(status_code=400, detail=str(e))
        
    async def dislike(self, post_id : str):

        try:

            await self.posts.update_one({"_id": ObjectId(post_id)}, {"$inc": {"dislikes": 1}})

        except Exception as e:

            return HTTPException(status_code=400, detail=str(e))
        
    async def like_comment(self, comment_id : str):

        try:

            await self.comments.update_one({"_id": ObjectId(comment_id)}, {"$inc": {"likes": 1}})

        except Exception as e:

            return HTTPException(status_code=400, detail=str(e))
        
    async def dislike_comment(self, comment_id : str):

        try:

            await self.comments.update_one({"_id": ObjectId(comment_id)}, {"$inc": {"dislikes": 1}})

        except Exception as e:

            return HTTPException(status_code=400, detail=str(e))