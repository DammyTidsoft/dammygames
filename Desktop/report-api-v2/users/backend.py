import logging

import jwt
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework_jwt.settings import api_settings

from .models import User
from .utils import get_mkanid_from_payload

logger = logging.getLogger(__name__)

jwt_decode_handler = api_settings.JWT_DECODE_HANDLER


class JSONWebTokenAuthentication(BaseAuthentication):
    www_authenticate_realm = "api"

    @staticmethod
    def get_jwt_value(request):
        auth = get_authorization_header(request).split()
        auth_header_prefix = api_settings.JWT_AUTH_HEADER_PREFIX.lower()

        if not auth:
            if api_settings.JWT_AUTH_COOKIE:
                return request.COOKIES.get(api_settings.JWT_AUTH_COOKIE)
            return None

        if auth[0].lower() != auth_header_prefix:
            return None

        if len(auth) == 1:
            msg = "Invalid Authorization header. No credentials provided."
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = "Invalid Authorization header. Credentials string should not contain spaces."
            raise exceptions.AuthenticationFailed(msg)

        return auth[1]

    def authenticate_header(self, request):
        return '{0} realm="{1}"'.format(
            api_settings.JWT_AUTH_HEADER_PREFIX, self.www_authenticate_realm
        )

    def authenticate(self, request):
        jwt_value = self.get_jwt_value(request)
        if jwt_value is None:
            return None
        try:
            payload = jwt_decode_handler(jwt_value)
        except jwt.ExpiredSignature:
            msg = "Signature has expired."
            logger.exception("Signature has expired")
            raise exceptions.AuthenticationFailed(msg)
        except jwt.DecodeError:
            logger.exception("Error decoding signature")
            msg = "Error decoding signature."
            raise exceptions.AuthenticationFailed(msg)
        except jwt.InvalidTokenError:
            logger.exception("Invalid Token")
            raise exceptions.AuthenticationFailed()

        user = self.authenticate_credentials(payload)

        return user, jwt_value

    @staticmethod
    def authenticate_credentials(payload):
        mkanid = get_mkanid_from_payload(payload)

        if not mkanid:
            msg = "Invalid payload."
            logger.exception("Invalid payload")
            raise exceptions.AuthenticationFailed(msg)

        user = User.objects.get_by_natural_key(mkanid)
        if not user.is_active:
            logger.exception("Account is disabled!")
            msg = "User account is disabled."
            raise exceptions.AuthenticationFailed(msg)

        return user

    @staticmethod
    def get_user_data(userid):
        try:
            return User.objects.get(pk=userid)
        except Exception:
            return None
