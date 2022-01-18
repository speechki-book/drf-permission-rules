from rest_framework import fields

from permission_rules.permission import CustomAccessPolicy


class AccessPolicyPermissionsField(fields.Field):
    default_actions = ["create", "retrieve", "update", "destroy"]

    def __init__(self, actions=None, additional_actions=None, global_only=False, object_only=False, **kwargs):
        """See class description for parameters and usage"""
        assert not (
            global_only and object_only
        ), "Both global_only and object_only cannot be set to true on a AccessPolicyPermissionsField"
        self.action_method_map = {}

        self.global_only = global_only
        self.object_only = object_only
        self.actions = self.default_actions if (actions is None) else actions
        if additional_actions is not None:
            self.actions = self.actions + additional_actions

        kwargs["source"] = "*"
        kwargs["read_only"] = True

        self.permission = None

        super().__init__(**kwargs)

    def to_representation(self, value):
        """
        Calls the developer defined permission methods
        (both global and object) and formats the results into a dictionary.
        """
        results = {}

        request = self.context["request"]
        view = self.context["view"]
        permissions = [perm for perm in view.get_permissions() if isinstance(perm, CustomAccessPolicy)]

        if permissions:
            permission = permissions[0]
            for action in self.actions:
                global_cond = permission.has_permission(request, view, action=action)
                obj_cond = permission.has_object_permission(request, view, value, action=action)
                results[action] = global_cond and obj_cond

        return results
