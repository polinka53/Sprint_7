import pytest
import allure

from utils.endpoints import CREATE_ORDER, LIST_ORDERS 
from fixtures.orders import build_order_payload


@allure.suite("Orders: create")
class TestCreateOrder:
    @allure.title("Можно создать заказ с одним цветом → 201 и есть track")
    @pytest.mark.parametrize("colors", [
        ["BLACK"],
        ["GREY"],
    ])
    def test_create_order_single_color(self, api, colors):
        payload = build_order_payload(colors)

        r = api.post(CREATE_ORDER, data=payload, timeout=12)

        assert r.status_code == 201, (
            f"Ожидали 201, получили {r.status_code}: {r.text}"
        )
        assert r.json().get("track"), (
            f"В ответе нет track: {r.text}"
        )

    @allure.title("Можно указать оба цвета → 201 и есть track")
    def test_create_order_both_colors(self, api):
        payload = build_order_payload(["BLACK", "GREY"])

        r = api.post(CREATE_ORDER, data=payload, timeout=12)

        assert r.status_code == 201, (
            f"Ожидали 201, получили {r.status_code}: {r.text}"
        )
        assert r.json().get("track"), (
            f"В ответе нет track: {r.text}"
        )

    @allure.title("Можно создать заказ без указания цвета → 201 и есть track")
    def test_create_order_no_color(self, api):
        payload = build_order_payload([])

        r = api.post(CREATE_ORDER, data=payload, timeout=12)

        assert r.status_code == 201, (
            f"Ожидали 201, получили {r.status_code}: {r.text}"
        )
        assert r.json().get("track"), (
            f"В ответе нет track: {r.text}"
        )


@allure.suite("Orders: list")
class TestOrdersList:
    @allure.title("Список заказов возвращается и это массив")
    def test_orders_list_is_array(self, api):
        r = api.get(LIST_ORDERS , timeout=12)

        assert r.status_code == 200, (
            f"Ожидали 200, получили {r.status_code}: {r.text}"
        )

        orders = r.json().get("orders")
        assert isinstance(orders, list), "Поле 'orders' должно быть списком"
        assert len(orders) > 0, "Список заказов пустой"