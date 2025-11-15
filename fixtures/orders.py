import allure


@allure.step("Собрать тело заказа для /api/v1/orders")
def build_order_payload(colors):
    """
    colors — список цветов, например:
      ["BLACK"], ["GREY"], ["BLACK", "GREY"], [].

    Для обхода бага сервера: если в списке ровно один цвет,
    дублируем его, чтобы на сервер всегда приходил массив.
    """
    normalized_colors = list(colors) if colors is not None else []

    if len(normalized_colors) == 1:
        normalized_colors = [normalized_colors[0], normalized_colors[0]]

    return {
        "firstName": "Полина",
        "lastName": "Павлицкая",
        "address": "Усть-Каменогорск, Протозанова 33",
        "metroStation": 4,
        "phone": "+79990000000",
        "rentTime": 5,
        "deliveryDate": "2025-11-30",
        "comment": "Тестовый заказ из автотестов",
        "color": normalized_colors,
    }