from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny

from . import models, serializers


class OfficeViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = serializers.OfficeSerializer
    permission_classes = (AllowAny,)
    pagination_class = None

    def get_queryset(self):
        return models.Office.objects.order_by("name")
