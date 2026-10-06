from functools import lru_cache

import redis

from permission_rules.app_settings import PERMISSION_RULES_SETTINGS

HOST = PERMISSION_RULES_SETTINGS["redis"]["host"]
PORT = PERMISSION_RULES_SETTINGS["redis"]["port"]
DB = PERMISSION_RULES_SETTINGS["redis"]["db"]
PASSWORD = PERMISSION_RULES_SETTINGS["redis"]["password"]
SSL = PERMISSION_RULES_SETTINGS["redis"].get("ssl", False)


@lru_cache(maxsize=1)
def get_redis_connect():
    # One client (connection pool) per process instead of a new connection per call. redis-py pools are
    # thread-safe and reset their connections after fork, so this is safe for prefork workers.
    return redis.Redis(host=HOST, port=PORT, db=DB, password=PASSWORD, ssl=SSL)


__all__ = ["get_redis_connect"]
