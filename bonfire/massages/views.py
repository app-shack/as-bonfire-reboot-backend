from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from drf_spectacular.utils import extend_schema
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from . import models, serializers


class TodaysMassageQueueEntryViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = (IsAuthenticated,)

    pagination_class = None

    def get_serializer_class(self):
        if self.action == "downgrade":
            return serializers.MassageQueueEntryDowngradeSerializer
        if self.action == "begin":
            return serializers.MassageQueueEntryBeginSerializer
        if self.action == "finish":
            return serializers.MassageQueueEntryFinishSerializer

        return serializers.MassageQueueEntrySerializer

    def get_queryset(self):
        return (
            models.MassageQueueEntry.objects.select_related(
                "user", "user__userprofileimage"
            )
            .filter(created_at__date=now().date())
            .exclude(status=models.MassageQueueEntry.QueueEntryStatus.DONE)
            .order_by("queue_position")
        )

    def get_object(self):
        return get_object_or_404(self.get_queryset(), user=self.request.user)

    @extend_schema(responses={status.HTTP_204_NO_CONTENT: None})
    @action(detail=True, methods=["patch"], url_path="downgrade")
    def downgrade(self, request, pk):
        obj = self.get_object()
        serializer = self.get_serializer(instance=obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    @extend_schema(responses={status.HTTP_204_NO_CONTENT: None})
    @action(detail=True, methods=["patch"], url_path="begin")
    def begin(self, request, pk):
        obj = self.get_object()
        serializer = self.get_serializer(instance=obj, data={})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    @extend_schema(responses={status.HTTP_204_NO_CONTENT: None})
    @action(detail=True, methods=["patch"], url_path="finish")
    def finish(self, request, pk):
        obj = self.get_object()
        serializer = self.get_serializer(instance=obj, data={})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)
