from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from permission_rules.app_settings import PERMISSION_RULES_SETTINGS
from permission_rules.connect import get_redis_connect
from permission_rules.models import PermissionRule


USE_REDIS = PERMISSION_RULES_SETTINGS["use_redis"]


@receiver(post_save, sender=PermissionRule)
def cache_rule_signal(sender, instance, created, **kwargs):
    if USE_REDIS and instance.is_active:
        r = get_redis_connect()
        r.delete(*[instance.key])
        r.set(instance.key, instance.dump_rule)


@receiver(post_delete, sender=PermissionRule)
def remove_rule_from_cache_signal(sender, instance, using, **kwargs):
    if USE_REDIS:
        r = get_redis_connect()
        r.delete(*[instance.key])
