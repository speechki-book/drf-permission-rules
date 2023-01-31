# drf-permission-rules
permission rules for DRF base on drf access policy

## Installation

```
pip install drf-permission-rules
```

## Usage

### ViewSet permissions
```
class UserViewSet(ModelViewSet, PermissionsActionMixin):
    ...

    @action(methods=["GET", "POST"], detail=False)
    def some_action(self, request, *args, **kwargs):
        ...


GET /api/users/permissions
Response:
{
    "create": true,
    "list": true,
    "some_action": false
}
```

### Multiple ViewSet permissions

```
# views.py
class UserViewSet(ModelViewSet, PermissionsActionMixin):
    ...

class BookViewSet(ModelViewSet, PermissionsActionMixin):
    ...

class AuthorViewSet(ModelViewSet, PermissionsActionMixin):
    ...


# urls.py
urlpatterns = [
    ...
    path("api/", include("permission_rules.urls")),
]


GET /api/users/permissions
Response:
{
    "User": {
        "create": true
        "list": true,
        "some_action": false
    }
    "Book": {
        "create": true,
        "list": true
    },
    "Author": {
        "create": false,
        "list": true
    }
}
```


## Speedup

You can get permissions from a file instead of a database.

```
# settings.py


PERMISSION_RULES_SETTINGS = {
    "use_file_instead_db": true,
    "permission_rules_file_path": "/path/to/permissions.json"
}
```
