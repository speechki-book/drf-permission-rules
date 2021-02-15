from django.contrib import admin
from django.db import models
from permission_rules.models import PermissionRule
from django_json_widget.widgets import JSONEditorWidget


@admin.register(PermissionRule)
class PermissionRuleAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "is_active"]
    search_fields = ["name"]
    list_filter = ["is_active"]

    formfield_overrides = {
        models.JSONField: {"widget": JSONEditorWidget},
    }
