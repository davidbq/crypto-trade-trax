import pandas as pd

from src.globals.constants import CSV_PATHS
from src.plotting.table import plot_dataframe

def load_predictions(predictions_path: str) -> pd.DataFrame:
    return pd.read_csv(predictions_path, index_col='Timestamp')

def display_crypto_price_predictions():
    predictions_path = CSV_PATHS['PREDICTIONS']
    df_predictions = load_predictions(predictions_path)

    plot_dataframe(df_predictions, "Crypto Price Predictions")

if __name__ == "__main__":
    display_crypto_price_predictions()
