from pandas import DataFrame
from ..data.csv_data_cleaner import load_csv_data
from .dtree_trainer import train_dt_model
from .rforest_trainer import train_rf_model
from ..globals.constants import MODEL_PATHS, CSV_PATHS, DATAFRAME_COLUMN_NAMES
from ..config.logging import info

OPEN_PRICE = DATAFRAME_COLUMN_NAMES['OPEN_PRICE']
CLOSE_PRICE = DATAFRAME_COLUMN_NAMES['CLOSE_PRICE']

DTREE = 'DTREE'
RFOREST = 'RFOREST'

def train_models_for_dataset(df: DataFrame, model_type: str, model_paths: dict) -> None:
    model_trainer = train_dt_model if model_type == DTREE else train_rf_model

    X = df.drop(columns=[OPEN_PRICE, CLOSE_PRICE])

    info(f'Prediction target {OPEN_PRICE}')
    y_open_price = df[OPEN_PRICE]
    model_trainer(X, y_open_price, model_paths[f'OPX_{model_type}_NO_HP_OPT'], False)
    model_trainer(X, y_open_price, model_paths[f'OPX_{model_type}_WITH_HP_OPT'])

    info(f'Prediction target {CLOSE_PRICE}')
    y_close_price = df[CLOSE_PRICE]
    model_trainer(X, y_close_price, model_paths[f'CPX_{model_type}_NO_HP_OPT'], False)
    model_trainer(X, y_close_price, model_paths[f'CPX_{model_type}_WITH_HP_OPT'])

def train_all_models():
    datasets = {
        'BTC_HISTORICAL': CSV_PATHS['CRYPTO']['BTC_HISTORICAL'],
        'BTC_RECENT': CSV_PATHS['CRYPTO']['BTC_RECENT'],
        'FET_HISTORICAL': CSV_PATHS['CRYPTO']['FET_HISTORICAL'],
        'FET_RECENT': CSV_PATHS['CRYPTO']['FET_RECENT']
    }

    for key in datasets.keys():
        df = load_csv_data(CSV_PATHS['CRYPTO'][key], convert_dates=False)
        info(f'Starting model training for dataset: {key} and model type {DTREE}')
        train_models_for_dataset(df, DTREE, MODEL_PATHS[key][DTREE])
        '''info(f'Starting model training for dataset: {key} and model type {RFOREST}')
        train_models_for_dataset(dataset, RFOREST, MODEL_PATHS[key][RFOREST])'''
        info(f'Completed model training for dataset: {key}')

    info('All models trained successfully.')
