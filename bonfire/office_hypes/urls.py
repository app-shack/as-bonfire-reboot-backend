from django.urls import path

from . import views

app_name = "office_hypes"


urlpatterns = [
    path(
        "todays-office-hype/",
        views.TodaysOfficeHypeView.as_view(),
        name="todays-office-hype",
    ),
    path(
        "last-weeks-office-hype/",
        views.LastWeeksOfficeHypeView.as_view(),
        name="last-weeks-office-hype",
    ),
    path(
        "todays-attendance/",
        views.TodaysAttendanceView.as_view(),
        name="todays-attendance",
    ),
]
