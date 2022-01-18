from django.apps import AppConfig

from permission_rules.utils import clear_cache


class PermissionRulesConfig(AppConfig):
    name = "permission_rules"

    def ready(self):
        import permission_rules.signals

        clear_cache()
