import pandas as pd
from typing import List
from ..globals.constants import CLEAN_DATA

def clean_daily_data(df: pd.DataFrame) -> pd.DataFrame:
    return df[CLEAN_DATA['DAILY_RELEVANT_COLS']]


def clean_weekly_data(df: pd.DataFrame) -> pd.DataFrame:
    return df[CLEAN_DATA['WEEKLY_RELEVANT_COLS']]
