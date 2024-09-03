import asyncio
from typing import Dict, Any

from pandas import DataFrame, read_csv

from ..config.logging import info
from ..globals.constants import MODEL_PATHS, CSV_PATHS, DAILY_COL_NAMES
from ..utils.df_modeling_preparation import prepare_daily_data_for_modeling
from .dtree_trainer import train_dt_model
from .rforest_trainer import train_rf_model

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
            'n_jobs': [-1]
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
            'n_jobs': [-1]
        }
    }
}

async def train_model(train_function, X, y, params, model_path, dataset_key, model_type):
    info(f'Starting {model_type} model training for {dataset_key}')
    await asyncio.to_thread(train_function, X, y, params, model_path)
    info(f'Finished {model_type} model training for {dataset_key}')

async def train_models_for_dataset(df: DataFrame, param_grids: Dict[str, Dict[str, Any]], model_paths: Dict[str, str], dataset_key: str) -> None:
    info(f'Preparing data for {dataset_key}')
    df_cleaned = prepare_daily_data_for_modeling(df).dropna()
    X = df_cleaned.drop(columns=[DAILY_COL_NAMES['CLOSE_PRICE']])
    y = df_cleaned[DAILY_COL_NAMES['CLOSE_PRICE']]

    model_types = {
        'DTREE': train_dt_model,
        'RFOREST': train_rf_model
    }

    await asyncio.gather(*[
        train_model(train_function, X, y, param_grids[model_type], model_paths[model_type], dataset_key, model_type)
        for model_type, train_function in model_types.items()
    ])

async def train_all_models():
    datasets = {
        'BTC': CSV_PATHS['CRYPTO']['DAILY']['BTC'],
        'FET': CSV_PATHS['CRYPTO']['DAILY']['FET'],
    }

    await asyncio.gather(*[
        train_models_for_dataset(read_csv(path), PARAM_GRIDS[key], MODEL_PATHS[key], key)
        for key, path in datasets.items()
    ])

    info('All models for all datasets trained successfully.')
