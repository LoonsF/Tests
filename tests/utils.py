from fastapi.testclient import TestClient


class TestCliente:
    def __init__(self, app):
        self.client = TestClient(app)

    def get(self, url, params=None):
        return self.client.get(url, params=params)

    def post(self, url, json=None):
        return self.client.post(url, json=json)

    def put(self, url, json=None):
        return self.client.put(url, json=json)

    def delete(self, url):
        return self.client.delete(url)
