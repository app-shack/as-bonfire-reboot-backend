# Generated by Django 4.2.13 on 2024-05-14 11:54

import uuid

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="SlackMessage",
            fields=[
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("slack_channel", models.CharField(db_index=True, max_length=255)),
                ("slack_user", models.CharField(db_index=True, max_length=255)),
                ("message", models.TextField()),
                ("external_id", models.CharField(max_length=255, unique=True)),
                ("raw_data", models.JSONField(blank=True, default=dict)),
            ],
            options={
                "abstract": False,
            },
        ),
    ]