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
