from django.db import models
from django.utils.translation import gettext_lazy as _

from users.models import User
from utils.models import TimestampedModel, UUIDModel


class Leaderboard(UUIDModel, TimestampedModel):
    name = models.CharField(max_length=50)
    objects = models.Manager()

    def __str__(self):
        return f"{self.name} ({self.id})"


class LeaderboardMember(UUIDModel, TimestampedModel):
    leaderboard = models.ForeignKey(
        Leaderboard, on_delete=models.CASCADE, related_name="members"
    )
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    nickname = models.CharField(max_length=50)
    rating = models.FloatField(default=1000)
    wins = models.PositiveIntegerField(default=0)
    losses = models.PositiveIntegerField(default=0)
    ties = models.PositiveIntegerField(default=0)
    objects = models.Manager()

    def __str__(self):
        return f"{self.nickname} ({self.user})"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["leaderboard", "nickname"], name="unique_leaderboard_nickname"
            )
        ]


class LeaderboardMatch(UUIDModel, TimestampedModel):
    player_a = models.ForeignKey(
        LeaderboardMember, on_delete=models.CASCADE, related_name="player_as"
    )
    player_b = models.ForeignKey(
        LeaderboardMember, on_delete=models.CASCADE, related_name="player_bs"
    )

    class MatchResult(models.TextChoices):
        TIE = "tie", _("Tie")
        PLAYER_A_WIN = "player_a_win", _("Player A Win")
        PLAYER_B_WIN = "player_b_win", _("Player B Win")

    result = models.CharField(
        max_length=255,
        choices=MatchResult.choices,
        default=MatchResult.TIE,
    )

    objects = models.Manager()
