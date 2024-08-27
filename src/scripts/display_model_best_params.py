import pandas as pd
from ..plotting.table import plot_dataframe
from ..config.logging import info
from ..globals.constants import CSV_PATHS, BEST_PARAMS_DF_COL_NAMES

CSV_PATH = CSV_PATHS['OPT_HP']
MODEL_PATH = BEST_PARAMS_DF_COL_NAMES['MODEL_PATH']

def load_best_params() -> pd.DataFrame:
    return pd.read_csv(CSV_PATH, index_col='Timestamp', parse_dates=True)

def display_best_params() -> None:
    df = load_best_params()
    if df is not None and not df.empty:
        plot_dataframe(df, f'Best Parameters for {CSV_PATH}')
    else:
        info(f'No data to display for {CSV_PATH}.')

if __name__ == "__main__":
    display_best_params()
