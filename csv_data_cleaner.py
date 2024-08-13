import pandas as pd
from constants import DATAFRAME_UNUSED_COLUMNS, DATAFRAME_COLUMN_NAMES
from logging_config import info

COLUMNS_TO_REMOVE = DATAFRAME_UNUSED_COLUMNS
# Column names
OPEN_PRICE = DATAFRAME_COLUMN_NAMES['OPEN_PRICE']
HIGH_PRICE = DATAFRAME_COLUMN_NAMES['HIGH_PRICE']
LOW_PRICE = DATAFRAME_COLUMN_NAMES['LOW_PRICE']
CLOSE_PRICE = DATAFRAME_COLUMN_NAMES['CLOSE_PRICE']
VOLUME = DATAFRAME_COLUMN_NAMES['VOLUME']
OPEN_TIME = DATAFRAME_COLUMN_NAMES['OPEN_TIME']
CLOSE_TIME = DATAFRAME_COLUMN_NAMES['CLOSE_TIME']
# Set of columns
COLUMNS_FLOAT = [OPEN_PRICE, HIGH_PRICE, LOW_PRICE, CLOSE_PRICE, VOLUME]
COLUMNS_DATE = [OPEN_TIME, CLOSE_TIME]
# Units
MS_UNIT = 'ms'

def create_df_from_csv(file_path: str) -> pd.DataFrame:
    try:
        info(f"Loading CSV file from {file_path}.")
        return pd.read_csv(file_path)
    except FileNotFoundError:
        info(f"Error: The file {file_path} was not found.")
        return pd.DataFrame()

def drop_unused_columns(df: pd.DataFrame) -> pd.DataFrame:
    df.drop(columns=COLUMNS_TO_REMOVE, inplace=True)
    info(f"Dropped unused columns: {COLUMNS_TO_REMOVE}.")
    return df

def standardize_data(df: pd.DataFrame, convert_dates: bool = True) -> pd.DataFrame:
    df.replace('', pd.NA, inplace=True)
    df.dropna(inplace=True)

    for col in COLUMNS_FLOAT:
        df[col] = df[col].astype(float)

    for col in COLUMNS_DATE:
        if convert_dates:
            df[col] = pd.to_datetime(df[col], unit=MS_UNIT)
        else:
            df[col] = df[col].astype(int)

    df.set_index(OPEN_TIME, inplace=True)
    info("Data standardization completed.")
    return df

def load_csv_data(file_path: str, convert_dates: bool = True) -> pd.DataFrame:
    df = create_df_from_csv(file_path)
    df = drop_unused_columns(df)
    df = standardize_data(df, convert_dates)

    return df
