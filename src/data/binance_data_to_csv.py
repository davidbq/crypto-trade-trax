import pandas as pd
from typing import List
from ..utils.date_utils import get_yesterday_date, six_months_ago_monday
from .fetch_binance_data import fetch_binance_data
from ..globals.constants import FETCH_DATA, SYMBOLS, CSV_PATHS
from ..config.logging import info

HISTORICAL_START_DATE = FETCH_DATA['HISTORICAL_START_DATE']
RECENT_START_DATE = six_months_ago_monday()
END_DATE = get_yesterday_date()
INTERVAL = FETCH_DATA['INTERVAL']
BINANCE_COLUMNS = FETCH_DATA['BINANCE_COLUMNS']

def save_data_to_csv(data: List, file_path: str) -> None:
    df = pd.DataFrame(data, columns=BINANCE_COLUMNS)
    df.to_csv(file_path, index=False, encoding='utf-8')

    info(f"Data successfully saved to {file_path}")

def process_binance_data():
    data_to_process = [
        {'symbol': 'BTC_USDT', 'start_date': HISTORICAL_START_DATE, 'file_path': CSV_PATHS['BTC_HISTORICAL']},
        {'symbol': 'BTC_USDT', 'start_date': RECENT_START_DATE, 'file_path': CSV_PATHS['BTC_RECENT']},
        {'symbol': 'FET_USDT', 'start_date': HISTORICAL_START_DATE, 'file_path': CSV_PATHS['FET_HISTORICAL']},
        {'symbol': 'FET_USDT', 'start_date': RECENT_START_DATE, 'file_path': CSV_PATHS['FET_RECENT']}
    ]
    for entry in data_to_process:
        data = fetch_binance_data(SYMBOLS[entry['symbol']], INTERVAL, entry['start_date'], END_DATE)
        save_data_to_csv(data, entry['file_path'])

    info("All data processed and saved successfully.")