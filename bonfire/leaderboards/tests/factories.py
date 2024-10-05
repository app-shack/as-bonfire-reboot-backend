import factory

from users.tests.factories import UserFactory

from .. import models


class LeaderboardFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Leaderboard

    owner = factory.SubFactory(UserFactory)
    name = factory.Faker("name")


class LeaderboardMemberFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.LeaderboardMember

    leaderboard = factory.SubFactory(LeaderboardFactory)
    user = factory.SubFactory(UserFactory)
    nickname = factory.Faker("name")
    rating = factory.Faker("pyfloat", min_value=-10000.0, max_value=10000.0)
    wins = factory.Faker("pyint")
    losses = factory.Faker("pyint")
    ties = factory.Faker("pyint")


class LeaderboardMatchFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.LeaderboardMatch

    player_a = factory.SubFactory(LeaderboardMemberFactory)
    player_b = factory.SubFactory(LeaderboardMemberFactory)
    result = factory.Iterator(models.LeaderboardMatch.MatchResult.values)
