import redis
import os
from dotenv import load_dotenv

load_dotenv()

def get_redis_client():
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/1")
    return redis.Redis.from_url(redis_url)

async def is_content_processed(content_id: str) -> bool:
    client = get_redis_client()
    return client.exists(content_id) == 1

async def mark_content_processed(content_id: str):
    client = get_redis_client()
    client.set(content_id, "processed", ex=604800)
