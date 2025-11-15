import random
import string

import pytest
import allure

from utils.endpoints import CREATE_COURIER, LOGIN_COURIER
from fixtures.data import KNOWN_LOGIN, KNOWN_PASSWORD, KNOWN_FIRST_NAME


def _rand_str(n: int = 10) -> str:
    alphabet = string.ascii_lowercase + string.digits
    return "".join(random.choice(alphabet) for _ in range(n))


@allure.step("Сформировать валидный payload курьера")
def build_courier() -> dict:
    return {
        "login": f"qa_{_rand_str(8)}",
        "password": _rand_str(10),
        "firstName": "QA",
    }


@allure.step("Сформировать payload логина")
def build_login(login: str, password: str) -> dict:
    return {"login": login, "password": password}


@pytest.fixture
@allure.step("Подготовить новый payload курьера")
def new_courier_payload() -> dict:
    """Просто отдаёт валидный payload курьера."""
    return build_courier()


@pytest.fixture
@allure.step("Создать курьера и вернуть его payload")
def created_courier(api, new_courier_payload) -> dict:
    """
    Создаёт курьера с валидными данными и возвращает ТОЛЬКО payload.
    Без assert'ов и без удаления — это разрешено, ревьюер просил
    только убрать проверки из фикстур.
    """
    api.post(CREATE_COURIER, data=new_courier_payload, timeout=12)
    return new_courier_payload


@allure.step("Убедиться, что курьер с известными данными существует")
def ensure_known_courier(api) -> None:
    """Если курьера с KNOWN_LOGIN нет — создаём его."""
    r = api.post(
        LOGIN_COURIER,
        data={"login": KNOWN_LOGIN, "password": KNOWN_PASSWORD},
        timeout=12,
    )

    if r.status_code == 404:
        api.post(
            CREATE_COURIER,
            data={
                "login": KNOWN_LOGIN,
                "password": KNOWN_PASSWORD,
                "firstName": KNOWN_FIRST_NAME,
            },
            timeout=12,
        )