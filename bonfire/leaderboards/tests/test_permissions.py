from unittest.mock import Mock

from users.tests.factories import UserFactory
from utils.test import PermissionTestCase

from .. import models, permissions
from . import factories


class OwnerPermissionTests(PermissionTestCase):
    permission_class = permissions.IsOwnerOrReadOnly

    def setUp(self):
        self.leaderboard = factories.LeaderboardFactory()
        self.user = self.leaderboard.owner
        self.unauthorized_user = UserFactory()

    def test_success(self):
        request = Mock(user=self.user, data={})
        self.assertTrue(self.perm_obj_call(request, None, self.leaderboard))

    def test_fail(self):
        request = Mock(user=self.unauthorized_user, data={})
        self.assertFalse(self.perm_obj_call(request, None, self.leaderboard))


class MemberUserPermissionTests(PermissionTestCase):
    permission_class = permissions.IsMemberUserOrReadOnly

    def setUp(self):
        self.member = factories.LeaderboardMemberFactory()
        self.user = self.member.user
        self.unauthorized_user = UserFactory()

    def test_success(self):
        request = Mock(user=self.user, data={})
        self.assertTrue(self.perm_obj_call(request, None, self.member))

    def test_fail(self):
        request = Mock(user=self.unauthorized_user, data={})
        self.assertFalse(self.perm_obj_call(request, None, self.member))


class MatchWinnerPermissionTests(PermissionTestCase):
    permission_class = permissions.IsMatchWinnerOrReadOnly

    def setUp(self):
        self.match_win = factories.LeaderboardMatchFactory(
            result=models.LeaderboardMatch.MatchResult.PLAYER_A_WIN
        )
        self.match_tie = factories.LeaderboardMatchFactory(
            result=models.LeaderboardMatch.MatchResult.TIE
        )

    def test_winner_report(self):
        request = Mock(user=self.match_win.player_a.user, data={})
        self.assertTrue(self.perm_obj_call(request, None, self.match_win))

    def test_loser_report(self):
        request = Mock(user=self.match_win.player_b.user, data={})
        self.assertFalse(self.perm_obj_call(request, None, self.match_win))

    def test_tie_report(self):
        request = Mock(user=self.match_tie.player_a.user, data={})
        self.assertTrue(self.perm_obj_call(request, None, self.match_tie))

        request = Mock(user=self.match_tie.player_b.user, data={})
        self.assertTrue(self.perm_obj_call(request, None, self.match_tie))
