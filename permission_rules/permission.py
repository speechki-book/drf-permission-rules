import json
from typing import List, Optional

from rest_access_policy import AccessPolicy, AccessPolicyException

from permission_rules.app_settings import PERMISSION_RULES_SETTINGS
from permission_rules.connect import get_redis_connect
from permission_rules.services.permission_rules_getter import get_permission_rule


USE_REDIS = PERMISSION_RULES_SETTINGS["use_redis"]
USE_FILE = PERMISSION_RULES_SETTINGS["use_file_instead_db"]
PREFIX = PERMISSION_RULES_SETTINGS["prefix"]


class CustomAccessPolicy(AccessPolicy):
    name = ""
    DEFAULT_STATEMENTS = [
        {
            "action": ["*"],
            "principal": ["*"],
            "effect": "allow",
        }
    ]
    ADDITIONAL_STATEMENTS = []
    SAFE_METHODS = ("HEAD", "OPTIONS")

    @classmethod
    def scope_queryset(cls, request, qs, action: Optional[str] = None):
        return qs.none()

    def _get_statements_matching_action(self, request, action: str, statements: List[dict]):
        """
        Filter statements and return only those that match the specified
        action.
        """
        matched = []

        for statement in statements:
            if (action in statement["action"] or "*" in statement["action"]) or (
                "<safe_methods>" in statement["action"] and request.method in self.SAFE_METHODS
            ):

                matched.append(statement)

        return matched

    def get_user_group_values(self, user) -> List[str]:
        return getattr(user, "user_group_values", [])

    def _get_policy_statements_from_db(self) -> List[dict]:
        permission_rule = get_permission_rule(self.name)

        if permission_rule:
            return permission_rule.rule

        return self.DEFAULT_STATEMENTS

    def _get_policy_statements_from_redis(self) -> List[dict]:
        key = f"{PREFIX}{self.name}"

        r = get_redis_connect()
        statements_raw = r.get(key)

        if statements_raw is None:
            statements = self._get_policy_statements_from_db()
            r.set(key, json.dumps(statements))
        else:
            statements = json.loads(statements_raw)

        return statements + self.ADDITIONAL_STATEMENTS

    def get_policy_statements(self, request, view) -> List[dict]:
        if USE_REDIS and not USE_FILE:
            statements = self._get_policy_statements_from_redis()
        else:
            statements = self._get_policy_statements_from_db()

        return statements + self.ADDITIONAL_STATEMENTS

    def has_permission(self, request, view, action: Optional[str] = None) -> bool:
        if action is None:
            action = self._get_invoked_action(view)

        statements = self.get_policy_statements(request, view)
        if len(statements) == 0:
            return False

        return self._evaluate_statements(statements, request, view, action)

    def has_object_permission(self, request, view, obj, action: Optional[str] = None):
        if action is None:
            action = self._get_invoked_action(view)

        statements = self.get_policy_statements(request, view)
        if len(statements) == 0:
            return False

        return self._evaluate_statements(statements, request, view, action, obj)

    def _evaluate_statements(self, statements: List[dict], request, view, action: str, obj=None) -> bool:
        statements = self._normalize_statements(statements)
        matched = self._get_statements_matching_principal(request, statements)
        matched = self._get_statements_matching_action(request, action, matched)

        matched = self._get_statements_matching_context_conditions(request, view, action, matched, obj)

        denied = [_ for _ in matched if _["effect"] != "allow"]

        if len(matched) == 0 or len(denied) > 0:
            return False

        return True

    def _get_statements_matching_context_conditions(
        self, request, view, action: str, statements: List[dict], obj=None
    ):
        """
        Filter statements and only return those that match all of their
        custom context conditions; if no conditions are provided then
        the statement should be returned.
        """
        matched = []
        condition_name = "condition"
        if obj is not None:
            condition_name = "obj_condition"

        for statement in statements:
            if len(statement.get(condition_name, [])) == 0:
                matched.append(statement)
                continue

            fails = 0

            for condition in statement[condition_name]:
                passed = self._check_condition(condition, request, view, action, obj)

                if not passed:
                    fails += 1
                    break

            if fails == 0:
                matched.append(statement)

        return matched

    def _check_condition(self, condition: str, request, view, action: str, obj=None):
        """
        Evaluate a custom context condition; if method does not exist on
        the access policy class, then return False.
        Condition value can contain a value that is passed to method, if
        formatted as `<method_name>:<arg_value>`.
        """
        parts = condition.split(":", 1)
        method_name = parts[0]
        arg = parts[1] if len(parts) == 2 else None
        method = self._get_condition_method(method_name)

        if arg is not None:
            result = method(request, view, action, arg)
        elif obj is not None:
            result = method(request, view, action, obj)
        else:
            result = method(request, view, action)

        if type(result) is not bool:
            raise AccessPolicyException("condition '%s' must return true/false, not %s" % (condition, type(result)))

        return result


class AdminAccessPolicy(CustomAccessPolicy):
    DEFAULT_STATEMENTS = [
        {
            "action": ["*"],
            "principal": ["group:administrators"],
            "effect": "allow",
        }
    ]
