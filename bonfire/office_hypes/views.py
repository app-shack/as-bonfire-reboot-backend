from datetime import timedelta

from django.core.cache import cache
from django.utils.timezone import now
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from slack.models import SlackMessage
from users.models import User

from . import hype, serializers


class TodaysAttendanceView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.TodaysAttendanceSerializer

    def get_object(self):
        slack_ids = User.objects.active_slack_users().values("slack_id")
        num_check_ins = (
            SlackMessage.objects.todays_messages()
            .working_location_messages()
            .filter(
                slack_user__in=slack_ids,
            )
            .distinct("slack_user")
            .count()
        )

        today = now()
        total_checked_in_percentage = 0
        office_check_ins = 0
        for office in serializers.Office.values:
            check_ins = hype._calculate_office_check_ins(today.date(), office).count()
            office_check_ins += check_ins

        if office_check_ins:
            total_checked_in_percentage = round(office_check_ins / num_check_ins, 2)

        return {"total_checked_in_percentage": total_checked_in_percentage}


class TodaysOfficeHypeView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.OfficeHypeSerializer
    pagination_class = None

    def get_queryset(self):
        return [
            hype.calculate_hype(now().date(), office)
            for office in serializers.Office.values
        ]


class LastWeeksOfficeHypeView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.WeekOfficeHypeSerializer
    pagination_class = None

    cache_timeout = int(timedelta(days=1).total_seconds())

    def get_queryset(self):
        cache_key = f"last-weeks-office-hype-{now().date()}"

        queryset = cache.get(cache_key)
        if not queryset:
            queryset = self._get_queryset()
            cache.set(cache_key, queryset, self.cache_timeout)
        return queryset

    def _get_queryset(self):
        today = now()
        dates = [(today - timedelta(days=i)).date() for i in range(1, 8)]
        dates = filter(lambda d: (d.weekday() < 5), dates)

        return [
            {
                "date": date,
                "hype": [
                    hype.calculate_hype(date, office)
                    for office in serializers.Office.values
                ],
            }
            for date in dates
        ]
