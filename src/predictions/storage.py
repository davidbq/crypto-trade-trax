from pandas import DataFrame
from typing import Dict, Any, List
from os import path
from ..globals.constants import CSV_PATHS
from ..config.logging import info
from datetime import datetime
import traceback
from logging import error

def save_predictions_to_csv(predictions: List[Dict[str, Any]]):
    try:
        now = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        filename = CSV_PATHS['PREDICTIONS']

        df = DataFrame([predictions])
        df.index = [now]
        df.index.name = 'Timestamp'

        df.to_csv(filename, mode='a', header=not path.isfile(filename))

        info(f'Predictions saved to {filename}')
    except Exception as e:
        error(f'An error occurred while saving predictions: {str(e)}')
        error(traceback.format_exc())
