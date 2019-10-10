import requests


class APIClient:
    def __init__(self, base_address):
        self.base_address = base_address

    def get(self, path="/", params=None):
        return requests.get(url=self.base_address + path, params=params)
