from django.db import models

from utils.models import TimestampedModel, UUIDModel


class MassageQueueEntry(UUIDModel, TimestampedModel):
    class QueueEntryStatus(models.TextChoices):
        WAITING = "waiting", "Waiting"
        IN_PROGRESS = "in_progress", "In progress"
        DONE = "done", "Done"

    user = models.ForeignKey("users.User", on_delete=models.CASCADE)

    status = models.CharField(
        choices=QueueEntryStatus.choices, default=QueueEntryStatus.WAITING.value
    )

    queue_position = models.IntegerField()
