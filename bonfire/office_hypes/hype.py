from datetime import date

from django.contrib.postgres.search import SearchQuery, SearchVector

from slack.models import SlackMessage, SlackReaction
from users.models import User

from . import serializers

HYPE_MATCHES = {
    serializers.Office.UPPSALA: ["dragon", "drake", "uppsala"],
    serializers.Office.STOCKHOLM: ["wood", "stockholm"],
}


def calculate_hype(date: date, office: serializers.Office):
    hype_number = _calculate_hype_number(date, office)
    hype_level = _calculate_hype_level(hype_number)

    return {
        "location": office,
        "hype_number": hype_number,
        "hype_level": hype_level,
    }


def _calculate_office_check_ins(date: date, office: serializers.Office):
    search_vector = SearchQuery(" | ".join(HYPE_MATCHES[office]), search_type="raw")

    first_msg_from_user = (
        SlackMessage.objects.message_for_date(date)
        .working_location_messages()
        .filter(
            slack_user__in=User.objects.active_slack_users().values("slack_id"),
        )
        .order_by("slack_user", "created_at")
        .distinct("slack_user")
        .values_list("pk")
    )

    return (
        SlackMessage.objects.filter(pk__in=first_msg_from_user)
        .annotate(
            search=SearchVector("message"),
        )
        .filter(search=search_vector)
        .values_list("pk", flat=True)
    )


def _calculate_hype_number(date: date, office: serializers.Office):
    msgs = _calculate_office_check_ins(date, office)

    num_reactions = SlackReaction.objects.filter(
        slack_user__in=User.objects.active_slack_users().values("slack_id"),
        slack_message__in=msgs,
    ).count()

    modifier = round(1 + num_reactions / 100, 1)
    if modifier > 2:
        modifier = 2

    return int(len(msgs) * modifier)


def _calculate_hype_level(hype_number: int):
    if hype_number > 50:
        return serializers.HypeLevel.THREE
    if hype_number > 30:
        return serializers.HypeLevel.TWO
    if hype_number > 10:
        return serializers.HypeLevel.ONE

    return serializers.HypeLevel.ZERO
