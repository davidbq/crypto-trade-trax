from pandas import DataFrame, Series
from sklearn.ensemble import RandomForestRegressor

from .base_trainer import train_and_save_model

def train_rf_model(X: DataFrame, y: Series, param_grid: dict, model_path: str):
    model = RandomForestRegressor(random_state=20)
    train_and_save_model(model, param_grid, X, y, model_path)
