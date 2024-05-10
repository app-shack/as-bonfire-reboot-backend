import os

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower
from django.utils.translation import gettext_lazy as _

from slack_client.client import SlackClient
from utils.image import url_to_django_image
from utils.models import ImageResizeMixIn, TimestampedModel, UUIDModel

from . import tasks


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The Email must be set.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self._create_user(email, password, **extra_fields)

    def normalize_email(self, email):
        return email.lower()

    def get_by_natural_key(self, email):
        return self.get(**{self.model.USERNAME_FIELD: email.lower()})


class User(UUIDModel, TimestampedModel, AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)

    is_staff = models.BooleanField(
        default=False,
        help_text=_("Designates whether the user can log into staff site."),
    )
    is_active = models.BooleanField(
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    USERNAME_FIELD = "email"
    objects = UserManager()

    class Meta:
        constraints = [
            UniqueConstraint(
                Lower("email"),
                name="email_unique_case_insensitive",
            )
        ]

    def __str__(self):
        return self.email

    @property
    def has_profile_image(self) -> bool:
        return hasattr(self, "userprofileimage")

    def get_full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    def send_password_reset_email(self):
        # token = default_token_generator.make_token(self)
        raise NotImplementedError

    def sync_with_slack(self):
        if not self.email:
            raise Exception

        c = SlackClient()
        r = c.search_email(self.email)

        self.first_name = r.user.profile.first_name
        self.last_name = r.user.profile.last_name
        self.save()

        if self.has_profile_image:
            self.userprofileimage.delete()

        UserProfileImage.objects.create_from_url(self, r.user.profile.image_original)


def get_user_profile_image_filename(instance, filename):
    return os.path.join("user-profile-images", str(instance.pk), filename)


class UserProfileImageManager(models.Manager):
    def create_from_url(self, user: User, url: str):
        image = url_to_django_image(url, "original")
        UserProfileImage.objects.create(
            user=user,
            original=image,
        )


class UserProfileImage(TimestampedModel, ImageResizeMixIn):
    _post_process_task = tasks.post_process_user_profile_image_task
    _image_config = {
        "normal": (256, 256),
    }

    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)

    original = models.ImageField(
        _("The originally uploaded image"),
        upload_to=get_user_profile_image_filename,
        name="original",
    )

    normal = models.ImageField(
        _("The 'normal size' converted original image"),
        upload_to=get_user_profile_image_filename,
        null=True,
        blank=True,
    )

    objects = UserProfileImageManager()
