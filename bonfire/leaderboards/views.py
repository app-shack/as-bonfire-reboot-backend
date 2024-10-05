from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from . import models, permissions, serializers


class LeaderboardView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.LeaderboardSerializer
    permission_classes = (permissions.IsOwnerOrReadOnly,)
    http_method_names = [
        "delete",
        "get",
        "patch",
    ]
    queryset = models.Leaderboard.objects.all()


class LeaderboardListView(generics.ListAPIView):
    serializer_class = serializers.LeaderboardSerializer
    permission_classes = (IsAuthenticated,)
    queryset = models.Leaderboard.objects.all()


class LeaderboardCreateView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.LeaderboardCreateSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LeaderboardMemberCreateView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.LeaderboardMemberCreateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LeaderboardMemberView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsMemberUserOrReadOnly,)
    serializer_class = serializers.LeaderboardMemberSerializer
    queryset = models.LeaderboardMember.objects.all()

    http_method_names = [
        "delete",
        "get",
        "patch",
        "post",
    ]


class LeaderboardMemberListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.LeaderboardMemberSerializer

    def get_queryset(self):
        leaderboard = self.kwargs.get("leaderboard")
        return models.LeaderboardMember.objects.filter(leaderboard=leaderboard)


class LeaderboardCreateMatchView(generics.CreateAPIView):
    serializer_class = serializers.LeaderboardMatchCreateSerializer
    permission_classes = (permissions.IsMatchWinnerOrReadOnly,)
    http_method_names = ["post"]

    def perform_create(self, serializer):
        match = serializer.save()
        match.update_elo()
