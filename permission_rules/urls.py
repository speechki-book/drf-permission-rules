from django.urls import include, path

from rest_framework.routers import DefaultRouter

from permission_rules.views import PermissionsViewset


router = DefaultRouter()
router.register("", PermissionsViewset, basename="permissions")

urlpatterns = [path("permissions/", include(router.urls))]
