from django.contrib.postgres.operations import BtreeGinExtension, TrigramExtension
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_user_coordinates_updated_at_user_latitude_and_more"),
    ]

    operations = [
        TrigramExtension(),
        BtreeGinExtension(),
    ]
