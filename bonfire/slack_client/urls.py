from django.urls import path

from . import views

app_name = "slack_client"


urlpatterns = [
    path("work-location/", views.GetWorkLocationsView.as_view(), name="work-location"),
]
