from __future__ import annotations

from dataclasses import dataclass, fields

from django.conf import settings
from django.utils.timezone import datetime
from rest_framework import serializers

from . import models


def dataclass_from_kwargs(cls, **kwargs) -> BaseEvent:
    names = set([f.name for f in fields(cls)])
    filtered_kwargs = {k: v for k, v in kwargs.items() if k in names}
    return cls(**filtered_kwargs)


class BaseEvent:
    def handle(self):
        raise NotImplementedError


@dataclass
class ChannelEventItem:
    channel: str
    ts: str
    type: str

    def __post_init__(self):
        self.ts = datetime.fromtimestamp(float(self.ts)).astimezone(settings.TZ)


@dataclass
class ChannelMessageEvent(BaseEvent):
    type: str
    channel: str
    user: str
    text: str
    ts: str
    event_ts: datetime
    channel_type: str

    def __post_init__(self):
        self.event_ts = datetime.fromtimestamp(float(self.event_ts)).astimezone(
            settings.TZ
        )

    def handle(self, raw_data: dict):
        if self.channel == settings.SLACK_WORKING_LOCATION_CHANNEL:
            models.SlackMessage.objects.create(
                slack_channel=self.channel,
                slack_user=self.user,
                slack_ts=self.event_ts,
                message=self.text,
                raw_data=raw_data,
            )


@dataclass
class ChannelMessageDeletedEvent(BaseEvent):
    type: str
    channel: str
    deleted_ts: datetime

    def __post_init__(self):
        self.deleted_ts = datetime.fromtimestamp(float(self.deleted_ts)).astimezone(
            settings.TZ
        )

    def handle(self, raw_data: dict):
        if self.channel == settings.SLACK_WORKING_LOCATION_CHANNEL:
            models.SlackMessage.objects.filter(slack_ts=self.deleted_ts).delete()


@dataclass
class ChannelMessageReactionAddedEvent(BaseEvent):
    event_ts: datetime
    item: ChannelEventItem
    reaction: str
    type: str
    user: str

    def __post_init__(self):
        self.event_ts = datetime.fromtimestamp(float(self.event_ts)).astimezone(
            settings.TZ
        )
        if self.item["type"] == "message":
            self.item = dataclass_from_kwargs(ChannelEventItem, **self.item)

    def handle(self, raw_data: dict):
        if self.item.channel == settings.SLACK_WORKING_LOCATION_CHANNEL:
            try:
                slack_message = models.SlackMessage.objects.get(slack_ts=self.item.ts)
            except models.SlackMessage.DoesNotExist:
                pass
            else:
                models.SlackReaction.objects.create(
                    slack_message=slack_message,
                    slack_reaction=self.reaction,
                    slack_user=self.user,
                    slack_ts=self.event_ts,
                    raw_data=raw_data,
                )


@dataclass
class ChannelMessageReactionRemovedEvent(BaseEvent):
    event_ts: datetime
    item: ChannelEventItem
    reaction: str
    type: str
    user: str

    def __post_init__(self):
        self.event_ts = datetime.fromtimestamp(float(self.event_ts)).astimezone(
            settings.TZ
        )

        if self.item["type"] == "message":
            self.item = dataclass_from_kwargs(ChannelEventItem, **self.item)

    def handle(self, raw_data: dict):
        if self.item.channel == settings.SLACK_WORKING_LOCATION_CHANNEL:
            models.SlackReaction.objects.filter(
                slack_message__slack_ts=self.item.ts,
                slack_reaction=self.reaction,
                slack_user=self.user,
            ).delete()


@dataclass
class EventCallback:
    type: str
    event: BaseEvent

    def __post_init__(self):
        if self.event["type"] == "message":
            if self.event.get("subtype") == "message_deleted":
                self.event = dataclass_from_kwargs(
                    ChannelMessageDeletedEvent, **self.event
                )
            else:
                self.event = dataclass_from_kwargs(ChannelMessageEvent, **self.event)

        elif self.event["type"] == "reaction_added":
            self.event = dataclass_from_kwargs(
                ChannelMessageReactionAddedEvent, **self.event
            )

        elif self.event["type"] == "reaction_removed":
            self.event = dataclass_from_kwargs(
                ChannelMessageReactionRemovedEvent, **self.event
            )


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
            e = dataclass_from_kwargs(EventCallback, **self.initial_data)
            e.event.handle(raw_data=self.initial_data)
