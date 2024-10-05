from rest_framework.test import APITestCase

from .. import models
from . import factories


class LeaderboardMatchTests(APITestCase):
    def setUp(self):
        self.leaderboard = factories.LeaderboardFactory()

    def test_elo_success(self):
        player_a = factories.LeaderboardMemberFactory(
            rating=1000.0, losses=0, ties=0, wins=0, leaderboard=self.leaderboard
        )
        player_b = factories.LeaderboardMemberFactory(
            rating=1000.0, losses=0, ties=0, wins=0, leaderboard=self.leaderboard
        )
        data = {
            "player_a": player_a,
            "player_b": player_b,
            "result": models.LeaderboardMatch.MatchResult.PLAYER_A_WIN,
        }
        match = factories.LeaderboardMatchFactory(**data)
        match.update_elo()
        player_a.refresh_from_db()
        player_b.refresh_from_db()

        self.assertEqual(player_a.losses, 0)
        self.assertEqual(player_a.ties, 0)
        self.assertEqual(player_a.wins, 1)
        self.assertEqual(player_a.rating, 1042.0)

        self.assertEqual(player_b.losses, 1)
        self.assertEqual(player_b.ties, 0)
        self.assertEqual(player_b.wins, 0)
        self.assertEqual(player_b.rating, 958.0)

    def test_elo_zero(self):
        player_a = factories.LeaderboardMemberFactory(
            rating=1000.0, losses=0, ties=0, wins=0, leaderboard=self.leaderboard
        )
        player_b = factories.LeaderboardMemberFactory(
            rating=0.0, losses=0, ties=0, wins=0, leaderboard=self.leaderboard
        )
        data = {
            "player_a": player_a,
            "player_b": player_b,
            "result": models.LeaderboardMatch.MatchResult.PLAYER_A_WIN,
        }
        match = factories.LeaderboardMatchFactory(**data)
        match.update_elo()
        player_a.refresh_from_db()
        player_b.refresh_from_db()

        self.assertEqual(player_a.losses, 0)
        self.assertEqual(player_a.ties, 0)
        self.assertEqual(player_a.wins, 1)
        self.assertEqual(player_a.rating, 1000.2647939713938)

        self.assertEqual(player_b.losses, 1)
        self.assertEqual(player_b.ties, 0)
        self.assertEqual(player_b.wins, 0)
        self.assertEqual(player_b.rating, -0.26479397139385774)

    def test_tie(self):
        player_a = factories.LeaderboardMemberFactory(
            rating=1000.0, losses=0, ties=0, wins=0, leaderboard=self.leaderboard
        )
        player_b = factories.LeaderboardMemberFactory(
            rating=1000.0, losses=0, ties=0, wins=0, leaderboard=self.leaderboard
        )
        data = {
            "player_a": player_a,
            "player_b": player_b,
            "result": models.LeaderboardMatch.MatchResult.TIE,
        }
        match = factories.LeaderboardMatchFactory(**data)
        match.update_elo()
        player_a.refresh_from_db()
        player_b.refresh_from_db()

        self.assertEqual(player_a.losses, 0)
        self.assertEqual(player_a.ties, 1)
        self.assertEqual(player_a.wins, 0)
        self.assertEqual(player_a.rating, 1000.0)

        self.assertEqual(player_b.losses, 0)
        self.assertEqual(player_b.ties, 1)
        self.assertEqual(player_b.wins, 0)
        self.assertEqual(player_b.rating, 1000.0)
