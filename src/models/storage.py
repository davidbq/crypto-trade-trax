from traceback import format_exc
from datetime import datetime
from typing import Dict, Any, Optional

import pandas as pd
from joblib import dump
from sklearn.base import BaseEstimator

from ..config.logging import info
from ..globals.constants import CSV_PATHS

def save_model(model: BaseEstimator, model_path: str) -> None:
    try:
        dump(model, model_path)
    except Exception as e:
        info(f'Error saving model: {e}')
        info(format_exc())

def _format_params(params: Dict[str, Any]) -> Dict[str, str]:
    return {k: str(v) if v is not None else float('inf') for k, v in params.items()}

def create_tuning_result_row(model_type: str, best_params: Dict[str, Any], mae_cv: float) -> Dict[str, Any]:
    formatted_params = _format_params(best_params)
    return {
        'Timestamp': datetime.now().strftime('%d-%m-%Y %H:%M:%S'),
        'Model Type': model_type,
        'MAE CV': mae_cv,
        **formatted_params
    }

def _read_existing_csv(csv_path: str) -> Optional[pd.DataFrame]:
    if pd.io.common.file_exists(csv_path):
        return pd.read_csv(csv_path)
    return None

def _update_csv(existing_df: pd.DataFrame, new_df: pd.DataFrame, csv_path: str) -> None:
    if set(existing_df.columns) == set(new_df.columns):
        new_df.to_csv(csv_path, mode='a', header=False, index=False)
    else:
        all_columns = list(dict.fromkeys(new_df.columns.tolist() + existing_df.columns.tolist()))
        combined_df = pd.concat([existing_df.reindex(columns=all_columns), new_df.reindex(columns=all_columns)], ignore_index=True)
        combined_df.to_csv(csv_path, index=False)

def _save_dataframe(df: pd.DataFrame, csv_path: str) -> None:
    try:
        existing_df = _read_existing_csv(csv_path)
        if existing_df is None:
            df.to_csv(csv_path, index=False)
        else:
            _update_csv(existing_df, df, csv_path)
    except Exception as e:
        info(f'Error saving data: {e}')
        info(format_exc())

def save_model_tuning_results(model_type: str, best_params: Dict[str, Any], mae_cv: float) -> None:
    csv_path = CSV_PATHS['MODEL_TUNING_RESULTS']
    row_data = create_tuning_result_row(model_type, best_params, mae_cv)
    df = pd.DataFrame([row_data])
    _save_dataframe(df, csv_path)
