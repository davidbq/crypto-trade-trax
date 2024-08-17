import pandas as pd
from ..utils.plot import plot_dataframe
from ..config.logging import info
from ..globals.constants import CSV_PATHS, DATAFRAME_COLUMN_NAMES

CSV_PATH = CSV_PATHS['OPT_HP']

def read_best_params() -> pd.DataFrame:
    return pd.read_csv(CSV_PATH, index_col='Timestamp', parse_dates=True)

def display_best_params() -> None:
    MODEL_PATH = DATAFRAME_COLUMN_NAMES['MODEL_PATH']
    df = read_best_params()
    df = df.sort_values(by=[MODEL_PATH, 'MAE test'])
    if not df.empty:
        plot_dataframe(df, f'Best Parameters for {CSV_PATH}')
    else:
        info(f'No data to display for {CSV_PATH}.')

if __name__ == "__main__":
    display_best_params()
