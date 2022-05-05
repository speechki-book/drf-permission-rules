from collections import defaultdict
from typing import Any, Dict, List, Type, Union

from rest_framework.permissions import BasePermission
from rest_framework import viewsets

from permission_rules.permission import CustomAccessPolicy
from permission_rules.services.permission_rules_getter import get_permission_rules


ViewSetName = str
ActionName = str
Permissions = List[Union[BasePermission, CustomAccessPolicy]]
PermissionClasses = List[Union[Type[BasePermission], Type[CustomAccessPolicy]]]


class CachedCustomAccessPolicy(CustomAccessPolicy):
    # For compatibility with AccessPolicy
    def __new__(cls, *args, **kwargs):
        if not args and not kwargs:
            return CustomAccessPolicy(*args, **kwargs)

        return super().__new__(cls)

    def __init__(self, name: str, original_permission: CustomAccessPolicy, cached_permissions):
        self.name = name
        self.original_permission = original_permission
        self.cached_statements = cached_permissions

    def __getattr__(self, name: str) -> Any:
        return getattr(self.original_permission, name)

    def get_policy_statements(self, request, view) -> List[dict]:
        statements = self.cached_statements.get(self.name, self.original_permission.DEFAULT_STATEMENTS)
        statements += self.original_permission.ADDITIONAL_STATEMENTS
        return statements


class PermissionsGetter:
    def __init__(self, viewsets: List[viewsets.GenericViewSet], request):
        self.viewsets = viewsets
        self.request = request

    def _get_not_detail_actions(self, viewset: viewsets.GenericViewSet) -> list:
        not_detail_actions = []

        list_action = getattr(viewset, "list", None)
        if list_action:
            not_detail_actions.append(list_action)

        create_action = getattr(viewset, "create", None)
        if create_action:
            not_detail_actions.append(create_action)

        actions = viewset.get_extra_actions()
        for view_action in actions:
            if not view_action.detail and view_action.__name__ != "permissions":
                not_detail_actions.append(view_action)

        return not_detail_actions

    def _get_viewset_permission_classes(self, viewset: viewsets.GenericViewSet) -> PermissionClasses:
        permission_classes: PermissionClasses = getattr(viewset.__class__, "permission_classes", [])

        if viewset.permission_classes:
            permission_classes += viewset.permission_classes

        return permission_classes

    def _get_cached_permissions(
        self, permission_classes_map: Dict[ViewSetName, PermissionClasses]
    ) -> Dict[ViewSetName, Permissions]:
        result = defaultdict(list)
        permission_rule_names = set()

        for viewset_name in permission_classes_map:
            for permission_class in permission_classes_map[viewset_name]:
                if issubclass(permission_class, CustomAccessPolicy):
                    permission_rule_names.add(permission_class.name)

        cached_permissions = {rule.name: rule.rule for rule in get_permission_rules(permission_rule_names)}

        for viewset_name in permission_classes_map:
            for permission_class in permission_classes_map[viewset_name]:
                if issubclass(permission_class, CustomAccessPolicy):
                    permission = CachedCustomAccessPolicy(
                        permission_class.name, permission_class(), cached_permissions
                    )
                else:
                    permission = permission_class()

                result[viewset_name].append(permission)

        return result

    def _get_permissions_map(self) -> Dict[ViewSetName, Permissions]:
        permissions_classes_map: Dict[ViewSetName, PermissionClasses] = {}

        for viewset in self.viewsets:
            name = viewset.__class__.__name__
            permissions_classes_map[name] = self._get_viewset_permission_classes(viewset)

        return self._get_cached_permissions(permissions_classes_map)

    def _check_permissions(
        self,
        viewset: viewsets.GenericViewSet,
        action,
        permissions: List[Union[BasePermission, CustomAccessPolicy]],
    ) -> bool:
        for permission in permissions:
            allowed = True

            if isinstance(permission, CustomAccessPolicy):
                allowed = permission.has_permission(self.request, viewset, action=action.__name__)
            else:
                allowed = permission.has_permission(self.request, viewset)

            if not allowed:
                return False

        return True

    def _get_viewsets_permissions(self) -> Dict[ViewSetName, Dict[ActionName, bool]]:
        permissions_map = self._get_permissions_map()

        result = {}

        for viewset in self.viewsets:
            viewset_name = viewset.__class__.__name__
            viewset_permissions = {}

            not_detail_actions = self._get_not_detail_actions(viewset)

            for action in not_detail_actions:
                viewset_permissions[action.__name__] = self._check_permissions(
                    viewset, action, permissions_map[viewset_name]
                )

            result[viewset_name] = viewset_permissions

        return result

    @classmethod
    def get_viewsets_permissions(
        cls, viewsets: List[viewsets.GenericViewSet], request
    ) -> Dict[ViewSetName, Dict[ActionName, bool]]:
        getter = cls(viewsets, request)
        return getter._get_viewsets_permissions()
