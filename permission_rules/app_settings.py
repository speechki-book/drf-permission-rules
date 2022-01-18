from django.conf import settings


if hasattr(settings, "PERMISSION_RULES_SETTINGS"):
    PERMISSION_RULES_SETTINGS = settings.PERMISSION_RULES_SETTINGS
else:
    PERMISSION_RULES_SETTINGS = {
        "use_redis": False,
        "prefix": "permission_rule_",
        "redis": {"host": "localhost", "port": "6379", "db": 0, "password": ""},
        "use_file_instead_db": False,
        "permission_rules_file_path": "",
    }
