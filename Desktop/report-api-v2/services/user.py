from users.models import User

POST_MAP = {"1": "stateId", "2": "dilaId", "3": "jamatId"}


class UserService:
    def __init__(self, user, refresh_data=False):
        self.user = user
        self.user_details = user.get_user_data(refresh=refresh_data)
        self.response = None

    @classmethod
    def get_or_create(cls, mkanid, password, **kwargs):
        try:
            user = User.objects.get(mkanid=mkanid)
        except User.DoesNotExist:
            user = User(mkanid=mkanid)
        user.set_password(password)
        for key, value in kwargs.items():
            setattr(user, key, value)
        user.save()
        return user

    def is_qaid(self):
        for permission in self.user.permissions:
            perm_level = permission.split(":")[1]
            if perm_level in ["1", "2", "3"]:
                return True
        return False

    def is_admin(self):
        return self.user.is_superuser or self.user.is_staff

    def is_mulk(self):
        for permission in self.user.permissions:
            perm_level = permission.split(":")[1]
            if perm_level == "0":
                return True
        return False

    @property
    def post(self):
        return self.user_details.get("post", "")

    @property
    def report_level(self):
        return self.user.permissions[0].split(":")[1]

    @property
    def get_post_id(self):
        return self.user_details.get(POST_MAP[self.report_level])

    def get_post_metadata(self):
        if self.report_level == "0":
            return {"mulk": "Mulk Officer"}
        if self.report_level == "1":
            return {
                "stateId": self.user_details.get("stateId"),
                "stateName": self.user_details.get("state"),
            }
        if self.report_level == "2":
            return {
                "dilaId": self.user_details.get("dilaId"),
                "dilaName": self.user_details.get("dila"),
            }
        if self.report_level == "3":
            return {
                "muqamiId": self.user_details.get("jamatId"),
                "muqamiName": self.user_details.get("muqami"),
            }
