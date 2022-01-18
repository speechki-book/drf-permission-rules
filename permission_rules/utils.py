from permission_rules.app_settings import PERMISSION_RULES_SETTINGS
from permission_rules.connect import get_redis_connect


def clear_cache(chunk_size: int = 100) -> bool:
    if not PERMISSION_RULES_SETTINGS["use_redis"]:
        return False

    r = get_redis_connect()
    prefix = PERMISSION_RULES_SETTINGS["prefix"]

    cursor = 0
    ns_keys = prefix + "*"
    while cursor != 0:
        cursor, keys = r.scan(cursor=cursor, match=ns_keys, count=chunk_size)
        if keys:
            r.delete(*keys)

    return True
