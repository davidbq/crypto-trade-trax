import pandas as pd
from typing import List
from ..globals.constants import BINANCE_COL_NAMES

OPEN_TIME = BINANCE_COL_NAMES['OPEN_TIME']
OPEN_PRICE = BINANCE_COL_NAMES['OPEN_PRICE']
CLOSE_PRICE = BINANCE_COL_NAMES['CLOSE_PRICE']
HIGH_PRICE = BINANCE_COL_NAMES['HIGH_PRICE']
LOW_PRICE = BINANCE_COL_NAMES['LOW_PRICE']
VOLUME = BINANCE_COL_NAMES['VOLUME']
NUMBER_OF_TRADES = BINANCE_COL_NAMES['NUMBER_OF_TRADES']
TAKER_BUY_BASE_VOLUME = BINANCE_COL_NAMES['TAKER_BUY_BASE_VOLUME']

def format_columns_to_float(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    df = df.copy()
    for col in columns:
        df[col] = df[col].astype(float)
    return df

def set_datetime_index(df: pd.DataFrame, time_column: str) -> pd.DataFrame:
    df = df.copy()
    df[time_column] = pd.to_datetime(df[time_column].astype(float), unit='ms')
    df.set_index(time_column, inplace=True)
    return df

def format_daily_data(df: pd.DataFrame) -> pd.DataFrame:
    columns_to_float = [
        OPEN_PRICE, CLOSE_PRICE, HIGH_PRICE,
        LOW_PRICE, VOLUME, NUMBER_OF_TRADES,
        TAKER_BUY_BASE_VOLUME
    ]

    df = format_columns_to_float(df, columns_to_float)
    df = set_datetime_index(df, OPEN_TIME)

    return df

def format_weekly_data(df: pd.DataFrame) -> pd.DataFrame:
    columns_to_float = [ OPEN_PRICE, CLOSE_PRICE ]

    df = format_columns_to_float(df, columns_to_float)
    df = set_datetime_index(df, OPEN_TIME)

    return df
