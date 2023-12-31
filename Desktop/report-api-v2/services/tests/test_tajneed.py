from django.test import TestCase
from services.tajneed import TajneedService
from users.models import User


class TestTajneedService(TestCase):
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
            },
        )

        cls.service = TajneedService(cls.user)

    def test_get_dilas(self):
        pass

    def test_get_states(self):
        pass

    def test_get_muqamis(self):
        pass

    def test_get_dila(self):
        pass

    def test_get_state(self):
        pass

    def test_get_muqami(self):
        pass

    def test_get_user_data(self):
        pass

    def test_get_post_suffix(self):
        pass

    def test_get_id(self):
        pass

    def test_get_children(self):
        pass

    def test_atfal_tajnid(self):
        pass

    def test_get_statistics(self):
        pass

    def test_khudam_tajnid(self):
        pass

    def test_overage(self):
        pass
