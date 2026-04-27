import redis
from dotenv import load_dotenv
import os
from typing import Any

load_dotenv()

class RedisClient:

    def __init__(self):
        
        pool = redis.asyncio.ConnectionPool(

            host=os.getenv("REDIS_HOST"),
            port=os.getenv("REDIS_PORT"),
            db=0,
            decode_responses=True

        )

        self.r = redis.asyncio.Redis(connection_pool=pool)

    async def test_connection(self) -> bool:

        return await self.r.ping()
    
    async def set(self, key: str, value : Any, expire : int = None) -> bool:

        await self.r.json().set(key, '$', value)

    async def get(self, key : str):

        return await self.r.json().get(key)