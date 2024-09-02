from datetime import datetime
from logging import error
from os import path
from traceback import format_exc
from typing import Any, Dict, List

from pandas import DataFrame, io

from ..config.logging import info
from ..globals.constants import CSV_PATHS

def save_dataframe(df: DataFrame, csv_path: str) -> None:
    try:
        df.to_csv(csv_path, mode='a', header=not io.common.file_exists(csv_path))
    except Exception as e:
        info(f'Error saving data: {e}')
        info(format_exc())

def save_predictions(predictions: List[Dict[str, Any]]):
    try:
        filename = CSV_PATHS['PREDICTIONS']
        df = DataFrame(predictions)
        df['Timestamp'] = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        df.set_index('Timestamp', inplace=True)
        save_dataframe(df, filename)
    except Exception as e:
        error(f'An error occurred while saving predictions: {str(e)}')
        error(format_exc())
