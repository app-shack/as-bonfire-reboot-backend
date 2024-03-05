import json
from dataclasses import dataclass

import requests
from django.conf import settings


@dataclass
class Action:
    output_action: str
    output_number: str


class FlexException(Exception):
    pass


def open_door(unit_id, output_number):
    send_action(unit_id, Action("on", output_number))


def close_door(unit_id, output_number):
    send_action(unit_id, Action("off", output_number))


def _send(path, params=None, data=None, method="POST") -> dict:
    base_data = {
        "user": settings.FLEX_API_USER,
        "pass": settings.FLEX_API_PASSWORD,
        "lang": "sv",
    }

    if data:
        data = {**base_data, **data}

    response = requests.request(
        method,
        f"{settings.FLEX_API_URL}{path}",
        params=params,
        json=data,
        timeout=(2, 2),
    )

    try:
        response.raise_for_status()
    except requests.HTTPError:
        raise
    except (requests.ReadTimeout, requests.ConnectTimeout):
        raise

    return response.json()


def get_connections():
    response = _send("appLogin")["d"]
    return json.loads(response)


def send_action(unit_id, action: Action):
    data = {
        "unitId": unit_id,
        "OutputAction": action.output_action,
        "OutputNumber": action.output_number,
    }

    return _send("appControl2", data=data)


def get_connection_status(unit_id):
    data = {
        "unitId": unit_id,
        "demandfetch": True,
    }

    response = _send("appStatus", data=data)["d"]
    return json.loads(response)
