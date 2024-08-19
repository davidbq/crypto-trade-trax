from pandas import DataFrame
from ..globals.constants import CRYPTO_DF_COLS_NAMES

def build_weekly_metrics_df(df: DataFrame) -> DataFrame:
    '''
    Processes a DataFrame containing daily cryptocurrency price data to calculate weekly percentage changes,
    starting from the first complete week (Monday to Sunday) in the dataset. The resulting DataFrame provides
    a pivot table with the percentage change for each day of the week, indexed by week number.
    '''
    DAY_OF_WEEK = CRYPTO_DF_COLS_NAMES['DAY_OF_WEEK']
    WEEK_NUMBER = CRYPTO_DF_COLS_NAMES['WEEK_NUMBER']
    OPEN_PRICE = CRYPTO_DF_COLS_NAMES['OPEN_PRICE']
    CLOSE_PRICE = CRYPTO_DF_COLS_NAMES['CLOSE_PRICE']
    PERCENT_CHANGE = CRYPTO_DF_COLS_NAMES['PERCENT_CHANGE']
    DAY_OF_WEEK_NAMES = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    df = df.copy()

    # Find the first Monday in the dataset
    first_monday_idx = df.index[df.index.day_name() == 'Monday'].min()

    # Filter out the data before this first Monday
    df = df[df.index >= first_monday_idx]

    df[DAY_OF_WEEK] = df.index.day_name()
    # Week number relative to the first week in the dataset
    df[WEEK_NUMBER] = (df.index - df.index.min()).days // 7 + 1
    df[PERCENT_CHANGE] = ((df[CLOSE_PRICE] - df[OPEN_PRICE]) / df[OPEN_PRICE]) * 100

    df = df.pivot_table(index=WEEK_NUMBER, columns=DAY_OF_WEEK, values=PERCENT_CHANGE)

    return df[DAY_OF_WEEK_NAMES]

def transform_data(df: DataFrame) -> DataFrame:
    return build_weekly_metrics_df(df)
