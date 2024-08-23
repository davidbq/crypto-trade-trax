from pandas import DataFrame
from ..utils.technical_indicators import add_technical_indicators
from ..globals.constants import WEEKLY_COL_NAMES, DAILY_COL_NAMES

def build_weekly_metrics_df(df: DataFrame) -> DataFrame:
    '''
    Processes a DataFrame containing daily cryptocurrency price data to calculate weekly percentage changes,
    starting from the first complete week (Monday to Sunday) in the dataset. The resulting DataFrame provides
    a pivot table with the percentage change for each day of the week, indexed by week number.
    '''
    DAY_OF_WEEK = WEEKLY_COL_NAMES['DAY_OF_WEEK']
    WEEK_NUMBER = WEEKLY_COL_NAMES['WEEK_NUMBER']
    OPEN_PRICE = WEEKLY_COL_NAMES['OPEN_PRICE']
    CLOSE_PRICE = WEEKLY_COL_NAMES['CLOSE_PRICE']
    PERCENT_CHANGE = WEEKLY_COL_NAMES['PERCENT_CHANGE']
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

def calculate_last_day_values(df: DataFrame) -> DataFrame:
    df[DAILY_COL_NAMES['LD_OPEN_PRICE']] = df[DAILY_COL_NAMES['OPEN_PRICE']].shift(1)
    df[DAILY_COL_NAMES['LD_HIGH_PRICE']] = df[DAILY_COL_NAMES['HIGH_PRICE']].shift(1)
    df[DAILY_COL_NAMES['LD_LOW_PRICE']] = df[DAILY_COL_NAMES['LOW_PRICE']].shift(1)
    df[DAILY_COL_NAMES['LD_CLOSE_PRICE']] = df[DAILY_COL_NAMES['CLOSE_PRICE']].shift(1)
    df[DAILY_COL_NAMES['LD_VOLUME']] = df[DAILY_COL_NAMES['VOLUME']].shift(1)
    df[DAILY_COL_NAMES['LD_NUMBER_OF_TRADES']] = df[DAILY_COL_NAMES['NUMBER_OF_TRADES']].shift(1)
    df[DAILY_COL_NAMES['LD_TAKER_BUY_VOLUME']] = df[DAILY_COL_NAMES['TAKER_BUY_BASE_ASSET_VOLUME']].shift(1)
    df[DAILY_COL_NAMES['LD_PERCENTAGE_CHANGE']] = df[DAILY_COL_NAMES['PERCENT_CHANGE']].shift(1)

    # RSI, Bollinger Bands, MACD, ATR, OBV, Momentum, ROC, Williams %R, Stochastic Oscillator
    df[DAILY_COL_NAMES['LD_RSI_14']] = df[DAILY_COL_NAMES['RSI_14']].shift(1)
    df[DAILY_COL_NAMES['LD_BBU_20']] = df[DAILY_COL_NAMES['BBU_20']].shift(1)
    df[DAILY_COL_NAMES['LD_BBL_20']] = df[DAILY_COL_NAMES['BBL_20']].shift(1)
    df[DAILY_COL_NAMES['LD_MACD_LINE']] = df[DAILY_COL_NAMES['MACD_LINE']].shift(1)
    df[DAILY_COL_NAMES['LD_MACD_SIGNAL_LINE']] = df[DAILY_COL_NAMES['MACD_SIGNAL_LINE']].shift(1)
    df[DAILY_COL_NAMES['LD_MACD_HISTOGRAM']] = df[DAILY_COL_NAMES['MACD_HISTOGRAM']].shift(1)
    df[DAILY_COL_NAMES['LD_TR_CURRENT']] = df[DAILY_COL_NAMES['TR_CURRENT']].shift(1)
    df[DAILY_COL_NAMES['LD_ATR_14']] = df[DAILY_COL_NAMES['ATR_14']].shift(1)
    df[DAILY_COL_NAMES['LD_OBV']] = df[DAILY_COL_NAMES['OBV']].shift(1)
    df[DAILY_COL_NAMES['LD_MOMENTUM_10']] = df[DAILY_COL_NAMES['MOMENTUM_10']].shift(1)
    df[DAILY_COL_NAMES['LD_ROC_14']] = df[DAILY_COL_NAMES['ROC_14']].shift(1)
    df[DAILY_COL_NAMES['LD_WILLR_14']] = df[DAILY_COL_NAMES['WILLR_14']].shift(1)
    df[DAILY_COL_NAMES['LD_STOCH_K']] = df[DAILY_COL_NAMES['STOCH_K']].shift(1)
    df[DAILY_COL_NAMES['LD_STOCH_D']] = df[DAILY_COL_NAMES['STOCH_D']].shift(1)

    # SMA and EMA
    for period in [3, 7, 20, 50, 200]:
        df[DAILY_COL_NAMES[f'LD_SMA_{period}']] = df[DAILY_COL_NAMES[f'SMA_{period}']].shift(1)
        df[DAILY_COL_NAMES[f'LD_EMA_{period}']] = df[DAILY_COL_NAMES[f'EMA_{period}']].shift(1)

    return df

def calculate_last_3_7_day_values(df: DataFrame) -> DataFrame:
    df[DAILY_COL_NAMES['L3D_TOTAL_TRADES']] = df[DAILY_COL_NAMES['NUMBER_OF_TRADES']].rolling(window=3).sum().shift(1)
    df[DAILY_COL_NAMES['L3D_AVG_TAKER_BUY_VOLUME']] = df[DAILY_COL_NAMES['TAKER_BUY_BASE_ASSET_VOLUME']].rolling(window=3).mean().shift(1)

    df[DAILY_COL_NAMES['L7D_TOTAL_TRADES']] = df[DAILY_COL_NAMES['NUMBER_OF_TRADES']].rolling(window=7).sum().shift(1)
    df[DAILY_COL_NAMES['L7D_AVG_TAKER_BUY_VOLUME']] = df[DAILY_COL_NAMES['TAKER_BUY_BASE_ASSET_VOLUME']].rolling(window=7).mean().shift(1)
    return df

def build_daily_metrics(df: DataFrame) -> DataFrame:
    df = add_technical_indicators(df)
    df[DAILY_COL_NAMES['PERCENT_CHANGE']] = ((df[DAILY_COL_NAMES['CLOSE_PRICE']] - df[DAILY_COL_NAMES['OPEN_PRICE']]) / df[DAILY_COL_NAMES['OPEN_PRICE']]) * 100
    df = calculate_last_day_values(df)
    df = calculate_last_3_7_day_values(df)
    return df
