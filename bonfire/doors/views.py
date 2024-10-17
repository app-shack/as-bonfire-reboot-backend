from django.http import Http404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle

from . import models, serializers


class AuthenticatedUserRateThrottle(UserRateThrottle):
    rate = "5/minute"

    def allow_request(self, request, view):
        if request.user.is_superuser:
            return True

        return super().allow_request(request, view)


class DoorMixIn:
    def get_object(self):
        slug = self.get_slug()
        try:
            door = models.Door.objects.get(slug=slug)
        except models.Door.DoesNotExist:
            raise Http404
        return door

    def get_slug(self):
        return self.request.path_info.split("/")[3]


class DoorView(DoorMixIn, generics.RetrieveAPIView):
    serializer_class = serializers.DoorSerializer
    permission_classes = (IsAuthenticated,)


class DoorUnlockView(DoorMixIn, generics.UpdateAPIView):
    serializer_class = serializers.DoorSerializer
    permission_classes = (IsAuthenticated,)
    throttle_classes = (AuthenticatedUserRateThrottle,)

    http_method_names = [
        "patch",
    ]

    def update(self, request, *args, **kwargs):
        door = self.get_object()
        door.unlock()

        models.DoorLog.objects.create_from_door(door, request.user)

        return Response({}, status=status.HTTP_200_OK)


class DoorLockView(DoorMixIn, generics.UpdateAPIView):
    serializer_class = serializers.DoorSerializer
    permission_classes = (IsAuthenticated,)
    throttle_classes = (AuthenticatedUserRateThrottle,)

    http_method_names = [
        "patch",
    ]

    def update(self, request, *args, **kwargs):
        door = self.get_object()
        door.lock()

        models.DoorLog.objects.create_from_door(door, request.user)

        return Response({}, status=status.HTTP_200_OK)
