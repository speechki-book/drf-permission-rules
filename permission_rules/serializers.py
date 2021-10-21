from drf_yasg import openapi

from rest_framework import serializers


class ViewSetPermissionsSerializer(serializers.BaseSerializer):
    class Meta:
        swagger_schema_fields = {
            "type": openapi.TYPE_OBJECT,
            "properties": {
                "$action_name": openapi.Schema(
                    title="is allowd",
                    type=openapi.TYPE_BOOLEAN,
                ),
            },
        }


class AllViewSetsPermissionsSerializer(serializers.BaseSerializer):
    class Meta:
        swagger_schema_fields = {
            "type": openapi.TYPE_OBJECT,
            "properties": {
                "$viewset_name": ViewSetPermissionsSerializer.Meta.swagger_schema_fields,
            },
        }
