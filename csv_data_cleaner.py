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
# Set of columns
COLUMNS_FLOAT = [OPEN_PRICE, HIGH_PRICE, LOW_PRICE, CLOSE_PRICE, VOLUME]
COLUMNS_DATE = [OPEN_TIME, CLOSE_TIME]
# Units
MS_UNIT = 'ms'

def create_df_from_csv(file_path: str) -> pd.DataFrame:
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return pd.DataFrame()

def drop_unused_columns(df: pd.DataFrame) -> pd.DataFrame:
    return df.drop(columns=COLUMNS_TO_REMOVE, inplace=True)

def standardize_data(df: pd.DataFrame) -> pd.DataFrame:
    for col in COLUMNS_FLOAT:
        df[col] = df[col].astype(float)

    for col in COLUMNS_DATE:
        df[col] = pd.to_datetime(df[col], unit=MS_UNIT)

    df.set_index(OPEN_TIME, inplace=True)

    return df

def load_csv_data(file_path: str, drop_columns: bool=True, standardize: bool = True) -> pd.DataFrame:
    df = create_df_from_csv(file_path)

    if drop_columns:
        df = drop_unused_columns(df)
    if standardize:
        df = standardize_data(df)

    return df
