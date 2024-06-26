# Generated by Django 4.2.13 on 2024-05-10 13:08

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models

import users.models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserProfileImage",
            fields=[
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "original",
                    models.ImageField(
                        upload_to=users.models.get_user_profile_image_filename,
                        verbose_name="The originally uploaded image",
                    ),
                ),
                (
                    "normal",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=users.models.get_user_profile_image_filename,
                        verbose_name="The 'normal size' converted original image",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
