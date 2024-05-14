from django.db import models

from utils.models import TimestampedModel, UUIDModel


class SlackMessage(UUIDModel, TimestampedModel):
    slack_channel = models.CharField(db_index=True, max_length=255)
    slack_user = models.CharField(db_index=True, max_length=255)
    slack_ts = models.DateTimeField()
    message = models.TextField()

    external_id = models.CharField(unique=True, max_length=255)

    raw_data = models.JSONField(default=dict, blank=True)


class SlackReaction(UUIDModel, TimestampedModel):
    slack_message = models.ForeignKey(SlackMessage, on_delete=models.CASCADE)

    slack_reaction = models.CharField()
    slack_user = models.CharField(db_index=True, max_length=255)
    slack_ts = models.DateTimeField()

    raw_data = models.JSONField(default=dict, blank=True)
