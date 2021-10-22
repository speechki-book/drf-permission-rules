# drf-permission-rules
permission rules for DRF base on drf access policy

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
