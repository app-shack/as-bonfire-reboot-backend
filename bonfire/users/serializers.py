from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from utils.fields import LowerCaseEmailField

from . import models


class AccessTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField(read_only=True)
    access = serializers.CharField(read_only=True)


class UserMeSerializer(serializers.ModelSerializer):
    email = LowerCaseEmailField(
        validators=[
            UniqueValidator(queryset=models.User.objects.all(), lookup="iexact")
        ]
    )

    class Meta:
        model = models.User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
        )
        read_only_fields = ("id",)
