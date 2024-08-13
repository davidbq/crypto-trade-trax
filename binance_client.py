from binance.client import Client
from config import get_api_key, get_secret_key

api_key = get_api_key()
secret_key = get_secret_key()

client = Client(api_key, secret_key)

def get_binance_client():
    return client