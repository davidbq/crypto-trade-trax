import pandas as pd
from constants import DATAFRAME_UNUSED_COLUMNS, DATAFRAME_COLUMN_NAMES

COLUMNS_TO_REMOVE = DATAFRAME_UNUSED_COLUMNS
# Column names
OPEN_PRICE = DATAFRAME_COLUMN_NAMES['OPEN_PRICE']
HIGH_PRICE = DATAFRAME_COLUMN_NAMES['HIGH_PRICE']
LOW_PRICE = DATAFRAME_COLUMN_NAMES['LOW_PRICE']
CLOSE_PRICE = DATAFRAME_COLUMN_NAMES['CLOSE_PRICE']
VOLUME = DATAFRAME_COLUMN_NAMES['VOLUME']
OPEN_TIME = DATAFRAME_COLUMN_NAMES['OPEN_TIME']
CLOSE_TIME = DATAFRAME_COLUMN_NAMES['CLOSE_TIME']
MS_UNIT = 'ms'

def _drop_unused_columns(file_path: str) -> pd.DataFrame:
    df = pd.read_csv(file_path)
    df.drop(columns=COLUMNS_TO_REMOVE, inplace=True)
    return df

def _standardize_data(file_path: str) -> pd.DataFrame:
    df = _drop_unused_columns(file_path)
    for col in [OPEN_PRICE, HIGH_PRICE, LOW_PRICE, CLOSE_PRICE, VOLUME]:
        df[col] = df[col].astype(float)

    df[OPEN_TIME] = pd.to_datetime(df[OPEN_TIME], unit=MS_UNIT)
    df[CLOSE_TIME] = pd.to_datetime(df[CLOSE_TIME], unit=MS_UNIT)

    df.set_index(OPEN_TIME, inplace=True)

    return df

def get_filtered_data(file_path: str) -> pd.DataFrame:
    return _drop_unused_columns(file_path)

def get_standarized_data(file_path: str) -> pd.DataFrame:
    return _standardize_data(file_path)