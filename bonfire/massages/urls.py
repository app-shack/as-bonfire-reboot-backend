from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = "massages"

router = DefaultRouter()
router.register(
    "todays-queue",
    views.TodaysMassageQueueEntryViewSet,
    basename="todays-queue",
)

urlpatterns = [
    path("", include(router.urls)),
]
