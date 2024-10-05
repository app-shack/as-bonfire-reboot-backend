from rest_framework import serializers

from . import models


class LeaderboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Leaderboard
        fields = ("id", "owner", "name")
        read_only_fields = (
            "id",
            "owner",
        )


class LeaderboardCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Leaderboard
        fields = ("id", "owner", "name")
        read_only_fields = ("id", "owner")


class LeaderboardMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LeaderboardMember
        fields = (
            "id",
            "leaderboard",
            "user",
            "nickname",
            "rating",
            "wins",
            "losses",
            "ties",
        )
        read_only_fields = (
            "id",
            "leaderboard",
            "user",
            "rating",
            "wins",
            "losses",
            "ties",
        )


class LeaderboardMemberCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LeaderboardMember
        fields = (
            "id",
            "leaderboard",
            "user",
            "nickname",
            "rating",
            "wins",
            "losses",
            "ties",
        )
        read_only_fields = ("id", "rating", "user", "wins", "losses", "ties")


class LeaderboardMatchCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LeaderboardMatch
        fields = (
            "id",
            "player_a",
            "player_b",
            "result",
        )
        read_only_fields = ("id",)

    def validate(self, data):
        if data["player_a"] == data["player_b"]:
            raise serializers.ValidationError("Players cannot be the same.")
        else:
            player_a = models.LeaderboardMember.objects.get(id=data["player_a"].id)
            player_b = models.LeaderboardMember.objects.get(id=data["player_b"].id)
            if player_a.leaderboard != player_b.leaderboard:
                raise serializers.ValidationError(
                    "Players must belong to the same leaderboard."
                )
        return data
