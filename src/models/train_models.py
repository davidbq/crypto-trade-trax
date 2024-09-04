import asyncio
from typing import Dict, Any

from pandas import DataFrame, read_csv

from ..config.logging import info
from ..globals.constants import MODEL_PATHS, CSV_PATHS, DAILY_COL_NAMES
from ..utils.df_modeling_preparation import prepare_daily_data_for_modeling
from .dtree_trainer import train_dt_model
from .rforest_trainer import train_rf_model
from .xgboost_trainer import train_xgb_model

PARAM_GRIDS = {
    'BTC': {
        'DTREE': {
            'max_depth': [None],
            'min_samples_split' :[50],
            'max_leaf_nodes': [90]
        },
        'RFOREST': {
            'n_estimators': [278],
            'max_features': [0.5],
            'max_depth': [6],
            'n_jobs': [-1]
        },
        'XGBOOST': {
            'n_estimators': [53],
            'max_depth': [3],
            'learning_rate': [0.1],
            'n_jobs': [-1]
        }
    },
    'FET': {
        'DTREE': {
            'max_depth': [None],
            'min_samples_split' :[50],
            'max_leaf_nodes': [75]
        },
        'RFOREST': {
            'n_estimators': [155],
            'max_features': [0.8],
            'max_depth': [15],
            'n_jobs': [-1]
        },
        'XGBOOST': {
            'n_estimators': [290],
            'max_depth': [2],
            'learning_rate': [0.08],
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
        'RFOREST': train_rf_model,
        'XGBOOST': train_xgb_model
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
