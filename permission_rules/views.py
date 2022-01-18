from typing import Dict

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from drf_yasg.utils import swagger_auto_schema

from permission_rules.mixins import PermissionActionMixinMeta
from permission_rules.serializers import AllViewSetsPermissionsSerializer
from permission_rules.services.permissions_getter import ActionName, PermissionsGetter, ViewSetName


class PermissionsViewset(GenericViewSet):
    def _get_viewset_map(self, request) -> Dict[ViewSetName, Dict[ActionName, bool]]:
        viewsets = [vs() for vs in PermissionActionMixinMeta.__inheritors__]

        result = {}
        permissions_map = PermissionsGetter.get_viewsets_permissions(viewsets, request)

        for viewset_name in permissions_map:
            name = viewset_name.replace("ViewSet", "")
            result[name] = permissions_map[viewset_name]

        return result

    @swagger_auto_schema(method="get", responses={200: AllViewSetsPermissionsSerializer})
    @action(methods=["GET"], detail=False)
    def get(self, request, *args, **kwargs):
        return Response(self._get_viewset_map(request))
