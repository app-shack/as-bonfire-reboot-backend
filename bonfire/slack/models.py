from django.conf import settings
from django.db import models
from django.utils.timezone import now

from utils.models import TimestampedModel, UUIDModel


class SlackMessageQuerySet(models.QuerySet):
    def message_for_date(self, date):
        return self.filter(created_at__date=date)

    def todays_messages(self):
        return self.message_for_date(date=now().date())

    def working_location_messages(self):
        return self.filter(slack_channel=settings.SLACK_WORKING_LOCATION_CHANNEL)


class SlackMessage(UUIDModel, TimestampedModel):
    slack_channel = models.CharField(db_index=True, max_length=255)
    slack_user = models.CharField(db_index=True, max_length=255)
    slack_ts = models.DateTimeField()
    message = models.TextField()

    raw_data = models.JSONField(default=dict, blank=True)

    objects = SlackMessageQuerySet.as_manager()


class SlackReaction(UUIDModel, TimestampedModel):
    slack_message = models.ForeignKey(SlackMessage, on_delete=models.CASCADE)

    slack_reaction = models.CharField()
    slack_user = models.CharField(db_index=True, max_length=255)
    slack_ts = models.DateTimeField()

    raw_data = models.JSONField(default=dict, blank=True)
