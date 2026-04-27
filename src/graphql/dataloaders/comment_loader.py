from aiodataloader import DataLoader
from typing import List, Dict, Any
from ...database.database import DataBase

class CommentLoader(DataLoader):
    
    def __init__(self, db: DataBase):
        super().__init__()
        self.db = db
    
    async def batch_load_fn(self, post_ids: List[str]) -> List[List[Dict]]:
        
        pipeline = [
            {"$match": {"post_id": {"$in": post_ids}, "parent_id": None}},
            {"$sort": {"datetime": -1}},
            {"$group": {
                "_id": "$post_id",
                "comments": {"$push": "$$ROOT"}
            }}
        ]
        
        cursor = self.db.comments.aggregate(pipeline)
        
        comments_by_post = {}
        
        async for doc in cursor:
            comments_by_post[doc["_id"]] = doc["comments"]
        
        return [comments_by_post.get(post_id, []) for post_id in post_ids]
    
