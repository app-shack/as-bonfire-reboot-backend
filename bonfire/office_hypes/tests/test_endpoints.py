from django.core.cache import cache
from django.test import override_settings
from django.utils.timezone import now
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from slack.models import SlackMessage
from slack.tests.factories import SlackMessageFactory, SlackReactionFactory
from users.tests.factories import UserFactory


class TodaysAttendanceViewTests(APITestCase):
    SLACK_WORKING_LOCATION_CHANNEL = "working-location"

    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.user_2 = UserFactory()

        UserFactory()

        SlackMessageFactory(
            slack_user=cls.user.slack_id,
            slack_channel=cls.SLACK_WORKING_LOCATION_CHANNEL,
            message="dragon",
        )
        SlackMessageFactory(
            slack_user=cls.user_2.slack_id,
            slack_channel=cls.SLACK_WORKING_LOCATION_CHANNEL,
            message="wfh",
        )
        SlackMessageFactory(
            slack_user=cls.user.slack_id,
            slack_channel="something-else",
        )

        SlackMessageFactory(  # non bonfire user
            slack_channel=cls.SLACK_WORKING_LOCATION_CHANNEL,
        )
        SlackMessageFactory(
            slack_channel="something-else",
        )

        cls.detail_url = reverse(
            "office_hypes:todays-attendance",
        )

    def setUp(self) -> None:
        self.client.force_authenticate(self.user)

    @override_settings(SLACK_WORKING_LOCATION_CHANNEL=SLACK_WORKING_LOCATION_CHANNEL)
    def test_retrieve(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data["total_checked_in_percentage"], 0.5)

    @override_settings(SLACK_WORKING_LOCATION_CHANNEL=SLACK_WORKING_LOCATION_CHANNEL)
    def test_retrieve_divide_by_zero(self):
        SlackMessage.objects.all().delete()

        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data["total_checked_in_percentage"], 0)


class TodaysOfficeHypeViewTests(APITestCase):
    SLACK_WORKING_LOCATION_CHANNEL = "working-location"

    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.non_active_user = UserFactory(slack_id=None)

        cls.msg = SlackMessageFactory(
            slack_user=cls.user.slack_id,
            slack_channel=cls.SLACK_WORKING_LOCATION_CHANNEL,
            message="dragon",
        )
        SlackMessageFactory(  # check ins should be counted once
            slack_user=cls.user.slack_id,
            slack_channel=cls.SLACK_WORKING_LOCATION_CHANNEL,
            message=":stockholm:",
        )
        SlackMessageFactory(
            slack_user=cls.user.slack_id,
            slack_channel="something-else",
        )

        SlackMessageFactory(  # non bonfire user
            slack_channel=cls.SLACK_WORKING_LOCATION_CHANNEL,
        )
        SlackMessageFactory(
            slack_channel="something-else",
        )

        # Creating some dragon hype
        for _ in range(10):
            msg = SlackMessageFactory(
                slack_user=UserFactory().slack_id,
                slack_channel=cls.SLACK_WORKING_LOCATION_CHANNEL,
                message="drake",
            )

            SlackReactionFactory.create_batch(
                5,
                slack_message=msg,
                slack_user=msg.slack_user,
            )

        cls.list_url = reverse(
            "office_hypes:todays-office-hype",
        )

    def setUp(self) -> None:
        self.client.force_authenticate(self.user)

    @override_settings(SLACK_WORKING_LOCATION_CHANNEL=SLACK_WORKING_LOCATION_CHANNEL)
    def test_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for r in response.data:
            self.assertIn("hype_level", r)
            self.assertIn("hype_number", r)
            self.assertIn("location", r)


class LastWeeksOfficeHypeViewTests(APITestCase):
    SLACK_WORKING_LOCATION_CHANNEL = "working-location"

    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.non_active_user = UserFactory(slack_id=None)

        cls.msg = SlackMessageFactory(
            slack_user=cls.user.slack_id,
            slack_channel=cls.SLACK_WORKING_LOCATION_CHANNEL,
            message="dragon",
        )
        SlackMessageFactory(  # check ins should be counted once
            slack_user=cls.user.slack_id,
            slack_channel=cls.SLACK_WORKING_LOCATION_CHANNEL,
            message=":stockholm:",
        )
        SlackMessageFactory(
            slack_user=cls.user.slack_id,
            slack_channel="something-else",
        )

        SlackMessageFactory(  # non bonfire user
            slack_channel=cls.SLACK_WORKING_LOCATION_CHANNEL,
        )
        SlackMessageFactory(
            slack_channel="something-else",
        )

        # Creating some dragon hype
        for _ in range(10):
            msg = SlackMessageFactory(
                slack_user=UserFactory().slack_id,
                slack_channel=cls.SLACK_WORKING_LOCATION_CHANNEL,
                message="drake",
            )

            SlackReactionFactory.create_batch(
                5,
                slack_message=msg,
                slack_user=msg.slack_user,
            )

        cls.list_url = reverse(
            "office_hypes:last-weeks-office-hype",
        )

    def setUp(self) -> None:
        self.client.force_authenticate(self.user)

        cache.clear()

    @override_settings(SLACK_WORKING_LOCATION_CHANNEL=SLACK_WORKING_LOCATION_CHANNEL)
    def test_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for r in response.data:
            self.assertIn("date", r)
            self.assertIn("hype", r)

            for rh in r["hype"]:
                self.assertIn("hype_level", rh)
                self.assertIn("hype_number", rh)
                self.assertIn("location", rh)

        cache_key = f"last-weeks-office-hype-{now().date()}"
        cached_data = cache.get(cache_key)
        self.assertIsNotNone(cached_data)
