import json
from unittest.mock import patch
from django.test import TestCase
from services.login import LoginService

class TestLoginService(TestCase):
    def setUp(self):
        self.valid_mkanid = "Valid_mkanid"
        self.valid_password = "Valid_password"

        self.invalid_mkanid = "invalid_mkanid"
        self.invalid_password = "invalid_password"

        self.valid_response_data = {
            "name": "abdullah",
            "surname": "yusuff",
            "muqam": "liberty",
            "post": "qaid",
        }

        self.invalid_response_data = {
            "error": "Invalid credentials",
            "message": "Invalid credentials",
        }

    @patch("services.login.requests.post")
    @patch("services.login.UserService.get_or_create")
    def test_login(self, mock_get_or_create, mock_post):
        mock_response = self.create_mock_response(json.dumps(self.valid_response_data), status_code=200)
        mock_post.return_value = mock_response

        login_service = LoginService(self.valid_mkanid, self.valid_password)
        status_code, data = login_service.login()

        self.assertEqual(status_code, 200)
        self.assertEqual(data["fullname"], "abdullah yusuff")
        self.assertEqual(data["post"], "qaid")
        self.assertTrue(mock_get_or_create.called)

    @patch("services.login.requests.post")
    def test_failed_login(self, mock_post):
        mock_response = self.create_mock_response(json.dumps(self.invalid_response_data), status_code=401)
        mock_post.return_value = mock_response

        login_service = LoginService(self.invalid_mkanid, self.invalid_password)
        status_code, data = login_service.login()

        self.assertEqual(status_code, 401)
        self.assertEqual(data["error"], self.invalid_response_data["error"])
        self.assertEqual(data["message"], self.invalid_response_data["message"])

    def create_mock_response(self, content, status_code):
        class MockResponse:
            def __init__(self, content, status_code):
                self.content = content.encode("utf-8")
                self.status_code = status_code

            def json(self):
                return json.loads(self.content.decode("utf-8"))

        return MockResponse(content, status_code)
