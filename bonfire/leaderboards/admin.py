from django.contrib import admin

from . import models


@admin.register(models.Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "owner",
    )
    fields = (
        "created_at",
        "updated_at",
        "name",
        "owner",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )


@admin.register(models.LeaderboardMember)
class LeaderboardMemberAdmin(admin.ModelAdmin):
    list_display = (
        "leaderboard",
        "user",
        "nickname",
        "rating",
        "wins",
        "losses",
        "ties",
    )
    fields = (
        "created_at",
        "updated_at",
        "leaderboard",
        "user",
        "nickname",
        "rating",
        "wins",
        "losses",
        "ties",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
        "wins",
        "losses",
        "ties",
    )


@admin.register(models.LeaderboardMatch)
class LeaderboardMatchAdmin(admin.ModelAdmin):
    list_display = ("player_a", "player_b", "result")
    fields = (
        "created_at",
        "updated_at",
        "player_a",
        "player_b",
        "result",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
