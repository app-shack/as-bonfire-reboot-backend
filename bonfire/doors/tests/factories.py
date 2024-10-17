import factory

from .. import models


class DoorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Door
