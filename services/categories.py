import requests
from config import SHEET_URL

def fetch_categories():
    response = requests.get(f"{SHEET_URL}?sheet=storage_list")
    if response.status_code != 200:
        return []
    data = response.json()
    return sorted(set(row.get("category", "Без категории") for row in data if row.get("category")))