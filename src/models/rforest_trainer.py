from sklearn.ensemble import RandomForestRegressor
from pandas import DataFrame, Series
from .base_trainer import train_and_save_model

RF_PARAM_GRID = {
    'criterion': ['squared_error', 'absolute_error', 'friedman_mse', 'poisson' ],
    'n_estimators': [100, 120, 150],
    'max_depth': [None, 10, 15],
}

def train_rf_model(X: DataFrame, y: Series, model_path: str, hp_opt: bool = True):
    model = RandomForestRegressor(random_state=20)
    train_and_save_model(model, RF_PARAM_GRID, X, y, model_path, hp_opt)
