import logging
from unittest import TestCase, mock

from users.models import User
from users.tests.fixtures import member_data, get_user_mock

logger = logging.getLogger(__name__)


# Create your tests here.


@mock.patch("users.models.User.get_user_data", get_user_mock)
class TestUser(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.user = User.objects.create_user(mkanid="K12345", password="test1234")

    def test_user_created(self):
        self.assertEqual(self.user.mkanid, "K12345")
        self.assertTrue(self.user.check_password("test1234"))

    def test_user_details(self):
        self.assertEqual(self.user.get_user_data(), member_data)

    def test_user_details_refresh(self):
        self.assertEqual(self.user.get_user_data(refresh=True), member_data)
