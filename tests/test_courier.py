import pytest
import allure

from utils.endpoints import CREATE_COURIER, LOGIN_COURIER
from fixtures.data import build_courier, build_login

KNOWN_LOGIN = "polinka53"
KNOWN_PASSWORD = "poli123"
KNOWN_FIRST_NAME = "polina"


def _ensure_courier_exists(api, login, password, first_name):
    """
    Гарантированно создает курьера, если его еще нет.
    201 ({ok: true}) — все хорошо
    409 — уже существует — тоже ок для наших целей
    """
    payload = {"login": login, "password": password, "firstName": first_name}
    r = api.post(CREATE_COURIER, data=payload, timeout=12)
    if r.status_code not in (201, 409):
        pytest.fail(f"Не удалось подготовить курьера: {r.status_code}: {r.text}")


@allure.suite("Courier")
class TestCreateCourier:

    @allure.title("Курьера можно создать → 201 и ok=true")
    def test_create_courier_success(self, api):
        payload = build_courier()
        r = api.post(CREATE_COURIER, data=payload, timeout=12)
        assert r.status_code == 201, f"Ожидали 201, получили {r.status_code}: {r.text}"
        assert r.json().get("ok") is True

    @allure.title("Для создания курьера нужны логин и пароль → 400")
    @pytest.mark.parametrize("missing", ["login", "password"])
    def test_create_courier_missing_required(self, api, missing):
        payload = build_courier()
        payload.pop(missing)
        r = api.post(CREATE_COURIER, data=payload, timeout=12)
        assert r.status_code == 400, f"Ожидали 400, получили {r.status_code}: {r.text}"
        assert r.json().get("message") in (
            "Недостаточно данных для создания учетной записи",
            "Недостаточно данных для создания учетной записи."
        )


@allure.suite("Login")
class TestLoginCourier:

    @allure.title("Курьер может авторизоваться → 200 и есть id")
    def test_login_success(self, api):
        _ensure_courier_exists(api, KNOWN_LOGIN, KNOWN_PASSWORD, KNOWN_FIRST_NAME)
        r = api.post(LOGIN_COURIER, data=build_login(KNOWN_LOGIN, KNOWN_PASSWORD), timeout=12)
        assert r.status_code == 200, f"Ожидали 200, получили {r.status_code}: {r.text}"
        assert "id" in r.json() and isinstance(r.json()["id"], int)

    @allure.title("Для авторизации нужен login → 400 (ключ отсутствует)")
    def test_login_missing_login(self, api):
        payload = build_login("any_login", "any_pass")
        payload.pop("login")
        r = api.post(LOGIN_COURIER, data=payload, timeout=12)
        assert r.status_code == 400, f"Ожидали 400, получили {r.status_code}: {r.text}"
        assert r.json().get("message") in (
            "Недостаточно данных для входа",
            "Недостаточно данных для входа."
        )

    @allure.title("Неверные логин/пароль → 404 'Учетная запись не найдена'")
    @pytest.mark.parametrize(
        "login,password",
        [
            ("no_such_login__", KNOWN_PASSWORD),   
            (KNOWN_LOGIN, "__bad_pass__"),         
        ],
    )
    def test_login_wrong_credentials(self, api, login, password):
        _ensure_courier_exists(api, KNOWN_LOGIN, KNOWN_PASSWORD, KNOWN_FIRST_NAME)
        r = api.post(LOGIN_COURIER, data=build_login(login, password), timeout=12)
        assert r.status_code == 404, f"Ожидали 404, получили {r.status_code}: {r.text}"
        assert r.json().get("message") in (
            "Учетная запись не найдена",
            "Учетная запись не найдена."
        )