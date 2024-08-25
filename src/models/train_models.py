from pandas import DataFrame, read_csv
from .dtree_trainer import train_dt_model
from .rforest_trainer import train_rf_model
from ..utils.df_modeling_preparation import prepare_daily_data_for_modeling
from ..globals.constants import MODEL_PATHS, CSV_PATHS, DAILY_COL_NAMES
from ..config.logging import info

PARAM_GRIDS = {
    'BTC':{
        'DTREE': {
            'criterion': ['absolute_error'],
            'max_depth': [None],
            'max_leaf_nodes': [50]
        },
        'RFOREST': {
            'criterion': ['absolute_error'],
            'n_estimators': [280],
            'max_depth': [7],
        }
    },
    'FET': {
        'DTREE':{
            'criterion': ['friedman_mse'],
            'max_depth': [None],
            'max_leaf_nodes': [85]
        },
        'RFOREST': {
                'criterion': ['absolute_error'],
                'n_estimators': [150],
                'max_depth': [12],
        }
    }
}


def train_models_for_dataset(df: DataFrame, param_grids: dict, model_paths: dict) -> None:
    df_cleand = prepare_daily_data_for_modeling(df)
    df_cleaned = df_cleand.dropna()
    X = df_cleaned.drop(columns=[DAILY_COL_NAMES['CLOSE_PRICE']])
    y = df_cleaned[DAILY_COL_NAMES['CLOSE_PRICE']]

    info('Starting model training type DTREE')
    train_dt_model(X, y, param_grids['DTREE'], model_paths['DTREE'])
    info('Completed model training type DTREE')

    info('Starting model training type RFOREST')
    train_rf_model(X, y, param_grids['RFOREST'], model_paths['RFOREST'])
    info('Completed model training type RFOREST')

def train_all_models():
    datasets = {
        'BTC': CSV_PATHS['CRYPTO']['DAILY']['BTC'],
        'FET': CSV_PATHS['CRYPTO']['DAILY']['FET'],
    }

    for key in datasets.keys():
        df = read_csv(CSV_PATHS['CRYPTO']['DAILY'][key])

        info(f'Starting model training for dataset: {key}')
        train_models_for_dataset(df, PARAM_GRIDS[key], MODEL_PATHS[key])
        info(f'Completed model training for dataset: {key}')

    info('All models trained successfully.')
