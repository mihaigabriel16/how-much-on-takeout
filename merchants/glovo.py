import requests
import re
from config import BASE_URL_GLOVO, GLOVO_AUTH_TOKEN

def process_glovo_orders(orders):
    total_sum = 0.0
    order_count = 0
    for order in orders:
        footer_left_data = order["footer"]["left"]["data"]
        amount = re.search(r"([\d,]+)\sRON", footer_left_data)
        if amount:
            numeric_value = float(amount.group(1).replace(",", "."))
            total_sum += numeric_value
            order_count += 1
    return total_sum, order_count

def fetch_glovo_orders():
    if not GLOVO_AUTH_TOKEN:
        print("GLOVO_AUTH_TOKEN is missing.")
        return 0.0, 0
    
    offset = 0
    total_sum = 0.0
    order_count = 0
    headers = {
        "Authorization": f"Bearer {GLOVO_AUTH_TOKEN}", 
        "Glovo-App-Platform": "web",
    }

    while True:
        url = BASE_URL_GLOVO.format(offset)
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(f"Failed to fetch Glovo data. Status code: {response.status_code}")
            break

        data = response.json()
        if "orders" in data:
            sum_part, count_part = process_glovo_orders(data["orders"])
            total_sum += sum_part
            order_count += count_part
        else:
            print("No 'orders' key found in Glovo response.")
            break

        next_page = data.get("pagination", {}).get("next")
        if not next_page:
            break
        else:
            offset = next_page.get("offset", offset)

    return total_sum, order_count
