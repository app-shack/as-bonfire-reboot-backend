import math

from django.http import Http404
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from . import models, serializers


class LeaderboardMixIn:
    def get_object(self):
        id = self.get_id()
        try:
            leaderboard = models.Leaderboard.objects.get(id=id)
        except models.Leaderboard.DoesNotExist:
            raise Http404
        return leaderboard

    def get_id(self):
        return self.request.path_info.split("/")[3]


class LeaderboardView(generics.RetrieveAPIView):
    serializer_class = serializers.LeaderboardSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        return Response({}, status=status.HTTP_200_OK)


class LeaderboardCreateView(LeaderboardMixIn, generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.LeaderboardSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.validated_data)
        return Response(
            serializer.validated_data, status=status.HTTP_201_CREATED, headers=headers
        )


class LeaderboardDestroyView(generics.DestroyAPIView):
    serializer_class = serializers.LeaderboardSerializer
    permission_classes = (IsAuthenticated,)

    http_method_names = [
        "delete",
    ]

    def destroy(self, request, *args, **kwargs):
        leaderboard = self.get_object()
        leaderboard.delete()

        return Response({}, status=status.HTTP_200_OK)


class LeaderboardCreateMatchView(LeaderboardMixIn, generics.CreateAPIView):
    serializer_class = serializers.LeaderboardCreateMatchSerializer
    permission_classes = (AllowAny,)
    http_method_names = ["post"]

    def perform_create(self, serializer):
        match = serializer.save()
        member_count = match.player_a.leaderboard.members.count()
        constant_k = member_count * 42
        player_a = match.player_a
        player_b = match.player_b
        result = match.result

        if match.result == models.LeaderboardMatch.MatchResult.PLAYER_A_WIN:
            score_a = 1.0
            score_b = 0.0
            player_a.wins += 1
            player_b.losses += 1
        elif result == models.LeaderboardMatch.MatchResult.PLAYER_B_WIN:
            score_a = 0.0
            score_b = 1.0
            player_a.losses += 1
            player_b.wins += 1
        else:
            score_a = 0.5
            score_b = 0.5
            player_a.ties += 1
            player_b.ties += 1

        elo_a = 1 / (1 + math.pow(10, (player_b.rating - player_a.rating) / 400))
        elo_b = 1 / (1 + math.pow(10, (player_a.rating - player_b.rating) / 400))

        player_a.rating = player_a.rating + constant_k * (score_a - elo_a)
        player_b.rating = player_b.rating + constant_k * (score_b - elo_b)

        player_a.save()
        player_b.save()

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(response.data, status=status.HTTP_201_CREATED)
