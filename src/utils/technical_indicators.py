import pandas as pd
from pandas import DataFrame
from ..globals.constants import DAILY_COL_NAMES

HIGH_PRICE = DAILY_COL_NAMES['HIGH_PRICE']
LOW_PRICE = DAILY_COL_NAMES['LOW_PRICE']
CLOSE_PRICE = DAILY_COL_NAMES['CLOSE_PRICE']
VOLUME = DAILY_COL_NAMES['VOLUME']
RSI_14 = DAILY_COL_NAMES['RSI_14']
BBU_20 = DAILY_COL_NAMES['BBU_20']
BBL_20 = DAILY_COL_NAMES['BBL_20']
MACD_LINE = DAILY_COL_NAMES['MACD_LINE']
MACD_SIGNAL_LINE = DAILY_COL_NAMES['MACD_SIGNAL_LINE']
MACD_HISTOGRAM = DAILY_COL_NAMES['MACD_HISTOGRAM']
TR_CURRENT = DAILY_COL_NAMES['TR_CURRENT']
ATR_14 = DAILY_COL_NAMES['ATR_14']
OBV = DAILY_COL_NAMES['OBV']
MOMENTUM_10 = DAILY_COL_NAMES['MOMENTUM_10']
ROC_14 = DAILY_COL_NAMES['ROC_14']
WILLR_14 = DAILY_COL_NAMES['WILLR_14']
STOCH_K = DAILY_COL_NAMES['STOCH_K']
STOCH_D = DAILY_COL_NAMES['STOCH_D']

def calculate_sma(df: DataFrame, period: int) -> DataFrame:
    """
    SMA smooths out price data to identify trends over a specific period.
    """
    col_name = DAILY_COL_NAMES[f'SMA_{period}']
    df[col_name] = df[CLOSE_PRICE].rolling(window=period).mean()
    return df

def calculate_ema(df: DataFrame, period: int) -> DataFrame:
    """
    EMA gives more weight to recent prices, making it more responsive to new data.
    """
    col_name = DAILY_COL_NAMES[f'EMA_{period}']
    df[col_name] = df[CLOSE_PRICE].ewm(span=period, adjust=False).mean()
    return df

def calculate_rsi(df: DataFrame, period: int) -> DataFrame:
    """
    RSI measures the speed and change of price movements to identify overbought or oversold conditions.
    """
    delta = df[CLOSE_PRICE].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    df[RSI_14] = 100 - (100 / (1 + rs))
    return df

def calculate_bollinger_bands(df: DataFrame, period: int) -> DataFrame:
    """
    Bollinger Bands consist of a SMA and two standard deviations to measure market volatility.
    """
    sma = df[CLOSE_PRICE].rolling(window=period).mean()
    std = df[CLOSE_PRICE].rolling(window=period).std()
    df[BBU_20] = sma + (std * 2)
    df[BBL_20] = sma - (std * 2)
    return df

def calculate_macd(df: DataFrame) -> DataFrame:
    """
    MACD is a trend-following momentum indicator that shows the relationship between two EMAs.
    """
    ema_12 = df[CLOSE_PRICE].ewm(span=12, adjust=False).mean()
    ema_26 = df[CLOSE_PRICE].ewm(span=26, adjust=False).mean()
    df[MACD_LINE] = ema_12 - ema_26
    df[MACD_SIGNAL_LINE] = df[MACD_LINE].ewm(span=9, adjust=False).mean()
    df[MACD_HISTOGRAM] = df[MACD_LINE] - df[MACD_SIGNAL_LINE]
    return df

def calculate_atr(df: DataFrame, period: int) -> DataFrame:
    df[TR_CURRENT] = df[[HIGH_PRICE, LOW_PRICE, CLOSE_PRICE]].max(axis=1) - df[[HIGH_PRICE, LOW_PRICE, CLOSE_PRICE]].min(axis=1)
    """
    ATR measures market volatility by decomposing the entire range of an asset price.
    """
    df[ATR_14] = df[TR_CURRENT].rolling(window=period).mean()
    return df

def calculate_obv(df: DataFrame) -> DataFrame:
    """
    OBV uses volume flow to predict changes in stock price, adding volume on up days and subtracting on down days.
    """
    df[OBV] = (df[VOLUME].where(df[CLOSE_PRICE] > df[CLOSE_PRICE].shift(1), -df[VOLUME])).cumsum()
    return df

def calculate_momentum(df: DataFrame, period: int) -> DataFrame:
    """
    Momentum measures the speed or velocity of price changes to identify potential reversals.
    """
    df[MOMENTUM_10] = df[CLOSE_PRICE].diff(period)
    return df

def calculate_roc(df: DataFrame, period: int) -> DataFrame:
    """
    ROC is a momentum oscillator that measures the percentage change in price from one period to the next.
    """
    df[ROC_14] = df[CLOSE_PRICE].pct_change(periods=period) * 100
    return df

def calculate_williams_r(df: DataFrame, period: int) -> DataFrame:
    """
    Williams %R identifies overbought and oversold levels by comparing the closing price to the high-low range.
    """
    high = df[HIGH_PRICE].rolling(window=period).max()
    low = df[LOW_PRICE].rolling(window=period).min()
    df[WILLR_14] = ((high - df[CLOSE_PRICE]) / (high - low)) * -100
    return df

def calculate_stochastic_oscillator(df: DataFrame, k_period: int, d_period: int) -> DataFrame:
    """
    The Stochastic Oscillator compares the current close price to the range of prices over a specific period to identify momentum.
    """
    low_min = df[LOW_PRICE].rolling(window=k_period).min()
    high_max = df[HIGH_PRICE].rolling(window=k_period).max()
    df[STOCH_K] = ((df[CLOSE_PRICE] - low_min) / (high_max - low_min)) * 100
    df[STOCH_D] = df[STOCH_K].rolling(window=d_period).mean()
    return df

def add_technical_indicators(df: DataFrame) -> DataFrame:
    df = calculate_sma(df, 3)
    df = calculate_sma(df, 7)
    df = calculate_sma(df, 20)
    df = calculate_sma(df, 50)
    df = calculate_sma(df, 200)

    df = calculate_ema(df, 3)
    df = calculate_ema(df, 7)
    df = calculate_ema(df, 20)
    df = calculate_ema(df, 50)
    df = calculate_ema(df, 200)

    df = calculate_rsi(df, 14)
    df = calculate_bollinger_bands(df, 20)
    df = calculate_macd(df)
    df = calculate_atr(df, 14)
    df = calculate_obv(df)
    df = calculate_momentum(df, 10)
    df = calculate_roc(df, 14)
    df = calculate_williams_r(df, 14)
    df = calculate_stochastic_oscillator(df, 14, 3)

    return df
