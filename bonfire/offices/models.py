from django.db import models

from utils.models import TimestampedModel, UUIDModel


class Office(UUIDModel, TimestampedModel):
    name = models.CharField(max_length=255)

    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True
    )

    def __str__(self):
        return self.name
