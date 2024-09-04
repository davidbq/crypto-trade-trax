from datetime import datetime
from typing import Dict

import pandas as pd

from ..globals.constants import CSV_PATHS, MODEL_TYPES
from ..plotting.table import plot_dataframe

DATE_FORMAT = '%d-%m-%Y'
TARGET_DATE_FORMAT = '%Y-%m-%d'

def _calculate_error(predicted: float, actual: float) -> float:
    return abs(predicted - actual) / actual * 100

def _compare_predictions(df_predictions: pd.DataFrame, df_actual: pd.DataFrame, crypto: str) -> pd.DataFrame:
    results = []
    for _, pred_row in df_predictions[df_predictions['Crypto'] == crypto].iterrows():
        pred_date = datetime.strptime(pred_row['Date Target'], DATE_FORMAT).strftime(TARGET_DATE_FORMAT)
        actual_row = df_actual[df_actual['Open Time'] == pred_date]

        if not actual_row.empty:
            actual_price = actual_row['Close Price'].values[0]
            result = {'Date': pred_date, 'Actual': round(actual_price, 2)}

            for model_type in MODEL_TYPES:
                pred_price = pred_row[model_type]
                error = _calculate_error(pred_price, actual_price)
                result[model_type] = round(pred_price, 2)
                result[f'{model_type}_Error%'] = round(error, 2)

            results.append(result)

    return pd.DataFrame(results)

def _calculate_average_errors(df_results: pd.DataFrame) -> Dict[str, float]:
    return {
        model_type: df_results[f'{model_type}_Error%'].mean()
        for model_type in MODEL_TYPES
    }

def analyze_prediction_accuracy(cryptos):
    df_predictions = pd.read_csv(CSV_PATHS['PREDICTIONS'])
    results = {}
    avg_errors = {'Crypto': []}
    for model_type in MODEL_TYPES:
        avg_errors[f'{model_type}_Avg_Error%'] = []

    for crypto in cryptos:
        df_crypto = pd.read_csv(CSV_PATHS['CRYPTO']['DAILY'][crypto])
        df_results = _compare_predictions(df_predictions, df_crypto, crypto)
        results[crypto] = df_results

        plot_dataframe(df_results, f'{crypto} Prediction Accuracy')

        crypto_avg_errors = _calculate_average_errors(df_results)
        avg_errors['Crypto'].append(crypto)
        for model_type in MODEL_TYPES:
            avg_errors[f'{model_type}_Avg_Error%'].append(crypto_avg_errors[model_type])

    df_avg_errors = pd.DataFrame(avg_errors)
    plot_dataframe(df_avg_errors, 'Average Prediction Errors')

    return results, df_avg_errors
