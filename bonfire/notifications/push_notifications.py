from dataclasses import asdict, dataclass
from enum import Enum
from typing import Optional
from uuid import UUID

from firebase_admin.messaging import Message, Notification


class IDTypeEnum(Enum):
    EVENT = "event"


@dataclass
class NotificationDataPayload:
    id: Optional[str] = None
    id_type: Optional[IDTypeEnum] = None

    @staticmethod
    def asdict_factory(data):
        def convert_value(obj):
            if isinstance(obj, Enum):
                return obj.value
            if isinstance(obj, UUID):
                return str(obj)
            return obj

        return dict((k, convert_value(v)) for k, v in data if v)

    def to_dict(self) -> dict[str, str]:
        return asdict(self, dict_factory=self.asdict_factory)


def event_was_created(event) -> Message:
    title = "Fire in the hål!!! 🔥🔥🔥🔥"

    message_body = " ".join(
        [
            "Nu jääävlar!!",
        ]
    )

    return Message(
        notification=Notification(
            title=title,
            body=message_body,
        ),
        data=NotificationDataPayload(
            id=event.pk,
            id_type=IDTypeEnum.EVENT,
        ).to_dict(),
    )


def event_was_updated(event) -> Message:
    title = "Fire in the hål!!! 🔥🔥🔥🔥"

    message_body = " ".join(
        [
            "Nu jääävlar!!",
        ]
    )

    return Message(
        notification=Notification(
            title=title,
            body=message_body,
        ),
        data=NotificationDataPayload(
            id=event.pk,
            id_type=IDTypeEnum.EVENT,
        ).to_dict(),
    )


def event_was_deleted(event_name) -> Message:
    title = "Fire in the hål!!! 🔥🔥🔥🔥"

    message_body = " ".join(
        [
            "Nu jääävlar!!",
        ]
    )

    return Message(
        notification=Notification(
            title=title,
            body=message_body,
        ),
    )


def event_is_starting(event) -> Message:
    title = "Fire in the hål!!! 🔥🔥🔥🔥"

    message_body = " ".join(
        [
            "Nu jääävlar!!",
        ]
    )

    return Message(
        notification=Notification(
            title=title,
            body=message_body,
        ),
        data=NotificationDataPayload(
            id=event.pk,
            id_type=IDTypeEnum.EVENT,
        ).to_dict(),
    )
