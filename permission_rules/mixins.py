from typing import List, Type

from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets

from drf_yasg.utils import swagger_auto_schema

from permission_rules.serializers import ViewSetPermissionsSerializer
from permission_rules.services.permissions_getter import PermissionsGetter


class PermissionActionMixinMeta(type):
    __inheritors__: List[Type[viewsets.GenericViewSet]] = []

    def __new__(cls, name, bases, dict_):
        class_ = type.__new__(cls, name, bases, dict_)

        if name != "PermissionsActionMixin":
            cls.__inheritors__.append(class_)  # type: ignore

        return class_


class PermissionsActionMixin(viewsets.GenericViewSet, metaclass=PermissionActionMixinMeta):
    def _get_permissions_map(self, request):
        permissions_map = PermissionsGetter.get_viewsets_permissions([self], request)
        return permissions_map[self.__class__.__name__]

    @swagger_auto_schema(method="get", responses={200: ViewSetPermissionsSerializer})
    @action(
        methods=["GET"],
        detail=False,
        url_name="permissions",
        permission_classes=(IsAuthenticated,),
    )
    def permissions(self, request, *ags, **kwargs):
        return Response(self._get_permissions_map(request))
