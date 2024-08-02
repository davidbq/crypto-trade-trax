from dotenv import load_dotenv
from os import getenv

load_dotenv()

api_key = getenv('API_KEY')
secret_key = getenv('SECRET_KEY')

def get_api_key():
  return api_key

def get_secret_key():
  return secret_key
