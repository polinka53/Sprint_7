BASE_URL = "https://qa-scooter.praktikum-services.ru"

# Курьеры
CREATE_COURIER = "/api/v1/courier"              # POST (form)
LOGIN_COURIER  = "/api/v1/courier/login"        # POST (form)
DELETE_COURIER = "/api/v1/courier/{courier_id}" # DELETE 

# Заказы
CREATE_ORDER   = "/api/v1/orders"               # POST (json)
LIST_ORDERS    = "/api/v1/orders"               # GET