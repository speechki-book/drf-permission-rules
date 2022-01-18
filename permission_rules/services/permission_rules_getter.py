from typing import List, Optional, Set, Union

from permission_rules.app_settings import PERMISSION_RULES_SETTINGS
from permission_rules.models import PermissionRule
from permission_rules.services.permission_rules_file import PermissionRulesFromFileContainer


USE_FILE = PERMISSION_RULES_SETTINGS["use_file_instead_db"]
FILE_PATH = PERMISSION_RULES_SETTINGS["permission_rules_file_path"]


def _get_permission_rule_from_db(name: str) -> Optional[PermissionRule]:
    try:
        return PermissionRule.objects.get(name=name)
    except PermissionRule.DoesNotExist:
        return None


def get_permission_rule(name: str) -> Optional[PermissionRule]:
    if USE_FILE:
        return PermissionRulesFromFileContainer.get_permission_rule(name)
    else:
        return _get_permission_rule_from_db(name)


def _get_permission_rules_from_db(names: Union[List[str], Set[str]]) -> List[PermissionRule]:
    return list(PermissionRule.objects.filter(name__in=names).all())


def get_permission_rules(names: Union[List[str], Set[str]]) -> List[PermissionRule]:
    if USE_FILE:
        return PermissionRulesFromFileContainer.get_permission_rules(names)
    else:
        return _get_permission_rules_from_db(names)
