from sklearn.tree import DecisionTreeRegressor
from pandas import DataFrame, Series
from .base_trainer import train_and_save_model

def train_dt_model(X: DataFrame, y: Series, param_grid: dict, model_path: str):
    model = DecisionTreeRegressor(random_state=20)
    train_and_save_model(model, param_grid, X, y, model_path)
