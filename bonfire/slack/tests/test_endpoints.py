from django.conf import settings
from django.utils.timezone import datetime
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from .. import models
from . import factories


class IncomingSlackEventWebhookViewTests(APITestCase):
    CHANNEL_MESSAGE_WORKING_CHANNEL = {
        "token": "one-long-verification-token",
        "team_id": "T123ABC456",
        "api_app_id": "A123ABC456",
        "event": {
            "type": "message",
            "channel": "C123ABC456",
            "user": "U123ABC456",
            "text": "Live long and prospect.",
            "ts": "1355517523.000005",
            "event_ts": "1355517523.000005",
            "channel_type": "channel",
        },
        "type": "event_callback",
        "authed_teams": [
            "T123ABC456",
        ],
        "event_id": "Ev123ABC456",
        "event_time": 1355517523,
    }

    CHANNEL_MESSAGE_OTHER_CHANNEL = {
        "token": "one-long-verification-token",
        "team_id": "T123ABC456",
        "api_app_id": "A123ABC456",
        "event": {
            "type": "message",
            "channel": "other_channel",
            "user": "U123ABC456",
            "text": "Live long and prospect.",
            "ts": "1355517523.000005",
            "event_ts": "1355517523.000005",
            "channel_type": "channel",
        },
        "type": "event_callback",
        "authed_teams": [
            "T123ABC456",
        ],
        "event_id": "Ev123ABC456",
        "event_time": 1355517523,
    }

    CHANNEL_MESSAGE_CHANGED_WORKING_CHANNEL = {
        "api_app_id": "A072FHKBNBH",
        "authorizations": None,
        "context_enterprise_id": None,
        "context_team_id": "T03UWSJSK",
        "event": {
            "channel": "C123ABC456",
            "channel_type": "channel",
            "event_ts": "1715758508.034900",
            "hidden": True,
            "message": {
                "blocks": [
                    {
                        "block_id": "'SAqU/'",
                        "elements": "[{'type': 'rich_text_section', 'elements': [{'type': 'text', 'text': 'WFH (OOO @ 11)'}]}]",  # noqa
                        "type": "'rich_text'",
                    }
                ],
                "client_msg_id": "5cce6c9e-6385-4abc-a98c-38ad536a2ec1",
                "edited": {"ts": "1715758508.000000", "user": "U05TR1B8N74"},
                "source_team": "T03UWSJSK",
                "team": "T03UWSJSK",
                "text": "WFH (OOO @ 11)",
                "ts": "1715757464.051429",
                "type": "message",
                "user": "U05TR1B8N74",
                "user_team": "T03UWSJSK",
            },
            "previous_message": {
                "blocks": [
                    {
                        "block_id": "'CTzww'",
                        "elements": "[{'type': 'rich_text_section', 'elements': [{'type': 'text', 'text': 'WFH'}]}]",  # noqa
                        "type": "'rich_text'",
                    }
                ],
                "client_msg_id": "5cce6c9e-6385-4abc-a98c-38ad536a2ec1",
                "team": "T03UWSJSK",
                "text": "WFH",
                "ts": "1715757464.051429",
                "type": "message",
                "user": "U05TR1B8N74",
            },
            "subtype": "message_changed",
            "ts": "1715758508.034900",
            "type": "message",
        },
        "event_id": "Ev073AP37MSS",
        "event_time": 1715758508,
        "team_id": "T03UWSJSK",
        "token": "[Filtered]",
        "type": "event_callback",
    }

    CHANNEL_MESSAGE_CHANGED_OTHER_CHANNEL = {
        "api_app_id": "A072FHKBNBH",
        "authorizations": None,
        "context_enterprise_id": None,
        "context_team_id": "T03UWSJSK",
        "event": {
            "channel": "other_channel",
            "channel_type": "channel",
            "event_ts": "1715758508.034900",
            "hidden": True,
            "message": {
                "blocks": [
                    {
                        "block_id": "'SAqU/'",
                        "elements": "[{'type': 'rich_text_section', 'elements': [{'type': 'text', 'text': 'WFH (OOO @ 11)'}]}]",  # noqa
                        "type": "'rich_text'",
                    }
                ],
                "client_msg_id": "5cce6c9e-6385-4abc-a98c-38ad536a2ec1",
                "edited": {"ts": "1715758508.000000", "user": "U05TR1B8N74"},
                "source_team": "T03UWSJSK",
                "team": "T03UWSJSK",
                "text": "WFH (OOO @ 11)",
                "ts": "1715757464.051429",
                "type": "message",
                "user": "U05TR1B8N74",
                "user_team": "T03UWSJSK",
            },
            "previous_message": {
                "blocks": [
                    {
                        "block_id": "'CTzww'",
                        "elements": "[{'type': 'rich_text_section', 'elements': [{'type': 'text', 'text': 'WFH'}]}]",  # noqa
                        "type": "'rich_text'",
                    }
                ],
                "client_msg_id": "5cce6c9e-6385-4abc-a98c-38ad536a2ec1",
                "team": "T03UWSJSK",
                "text": "WFH",
                "ts": "1715757464.051429",
                "type": "message",
                "user": "U05TR1B8N74",
            },
            "subtype": "message_changed",
            "ts": "1715758508.034900",
            "type": "message",
        },
        "event_id": "Ev073AP37MSS",
        "event_time": 1715758508,
        "team_id": "T03UWSJSK",
        "token": "[Filtered]",
        "type": "event_callback",
    }

    CHANNEL_MESSAGE_DELETED_WORKING_CHANNEL = {
        "api_app_id": "A072FHKBNBH",
        "authorizations": None,
        "context_enterprise_id": None,
        "context_team_id": "T03UWSJSK",
        "event": {
            "channel": "C123ABC456",
            "channel_type": "channel",
            "deleted_ts": "1715699820.013519",
            "event_ts": "1715699842.030500",
            "hidden": True,
            "previous_message": {
                "blocks": [
                    {
                        "block_id": "'XWaxq'",
                        "elements": "[{'type': 'rich_text_section', 'elements': [{'type': 'text', 'text': 'bonfire!'}]}]",  # noqa
                        "type": "'rich_text'",
                    }
                ],
                "client_msg_id": "0b0e163a-9629-435e-8466-a5089f99a7c5",
                "team": "T03UWSJSK",
                "text": "bonfire!",
                "ts": "1715699820.013519",
                "type": "message",
                "user": "U03UK3FE127",
            },
            "subtype": "message_deleted",
            "ts": "1715699842.030500",
            "type": "message",
        },
        "event_id": "Ev072YPBS2KH",
        "event_time": 1715699842,
        "team_id": "T03UWSJSK",
        "token": "[Filtered]",
        "type": "event_callback",
    }

    CHANNEL_MESSAGE_DELETED_OTHER_CHANNEL = {
        "api_app_id": "A072FHKBNBH",
        "authorizations": None,
        "context_enterprise_id": None,
        "context_team_id": "T03UWSJSK",
        "event": {
            "channel": "other_channel",
            "channel_type": "channel",
            "deleted_ts": "1715699820.013519",
            "event_ts": "1715699842.030500",
            "hidden": True,
            "previous_message": {
                "blocks": [
                    {
                        "block_id": "'XWaxq'",
                        "elements": "[{'type': 'rich_text_section', 'elements': [{'type': 'text', 'text': 'bonfire!'}]}]",  # noqa
                        "type": "'rich_text'",
                    }
                ],
                "client_msg_id": "0b0e163a-9629-435e-8466-a5089f99a7c5",
                "team": "T03UWSJSK",
                "text": "bonfire!",
                "ts": "1715699820.013519",
                "type": "message",
                "user": "U03UK3FE127",
            },
            "subtype": "message_deleted",
            "ts": "1715699842.030500",
            "type": "message",
        },
        "event_id": "Ev072YPBS2KH",
        "event_time": 1715699842,
        "team_id": "T03UWSJSK",
        "token": "[Filtered]",
        "type": "event_callback",
    }

    CHANNEL_JOINED = {
        "api_app_id": "A072FHKBNBH",
        "authorizations": None,
        "context_enterprise_id": None,
        "context_team_id": "T03UWSJSK",
        "event": {
            "channel": "C06LVSLSXDL",
            "channel_type": "channel",
            "event_ts": "1715689807.952509",
            "inviter": "U03UK3FE127",
            "subtype": "channel_join",
            "text": "<@U072W1J7P99> has joined the channel",
            "ts": "1715689807.952509",
            "type": "message",
            "user": "U072W1J7P99",
        },
        "event_id": "Ev073C6DMUDQ",
        "event_time": 1715689807,
        "team_id": "T03UWSJSK",
        "token": "[Filtered]",
        "type": "event_callback",
    }

    REACTION_ADDED_WORKING_CHANNEL = {
        "api_app_id": "A072FHKBNBH",
        "authorizations": None,
        "context_enterprise_id": None,
        "context_team_id": "T03UWSJSK",
        "event": {
            "event_ts": "1715690227.003000",
            "item": {
                "channel": "C123ABC456",
                "ts": "1715689807.952509",
                "type": "message",
            },
            "reaction": "fire",
            "type": "reaction_added",
            "user": "U02NZHS9TPD",
        },
        "event_id": "Ev07411BRTCY",
        "event_time": 1715690227,
        "team_id": "T03UWSJSK",
        "token": "[Filtered]",
        "type": "event_callback",
    }

    REACTION_ADDED_OTHER_CHANNEL = {
        "api_app_id": "A072FHKBNBH",
        "authorizations": None,
        "context_enterprise_id": None,
        "context_team_id": "T03UWSJSK",
        "event": {
            "event_ts": "1715690227.003000",
            "item": {
                "channel": "other_channel",
                "ts": "1715689807.952509",
                "type": "message",
            },
            "reaction": "fire",
            "type": "reaction_added",
            "user": "U02NZHS9TPD",
        },
        "event_id": "Ev07411BRTCY",
        "event_time": 1715690227,
        "team_id": "T03UWSJSK",
        "token": "[Filtered]",
        "type": "event_callback",
    }

    REACTION_REMOVED_WORKING_CHANNEL = {
        "api_app_id": "A072FHKBNBH",
        "authorizations": None,
        "context_enterprise_id": None,
        "context_team_id": "T03UWSJSK",
        "event": {
            "type": "reaction_removed",
            "user": "U123ABC456",
            "reaction": "thumbsup",
            "item_user": "U222222222",
            "item": {
                "type": "message",
                "channel": "C123ABC456",
                "ts": "1360782400.498405",
            },
            "event_ts": "1360782804.083113",
        },
        "event_id": "Ev07411BRTCY",
        "event_time": 1715690227,
        "team_id": "T03UWSJSK",
        "token": "[Filtered]",
        "type": "event_callback",
    }

    REACTION_REMOVED_OTHER_CHANNEL = {
        "api_app_id": "A072FHKBNBH",
        "authorizations": None,
        "context_enterprise_id": None,
        "context_team_id": "T03UWSJSK",
        "event": {
            "type": "reaction_removed",
            "user": "U123ABC456",
            "reaction": "thumbsup",
            "item_user": "U222222222",
            "item": {
                "type": "message",
                "channel": "other_channel",
                "ts": "1360782400.498405",
            },
            "event_ts": "1360782804.083113",
        },
        "event_id": "Ev07411BRTCY",
        "event_time": 1715690227,
        "team_id": "T03UWSJSK",
        "token": "[Filtered]",
        "type": "event_callback",
    }

    USER_PROFILE_CHANGED = {
        "type": "user_profile_changed",
        "user": {
            "id": "U1234567",
            "team_id": "T1234567",
            "name": "some-user",
            "deleted": False,
            "color": "4bbe2e",
            "real_name": "Some User",
            "tz": "America/Los_Angeles",
            "tz_label": "Pacific Daylight Time",
            "tz_offset": -25200,
            "profile": {
                "title": "",
                "phone": "",
                "skype": "",
                "real_name": "Some User",
                "real_name_normalized": "Some User",
                "display_name": "",
                "display_name_normalized": "",
                "fields": {},
                "status_text": "riding a train",
                "status_emoji": ":mountain_railway:",
                "status_emoji_display_info": [],
                "status_expiration": 0,
                "avatar_hash": "g12345678910",
                "first_name": "Some",
                "last_name": "User",
                "image_24": "https://secure.gravatar.com/avatar/cb0c2b2ca5e8de16be31a55a734d0f31.jpg?s=24&d=https%3A%2F%2Fdev.slack.com%2Fdev-cdn%2Fv1648136338%2Fimg%2Favatars%2Fuser_shapes%2Fava_0001-24.png",  # noqa
                "image_32": "https://secure.gravatar.com/avatar/cb0c2b2ca5e8de16be31a55a734d0f31.jpg?s=32&d=https%3A%2F%2Fdev.slack.com%2Fdev-cdn%2Fv1648136338%2Fimg%2Favatars%2Fuser_shapes%2Fava_0001-32.png",  # noqa
                "image_48": "https://secure.gravatar.com/avatar/cb0c2b2ca5e8de16be31a55a734d0f31.jpg?s=48&d=https%3A%2F%2Fdev.slack.com%2Fdev-cdn%2Fv1648136338%2Fimg%2Favatars%2Fuser_shapes%2Fava_0001-48.png",  # noqa
                "image_72": "https://secure.gravatar.com/avatar/cb0c2b2ca5e8de16be31a55a734d0f31.jpg?s=72&d=https%3A%2F%2Fdev.slack.com%2Fdev-cdn%2Fv1648136338%2Fimg%2Favatars%2Fuser_shapes%2Fava_0001-72.png",  # noqa
                "image_192": "https://secure.gravatar.com/avatar/cb0c2b2ca5e8de16be31a55a734d0f31.jpg?s=192&d=https%3A%2F%2Fdev.slack.com%2Fdev-cdn%2Fv1648136338%2Fimg%2Favatars%2Fuser_shapes%2Fava_0001-192.png",  # noqa
                "image_512": "https://secure.gravatar.com/avatar/cb0c2b2ca5e8de16be31a55a734d0f31.jpg?s=512&d=https%3A%2F%2Fdev.slack.com%2Fdev-cdn%2Fv1648136338%2Fimg%2Favatars%2Fuser_shapes%2Fava_0001-512.png",  # noqa
                "status_text_canonical": "",
                "team": "T1234567",
            },
            "is_admin": False,
            "is_owner": False,
            "is_primary_owner": False,
            "is_restricted": False,
            "is_ultra_restricted": False,
            "is_bot": False,
            "is_app_user": False,
            "updated": 1648596421,
            "is_email_confirmed": False,
            "who_can_share_contact_card": "EVERYONE",
            "locale": "en-US",
        },
        "cache_ts": 1648596421,
        "event_ts": "1648596712.000001",
    }

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("slack:incoming-slack-event-webhook")

    @staticmethod
    def unix_to_dt(unix) -> datetime:
        return datetime.fromtimestamp(float(unix)).astimezone(settings.TZ)

    def setUp(self) -> None:
        self.client.force_authenticate(None)

    def test_create_url_verification(self):
        data = {
            "token": "Jhj5dZrVaK7ZwHHjRyZWjbDl",
            "challenge": "3eZbrw1aBm2rZgRNFdxV2595E9CY3gmdALWMmHkvFXO7tYXAYM8P",
            "type": "url_verification",
        }

        with self.assertNumQueries(0):
            response = self.client.post(self.url, data=data)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        expected_response = {
            "challenge": data["challenge"],
        }
        self.assertEqual(response.data, expected_response)

    def test_create_event_callback_channel_message_working_channel(self):
        data = self.CHANNEL_MESSAGE_WORKING_CHANNEL.copy()

        with self.assertNumQueries(1):
            response = self.client.post(self.url, data=data, format="json")
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        num_msg = models.SlackMessage.objects.count()
        self.assertEqual(num_msg, 1)

        msg = models.SlackMessage.objects.first()
        self.assertEqual(msg.slack_channel, data["event"]["channel"])
        self.assertEqual(msg.slack_user, data["event"]["user"])
        self.assertEqual(msg.message, data["event"]["text"])
        self.assertDictEqual(msg.raw_data, data)

    def test_create_event_callback_channel_message_other_channel(self):
        data = self.CHANNEL_MESSAGE_OTHER_CHANNEL.copy()

        with self.assertNumQueries(0):
            response = self.client.post(self.url, data=data, format="json")
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        num_msg = models.SlackMessage.objects.count()
        self.assertEqual(num_msg, 0)

    def test_create_event_callback_channel_message_changed_working_channel(self):
        data = self.CHANNEL_MESSAGE_CHANGED_WORKING_CHANNEL.copy()

        msg = factories.SlackMessageFactory(
            slack_ts=self.unix_to_dt(data["event"]["ts"]), message="test"
        )

        with self.assertNumQueries(1):
            response = self.client.post(self.url, data=data, format="json")
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        num_msg = models.SlackMessage.objects.count()
        self.assertEqual(num_msg, 1)

        msg.refresh_from_db()
        self.assertEqual(msg.message, data["event"]["message"]["text"])

    def test_create_event_callback_channel_message_changed_other_channel(self):
        data = self.CHANNEL_MESSAGE_CHANGED_OTHER_CHANNEL.copy()

        factories.SlackMessageFactory(slack_ts=self.unix_to_dt(data["event"]["ts"]))

        with self.assertNumQueries(0):
            response = self.client.post(self.url, data=data, format="json")
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        num_msg = models.SlackMessage.objects.count()
        self.assertEqual(num_msg, 1)

    def test_create_event_callback_channel_message_deleted_working_channel(self):
        data = self.CHANNEL_MESSAGE_DELETED_WORKING_CHANNEL.copy()

        factories.SlackMessageFactory(
            slack_ts=self.unix_to_dt(data["event"]["deleted_ts"])
        )

        with self.assertNumQueries(3):
            response = self.client.post(self.url, data=data, format="json")
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        num_msg = models.SlackMessage.objects.count()
        self.assertEqual(num_msg, 0)

    def test_create_event_callback_channel_message_deleted_other_channel(self):
        data = self.CHANNEL_MESSAGE_DELETED_OTHER_CHANNEL.copy()

        with self.assertNumQueries(0):
            response = self.client.post(self.url, data=data, format="json")
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_event_callback_channel_join(self):
        data = self.CHANNEL_JOINED.copy()

        with self.assertNumQueries(0):
            response = self.client.post(self.url, data=data, format="json")
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        num_msg = models.SlackMessage.objects.count()
        self.assertEqual(num_msg, 0)

    def test_create_reaction_added_working_channel(self):
        data = self.REACTION_ADDED_WORKING_CHANNEL.copy()

        factories.SlackMessageFactory(
            slack_ts=self.unix_to_dt(data["event"]["item"]["ts"])
        )

        with self.assertNumQueries(2):
            response = self.client.post(self.url, data=data, format="json")
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        num_msg = models.SlackMessage.objects.count()
        self.assertEqual(num_msg, 1)

        num_reaction = models.SlackReaction.objects.count()
        self.assertEqual(num_reaction, 1)

        reaction = models.SlackReaction.objects.first()
        self.assertTrue(reaction.raw_data)

    def test_create_reaction_added_other_channel(self):
        data = self.REACTION_ADDED_OTHER_CHANNEL.copy()

        with self.assertNumQueries(0):
            response = self.client.post(self.url, data=data, format="json")
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        num_msg = models.SlackMessage.objects.count()
        self.assertEqual(num_msg, 0)

        num_reaction = models.SlackReaction.objects.count()
        self.assertEqual(num_reaction, 0)

    def test_create_reaction_added_working_channel_message_does_not_exist(self):
        data = self.REACTION_ADDED_WORKING_CHANNEL.copy()

        with self.assertNumQueries(1):
            response = self.client.post(self.url, data=data, format="json")
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        num_msg = models.SlackMessage.objects.count()
        self.assertEqual(num_msg, 0)

        num_reaction = models.SlackReaction.objects.count()
        self.assertEqual(num_reaction, 0)

    def test_create_reaction_removed_working_channel(self):
        data = self.REACTION_REMOVED_WORKING_CHANNEL.copy()

        msg = factories.SlackMessageFactory(
            slack_ts=self.unix_to_dt(data["event"]["item"]["ts"]),
        )
        factories.SlackReactionFactory(
            slack_message=msg,
            slack_user=data["event"]["user"],
            slack_reaction=data["event"]["reaction"],
        )

        with self.assertNumQueries(1):
            response = self.client.post(self.url, data=data, format="json")
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        num_msg = models.SlackMessage.objects.count()
        self.assertEqual(num_msg, 1)

        num_msg = models.SlackReaction.objects.count()
        self.assertEqual(num_msg, 0)

    def test_create_reaction_removed_other_channel(self):
        data = self.REACTION_REMOVED_OTHER_CHANNEL.copy()

        with self.assertNumQueries(0):
            response = self.client.post(self.url, data=data, format="json")
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        num_msg = models.SlackMessage.objects.count()
        self.assertEqual(num_msg, 0)

        num_reaction = models.SlackReaction.objects.count()
        self.assertEqual(num_reaction, 0)

    def test_create_reaction_removed_working_channel_reaction_does_not_exist(self):
        data = self.REACTION_REMOVED_WORKING_CHANNEL.copy()

        with self.assertNumQueries(1):
            response = self.client.post(self.url, data=data, format="json")
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        num_msg = models.SlackMessage.objects.count()
        self.assertEqual(num_msg, 0)

        num_reaction = models.SlackReaction.objects.count()
        self.assertEqual(num_reaction, 0)

    def test_create_user_profile_changed(self):
        data = self.USER_PROFILE_CHANGED.copy()

        with self.assertNumQueries(0):
            response = self.client.post(self.url, data=data, format="json")
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        num_msg = models.SlackMessage.objects.count()
        self.assertEqual(num_msg, 0)
