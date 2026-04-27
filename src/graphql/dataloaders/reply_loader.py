from aiodataloader import DataLoader
from ...database.database import DataBase
from typing import List, Dict

class ReplyLoader(DataLoader):
    
    def __init__(self, db: DataBase):
        super().__init__()
        self.db = db
    
    async def batch_load_fn(self, parent_ids: List[str]) -> List[List[Dict]]:
        
        pipeline = [
            {"$match": {"parent_id": {"$in": parent_ids}}},
            {"$sort": {"datetime": -1}},
            {"$group": {
                "_id": "$parent_id",
                "replies": {"$push": "$$ROOT"}
            }}
        ]
        
        cursor = self.db.comments.aggregate(pipeline)
        
        replies_by_parent = {}
        
        async for doc in cursor:
            replies_by_parent[doc["_id"]] = doc["replies"]
        
        return [replies_by_parent.get(parent_id, []) for parent_id in parent_ids]