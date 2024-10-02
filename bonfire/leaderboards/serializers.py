from rest_framework import serializers

from . import models


class LeaderboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Leaderboard
        fields = ("id", "name")
        read_only_fields = "id"


class LeaderboardMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LeaderboardMember
        fields = ("id", "name")
        read_only_fields = "id"


class LeaderboardCreateMatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LeaderboardMatch
        fields = ("player_a", "player_b", "result")

    def validate(self, data):
        if data["player_a"] == data["player_b"]:
            raise serializers.ValidationError("Players cannot be the same.")
        return data

    def create(self, validated_data):
        return super().create(validated_data)
