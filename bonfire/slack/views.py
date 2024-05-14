from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from . import serializers


class IncomingSlackEventWebhookView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = serializers.IncomingSlackEventWebhookSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.validated_data)
        return Response(
            serializer.validated_data, status=status.HTTP_201_CREATED, headers=headers
        )
