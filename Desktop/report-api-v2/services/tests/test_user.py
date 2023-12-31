from django.test import TestCase

from services.user import UserService
from users.models import User


class TestUserService(TestCase):
    user = None
    service = None

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            mkanid="1234567",
            password="test",
            user_details={
                "name": "test",
                "permissions": ["READ:1", "WRITE:1"],
                "post": "State Qaid",
                "jamatId": "1234567",
                "dilaId": "1",
                "stateId": "1",
                "state": "test",
                "dila": "test",
            },
        )

        cls.service = UserService(cls.user)

    def test_is_qaid(self):
        self.assertTrue(self.service.is_qaid())

    def test_is_admin(self):
        self.assertFalse(self.service.is_admin())

    def test_is_mulk(self):
        self.assertFalse(self.service.is_mulk())

    def test_post(self):
        self.assertEquals(self.service.post, "State Qaid")

    def test_report_level(self):
        self.assertEquals(self.service.report_level, "1")

    def test_get_post_id(self):
        self.assertEquals(self.service.get_post_id, "1")

    def test_get_or_create(self):
        self.assertEquals(self.service.get_or_create("1234567", "test"), self.user)

    def test_get_post_metadata(self):
        self.assertEquals(
            self.service.get_post_metadata(), {"stateName": "test", "stateId": "1"}
        )
