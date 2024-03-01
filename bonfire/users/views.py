from django.db.models import Count, OuterRef, Subquery
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.throttling import AnonRateThrottle

from . import models, permissions, serializers


class UserMeView(generics.RetrieveUpdateDestroyAPIView):
    """
    delete: Removes the currently logged in user (requires field 'password')
    """

    serializer_class = serializers.UserMeSerializer
    permission_classes = (IsAuthenticated,)

    def get_permissions(self):
        perms = super().get_permissions()
        if self.request.method not in (
            "GET",
            "HEAD",
            "POST",
            "PUT",
            "PATCH",
            "OPTIONS",
        ):
            perms.append(permissions.PasswordPermission())
        return perms

    def get_object(self):
        return self.request.user


class LoginThrottle(AnonRateThrottle):
    rate = "overriden/below"  # Needed but overriden by parse_rate()

    def parse_rate(self, rate):
        return 10, 60 * 15  # 10 requests per 15 minutes


class GetVibesView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.GetVibesSerializer

    def get_queryset(self):
        queryset = models.User.objects.exclude(vibe_gif="")
        subquery = Subquery(
            models.User.objects.filter(vibe_gif=OuterRef("vibe_gif"))
            .values("vibe_gif")
            .annotate(total=Count("vibe_gif"))
            .values("total")[:1]
        )
        queryset = queryset.distinct("vibe_gif").annotate(count=subquery)

        return queryset


class UserTokenObtainPairView(generics.CreateAPIView):
    throttle_classes = (LoginThrottle,)
    serializer_class = serializers.UserTokenObtainPairSerializer
    permission_classes = (AllowAny,)
