import pandas as pd
from typing import List
from ..globals.constants import FETCH_DATA

RELEVANT_BINANCE_COLS = FETCH_DATA['RELEVANT_BINANCE_COLS']

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    return df[RELEVANT_BINANCE_COLS]
