import requests

class ApiClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()

    def post(self, endpoint: str, **kwargs):
        """POST-запрос через общую сессию."""
        return self.session.post(self.base_url + endpoint, **kwargs)

    def get(self, endpoint: str, **kwargs):
        """GET-запрос через общую сессию."""
        return self.session.get(self.base_url + endpoint, **kwargs)

    def delete(self, endpoint: str, **kwargs):
        """DELETE-запрос через общую сессию."""
        return self.session.delete(self.base_url + endpoint, **kwargs)