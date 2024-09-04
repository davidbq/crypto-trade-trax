from typing import Dict

from pandas import DataFrame, Series
from sklearn.base import BaseEstimator
from sklearn.model_selection import GridSearchCV

from ..config.logging import info
from .evaluate import evaluate_model
from .storage import save_model_tuning_results, save_model

def train_model(model: BaseEstimator, param_grid: dict, X: DataFrame, y: Series) -> Dict:
    grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=5, scoring='neg_mean_absolute_error')
    grid_search.fit(X, y)
    opt_model = grid_search.best_estimator_

    eval_results = evaluate_model(opt_model, X, y)

    return {
        'trained_model': opt_model,
        'best_params': grid_search.best_params_,
        'eval_results': eval_results
    }

def train_and_save_model(model: BaseEstimator, param_grid: dict, X: DataFrame, y: Series, model_path: str):
    train_results = train_model(model, param_grid, X, y)
    trained_model, best_params = train_results['trained_model'], train_results['best_params']
    mae_cv = train_results['eval_results']['mae_cv']

    info(f'MAE (CV): {mae_cv:.4f}')

    model_type = type(trained_model).__name__
    save_model_tuning_results(model_type, best_params, mae_cv)
    save_model(trained_model, model_path)
    info(f'Model saved to {model_path}')
