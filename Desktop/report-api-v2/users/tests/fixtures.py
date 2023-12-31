member_data = {
    "stateId": 11,
    "dilaId": 24,
    "jamatId": 119,
    "surname": "Test",
    "names": "User",
    "dateOfBirth": "1981-10-08",
    "email": "test@gmail.com",
    "phoneNumber": "+2341234567",
    "mkanId": "K12345",
    "post": "Dila Qaid",
    "active": "Yes",
}

invalid_member_data = {
    "stateId": 11,
    "dilaId": 24,
    "jamatId": 119,
    "surname": "Test",
    "names": "User",
    "dateOfBirth": "1981-10-08",
    "email": "test@gmail.com",
    "phoneNumber": "+2341234567",
    "mkanId": "K12345",
    "post": "Member",
    "active": "Yes",
}


# Mocks


def get_user_mock(user, refresh=False):
    return member_data


class TajnidLoginMock:
    def __init__(self):
        self.status_code = 200

    def json(self):
        return member_data
