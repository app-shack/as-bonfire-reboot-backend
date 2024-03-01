from django.urls import include, path
from rest_framework import routers

from . import views

app_name = "offices"

router = routers.DefaultRouter()
router.register("office", views.OfficeViewSet, basename="office")


urlpatterns = [
    path("", include(router.urls)),
]
