from dataclasses import dataclass, fields

from django.conf import settings
from django.utils.timezone import datetime
from rest_framework import serializers

from . import models


@dataclass
class ChannelEventItem:
    channel: str
    ts: str
    type: str

    @classmethod
    def from_kwargs(cls, **kwargs):
        names = set([f.name for f in fields(cls)])
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in names}
        return cls(**filtered_kwargs)

    def __post_init__(self):
        self.ts = datetime.fromtimestamp(float(self.ts)).astimezone(settings.TZ)


@dataclass
class ChannelMessageEvent:
    type: str
    channel: str
    user: str
    text: str
    ts: str
    event_ts: datetime
    channel_type: str

    @classmethod
    def from_kwargs(cls, **kwargs):
        names = set([f.name for f in fields(cls)])
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in names}
        return cls(**filtered_kwargs)

    def __post_init__(self):
        self.event_ts = datetime.fromtimestamp(float(self.event_ts)).astimezone(
            settings.TZ
        )


@dataclass
class ChannelMessageReactionAddedEvent:
    event_ts: datetime
    item: ChannelEventItem
    reaction: str
    type: str
    user: str

    @classmethod
    def from_kwargs(cls, **kwargs):
        names = set([f.name for f in fields(cls)])
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in names}
        return cls(**filtered_kwargs)

    def __post_init__(self):
        self.event_ts = datetime.fromtimestamp(float(self.event_ts)).astimezone(
            settings.TZ
        )
        if self.item["type"] == "message":
            self.item = ChannelEventItem.from_kwargs(**self.item)


@dataclass
class ChannelMessageReactionRemovedEvent:
    event_ts: datetime
    item: ChannelEventItem
    reaction: str
    type: str
    user: str

    @classmethod
    def from_kwargs(cls, **kwargs):
        names = set([f.name for f in fields(cls)])
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in names}
        return cls(**filtered_kwargs)

    def __post_init__(self):
        self.event_ts = datetime.fromtimestamp(float(self.event_ts)).astimezone(
            settings.TZ
        )

        if self.item["type"] == "message":
            self.item = ChannelEventItem.from_kwargs(**self.item)


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
        elif self.event["type"] == "reaction_added":
            self.event = ChannelMessageReactionAddedEvent.from_kwargs(**self.event)
        elif self.event["type"] == "reaction_removed":
            self.event = ChannelMessageReactionRemovedEvent.from_kwargs(**self.event)

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
                    slack_ts=e.event.event_ts,
                    message=e.event.text,
                    external_id=e.event_id,
                    raw_data=self.data,
                )

            if (
                isinstance(e.event, ChannelMessageReactionAddedEvent)
                and e.event.item.channel == settings.SLACK_WORKING_LOCATION_CHANNEL
            ):
                try:
                    slack_message = models.SlackMessage.objects.get(
                        slack_ts=e.event.item.ts
                    )
                except models.SlackMessage.DoesNotExist:
                    pass
                else:
                    models.SlackReaction.objects.create(
                        slack_message=slack_message,
                        slack_reaction=e.event.reaction,
                        slack_user=e.event.user,
                        slack_ts=e.event.event_ts,
                        raw_data=self.data,
                    )

            if (
                isinstance(e.event, ChannelMessageReactionRemovedEvent)
                and e.event.item.channel == settings.SLACK_WORKING_LOCATION_CHANNEL
            ):
                models.SlackReaction.objects.filter(
                    slack_message__slack_ts=e.event.item.ts,
                    slack_ts=e.event.event_ts,
                ).delete()
