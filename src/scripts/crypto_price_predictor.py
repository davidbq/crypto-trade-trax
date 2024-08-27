import joblib
from pandas import DataFrame, read_csv, concat
from logging import error
from os import path
from typing import Dict, Any, List
from ..utils.df_modeling_preparation import prepare_daily_data_for_modeling
from ..data.transformation import calculate_last_3_7_day_values
from ..globals.constants import MODEL_PATHS, CSV_PATHS, DAILY_COL_NAMES
from ..config.logging import info
from datetime import datetime
import traceback

def append_duplicate_last_row(df: DataFrame) -> DataFrame:
    df = df.copy()
    last_row = df.iloc[-1:].copy()
    return concat([df, last_row], ignore_index=True)

def populate_last_day_values(df: DataFrame) -> DataFrame:
    df = append_duplicate_last_row(df)

    for col_key, col_name in DAILY_COL_NAMES.items():
        if col_key.startswith('LD_'):
            df.loc[df.index[-1], col_name] = df.loc[df.index[-2], DAILY_COL_NAMES[col_key[3:]]]

    return df

def load_prediction_models(crypto: str) -> Dict[str, Any]:
    return {
        'DTREE': joblib.load(MODEL_PATHS[crypto]['DTREE']),
        'RFOREST': joblib.load(MODEL_PATHS[crypto]['RFOREST'])
    }

def prepare_prediction_data(crypto: str) -> DataFrame:
    df = read_csv(CSV_PATHS['CRYPTO']['DAILY'][crypto])
    df = populate_last_day_values(df)
    df_recent_rows = df.iloc[-8:]
    df_with_3_7_day_values = calculate_last_3_7_day_values(df_recent_rows)
    df_processed = prepare_daily_data_for_modeling(df_with_3_7_day_values)
    df_processed.drop(columns=[DAILY_COL_NAMES['CLOSE_PRICE']], inplace=True)
    return df_processed.iloc[-1:].copy()

def generate_predictions(crypto: str) -> Dict[str, Any]:
    try:
        models = load_prediction_models(crypto)
        prediction_input = prepare_prediction_data(crypto)

        model_predictions = {model_name: model.predict(prediction_input)[0] for model_name, model in models.items()}

        for model_name, prediction in model_predictions.items():
            info(f'{crypto} {model_name} prediction: {prediction}')

        model_predictions.update({
            'Crypto': crypto,
            'Target': DAILY_COL_NAMES['CLOSE_PRICE'],
            'Date Target': datetime.now().strftime('%d-%m-%Y')
        })
        return model_predictions
    except Exception as e:
        error(f'An error occurred during prediction generation for {crypto}: {str(e)}')
        error(traceback.format_exc())
        return None

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

def generate_and_save_predictions():
    for crypto in MODEL_PATHS.keys():
        prediction = generate_predictions(crypto)
        if prediction:
            save_predictions_to_csv(prediction)

if __name__ == '__main__':
    generate_and_save_predictions()
