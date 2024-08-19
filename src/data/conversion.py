import pandas as pd
from typing import List

BINANCE_COLUMNS = [ 'Open time', 'Open price', 'High price', 'Low price', 'Close price', 'Volume', 'Close time', 'Quote asset volume', 'Number of trades', 'Taker buy vol', 'Taker buy quote vol', 'Ignore']

def convert_data(data: List) -> pd.DataFrame:
    return pd.DataFrame(data, columns=BINANCE_COLUMNS)
