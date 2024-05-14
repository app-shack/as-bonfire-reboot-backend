from dataclasses import dataclass, fields

from django.conf import settings
from rest_framework import serializers

from . import models


@dataclass
class ChannelMessageEvent:
    type: str
    channel: str
    user: str
    text: str
    ts: str
    event_ts: str
    channel_type: str

    @classmethod
    def from_kwargs(cls, **kwargs):
        names = set([f.name for f in fields(cls)])
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in names}
        return cls(**filtered_kwargs)


@dataclass
class EventCallback:
    token: str
    event: ChannelMessageEvent
    type: str
    event_id: str
    event_time: int

    def __post_init__(self):
        if self.event["type"] == "message":
            self.event = ChannelMessageEvent.from_kwargs(**self.event)

    @classmethod
    def from_kwargs(cls, **kwargs):
        names = set([f.name for f in fields(cls)])
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in names}
        return cls(**filtered_kwargs)


# TODO: One serializer per msg type instead?
class IncomingSlackEventWebhookSerializer(serializers.Serializer):
    token = serializers.CharField(required=False)
    challenge = serializers.CharField(required=False)
    type = serializers.ChoiceField(
        choices=(
            "url_verification",
            "event_callback",
            "reaction_added",
            "reaction_removed",
            "user_profile_changed",
        )
    )

    team_id = serializers.CharField(required=False)
    api_app_id = serializers.CharField(required=False)
    event = serializers.DictField(required=False)
    authed_teams = serializers.ListField(child=serializers.CharField(), required=False)
    event_id = serializers.CharField(required=False)
    event_time = serializers.IntegerField(required=False)

    def validate(self, attrs):
        event_type = attrs["type"]

        if event_type == "url_verification":
            attrs = dict(challenge=attrs["challenge"])
        else:
            pass

        return attrs

    def save(self, **kwargs):
        event_type = self.validated_data.get("type")

        if event_type == "event_callback":
            e = EventCallback.from_kwargs(**self.validated_data)

            if (
                isinstance(e.event, ChannelMessageEvent)
                and e.event.channel == settings.SLACK_WORKING_LOCATION_CHANNEL
            ):
                models.SlackMessage.objects.create(
                    slack_channel=e.event.channel,
                    slack_user=e.event.user,
                    message=e.event.text,
                    external_id=e.event_id,
                    raw_data=self.data,
                )
