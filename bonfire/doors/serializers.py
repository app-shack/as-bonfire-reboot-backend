from rest_framework import serializers

from . import models


class DoorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Door
        fields = ("status",)
        read_only_fields = fields
