import factory

from utils.image import generate_test_image

from .. import models


class UserFactory(factory.django.DjangoModelFactory):
    email = factory.Sequence(lambda n: "%03d@example.com" % n)
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    password = factory.PostGenerationMethodCall("set_password", "test1234")

    slack_id = factory.Sequence(lambda n: "slack_id_%03d" % n)

    class Meta:
        model = models.User
        django_get_or_create = ("email",)

    @factory.post_generation
    def groups(obj, create, extracted, **kwargs):
        if not create:
            return

        if extracted is not None:
            obj.groups.set(extracted)


class UserProfileImageFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    original = factory.django.FileField(from_func=generate_test_image)

    class Meta:
        model = models.UserProfileImage
