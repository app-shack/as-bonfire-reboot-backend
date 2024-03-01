from django.db.models import Count, Value
from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from notifications.push_notifications import event_was_deleted

from . import models, serializers


class EventViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = serializers.EventSerializer
    permission_classes = (AllowAny,)
    pagination_class = None

    def get_serializer_class(self):
        if self.request.method in ("GET",):
            return serializers.EventDetailSerializer
        return serializers.EventSerializer

    def get_queryset(self):
        return (
            models.Event.objects.select_related("office")
            .annotate(
                # has_booking=Exists(
                #     models.Booking.objects.filter(
                #         event=OuterRef("pk"), user=self.request.user
                #     )
                # )
                has_booking=Value(False),
                number_of_bookings=Count("booking", distinct=True),
            )
            .order_by("name")
        )

    def perform_destroy(self, instance):
        event_was_deleted(instance.name)

        return super().perform_destroy(instance)


class BookingViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = serializers.BookingSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = None

    def get_queryset(self):
        return models.Booking.objects.filter(user=self.request.user).order_by(
            "event__start_date"
        )
