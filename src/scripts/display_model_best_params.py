import pandas as pd
from traceback import format_exc

from ..config.logging import info
from ..globals.constants import CSV_PATHS
from ..plotting.table import plot_dataframe

def load_best_params() -> pd.DataFrame:
    df = pd.read_csv(CSV_PATHS['MODEL_TUNING_RESULTS'], keep_default_na=False)
    return df.set_index('Timestamp').sort_index()

def display_best_params() -> None:

    try:
        df = load_best_params()
        if df.empty:
            info(f'No data to display for {CSV_PATHS["MODEL_TUNING_RESULTS"]}.')
        else:
            df_sorted = df.sort_values(by=['Model Type', 'MAE (test)'], ascending=[False, True])
            plot_dataframe(df_sorted, 'Best Parameters')
    except Exception as e:
        info(f'An error occurred while displaying best parameters: {str(e)}')
        info(format_exc())

if __name__ == "__main__":
    display_best_params()
