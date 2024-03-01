import datetime

from slack_sdk import WebClient

from bonfire import settings


def get_work_locations(start_day=None, end_day=None):
    """
    Get the work locations of the employees
    :param start_date: datetime.datetime
    :param end_date: datetime.datetime
    TODO add pagination support
    TODO turn this into a web socket
    """
    client = WebClient(token=settings.SLACK_TOKEN)

    if start_day is None:
        start_day = datetime.datetime.now().date()
    if end_day is None:
        end_day = datetime.datetime.now().date()

    start_date = datetime.datetime.combine(start_day, datetime.time.min)
    end_date = datetime.datetime.combine(end_day, datetime.time.max)
    result = client.conversations_history(
        channel=settings.WORK_LOCATION_CHANNEL_ID,
        oldest=str(start_date.timestamp()),
        latest=str(end_date.timestamp()),
    )

    mappings = {
        "seb": [":bankman-gangster:" "seb", "bank"],
        "stockholm": [":wood:", ":stockholm:", "wfs", "stockholm"],
        "home": [":house:", ":house_with_garden:", "wfh", "home", "house"],
        "uppsala": [
            ":dragon_face:",
            "wfo",
            ":drake-yep:",
            ":hq-dragon:",
            ":dragon:",
            "dragon",
            "drake",
        ],
        "ooo": [":face_with_thermometer:", "ooo"],
    }

    counters = {
        "uppsala": 0,
        "stockholm": 0,
        "seb": 0,
        "home": 0,
        "ooo": 0,
        "unknown": 0,
    }

    skipped_keywords = ["has joined the channel", "has left the channel"]

    for message in result["messages"]:
        if "text" in message:
            message_text = message["text"].lower()

            locations = [
                location
                for location, keywords in mappings.items()
                if any(keyword in message_text for keyword in keywords)
            ]

            if len(locations) == 0:
                if any(keyword in message_text for keyword in skipped_keywords):
                    continue
                counters["unknown"] += 1
                continue
            for location in locations:
                counters[location] += 1

    return counters
