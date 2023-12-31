import json

import requests
from django.conf import settings


class TajneedService:
    BASE_URL = settings.TAJNID_API_URL
    LOGIN_PATH = "/login"
    stats = {}

    def __init__(self, user, refresh=False):
        self.user = user
        user_service = user.get_service()
        self.report_level = user_service.report_level
        self.post_id = user_service.get_post_id

    def prepare_url(self, path: str = "") -> str:
        return self.BASE_URL + path

    def make_request(
        self, path, method="get", params=None, data=None, headers=None
    ) -> requests.Response:
        if data is None:
            data = {}
        if params is None:
            params = {}
        if headers is None:
            headers = {}

        if not method:
            method = "get"

        headers.update({"Accept": "application/json"})
        url = self.prepare_url(path)
        response = getattr(requests, method.lower())(
            url=url, params=params, data=data, headers=headers
        )
        return response

    def get_dila(self, dila_id):
        path = "/dila/%s" % dila_id
        response = self.make_request(path)

        if response.status_code == 200:
            dila = json.loads(response.content.decode("utf-8"))
            return dila["name"]
        else:
            return None

    def get_state(self, state_id):
        path = "/states/{}".format(state_id)
        response = self.make_request(path)

        if response.status_code == 200:
            state = json.loads(response.content.decode("utf-8"))
            return state["name"]
        else:
            return None

    def get_muqami(self, muqami_id):
        path = "/muqami/{}".format(muqami_id)
        response = self.make_request(path)

        if response.status_code == 200:
            muqami = json.loads(response.content.decode("utf-8"))
            return muqami["name"]
        else:
            return None

    def get_states(self):
        path = "/states/"
        response = self.make_request(path)
        if response.status_code == 200:
            return json.loads(response.content.decode("utf-8"))
        return None

    def get_dilas(self):
        path = "/dila/"
        response = self.make_request(path)
        if response.status_code == 200:
            return json.loads(response.content.decode("utf-8"))
        return None

    def get_muqamis(self):
        path = "/muqami/"
        response = self.make_request(path)
        if response.status_code == 200:
            return json.loads(response.content.decode("utf-8"))
        return None

    def get_user_data(self, mkan_id):
        path = "/members/{}".format(mkan_id)
        response = self.make_request(path)
        if response.status_code == 200:
            return json.loads(response.content.decode("utf-8"))
        else:
            return {}

    def get_post_suffix(self, mkan_id):
        path = "/members/{}".format(mkan_id)
        response = self.make_request(path)

        if response.status_code == 200:
            mkanq = json.loads(response.content.decode("utf-8"))
            if "Dila" in mkanq["post"]:
                return "2"
            if "State" in mkanq["post"]:
                return "1"
            if "Muqami" in mkanq["post"]:
                return "3"
        else:
            return None

    def get_id(self):
        if self.report_level == "2":
            return self.user_details["stateId"]
        elif self.report_level == "2":
            return self.user_details["dilaId"]
        else:
            return self.user_details["jamatId"]

    def get_children(self):
        if self.report_level == "1":
            path = "/states/{}/dilas".format(self.post_id)
        elif self.report_level == "2":
            path = "/dila/{}/muqamis".format(self.post_id)
        else:
            return []
        response = self.make_request(path)
        if response.status_code == 200:
            return response.json()
        return []

    def atfal_tajnid(self):
        stats = self.get_statistics()
        if stats:
            return stats["numberOfAtfalMembers"]
        return 0

    def get_statistics(self):
        if self.stats:
            return self.stats

        if self.report_level == "1":
            path = "/states/{}/statistics/".format(self.post_id)
        elif self.report_level == "2":
            path = "/dila/{}/statistics/".format(self.post_id)
        else:
            path = "/muqami/{}/statistics/".format(self.post_id)
        response = self.make_request(path)
        if response.status_code == 200:
            self.stats = response.json()
            return self.stats
        else:
            return {}

    def khudam_tajnid(self):
        stats = self.get_statistics()
        if stats:
            return stats["numberOfMembers"]
        return 0

    def overage(self):
        stats = self.get_statistics()
        if stats:
            return stats["numberOfOveragedMembers"]
