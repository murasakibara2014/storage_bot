import requests
import uuid
from config import SHEET_URL

def save_to_sheet(category, name, quantity):
    unique_id = str(uuid.uuid4())
    data = {
        "storageList": {
            "id": unique_id,
            "category": category,
            "name": name,
            "quantity": quantity
        }
    }
    response = requests.post(SHEET_URL, json=data)
    return response.status_code == 201

def update_quantity(category, name, quantity):
    query_url = f"{SHEET_URL}/search?name={name}&category={category}"
    response = requests.get(query_url)
    if response.status_code != 200 or not response.json():
        return False

    update_url = f"{SHEET_URL}/name/{name}?sheet=storage_list"
    data = {
        "data": {
            "name": name,
            "category": category,
            "quantity": str(quantity)
        }
    }
    response = requests.put(update_url, json=data)
    return response.status_code == 200

def get_all_items_grouped_by_category():
    response = requests.get(f"{SHEET_URL}?sheet=storage_list")
    if response.status_code != 200:
        return {}

    items = response.json()
    grouped = {}
    for item in items:
        category = item.get("category", "Без категории")
        grouped.setdefault(category, []).append(f"{item.get('name', 'Без имени')} — {item.get('quantity', '0')}")
    return grouped
