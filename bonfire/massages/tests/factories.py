import factory

from .. import models


class MassageQueueEntryFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory("users.tests.factories.UserFactory")
    status = models.MassageQueueEntry.QueueEntryStatus.WAITING.value
    queue_position = 0

    class Meta:
        model = models.MassageQueueEntry
