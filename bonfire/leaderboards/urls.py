from django.urls import path

from . import views

app_name = "leaderboards"

urlpatterns = [
    path("leaderboard/", views.LeaderboardView.as_view(), name="leaderboards"),
    path("create/", views.LeaderboardCreateView.as_view(), name="leaderboards-create"),
    path("delete/", views.LeaderboardDestroyView.as_view(), name="leaderboards-delete"),
    path(
        "add-match/",
        views.LeaderboardCreateMatchView.as_view(),
        name="leaderboards-add-match",
    ),
]
