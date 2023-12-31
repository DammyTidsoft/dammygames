import logging
from datetime import datetime

import jwt
from django.conf import settings
from rest_framework_jwt.settings import api_settings

from users.models import LoginAuditModel, User

BASE_URL = settings.TAJNID_API_URL
headers = {"Content-Type": "application/json"}
logger = logging.getLogger(__name__)


def jwt_payload_handler(mkanid, password, delta):
    # custom payload handler
    payload = {"mkanid": mkanid, "password": password, "exp": datetime.utcnow() + delta}

    return payload


def jwt_get_secret_key(payload=None):
    """
    For enhanced security you may want to use a secret key based on user.

    This way you have an option to logout only this user if:
        - token is compromised
        - password is changed
        - etc.
    """
    if api_settings.JWT_GET_USER_SECRET_KEY:
        user = User.objects.get(pk=payload.get("user_id"))
        key = str(api_settings.JWT_GET_USER_SECRET_KEY(user))
        return key
    return api_settings.JWT_SECRET_KEY


def jwt_encode_handler(payload):
    key = api_settings.JWT_PRIVATE_KEY or jwt_get_secret_key(payload)
    return jwt.encode(payload, key, api_settings.JWT_ALGORITHM).decode("utf-8")


def get_mkanid_from_payload(payload):
    return payload.get("mkanid")


def get_password_from_payload(payload):
    return payload.get("password")


def get_post(resp):
    return resp.json()["post"]


def log_user_login(**kwargs):
    mkanid = kwargs.get("logged_in_user")
    user = User.objects.filter(mkanid=mkanid).first()
    kwargs["user"] = user
    LoginAuditModel.objects.create(**kwargs)
