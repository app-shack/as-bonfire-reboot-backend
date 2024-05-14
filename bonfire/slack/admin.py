from django.contrib import admin

from . import models


@admin.register(models.SlackMessage)
class SlackMessageAdmin(admin.ModelAdmin):
    list_display = ("pk",)

    readonly_fields = (
        "slack_channel",
        "slack_user",
        "slack_ts",
        "message",
        "raw_data",
    )

    ordering = ("-created_at",)


@admin.register(models.SlackReaction)
class SlackReactionAdmin(admin.ModelAdmin):
    list_display = ("pk",)

    readonly_fields = (
        "slack_reaction",
        "slack_user",
        "slack_ts",
        "raw_data",
    )

    ordering = ("-created_at",)
