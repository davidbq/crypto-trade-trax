import logging
import traceback
from ..utils.date import get_yesterday_date
from .collection import fetch_binance_data
from .conversion import convert_data
from .cleaning import clean_data
from .formatting import format_data
from .transformation import transform_data
from .storage import store_data
from ..globals.constants import FETCH_DATA, SYMBOLS, CSV_PATHS
from ..config.logging import info

def process_symbol_data(symbol: str, start_date: str, end_date: str, interval: str, file_path: str) -> None:
    try:
        info(f'Starting data pipeline for {symbol}')
        data = fetch_binance_data(SYMBOLS[symbol], interval, start_date, end_date)
        df = convert_data(data)
        df_cleaned = clean_data(df)
        df_formatted = format_data(df_cleaned)
        df_transformed = transform_data(df_formatted)
        store_data(df_transformed, file_path)
        info(f'Data pipeline for {symbol} completed successfully')
    except Exception as e:
        logging.error(f'Error processing data for {symbol}: {e}')
        logging.error(traceback.format_exc())

def execute_data_pipeline() -> None:
    start_date = FETCH_DATA['HISTORICAL_START_DATE']
    end_date = get_yesterday_date()
    interval = FETCH_DATA['INTERVAL']
    btc_path = CSV_PATHS['CRYPTO']['BTC']
    fet_path = CSV_PATHS['CRYPTO']['FET']

    symbols_to_process = [
        {'symbol': 'BTC_USDT', 'file_path': btc_path },
        {'symbol': 'FET_USDT', 'file_path': fet_path }
    ]

    for entry in symbols_to_process:
        process_symbol_data(entry['symbol'], start_date, end_date, interval, entry['file_path'])
