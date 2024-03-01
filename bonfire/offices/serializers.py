from rest_framework import serializers

from . import models


class OfficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Office
        fields = (
            "id",
            "name",
            "longitude",
            "latitude",
        )
        read_only_fields = fields
