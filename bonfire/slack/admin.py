from django.contrib import admin

from . import models


@admin.register(models.SlackMessage)
class SlackMessageAdmin(admin.ModelAdmin):
    list_display = ("pk",)

    readonly_fields = (
        "slack_channel",
        "slack_user",
        "message",
        "external_id",
        "raw_data",
    )

    ordering = ("-created_at",)
