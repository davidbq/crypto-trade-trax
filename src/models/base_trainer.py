from sklearn.model_selection import GridSearchCV, train_test_split
from pandas import DataFrame, Series
from os import path
from sklearn.metrics import mean_absolute_error
from joblib import dump
from datetime import datetime
from sklearn.base import BaseEstimator
from typing import Dict
from ..config.logging import info
from ..globals.constants import CSV_PATHS, DATAFRAME_COLUMN_NAMES

extract_filename_from_path = lambda file_path: file_path.rsplit('/', 1)[-1].replace('.joblib', '')

def best_params_to_csv(best_params: Dict, mae_train: float, mae_test: float, model_path: str) -> None:
    OPT_HP_PATH = CSV_PATHS['OPT_HP']
    MODEL_PATH = DATAFRAME_COLUMN_NAMES['MODEL_PATH']

    df = DataFrame([best_params])
    df[MODEL_PATH] = extract_filename_from_path(model_path)
    df['MAE train'] = mae_train
    df['MAE test'] = mae_test

    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    df.index = [now]
    df.index.name = 'Timestamp'

    if not path.isfile(OPT_HP_PATH):
        df.to_csv(OPT_HP_PATH)
    else:
        df.to_csv(OPT_HP_PATH, mode='a', header=False)

def evaluate_model(model, X_train: DataFrame, y_train: Series, X_test: DataFrame, y_test: Series):
    y_predict_train = model.predict(X_train)
    y_predict_test = model.predict(X_test)

    mae_train = mean_absolute_error(y_train, y_predict_train)
    mae_test = mean_absolute_error(y_test, y_predict_test)

    info(f'MAE (train): {mae_train}')
    info(f'MAE (test): {mae_test}')

    return {
        'mae_train': mae_train,
        'mae_test': mae_test
    }

def train_model_with_hp_opt(model: BaseEstimator, param_grid: dict, X: DataFrame, y: Series) -> Dict:
    """
    Trains a model with hyperparameter optimization and returns a dictionary
    containing the optimized model, best parameters, and evaluation metrics.

    Returns:
    - A dictionary containing:
        - 'optimized_model': BaseEstimator : The model trained with the best found parameters.
        - 'best_params': Dict[str, Any] : The best parameters found during the grid search.
        - 'evaluation_metrics': Dict[str, float] : A dictionary with evaluation metrics (e.g., MAE).
    """
    grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=5, scoring='neg_mean_absolute_error')
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    grid_search.fit(X_train, y_train)

    opt_model = grid_search.best_estimator_

    eval_results = evaluate_model(opt_model, X_train, y_train, X_test, y_test)

    # Retrain the model with the best parameters on the entire dataset
    opt_model.fit(X, y)

    return {
        'trained_model': opt_model,
        'best_params': grid_search.best_params_,
        'eval_results': eval_results
    }

def train_model_with_default_hp(model: BaseEstimator, X: DataFrame, y: Series) -> BaseEstimator:
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    model.fit(X_train, y_train)

    evaluate_model(model, X_train, y_train, X_test, y_test)

    return model

def save_model(model: BaseEstimator, model_path: str) -> None:
    dump(model, model_path)

def train_and_save_model(model: BaseEstimator, param_grid: dict, X: DataFrame, y: Series, model_path: str, hp_opt: bool = True):
    if hp_opt:
        train_results = train_model_with_hp_opt(model, param_grid, X, y)
        trained_model, best_params = train_results['trained_model'], train_results['best_params']
        mae_train, mae_test = train_results['eval_results']['mae_train'], train_results['eval_results']['mae_test']
        best_params_to_csv(best_params, mae_train, mae_test, model_path)
    else:
        trained_model = train_model_with_default_hp(model, X, y)

    save_model(trained_model, model_path)
