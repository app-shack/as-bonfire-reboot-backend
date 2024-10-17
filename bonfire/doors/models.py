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
        try:
            client.open_door(self.external_id, self.output_number)
        except client.FlexException:
            self.status = self.StatusType.UNKNOWN
        else:
            self.status = self.StatusType.UNLOCKED
        finally:
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


class DoorLogManager(models.Manager):
    def create_from_door(self, door: Door, user):
        log = self.model(
            door=door,
            status=door.status,
            user_email=user.email,
            user_first_name=user.first_name,
            user_last_name=user.last_name,
        )
        log.save()
        return log


class DoorLog(UUIDModel, TimestampedModel):
    class StatusType(models.TextChoices):
        UNLOCKED = "unlocked"
        LOCKED = "locked"

    door = models.ForeignKey(Door, on_delete=models.CASCADE)
    status = models.CharField(max_length=255, choices=StatusType.choices)

    user_email = models.CharField()
    user_first_name = models.CharField()
    user_last_name = models.CharField()

    objects = DoorLogManager()
