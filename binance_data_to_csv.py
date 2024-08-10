import pandas as pd
from datetime import datetime, timedelta
from typing import List
from date_utils import get_yesterday_date, get_six_months_ago_monday
from fetch_binance_data import fetch_binance_data
from constants import FETCH_DATA, SYMBOLS

HISTORICAL_START_DATE = FETCH_DATA['HISTORICAL_START_DATE']
RECENT_START_DATE = get_six_months_ago_monday()
END_DATE = get_yesterday_date()
INTERVAL = FETCH_DATA['INTERVAL']
BINANCE_COLUMNS = FETCH_DATA['BINANCE_COLUMNS']

def raw_data_to_csv(data: List, file_name: str) -> None:
    df = pd.DataFrame(data, columns=BINANCE_COLUMNS)
    df.to_csv(f'data/{file_name}.csv', index=False, encoding='utf-8')

def binance_data_to_csv():
    fet_raw_historical_data = fetch_binance_data(SYMBOLS['FET_USDT'], INTERVAL, HISTORICAL_START_DATE, END_DATE)
    raw_data_to_csv(fet_raw_historical_data, 'fet_historical_data')
    fet_raw_recent_data = fetch_binance_data(SYMBOLS['FET_USDT'], INTERVAL, RECENT_START_DATE, END_DATE)
    raw_data_to_csv(fet_raw_recent_data, 'fet_recent_data')
    btc_raw_historical_data = fetch_binance_data(SYMBOLS['BTC_USDT'], INTERVAL, HISTORICAL_START_DATE, END_DATE)
    raw_data_to_csv(btc_raw_historical_data, 'btc_historical_data')
    btc_raw__recent_data = fetch_binance_data(SYMBOLS['BTC_USDT'], INTERVAL, RECENT_START_DATE, END_DATE)
    raw_data_to_csv(btc_raw__recent_data, 'btc_recent_data')