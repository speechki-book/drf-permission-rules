import redis

from permission_rules.app_settings import PERMISSION_RULES_SETTINGS


HOST = PERMISSION_RULES_SETTINGS["redis"]["host"]
PORT = PERMISSION_RULES_SETTINGS["redis"]["port"]
DB = PERMISSION_RULES_SETTINGS["redis"]["db"]
PASSWORD = PERMISSION_RULES_SETTINGS["redis"]["password"]


def get_redis_connect():
    return redis.Redis(host=HOST, port=PORT, db=DB, password=PASSWORD)


__all__ = ["get_redis_connect"]
