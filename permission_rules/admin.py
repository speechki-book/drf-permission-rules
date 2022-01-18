from django.contrib import admin
from django.db import models

from django_json_widget.widgets import JSONEditorWidget

from permission_rules.models import PermissionRule


@admin.register(PermissionRule)
class PermissionRuleAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "is_active"]
    search_fields = ["name"]
    list_filter = ["is_active"]

    formfield_overrides = {
        models.JSONField: {"widget": JSONEditorWidget},
    }
