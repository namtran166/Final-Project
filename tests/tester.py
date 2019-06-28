import json

from tests.utils import create_headers, load_decoded_response


class Tester:
    def __init__(self, tester):
        self.tester = tester

    def authorize(self, credentials):
        return self.tester.post(
            "/auth",
            headers=create_headers(),
            data=json.dumps(credentials)
        )

    def register(self, register_data):
        return self.tester.post(
            "/users",
            headers=create_headers(),
            data=json.dumps(register_data)
        )

    def get_access_token(self, credentials):
        response = self.authorize(credentials)
        data = load_decoded_response(response)
        return data['access_token']
