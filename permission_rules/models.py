import json

from django.db import models

from model_utils.models import TimeStampedModel

from permission_rules.app_settings import PERMISSION_RULES_SETTINGS
from permission_rules.connect import get_redis_connect


PREFIX = PERMISSION_RULES_SETTINGS["prefix"]


class PermissionRule(TimeStampedModel):
    name = models.CharField(max_length=50)
    rule = models.JSONField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    @property
    def dump_rule(self):
        return json.dumps(self.rule)

    @property
    def key(self):
        return f"{PREFIX}{self.name}"

    @classmethod
    def send_data_to_cache(cls):
        r = get_redis_connect()
        pipe = r.pipeline()
        for obj in cls.objects.filter(is_active=True):
            pipe.set(obj.key, obj.dump_rule)

        pipe.execute()
