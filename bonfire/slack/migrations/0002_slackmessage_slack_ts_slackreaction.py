# Generated by Django 4.2.13 on 2024-05-14 14:51

import uuid

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models
from django.utils.timezone import datetime


def unix_to_dt(unix) -> datetime:
    return datetime.fromtimestamp(float(unix)).astimezone(settings.TZ)


def set_slack_ts(apps, schema_state):
    SlackMessage = apps.get_model("slack", "SlackMessage")

    for m in SlackMessage.objects.all():
        m.slack_ts = unix_to_dt(m.raw_data["event"]["ts"])
        m.save()


class Migration(migrations.Migration):
    dependencies = [
        ("slack", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="slackmessage",
            name="slack_ts",
            field=models.DateTimeField(null=True),
        ),
        migrations.CreateModel(
            name="SlackReaction",
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
                ("slack_reaction", models.CharField()),
                ("slack_user", models.CharField(db_index=True, max_length=255)),
                ("slack_ts", models.DateTimeField()),
                (
                    "slack_message",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="slack.slackmessage",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.RunPython(
            set_slack_ts,
            migrations.RunPython.noop,
            elidable=True,
        ),
        migrations.AlterField(
            model_name="slackmessage",
            name="slack_ts",
            field=models.DateTimeField(),
        ),
    ]
