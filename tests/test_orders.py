import pytest
import allure
from utils.endpoints import CREATE_ORDER, LIST_ORDERS
from fixtures.data import build_order_payload

@allure.epic("Orders")
@allure.feature("Создание заказа")
class TestCreateOrder:
    @allure.title("Создание заказа: BLACK/GREY/оба/без цвета → 201 и есть track")
    @pytest.mark.parametrize("colors", [
        (["BLACK"], "BLACK"),
        (["GREY"], "GREY"),
        (["BLACK", "GREY"], "BOTH"),
        ([], "NONE")
    ], ids=["black", "grey", "both", "none"])
    @pytest.mark.smoke
    def test_create_order_colors(self, api, colors):
        color_list, _ = colors
        payload = build_order_payload(color_list)
        r = api.post(CREATE_ORDER, json=payload)
        assert r.status_code == 201, f"Ожидали 201, получили {r.status_code}: {r.text}"
        assert isinstance(r.json().get("track"), int)

@allure.epic("Orders")
@allure.feature("Список заказов")
class TestOrdersList:
    @allure.title("GET /orders возвращает список заказов")
    def test_orders_list(self, api):
        r = api.get(LIST_ORDERS)
        assert r.status_code == 200
        body = r.json()
        assert isinstance(body.get("orders"), list)