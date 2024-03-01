from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

app_name = "users"


urlpatterns = [
    path("me/", views.UserMeView.as_view(), name="user-me"),
    path(
        "me/coordinates/",
        views.UserMeCoordinatesView.as_view(),
        name="user-me-coordinates",
    ),
    path("token/", views.UserTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
