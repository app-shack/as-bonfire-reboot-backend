import math

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from users.models import User
from utils.models import TimestampedModel, UUIDModel


class Leaderboard(UUIDModel, TimestampedModel):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="leaderboards"
    )
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
    rating = models.FloatField(
        default=1000,
        # Prevents math range overflow when calculating elo
        validators=[MinValueValidator(-10000.0), MaxValueValidator(10000.0)],
    )
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

    def update_elo(self):
        member_count = self.player_a.leaderboard.members.count()
        constant_k = member_count * 42
        player_a = self.player_a
        player_b = self.player_b
        result = self.result

        if self.result == LeaderboardMatch.MatchResult.PLAYER_A_WIN:
            score_a = 1.0
            score_b = 0.0
            player_a.wins += 1
            player_b.losses += 1
        elif result == LeaderboardMatch.MatchResult.PLAYER_B_WIN:
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