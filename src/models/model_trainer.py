from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import GridSearchCV, train_test_split
import pandas as pd
from sklearn.metrics import mean_absolute_error
from joblib import dump
from sklearn.base import BaseEstimator
from ..config.logging import info

PARAM_GRID = {
    'criterion': ['squared_error', 'absolute_error', 'friedman_mse', 'entropy' ],
    'max_depth': [None, 5, 10, 20],
    'min_samples_split': [2, 3, 4, 5],
    'min_samples_leaf': [1, 2, 3],
    'max_features': [None, 'auto', '0.5', '0.75'],
    'max_leaf_nodes': [None, 50, 75, 100, 150],
}

def evaluate_model(model, X_train: pd.DataFrame, y_train: pd.Series, X_test: pd.DataFrame, y_test: pd.Series):
    y_predict_train = model.predict(X_train)
    y_predict_test = model.predict(X_test)

    mae_train = mean_absolute_error(y_train, y_predict_train)
    mae_test = mean_absolute_error(y_test, y_predict_test)

    info(f'MAE (train): {mae_train}')
    info(f'MAE (test): {mae_test}')

def train_model_with_hp_opt(X: pd.DataFrame, y: pd.Series) -> DecisionTreeRegressor:
    info("Starting model training with hyperparameter optimization.")
    model = DecisionTreeRegressor(random_state=20)
    grid_search = GridSearchCV(estimator=model, param_grid=PARAM_GRID, cv=5, scoring='neg_mean_absolute_error')
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=20)

    grid_search.fit(X_train, y_train)

    opt_model = grid_search.best_estimator_
    info(f"Best parameters found: {grid_search.best_params_}")

    evaluate_model(opt_model, X_train, y_train, X_test, y_test)

    info("Model training with hyperparameter optimization completed.")
    return opt_model

def train_model_with_default_hp(X: pd.DataFrame, y: pd.Series) -> DecisionTreeRegressor:
    info("Starting model training with default hyperparameters.")
    model = DecisionTreeRegressor(random_state = 10)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)
    model.fit(X_train, y_train)

    evaluate_model(model, X_train, y_train, X_test, y_test)

    info("Model training with default hyperparameters completed.")
    return model

def save_model(model: BaseEstimator, model_path: str) -> None:
    dump(model, model_path)
    info(f"Model saved to {model_path}")

def train_model(X: pd.DataFrame, y: pd.Series, model_path: str, hp_opt: bool = True):
    info("Starting model training process.")
    model = train_model_with_hp_opt(X, y) if hp_opt else train_model_with_default_hp(X, y)
    save_model(model, model_path)
    info("Model training process completed.")