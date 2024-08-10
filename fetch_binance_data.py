from typing import List, Any
from binance_client import get_binance_client

def fetch_binance_data(symbol: str, interval: str, start_date: str, end_date: str) -> List[List[Any]]:
    binance_client = get_binance_client()
    try:
        return binance_client.get_historical_klines(symbol, interval, start_date, end_date)
    except Exception as e:
        print(f"Error fetching historical data: {e}")
        return []