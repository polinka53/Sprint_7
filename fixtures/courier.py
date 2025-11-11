import pytest
from utils.endpoints import CREATE_COURIER, LOGIN_COURIER, DELETE_COURIER
from fixtures.data import build_courier, build_login

@pytest.fixture
def new_courier_payload():
    return build_courier()

@pytest.fixture
def created_courier(api, new_courier_payload):
    r = api.post(CREATE_COURIER, data=new_courier_payload)
    assert r.status_code == 201, f"Ожидали 201 при создании курьера, получили {r.status_code}: {r.text}"
    assert r.json().get("ok") is True
    yield new_courier_payload

    try:
        login_resp = api.post(
            LOGIN_COURIER,
            data=build_login(new_courier_payload["login"], new_courier_payload["password"])
        )
        if login_resp.status_code == 200 and "id" in login_resp.json():
            courier_id = login_resp.json()["id"]
            api.delete(DELETE_COURIER.format(courier_id=courier_id))
    except Exception:
        pass