import redis
import os
from dotenv import load_dotenv

load_dotenv()


def get_redis_client():
    return redis.Redis(host="redis", port=6379, db=0)


async def is_content_processed(content_id: str) -> bool:
    client = get_redis_client()
    return client.exists(content_id) == 1


async def mark_content_processed(content_id: str):
    client = get_redis_client()
    client.set(content_id, "processed", ex=172800)
