import uuid

from django.utils.timezone import now
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from .. import models
from . import factories


class LeaderboardViewTests(APITestCase):
    def setUp(self):
        self.leaderboard = factories.LeaderboardFactory()
        self.client.force_authenticate(user=self.leaderboard.owner)
        self.url = reverse(
            "leaderboards:leaderboard", kwargs={"pk": self.leaderboard.id}
        )
        self.list_url = reverse("leaderboards:leaderboard-list")
        self.create_url = reverse("leaderboards:leaderboard-create")

    def test_retrieve(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], str(self.leaderboard.id))
        self.assertEqual(response.data["name"], self.leaderboard.name)

    def test_update(self):
        data = {
            "id": "random-id",
            "name": "Ping Pong Q3 2024",
        }
        self.assertNotEqual(self.leaderboard.id, data["id"])
        self.assertNotEqual(self.leaderboard.name, data["name"])

        response = self.client.patch(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data["id"], str(self.leaderboard.id))
        self.assertNotEqual(response.data["name"], self.leaderboard.name)

        self.assertNotEqual(response.data["id"], data["id"])
        self.assertEqual(response.data["name"], data["name"])

        self.leaderboard.refresh_from_db()

        self.assertNotEqual(self.leaderboard.id, data["id"])
        self.assertEqual(self.leaderboard.name, data["name"])

    def test_create(self):
        data = {"name": "Ping Pong Q3 2024"}
        response = self.client.post(self.create_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], data["name"])
        self.assertFalse(
            models.Leaderboard.objects.filter(
                id=uuid.UUID(int=1234),
                created_at__date=now().date(),
            ).exists()
        )
        self.assertTrue(
            models.Leaderboard.objects.filter(
                id=response.data["id"],
                created_at__date=now().date(),
            ).exists()
        )

    def test_list(self):
        response = self.client.get(self.list_url, data={})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)


class LeaderboardMemberViewTests(APITestCase):
    def setUp(self):
        self.leaderboard = factories.LeaderboardFactory()
        self.members = factories.LeaderboardMemberFactory.create_batch(
            5, leaderboard=self.leaderboard
        )
        self.member = self.members[0]
        self.members_other = factories.LeaderboardMemberFactory.create_batch(3)
        self.client.force_authenticate(user=self.member.user)
        self.url = reverse(
            "leaderboards:leaderboard-member", kwargs={"pk": self.member.id}
        )
        self.list_url = reverse(
            "leaderboards:leaderboard-member-list",
            kwargs={"leaderboard": self.leaderboard.id},
        )
        self.create_url = reverse("leaderboards:leaderboard-member-create")

    def test_list(self):
        response = self.client.get(self.list_url, data={})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), len(self.members))

    def test_create(self):
        data = {
            "leaderboard": self.leaderboard.id,
            "nickname": "Bob the Builder",
        }
        response = self.client.post(self.create_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["leaderboard"], data["leaderboard"])
        self.assertEqual(response.data["user"], self.member.user.id)
        self.assertEqual(response.data["nickname"], data["nickname"])
        self.assertEqual(response.data["rating"], 1000.0)
        self.assertEqual(response.data["ties"], 0)
        self.assertEqual(response.data["wins"], 0)
        self.assertEqual(response.data["losses"], 0)
        models.LeaderboardMember.objects.filter(
            id=response.data["id"],
            created_at__date=now().date(),
        )

    def test_retrieve(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], str(self.member.id))
        self.assertEqual(response.data["leaderboard"], self.member.leaderboard.id)
        self.assertEqual(response.data["user"], self.member.user.id)
        self.assertEqual(response.data["nickname"], self.member.nickname)
        self.assertEqual(response.data["rating"], self.member.rating)
        self.assertEqual(response.data["wins"], self.member.wins)
        self.assertEqual(response.data["ties"], self.member.ties)
        self.assertEqual(response.data["losses"], self.member.losses)

    def test_update(self):
        data = {
            "nickname": "Bobby B",
            "rating": 999999999,
            "wins": 1337,
        }
        self.assertNotEqual(self.member.nickname, data["nickname"])
        self.assertNotEqual(self.member.rating, data["rating"])
        self.assertNotEqual(self.member.wins, data["wins"])

        response = self.client.patch(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertNotEqual(response.data["nickname"], str(self.member.nickname))
        self.assertEqual(response.data["rating"], self.member.rating)
        self.assertEqual(response.data["wins"], self.member.wins)

        self.member.refresh_from_db()

        self.assertEqual(self.member.nickname, data["nickname"])
        self.assertNotEqual(self.member.rating, data["rating"])
        self.assertNotEqual(self.member.wins, data["wins"])


class LeaderboardMatchViewTests(APITestCase):
    def setUp(self):
        self.player_a = factories.LeaderboardMemberFactory()
        self.player_b = factories.LeaderboardMemberFactory(
            leaderboard=self.player_a.leaderboard
        )
        self.client.force_authenticate(user=self.player_a)
        self.url = reverse("leaderboards:leaderboard-add-match")

    def test_create_success(self):
        data = {
            "player_a": self.player_a.id,
            "player_b": self.player_b.id,
            "result": str(models.LeaderboardMatch.MatchResult.PLAYER_A_WIN),
        }
        response = self.client.post(self.url, data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["player_a"], data["player_a"])
        self.assertEqual(response.data["player_b"], data["player_b"])
        self.assertEqual(response.data["result"], data["result"])

        models.LeaderboardMatch.objects.filter(
            id=response.data["id"],
            created_at__date=now().date(),
        )

    def test_create_different_leaderboards(self):
        other_player = factories.LeaderboardMemberFactory()
        data = {
            "player_a": self.player_a.id,
            "player_b": other_player.id,
            "result": str(models.LeaderboardMatch.MatchResult.PLAYER_A_WIN),
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_same_player(self):
        data = {
            "player_a": self.player_a.id,
            "player_b": self.player_a.id,
            "result": str(models.LeaderboardMatch.MatchResult.PLAYER_A_WIN),
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
