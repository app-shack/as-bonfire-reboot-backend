from django.db import models

from utils.models import TimestampedModel, UUIDModel


class Event(UUIDModel, TimestampedModel):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True
    )

    office = models.ForeignKey("offices.Office", on_delete=models.CASCADE)
    created_by = models.ForeignKey("users.User", on_delete=models.CASCADE)

    starting_notification_sent_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name


class Booking(UUIDModel, TimestampedModel):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
