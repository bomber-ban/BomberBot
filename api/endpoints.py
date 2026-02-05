# /home/xty/Documents/Projects/PetProject/BomberBot_GUI/BomberBot_GUI/api/endpoints.py
#DOMAIN = "https://bomberbot.cc"
DOMAIN = "http://127.0.0.1:8000"

SERVICE_STATUS_URL = f"{DOMAIN}/calls/api/endpoints/service/status"
BALANCE_URL = f"{DOMAIN}/calls/api/endpoints/account/get_balance"
CREATE_ORDER_TIME_URL = f"{DOMAIN}/calls/api/endpoints/create/time"
CREATE_ORDER_SMART_URL = f"{DOMAIN}/calls/api/endpoints/create/smart"
