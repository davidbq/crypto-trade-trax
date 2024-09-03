from typing import Dict

from pandas import DataFrame, Series
from sklearn.base import BaseEstimator
from sklearn.model_selection import GridSearchCV, train_test_split

from ..config.logging import info
from .evaluate import evaluate_model
from .storage import save_model_tuning_results, save_model

def train_model(model: BaseEstimator, param_grid: dict, X: DataFrame, y: Series) -> Dict:
    grid_search = GridSearchCV(estimator=model, param_grid=param_grid, scoring='neg_mean_absolute_error')
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=12)
    grid_search.fit(X_train, y_train)
    opt_model = grid_search.best_estimator_

    eval_results = evaluate_model(opt_model, X_train, y_train, X_test, y_test)

    opt_model.fit(X, y)

    return {
        'trained_model': opt_model,
        'best_params': grid_search.best_params_,
        'eval_results': eval_results
    }

def train_and_save_model(model: BaseEstimator, param_grid: dict, X: DataFrame, y: Series, model_path: str):
    train_results = train_model(model, param_grid, X, y)
    trained_model, best_params = train_results['trained_model'], train_results['best_params']
    mae_train = train_results['eval_results']['mae_train']
    mae_test = train_results['eval_results']['mae_test']

    info(f'MAE (train): {mae_train:.4f}')
    info(f'MAE (test): {mae_test:.4f}')

    model_type = type(trained_model).__name__
    save_model_tuning_results(model_type, best_params, mae_train, mae_test)
    save_model(trained_model, model_path)
    info(f'Model saved to {model_path}')
