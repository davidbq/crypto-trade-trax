import pandas as pd
from datetime import datetime, timedelta
from typing import List
from date_utils import get_yesterday_date, get_six_months_ago_monday
from fetch_binance_data import fetch_binance_data
from constants import FETCH_DATA, SYMBOLS

_HISTORICAL_START_DATE = FETCH_DATA['HISTORICAL_START_DATE']
_RECENT_START_DATE = get_six_months_ago_monday()
_END_DATE = get_yesterday_date()
_INTERVAL = FETCH_DATA['INTERVAL']
_BINANCE_COLUMNS = FETCH_DATA['BINANCE_COLUMNS']

def raw_data_to_csv(data: List, file_name: str) -> None:
    df = pd.DataFrame(data, columns=_BINANCE_COLUMNS)
    df.to_csv(f'data/{file_name}.csv', index=False, encoding='utf-8')

def binance_data_to_csv():
    fet_raw_historical_data = fetch_binance_data(SYMBOLS['FET_USDT'], _INTERVAL, _HISTORICAL_START_DATE, _END_DATE)
    raw_data_to_csv(fet_raw_historical_data, 'fet_historical_data')
    fet_raw_recent_data = fetch_binance_data(SYMBOLS['FET_USDT'], _INTERVAL, _RECENT_START_DATE, _END_DATE)
    raw_data_to_csv(fet_raw_recent_data, 'fet_recent_data')
    btc_raw_historical_data = fetch_binance_data(SYMBOLS['BTC_USDT'], _INTERVAL, _HISTORICAL_START_DATE, _END_DATE)
    raw_data_to_csv(btc_raw_historical_data, 'btc_historical_data')
    btc_raw__recent_data = fetch_binance_data(SYMBOLS['BTC_USDT'], _INTERVAL, _RECENT_START_DATE, _END_DATE)
    raw_data_to_csv(btc_raw__recent_data, 'btc_recent_data')