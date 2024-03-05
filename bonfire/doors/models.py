from django.db import models
from django.utils.translation import gettext_lazy as _

from flex_access import client
from utils.models import TimestampedModel, UUIDModel


class Door(UUIDModel, TimestampedModel):
    class StatusType(models.TextChoices):
        UNLOCKED = "unlocked", _("Unlocked")
        LOCKED = "locked", _("Locked")
        UNKNOWN = "unknown", _("Unknown")

    slug = models.CharField(unique=True)
    status = models.CharField(max_length=255, choices=StatusType.choices)

    external_id = models.CharField(unique=True)
    output_number = models.CharField()

    def __str__(self) -> str:
        return self.slug

    def unlock(self):
        client.open_door(self.external_id, self.output_number)

        self.status = self.StatusType.UNLOCKED
        self.save()

    def lock(self):
        try:
            client.close_door(self.external_id, self.output_number)
        except client.FlexException:
            self.status = self.StatusType.UNKNOWN
        else:
            self.status = self.StatusType.LOCKED
        finally:
            self.save()

    def refresh_status(self):
        r = client.get_connection_status(self.external_id)

        for o in r["status"]:
            if o["Name"] != self.output_number:
                continue

            raw_status = o["Value"]

            if raw_status == "0":
                self.status = self.StatusType.LOCKED
            elif raw_status == "1":
                self.status = self.StatusType.UNLOCKED
            else:
                self.status = self.StatusType.UNKNOWN

            self.save()
