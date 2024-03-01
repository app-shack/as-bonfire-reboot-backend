from fcm_django.models import FCMDevice
from rest_framework import serializers

from notifications.push_notifications import event_was_created, event_was_updated
from offices.models import Office
from users.models import User

from . import models


class OfficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Office
        fields = (
            "id",
            "name",
            "latitude",
            "longitude",
        )
        read_only_fields = fields


class EventDetailSerializer(serializers.ModelSerializer):
    number_of_bookings = serializers.IntegerField(read_only=True)
    has_booking = serializers.BooleanField(read_only=True, default=False)
    office = OfficeSerializer(read_only=True)

    class Meta:
        model = models.Event
        fields = (
            "id",
            "name",
            "description",
            "start_time",
            "end_time",
            "latitude",
            "longitude",
            "office",
            "number_of_bookings",
            "has_booking",
        )
        read_only_fields = fields


class EventSerializer(serializers.ModelSerializer):
    office = serializers.PrimaryKeyRelatedField(queryset=Office.objects)
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.Event
        fields = (
            "id",
            "name",
            "description",
            "start_time",
            "end_time",
            "latitude",
            "longitude",
            "office",
            "created_by",
        )
        read_only_fields = ("id",)

    def validate(self, attrs):
        if self.instance:
            current_user = self.context["request"].user
            if current_user != self.instance.created_by:
                raise serializers.ValidationError("Not your event bro!!")

        return super().validate(attrs)

    def notify_event_changed(self, instance, message):
        users = User.objects.get_close_users_pks(
            instance, instance.latitude, instance.longitude
        )
        FCMDevice.objects.filter(user__in=list(users)).send_message(message)

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)

        self.notify_event_changed(instance, event_was_updated(instance))

        return instance

    def create(self, validated_data):
        instance = super().create(validated_data)

        self.notify_event_changed(instance, event_was_created(instance))

        return instance


class BookingSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    event = serializers.PrimaryKeyRelatedField(queryset=models.Event.objects)

    class Meta:
        model = models.Booking
        fields = (
            "user",
            "event",
        )

    def validate(self, attrs):
        event = attrs["event"]
        user = attrs["user"]

        booking_exists = models.Booking.objects.filter(user=user, event=event).exists()
        if booking_exists:
            raise serializers.ValidationError("boooo booo")

        return attrs
