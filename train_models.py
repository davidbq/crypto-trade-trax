from pandas import DataFrame
from csv_data_cleaner import load_csv_data
from model_trainer import train_model
from constants import MODEL_PATHS, CSV_PATHS, DATAFRAME_COLUMN_NAMES

OPEN_PRICE = DATAFRAME_COLUMN_NAMES['OPEN_PRICE']
CLOSE_PRICE = DATAFRAME_COLUMN_NAMES['CLOSE_PRICE']

def train_models_for_dataset(df: DataFrame, model_paths: dict) -> None:
    X = df
    y_open_price = df[OPEN_PRICE]
    train_model(X, y_open_price, model_paths['OPX_DTREE_NO_HP_OPT'], False)
    train_model(X, y_open_price, model_paths['OPX_DTREE_WITH_HP_OPT'])

    y_close_price = df[CLOSE_PRICE]
    train_model(X, y_close_price, model_paths['CPX_DTREE_NO_HP_OPT'], False)
    train_model(X, y_close_price, model_paths['CPX_DTREE_WITH_HP_OPT'])

def train_all_models():
    datasets = {
        'BTC_HISTORICAL': CSV_PATHS['BTC_HISTORICAL'],
        'BTC_RECENT': CSV_PATHS['BTC_RECENT'],
        'FET_HISTORICAL': CSV_PATHS['FET_HISTORICAL'],
        'FET_RECENT': CSV_PATHS['FET_RECENT']
    }

    for key in datasets.keys():
        dataset = load_csv_data(CSV_PATHS[key], convert_dates=False)
        train_models_for_dataset(dataset, MODEL_PATHS[key])