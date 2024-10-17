from unittest.mock import patch

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from flex_access.client import FlexException
from users.tests.factories import UserFactory

from .. import models
from . import factories


class DoorViewTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()

        cls.dragon_door = factories.DoorFactory(slug="dragon")

        cls.dragon_detail_url = reverse("doors:door-dragon")
        cls.dragon_lock_url = reverse("doors:door-dragon-lock")
        cls.dragon_unlock_url = reverse("doors:door-dragon-unlock")

    def setUp(self) -> None:
        self.client.force_authenticate(self.user)

        flexy_patcher = patch("flex_access.client.send_action", autospec=True)
        self.addCleanup(flexy_patcher.stop)
        self.flexy_mock = flexy_patcher.start()

    def test_retrieve_dragon(self):
        with self.assertNumQueries(1):
            response = self.client.get(self.dragon_detail_url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.flexy_mock.assert_not_called()

    def test_dragon_lock(self):
        with self.assertNumQueries(3):
            response = self.client.patch(self.dragon_lock_url, data={})
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.dragon_door.refresh_from_db()

        self.flexy_mock.assert_called_once()

        self.assertEqual(models.DoorLog.objects.count(), 1)
        log = models.DoorLog.objects.first()

        self.assertEqual(log.door, self.dragon_door)
        self.assertEqual(log.status, models.Door.StatusType.LOCKED.value)
        self.assertEqual(log.user_first_name, self.user.first_name)
        self.assertEqual(log.user_last_name, self.user.last_name)
        self.assertEqual(log.user_email, self.user.email)

    def test_dragon_unlock(self):
        with self.assertNumQueries(3):
            response = self.client.patch(self.dragon_unlock_url, data={})
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.dragon_door.refresh_from_db()

        self.flexy_mock.assert_called_once()

        self.assertEqual(models.DoorLog.objects.count(), 1)
        log = models.DoorLog.objects.first()

        self.assertEqual(log.door, self.dragon_door)
        self.assertEqual(log.status, models.Door.StatusType.UNLOCKED.value)
        self.assertEqual(log.user_first_name, self.user.first_name)
        self.assertEqual(log.user_last_name, self.user.last_name)
        self.assertEqual(log.user_email, self.user.email)

    def test_dragon_unlock_flex_exception(self):
        self.flexy_mock.side_effect = FlexException

        with self.assertNumQueries(3):
            response = self.client.patch(self.dragon_unlock_url, data={})
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.flexy_mock.assert_called_once()

        self.assertEqual(models.DoorLog.objects.count(), 1)
        log = models.DoorLog.objects.first()

        self.assertEqual(log.door, self.dragon_door)
        self.assertEqual(log.status, models.Door.StatusType.UNKNOWN.value)
        self.assertEqual(log.user_first_name, self.user.first_name)
        self.assertEqual(log.user_last_name, self.user.last_name)
        self.assertEqual(log.user_email, self.user.email)

    def test_dragon_lock_flex_exception(self):
        self.flexy_mock.side_effect = FlexException

        with self.assertNumQueries(3):
            response = self.client.patch(self.dragon_lock_url, data={})
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.flexy_mock.assert_called_once()

        self.assertEqual(models.DoorLog.objects.count(), 1)
        log = models.DoorLog.objects.first()

        self.assertEqual(log.door, self.dragon_door)
        self.assertEqual(log.status, models.Door.StatusType.UNKNOWN.value)
        self.assertEqual(log.user_first_name, self.user.first_name)
        self.assertEqual(log.user_last_name, self.user.last_name)
        self.assertEqual(log.user_email, self.user.email)
