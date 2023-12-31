import json


class ResponseMock(object):
    def __init__(self, status_code, response_json=None):
        self.status_code = status_code
        self.response_json = response_json
        self.content = json.dumps(response_json)

    def json(self):
        return self.response_json

    def raise_for_status(self):
        pass

    def ok(self):
        return str(self.status_code).startswith("2")
