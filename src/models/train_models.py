from pandas import DataFrame
from ..data.csv_cleaner import load_csv_data
from .dtree_trainer import train_dt_model
from .rforest_trainer import train_rf_model
from ..globals.constants import MODEL_PATHS, CSV_PATHS, DATAFRAME_COLUMN_NAMES
from ..config.logging import info

OPEN_PRICE = DATAFRAME_COLUMN_NAMES['OPEN_PRICE']
CLOSE_PRICE = DATAFRAME_COLUMN_NAMES['CLOSE_PRICE']

DTREE = 'DTREE'
RFOREST = 'RFOREST'

def build_weekly_metrics_df(df: DataFrame) -> DataFrame:
    '''
    Processes a DataFrame containing daily cryptocurrency price data to calculate weekly percentage changes,
    starting from the first complete week (Monday to Sunday) in the dataset. The resulting DataFrame provides
    a pivot table with the percentage change for each day of the week, indexed by week number.
    '''

    DAY_OF_WEEK = DATAFRAME_COLUMN_NAMES['DAY_OF_WEEK']
    WEEK_NUMBER = DATAFRAME_COLUMN_NAMES['WEEK_NUMBER']
    OPEN_PRICE = DATAFRAME_COLUMN_NAMES['OPEN_PRICE']
    CLOSE_PRICE = DATAFRAME_COLUMN_NAMES['CLOSE_PRICE']
    PERCENT_CHANGE = DATAFRAME_COLUMN_NAMES['PERCENT_CHANGE']
    DAY_OF_WEEK_NAMES = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    # Find the first Monday in the dataset
    first_monday_idx = df.index[df.index.day_name() == 'Monday'][0]

    # Filter out the data before this first Monday
    df = df[df.index >= first_monday_idx]

    df[DAY_OF_WEEK] = df.index.day_name()
    # Week number relative to the first week in the dataset
    df[WEEK_NUMBER] = (df.index - df.index.min()).days // 7 + 1
    df[PERCENT_CHANGE] = ((df[CLOSE_PRICE] - df[OPEN_PRICE]) / df[OPEN_PRICE]) * 100

    df = df.pivot_table(index=WEEK_NUMBER, columns=DAY_OF_WEEK, values=PERCENT_CHANGE)

    return df[DAY_OF_WEEK_NAMES]

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
        'BTC': CSV_PATHS['CRYPTO']['BTC'],
        'FET': CSV_PATHS['CRYPTO']['FET'],
    }

    for key in datasets.keys():
        df = load_csv_data(CSV_PATHS['CRYPTO'][key])
        df_weekly_data = build_weekly_metrics_df(df)
        info(f'Starting model training for dataset: {key} and model type {DTREE}')
        train_models_for_dataset(df_weekly_data, DTREE, MODEL_PATHS[key][DTREE])
        '''info(f'Starting model training for dataset: {key} and model type {RFOREST}')
        train_models_for_dataset(dataset, RFOREST, MODEL_PATHS[key][RFOREST])'''
        info(f'Completed model training for dataset: {key}')

    info('All models trained successfully.')
