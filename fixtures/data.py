import random
import string

def rand_str(n=10, alphabet=string.ascii_lowercase):
    return "".join(random.choice(alphabet) for _ in range(n))

def build_courier(login=None, password=None, first_name=None):
    return {
        "login": login or rand_str(),
        "password": password or rand_str(),
        "firstName": first_name or rand_str()
    }

def build_login(login, password):
    return {"login": login, "password": password}

def build_order_payload(colors=None):
    return {
        "firstName": "Иван",
        "lastName": "Иванов",
        "address": "Москва, ул. Тестовая, 1",
        "metroStation": 4,
        "phone": "+7 999 111 22 33",
        "rentTime": 5,
        "deliveryDate": "2025-12-31",
        "comment": "Автотест Sprint_7",
        "color": colors or []
    }