from typing import List, Any
from ..clients.binance_client import get_binance_client
from ..config.logging import info

def fetch_binance_data(symbol: str, interval: str, start_date: str, end_date: str) -> List[List[Any]]:
    binance_client = get_binance_client()
    info(f"Fetching data for {symbol} from {start_date} to {end_date} with interval {interval}.")
    try:
        data = binance_client.get_historical_klines(symbol, interval, start_date, end_date)
        info(f"Data fetched successfully for {symbol}.")
        return data
    except Exception as e:
        info(f"Error fetching historical data for {symbol}: {e}")
        return []