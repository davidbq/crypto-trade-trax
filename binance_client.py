from binance.client import Client
from config import get_api_key, get_secret_key

_api_key = get_api_key()
_secret_key = get_secret_key()

_client = Client(_api_key, _secret_key)

def get_binance_client():
    return _client