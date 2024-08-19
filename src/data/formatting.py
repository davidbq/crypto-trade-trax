import pandas as pd
from ..globals.constants import CRYPTO_DF_COLS_NAMES

def standardize_data(df: pd.DataFrame) -> pd.DataFrame:
    # Column names
    OPEN_TIME = CRYPTO_DF_COLS_NAMES['OPEN_TIME']
    OPEN_PRICE = CRYPTO_DF_COLS_NAMES['OPEN_PRICE']
    CLOSE_PRICE = CRYPTO_DF_COLS_NAMES['CLOSE_PRICE']

    df = df.copy()

    df[OPEN_PRICE] = df[OPEN_PRICE].astype(float)
    df[CLOSE_PRICE] = df[CLOSE_PRICE].astype(float)

    df[OPEN_TIME] = pd.to_datetime(df[OPEN_TIME].astype(float), unit='ms')
    df.set_index(OPEN_TIME, inplace=True)

    return df

def format_data(df: pd.DataFrame) -> pd.DataFrame:
    return standardize_data(df)
