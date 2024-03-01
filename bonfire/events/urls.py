from django.urls import include, path
from rest_framework import routers

from . import views

app_name = "events"

router = routers.DefaultRouter()
router.register("event", views.EventViewSet, basename="event")
router.register("booking", views.BookingViewSet, basename="booking")


urlpatterns = [
    path("", include(router.urls)),
]
