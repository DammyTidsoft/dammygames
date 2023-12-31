from unittest import mock

from rest_framework.test import APITestCase

from common.tests import ResponseMock
from users.tests.fixtures import get_user_mock, member_data, invalid_member_data


@mock.patch("users.models.User.get_user_data", get_user_mock)
class TestObtainJWT(APITestCase):
    @mock.patch("requests.post", return_value=ResponseMock(200, member_data))
    def test_obtain_jwt(self, *args):
        data = {"mkanid": "K12345", "password": "test1234"}
        response = self.client.post("/auth/login/", data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["names"], "User Test")
        self.assertEqual(response.data["post"], "Dila Qaid")

    @mock.patch("requests.post", return_value=ResponseMock(403, invalid_member_data))
    def test_obtain_jwt_invalid(self, *args):
        data = {"mkanid": "K12345", "password": "test12345"}
        response = self.client.post("/auth/login/", data, format="json")
        self.assertEqual(response.status_code, 403)

    @mock.patch("requests.post", return_value=ResponseMock(403, invalid_member_data))
    def test_obtain_jwt_invalid_mkanid(self, *args):
        data = {"mkanid": "K1234", "password": "test1234"}
        response = self.client.post("/auth/login/", data, format="json")
        self.assertEqual(response.status_code, 403)

    @mock.patch("requests.post", return_value=ResponseMock(403, invalid_member_data))
    def test_obtain_jwt_invalid_mkanid_password(self, *args):
        data = {"mkanid": "K12345", "password": "test12345"}
        response = self.client.post("/auth/login/", data, format="json")
        self.assertEqual(response.status_code, 403)
