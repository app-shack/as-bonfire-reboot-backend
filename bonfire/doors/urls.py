from django.urls import path

from . import views

app_name = "doors"


urlpatterns = [
    path("door/dragon/", views.DoorView.as_view(), name="door-dragon"),
    path("door/dragon/lock/", views.DoorLockView.as_view(), name="door-dragon-lock"),
    path(
        "door/dragon/unlock/", views.DoorUnlockView.as_view(), name="door-dragon-unlock"
    ),
]
