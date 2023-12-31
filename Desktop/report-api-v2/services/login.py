import requests
from django.conf import settings

from services.user import UserService
from users.models import User
from users.utils import jwt_encode_handler, jwt_payload_handler

headers = {"Content-Type": "application/json"}
URL = "{}/authentication/".format(settings.TAJNID_API_URL)


class LoginService:
    def __init__(self, mkanid: str, password: str, **kwargs) -> None:
        self.mkanid = mkanid
        self.password = password
        self.response = None
        self.kwargs = kwargs

    def login(self) -> (int, dict):
        from common.permissions import get_permissions

        response = requests.post(
            URL, json={"mkanId": self.mkanid, "password": self.password}, **self.kwargs
        )
        self.response = response
        data = response.json()
        if not response.ok:
            self.log(False, data)
            return 401, {"error": data, "message": "Invalid credentials"}
        permissions = get_permissions(data)
        if not permissions:
            self.log(False, "No permissions")
            return 403, {"error": data, "message": "No permissions"}

        payload = jwt_payload_handler(
            self.mkanid, self.password, settings.JWT_AUTH.get("JWT_EXPIRATION_DELTA")
        )
        token = jwt_encode_handler(payload)
        user = UserService.get_or_create(
            self.mkanid,
            self.password,
            permissions=permissions,
            user_details=data,
            name=(data.get("names") + " " + data.get("surname")),
            post=data.get("post"),
        )
        user_service = UserService(user)
        data = user_service.get_post_metadata()
        data["token"] = token
        data["names"] = user.name
        data["post"] = user.post
        data["permissions"] = permissions
        self.log(True, "Login successful")
        return 200, data

    def log(self, success: bool, message: str) -> None:
        from users.models import LoginAuditModel

        data = self.response.json()
        LoginAuditModel.objects.create(
            user=User.objects.filter(mkanid=self.mkanid).first(),
            logged_in_success=success,
            message=message,
            logged_in_name=data.get("names", "") + " " + data.get("surname", ""),
        )
