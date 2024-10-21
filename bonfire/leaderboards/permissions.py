from rest_framework import permissions

from . import models


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to delete or update it.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user


class IsMemberUserOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow the member user of an object to delete or update it.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user


class IsMatchWinnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow the winner (or either player if its a tie) to report a match.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if obj.result == models.LeaderboardMatch.MatchResult.PLAYER_A_WIN:
            return request.user == obj.player_a.user
        elif obj.result == models.LeaderboardMatch.MatchResult.PLAYER_B_WIN:
            return request.user == obj.player_b.user
        else:
            return (
                request.user == obj.player_a.user or request.user == obj.player_b.user
            )
