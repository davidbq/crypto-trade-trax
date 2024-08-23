import pandas as pd
from typing import List
from ..globals.constants import BINANCE_COLS

def convert_to_dataframe(data: List) -> pd.DataFrame:
    return pd.DataFrame(data, columns=BINANCE_COLS)
