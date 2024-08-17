from sklearn.tree import DecisionTreeRegressor
from pandas import DataFrame, Series
from .base_trainer import train_and_save_model

PARAM_GRID = {
    'criterion': ['squared_error', 'absolute_error', 'friedman_mse', 'poisson' ],
    'max_depth': [None, 5, 7, 8, 9, 10, 11],
    'max_leaf_nodes': [None, 75, 125, 225, 230, 240, 245, 250],
}

def train_dt_model(X: DataFrame, y: Series, model_path: str, hp_opt: bool = True):
    model = DecisionTreeRegressor(random_state=20)
    train_and_save_model(model, PARAM_GRID, X, y, model_path, hp_opt)
