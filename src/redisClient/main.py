import redis.asyncio
from dotenv import load_dotenv
import os

load_dotenv()

class RedisClient:

    def __init__(self):
        
        pool = redis.ConnectionPool(

            host=os.getenv("REDIS_HOST"),
            port=os.getenv("REDIS_PORT"),
            db=0,
            decode_responses=True

        )

        self.r = redis.Redis(connection_pool=pool)

    async def test_connection(self) -> bool:

        return self.r.ping()
