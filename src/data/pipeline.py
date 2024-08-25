from pandas import DataFrame
import logging
import traceback
from ..utils.date import get_yesterday_date
from .collection import fetch_binance_data
from .conversion import convert_to_dataframe
from .cleaning import clean_weekly_data, clean_daily_data
from .formatting import format_weekly_data, format_daily_data
from .transformation import build_weekly_metrics_df, build_daily_metrics_df
from .storage import store_data
from ..globals.constants import FETCH_DATA, SYMBOLS, CSV_PATHS
from ..config.logging import info

def download_and_convert_data(symbol: str, start_date: str, end_date: str, interval: str) -> None:
    data = fetch_binance_data(SYMBOLS[symbol], interval, start_date, end_date)
    return convert_to_dataframe(data)

def weekly_data_pipeline(df: DataFrame, file_path: str) -> DataFrame:
    try:
        info(f'Starting weekly data pipeline')
        df_cleaned = clean_weekly_data(df)
        df_formatted = format_weekly_data(df_cleaned)
        df_transformed = build_weekly_metrics_df(df_formatted)
        store_data(df_transformed, file_path)
        info(f'Weelkly data pipeline completed successfully')
    except Exception as e:
        logging.error(f'Error processing weelkly data pipeline: {e}')
        logging.error(traceback.format_exc())

def daily_data_pipeline(df: DataFrame, file_path: str) -> None:
    try:
        info(f'Starting daily data pipeline')
        df_cleaned = clean_daily_data(df)
        df_formatted = format_daily_data(df_cleaned)
        df_transformed = build_daily_metrics_df(df_formatted)
        store_data(df_transformed, file_path)
        info(f'Daily data pipeline completed successfully')
    except Exception as e:
        logging.error(f'Error processing daily data pipeline: {e}')
        logging.error(traceback.format_exc())

def execute_data_pipelines() -> None:
    start_date = FETCH_DATA['HISTORICAL_START_DATE']
    end_date = get_yesterday_date()
    interval = FETCH_DATA['INTERVAL']
    btc_weekly_path = CSV_PATHS['CRYPTO']['WEEKLY']['BTC']
    fet_weekly_path = CSV_PATHS['CRYPTO']['WEEKLY']['FET']
    btc_daily_path = CSV_PATHS['CRYPTO']['DAILY']['BTC']
    fet_daily_path = CSV_PATHS['CRYPTO']['DAILY']['FET']

    symbols_to_process = [
        {'symbol': 'BTC_USDT', 'weekly_file_path': btc_weekly_path, 'daily_file_path': btc_daily_path },
        {'symbol': 'FET_USDT', 'weekly_file_path': fet_weekly_path, 'daily_file_path': fet_daily_path}
    ]

    for entry in symbols_to_process:
        info(f'Starting data pipelines for {entry["symbol"]}')
        df = download_and_convert_data(entry['symbol'], start_date, end_date, interval)
        weekly_data_pipeline(df, entry['weekly_file_path'])
        daily_data_pipeline(df, entry['daily_file_path'])
        info(f'Completed data pipelines for {entry["symbol"]}')
