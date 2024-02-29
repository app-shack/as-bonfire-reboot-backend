from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.tokens import RefreshToken

from google_client import client as google_client
from utils.fields import LowerCaseEmailField

from . import models


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


class UserTokenObtainPairSerializer(serializers.Serializer):
    INVALID_CREDENTIALS = "Invalid credentials"

    token = serializers.CharField(write_only=True)
    client_id = serializers.CharField(write_only=True)
    refresh = serializers.CharField(read_only=True)
    access = serializers.CharField(read_only=True)

    class Meta:
        fields = (
            "token",
            "client_id",
            "refresh",
            "access",
        )
        read_only_fields = (
            "refresh",
            "access",
        )

    def validate(self, attrs):
        token = attrs["token"]
        client_id = attrs["client_id"]

        id_info = google_client.verify_oauth2_token(token, client_id)

        if not google_client.validate_token(id_info):
            raise serializers.ValidationError(self.INVALID_CREDENTIALS)

        return dict(
            first_name=id_info["given_name"],
            last_name=id_info["family_name"],
            email=id_info["email"],
        )

    def create(self, validated_data):
        email = validated_data.pop("email")
        try:
            user = models.User.objects.get(email=email)
        except models.User.DoesNotExist:
            user = models.User(email=email, **validated_data)
            user.set_unusable_password()
            user.save()

        refresh = RefreshToken.for_user(user)
        tokens = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
        return tokens
