from pandas import DataFrame, Series
from xgboost import XGBRegressor

from .base_trainer import train_and_save_model

def train_xgb_model(X: DataFrame, y: Series, param_grid: dict, model_path: str):
    model = XGBRegressor(random_state=20)
    train_and_save_model(model, param_grid, X, y, model_path)
