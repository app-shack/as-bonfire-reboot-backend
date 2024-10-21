from django.urls import path

from . import views

app_name = "leaderboards"

urlpatterns = [
    path("list/", views.LeaderboardListView.as_view(), name="leaderboard-list"),
    path("<uuid:pk>/", views.LeaderboardView.as_view(), name="leaderboard"),
    path("create/", views.LeaderboardCreateView.as_view(), name="leaderboard-create"),
    path(
        "<uuid:leaderboard>/members/",
        views.LeaderboardMemberListView.as_view(),
        name="leaderboard-member-list",
    ),
    path(
        "members/create/",
        views.LeaderboardMemberCreateView.as_view(),
        name="leaderboard-member-create",
    ),
    path(
        "members/<uuid:pk>/",
        views.LeaderboardMemberView.as_view(),
        name="leaderboard-member",
    ),
    path(
        "add-match/",
        views.LeaderboardCreateMatchView.as_view(),
        name="leaderboard-add-match",
    ),
]
