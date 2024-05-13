from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase


class IncomingSlackEventWebhookViewTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("slack:incoming-slack-event-webhook")

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
