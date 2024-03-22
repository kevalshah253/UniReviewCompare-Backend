import redis
from src.utils.config import Config
redis_uri = redis.Redis(
    host=Config.REDIS_URL,
    port=18134,
    password=Config.REDIS_PASSWORD)
