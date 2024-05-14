from uuid import uuid4

import factory
from django.utils.timezone import now

from .. import models


class SlackMessageFactory(factory.django.DjangoModelFactory):
    slack_channel = factory.Sequence(lambda n: "%03d_channel" % n)
    slack_user = factory.Sequence(lambda n: "%03d_user" % n)
    slack_ts = factory.LazyFunction(now)

    external_id = factory.LazyFunction(uuid4)

    class Meta:
        model = models.SlackMessage


class SlackReactionFactory(factory.django.DjangoModelFactory):
    slack_message = factory.SubFactory(SlackMessageFactory)

    slack_reaction = factory.Sequence(lambda n: ":%03d_reaction:" % n)
    slack_user = factory.Sequence(lambda n: "%03d_user" % n)
    slack_ts = factory.LazyFunction(now)

    class Meta:
        model = models.SlackReaction
