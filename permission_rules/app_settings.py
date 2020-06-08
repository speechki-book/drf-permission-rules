from django.conf import settings

if settings.PERMISSION_RULES_SETTINGS is not None:
    PERMISSION_RULES_SETTINGS = settings.PERMISSION_RULES_SETTINGS
else:
    PERMISSION_RULES_SETTINGS = {
        "use_redis": False,
        "prefix": "permission_rule_",
        "redis": {
            "host": "localhost",
            "port": "6379",
            "db": 0,
            "password": ""
        }
    }
