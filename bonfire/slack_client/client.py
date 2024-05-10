from django.conf import settings
from slack_sdk import WebClient, errors

from slack_client.responses import SearchEmailResponse


class SlackClient(WebClient):
    def __init__(self, *args, **kwargs):
        super().__init__(token=settings.SLACK_TOKEN, *args, **kwargs)

    def search_email(self, email) -> SearchEmailResponse:
        try:
            r = self.users_lookupByEmail(email=email)

        except errors.SlackApiError as e:
            raise e

        return SearchEmailResponse.from_kwargs(**r.data)
