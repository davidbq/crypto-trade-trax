from pandas import DataFrame, read_csv
from typing import Dict, Any
from .dtree_trainer import train_dt_model
from .rforest_trainer import train_rf_model
from ..utils.df_modeling_preparation import prepare_daily_data_for_modeling
from ..globals.constants import MODEL_PATHS, CSV_PATHS, DAILY_COL_NAMES
from ..config.logging import info

PARAM_GRIDS = {
    'BTC': {
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
        'DTREE': {
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


def train_models_for_dataset(df: DataFrame, param_grids: Dict[str, Dict[str, Any]], model_paths: Dict[str, str]) -> None:
    df_cleaned = prepare_daily_data_for_modeling(df).dropna()
    X = df_cleaned.drop(columns=[DAILY_COL_NAMES['CLOSE_PRICE']])
    y = df_cleaned[DAILY_COL_NAMES['CLOSE_PRICE']]

    model_types = {
        'DTREE': train_dt_model,
        'RFOREST': train_rf_model
    }

    for model_type, train_function in model_types.items():
        info(f'Starting model training type {model_type}')
        train_function = train_dt_model if model_type == 'DTREE' else train_rf_model
        train_function(X, y, param_grids[model_type], model_paths[model_type])
        info(f'Completed model training type {model_type}')

def train_all_models():
    datasets = {
        'BTC': CSV_PATHS['CRYPTO']['DAILY']['BTC'],
        'FET': CSV_PATHS['CRYPTO']['DAILY']['FET'],
    }

    for key, path in datasets.items():
        df = read_csv(path)

        info(f'Starting model training for dataset: {key}')
        train_models_for_dataset(df, PARAM_GRIDS[key], MODEL_PATHS[key])
        info(f'Completed model training for dataset: {key}')

    info('All models trained successfully.')
