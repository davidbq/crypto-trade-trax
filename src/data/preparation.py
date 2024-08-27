from pandas import DataFrame, read_csv, concat
from ..globals.constants import CSV_PATHS, DAILY_COL_NAMES
from ..utils.df_modeling_preparation import prepare_daily_data_for_modeling
from .transformation import calculate_last_3_7_day_values

def append_duplicate_last_row(df: DataFrame) -> DataFrame:
    df = df.copy()
    last_row = df.iloc[-1:].copy()
    return concat([df, last_row], ignore_index=True)

def populate_last_day_values(df: DataFrame) -> DataFrame:
    df = append_duplicate_last_row(df)

    for col_key, col_name in DAILY_COL_NAMES.items():
        if col_key.startswith('LD_'):
            df.loc[df.index[-1], col_name] = df.loc[df.index[-2], DAILY_COL_NAMES[col_key[3:]]]

    return df

def prepare_prediction_data(crypto: str) -> DataFrame:
    df = read_csv(CSV_PATHS['CRYPTO']['DAILY'][crypto])
    df = populate_last_day_values(df)
    df_recent_rows = df.iloc[-8:]
    df_with_3_7_day_values = calculate_last_3_7_day_values(df_recent_rows)
    df_processed = prepare_daily_data_for_modeling(df_with_3_7_day_values)
    df_processed.drop(columns=[DAILY_COL_NAMES['CLOSE_PRICE']], inplace=True)
    return df_processed.iloc[-1:].copy()
