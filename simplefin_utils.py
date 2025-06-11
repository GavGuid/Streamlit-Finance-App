import os
import requests
from dotenv import load_dotenv

load_dotenv()

def get_simplefin_data():
    """Fetch account data from SimpleFIN API."""
    url = os.getenv("SIMPLEFIN_TOKEN_URL")
    if not url:
        raise ValueError("SIMPLEFIN_TOKEN_URL not set in .env")
    api_url = f"{url.rstrip('/')}/accounts"
    response = requests.get(api_url)
    return response.json()

data = get_simplefin_data()
needs_account = next(acc for acc in data['accounts'] if acc['name'] == 'Needs - 2188')
wants_account = next(acc for acc in data['accounts'] if acc['name'] == 'Wants - 8700')
planned_account = next(acc for acc in data['accounts'] if acc['name'] == 'Planned Expenses - 6501')

print(f"Needs Account Balance: {needs_account['balance']}")
print(f"Wants Account Balance: {wants_account['balance']}")
print(f"Planned Account Balance: {planned_account['balance']}")