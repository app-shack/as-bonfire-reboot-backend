from django.http import Http404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from . import models, serializers


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

    http_method_names = [
        "patch",
    ]

    def update(self, request, *args, **kwargs):
        door = self.get_object()
        door.unlock()

        return Response({}, status=status.HTTP_200_OK)


class DoorLockView(DoorMixIn, generics.UpdateAPIView):
    serializer_class = serializers.DoorSerializer
    permission_classes = (IsAuthenticated,)

    http_method_names = [
        "patch",
    ]

    def update(self, request, *args, **kwargs):
        door = self.get_object()
        door.lock()

        return Response({}, status=status.HTTP_200_OK)
