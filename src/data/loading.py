import pandas as pd
import os
from ..globals.constants import CRYPTO_DF_COLS_NAMES

def load_csv_data(file_path: str) -> pd.DataFrame:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    return pd.read_csv(file_path, index_col=CRYPTO_DF_COLS_NAMES['WEEK_NUMBER'])
