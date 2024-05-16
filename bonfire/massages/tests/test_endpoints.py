from django.utils.timezone import now
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from users.tests.factories import UserFactory

from .. import models
from . import factories


class TodaysMassageQueueEntryViewSetTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()

        cls.queue_entry_1 = factories.MassageQueueEntryFactory(
            queue_position=0,
        )
        cls.queue_entry_2 = factories.MassageQueueEntryFactory(
            user=cls.user,
            queue_position=2,
        )
        cls.queue_entry_3 = factories.MassageQueueEntryFactory(
            queue_position=1,
        )
        cls.queue_entry_4 = factories.MassageQueueEntryFactory(
            queue_position=3,
        )

        cls.detail_url = reverse(
            "massages:todays-queue-detail",
            kwargs={
                "pk": str(cls.queue_entry_2.pk),
            },
        )

        cls.list_url = reverse("massages:todays-queue-list")
        cls.downgrade_url = reverse(
            "massages:todays-queue-downgrade",
            kwargs={
                "pk": str(cls.queue_entry_2.pk),
            },
        )
        cls.begin_url = reverse(
            "massages:todays-queue-begin",
            kwargs={
                "pk": str(cls.queue_entry_2.pk),
            },
        )
        cls.finish_url = reverse(
            "massages:todays-queue-finish",
            kwargs={
                "pk": str(cls.queue_entry_2.pk),
            },
        )

    def setUp(self) -> None:
        self.client.force_authenticate(self.user)

    def test_list(self):
        with self.assertNumQueries(1):
            response = self.client.get(self.list_url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.data), 4)
        self.assertEqual(response.data[0]["id"], str(self.queue_entry_1.pk))
        self.assertEqual(response.data[1]["id"], str(self.queue_entry_3.pk))
        self.assertEqual(response.data[2]["id"], str(self.queue_entry_2.pk))
        self.assertEqual(response.data[3]["id"], str(self.queue_entry_4.pk))

    def test_list_with_done_status(self):
        self.queue_entry_1.status = models.MassageQueueEntry.QueueEntryStatus.DONE
        self.queue_entry_1.save()

        with self.assertNumQueries(1):
            response = self.client.get(self.list_url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data[0]["id"], str(self.queue_entry_3.pk))
        self.assertEqual(response.data[1]["id"], str(self.queue_entry_2.pk))
        self.assertEqual(response.data[2]["id"], str(self.queue_entry_4.pk))

    def test_create(self):
        self.queue_entry_2.delete()

        response = self.client.post(self.list_url, data={})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        models.MassageQueueEntry.objects.get(
            user=self.user,
            created_at__date=now().date(),
        )

    def test_destroy(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        with self.assertRaises(models.MassageQueueEntry.DoesNotExist):
            self.queue_entry_2.refresh_from_db()

        self.queue_entry_1.refresh_from_db()
        self.queue_entry_3.refresh_from_db()
        self.queue_entry_4.refresh_from_db()

        self.assertEqual(self.queue_entry_1.queue_position, 0)
        self.assertEqual(self.queue_entry_3.queue_position, 1)
        self.assertEqual(self.queue_entry_4.queue_position, 2)

    def test_downgrade(self):
        response = self.client.patch(
            self.downgrade_url,
            data={
                "queue_position": self.queue_entry_4.queue_position,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.queue_entry_1.refresh_from_db()
        self.queue_entry_2.refresh_from_db()
        self.queue_entry_3.refresh_from_db()
        self.queue_entry_4.refresh_from_db()

        self.assertEqual(self.queue_entry_1.queue_position, 0)
        self.assertEqual(self.queue_entry_3.queue_position, 1)
        self.assertEqual(self.queue_entry_4.queue_position, 2)
        self.assertEqual(self.queue_entry_2.queue_position, 3)

    def test_begin(self):
        response = self.client.patch(self.begin_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.queue_entry_2.refresh_from_db()

        self.assertEqual(
            self.queue_entry_2.status,
            models.MassageQueueEntry.QueueEntryStatus.IN_PROGRESS.value,
        )

    def test_finish(self):
        self.queue_entry_2.status = (
            models.MassageQueueEntry.QueueEntryStatus.IN_PROGRESS.value
        )
        self.queue_entry_2.save()

        response = self.client.patch(self.finish_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.queue_entry_2.refresh_from_db()

        self.assertEqual(
            self.queue_entry_2.status,
            models.MassageQueueEntry.QueueEntryStatus.DONE.value,
        )
