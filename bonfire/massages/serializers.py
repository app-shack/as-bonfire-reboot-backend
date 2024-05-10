from django.db import transaction
from django.db.models import F
from django.utils.timezone import now
from rest_framework import serializers

from users.models import User, UserProfileImage

from . import models


class MassageQueueUserProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfileImage
        fields = ("normal", "updated_at")
        read_only_fields = fields


class MassageQueueUserSerializer(serializers.ModelSerializer):
    profile_image = MassageQueueUserProfileImageSerializer(
        source="userprofileimage",
        read_only=True,
        allow_null=True,
    )

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "profile_image",
        )
        read_only_fields = fields


class MassageQueueEntrySerializer(serializers.ModelSerializer):
    ALREADY_IN_QUEUE = "Already in queue!"

    user = MassageQueueUserSerializer(read_only=True)

    class Meta:
        model = models.MassageQueueEntry
        fields = (
            "id",
            "status",
            "queue_position",
            "user",
        )
        read_only_fields = fields

    def validate(self, attrs):
        in_queue = models.MassageQueueEntry.objects.filter(
            user=self.context["request"].user, created_at__date=now().date()
        ).exists()
        if in_queue:
            raise serializers.ValidationError(self.ALREADY_IN_QUEUE)

        return attrs

    def save(self, **kwargs):
        next_queue_position = models.MassageQueueEntry.objects.filter(
            created_at__date=now().date()
        ).count()

        return super().save(
            user=self.context["request"].user,
            queue_position=next_queue_position,
            **kwargs,
        )


class MassageQueueEntryDowngradeSerializer(serializers.ModelSerializer):
    NOT_LOWER_QUEUE_POSITION = "Other queue entry is not in a lower position!"

    other_queue_entry = serializers.PrimaryKeyRelatedField(
        queryset=models.MassageQueueEntry.objects, write_only=True
    )

    class Meta:
        model = models.MassageQueueEntry
        fields = ("other_queue_entry",)
        read_only_fields = fields

    def validate(self, attrs):
        other_queue_entry = attrs["other_queue_entry"]

        if self.instance.queue_position >= other_queue_entry.queue_position:
            raise serializers.ValidationError(self.NOT_LOWER_QUEUE_POSITION)

        return attrs

    def save(self, **kwargs):
        other_queue_entry = self.validated_data["other_queue_entry"]

        with transaction.atomic():
            my_old_queue_position = self.instance.queue_position
            my_new_queue_position = other_queue_entry.queue_position

            models.MassageQueueEntry.objects.filter(
                created_at__date=now().date(),
                queue_position__gt=my_new_queue_position,
            ).update(queue_position=F("queue_position") + 1)

            self.instance.queue_position = my_new_queue_position + 1
            self.instance.save()

            models.MassageQueueEntry.objects.filter(
                created_at__date=now().date(),
                queue_position__gte=my_old_queue_position,
            ).update(queue_position=F("queue_position") - 1)


class MassageQueueEntryBeginSerializer(serializers.ModelSerializer):
    NOT_IN_WAITING_STATE = "Not in waiting state!"

    class Meta:
        model = models.MassageQueueEntry
        fields = ()

    def validate(self, attrs):
        is_expected_status = (
            self.instance.status
            == models.MassageQueueEntry.QueueEntryStatus.WAITING.value
        )
        if not is_expected_status:
            raise serializers.ValidationError(self.NOT_IN_WAITING_STATE)

        return attrs

    def save(self, **kwargs):
        self.instance.status = (
            models.MassageQueueEntry.QueueEntryStatus.IN_PROGRESS.value
        )
        self.instance.save()


class MassageQueueEntryFinishSerializer(serializers.ModelSerializer):
    NOT_IN_PROGRESS_STATE = "Not in progress state!"

    class Meta:
        model = models.MassageQueueEntry
        fields = ()

    def validate(self, attrs):
        is_expected_status = (
            self.instance.status
            == models.MassageQueueEntry.QueueEntryStatus.IN_PROGRESS.value
        )
        if not is_expected_status:
            raise serializers.ValidationError(self.NOT_IN_PROGRESS_STATE)

        return attrs

    def save(self, **kwargs):
        self.instance.status = models.MassageQueueEntry.QueueEntryStatus.DONE.value
        self.instance.save()
