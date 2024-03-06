from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from slack_sdk.errors import SlackApiError

from . import utils


class GetWorkLocationsView(generics.RetrieveAPIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        try:
            counters = utils.get_work_locations()

            return Response(counters)

        except SlackApiError as e:
            print(f"Error: {e}")

            return Response({"error": "Error fetching work locations"}, status=500)
