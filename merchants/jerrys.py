
import requests
import json
import base64
from config import BASE_URL_JERRYS, JERRYS_AUTH_TOKEN, JERRYS_X_API_KEY

def get_jerrys_user_id():
    token_data = JERRYS_AUTH_TOKEN.split(".")[1]
    token_data += "=" * ((4 - len(token_data) % 4) % 4)
    token_data = token_data.encode("utf-8")
    token_data = base64.b64decode(token_data)
    token_data = json.loads(token_data)
    return token_data["id"]

def process_jerrys_orders(orders):
    total_sum = 0.0
    order_count = 0
    for order in orders:
        amount = float(order["tips"]) + float(order["total"]) + float(order["transportCost"])
        total_sum += amount
        order_count += 1
    return total_sum, order_count

def fetch_jerrys_orders():
    if not JERRYS_AUTH_TOKEN:
        print("JERRYS_AUTH_TOKEN is missing.")
        return 0.0, 0
    if not JERRYS_X_API_KEY:
        print("JERRYS_X_API_KEY is missing.")
        return 0.0, 0

    total_sum = 0.0
    order_count = 0
    user_id = get_jerrys_user_id()
    headers = {
        "Authorization": f"Bearer {JERRYS_AUTH_TOKEN}",
        'AUTH-TYPE' : '2',
        'TEST': '0',
        'USER-ID': str(user_id),
        'X-API-KEY' : JERRYS_X_API_KEY,
    }

    url = BASE_URL_JERRYS.format(user_id)
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to fetch Jerry's data. Status code: {response.status_code}")
        return 0.0, 0
    # print ("Jerry's data: ", response.json())
    data = response.json()
    if "orders" in data:
        total_sum, order_count = process_jerrys_orders(data["orders"])
    else:
        print("No 'orders' key found in jerrys response.")
        return 0.0, 0

    return total_sum, order_count
