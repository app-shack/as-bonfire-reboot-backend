from django.conf import settings
from google.auth.transport import requests
from google.oauth2 import id_token


def verify_oauth2_token(token, client_id) -> dict:
    return id_token.verify_oauth2_token(token, requests.Request(), client_id)


def validate_token(id_info) -> bool:
    return id_info["hd"] == settings.GOOGLE_WHITELIST_DOMAIN
