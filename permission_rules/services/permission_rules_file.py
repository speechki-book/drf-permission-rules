import json
from typing import Dict, List, Optional, Set, Union

from permission_rules.app_settings import PERMISSION_RULES_SETTINGS
from permission_rules.models import PermissionRule


USE_FILE = PERMISSION_RULES_SETTINGS["use_file_instead_db"]
FILE_PATH = PERMISSION_RULES_SETTINGS["permission_rules_file_path"]


class PermissionRulesFromFileContainer:
    _rules: Dict[str, PermissionRule] = {}
    _loaded: bool = False

    @classmethod
    def _load(cls):
        if cls._loaded:
            return

        with open(FILE_PATH, "r") as p_file:
            rules_data = json.loads(p_file.read())

        for p_dict in rules_data:
            p_rule_data = p_dict["fields"]

            cls._rules[p_rule_data["name"]] = PermissionRule(
                name=p_rule_data["name"],
                rule=p_rule_data["rule"],
                is_active=p_rule_data["is_active"],
            )

        cls._loaded = True

    @classmethod
    def get_permission_rule(cls, name: str) -> Optional[PermissionRule]:
        cls._load()

        return cls._rules.get(name, None)

    @classmethod
    def get_permission_rules(cls, names: Union[List[str], Set[str]]) -> List[PermissionRule]:
        cls._load()

        result = []

        for name in names:
            permission_rule = cls._rules.get(name, None)

            if permission_rule:
                result.append(permission_rule)

        return result
