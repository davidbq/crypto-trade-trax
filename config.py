from dotenv import load_dotenv
from os import getenv

load_dotenv()

_api_key = getenv('API_KEY')
_secret_key = getenv('SECRET_KEY')

def get_api_key():
    return _api_key

def get_secret_key():
    return _secret_key