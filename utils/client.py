import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

BASE_URL = "https://qa-scooter.praktikum-services.ru"

class ApiClient:
    def __init__(self, base_url: str = BASE_URL, timeout: int = 30):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

        self.session = requests.Session()
        self.session.trust_env = False  
        adapter = HTTPAdapter(
            max_retries=Retry(
                total=0, connect=0, read=0, redirect=0, status=0, raise_on_status=False
            )
        )
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

        self.session.headers.update({"Connection": "close"})

    def _url(self, path: str) -> str:
        path = path if path.startswith("/") else f"/{path}"
        return f"{self.base_url}{path}"

    def post(self, path: str, *, timeout=None, **kwargs):
        self.session.cookies.clear()
        return self.session.post(
            self._url(path),
            timeout=timeout if timeout is not None else self.timeout,
            allow_redirects=False,
            **kwargs,
        )

    def get(self, path: str, *, timeout=None, **kwargs):
        self.session.cookies.clear()
        return self.session.get(
            self._url(path),
            timeout=timeout if timeout is not None else self.timeout,
            allow_redirects=False,
            **kwargs,
        )