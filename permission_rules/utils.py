from permission_rules.app_settings import PERMISSION_RULES_SETTINGS
from permission_rules.connect import get_redis_connect


def clear_cache(chunk_size: int = 100) -> bool:
    if not PERMISSION_RULES_SETTINGS["use_redis"]:
        return False

    r = get_redis_connect()
    prefix = PERMISSION_RULES_SETTINGS["prefix"]

    cursor = 0
    ns_keys = prefix + "*"
    # do/while: SCAN starts at cursor 0 and signals completion by returning cursor 0.
    while True:
        cursor, keys = r.scan(cursor=cursor, match=ns_keys, count=chunk_size)
        if keys:
            r.delete(*keys)
        if cursor == 0:
            break

    return True
