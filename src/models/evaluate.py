from pandas import DataFrame, Series
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import cross_val_score

def evaluate_model(model, X_train: DataFrame, y_train: Series, X_test: DataFrame, y_test: Series):
    y_predict_train = model.predict(X_train)
    y_predict_test = model.predict(X_test)

    mae_train = mean_absolute_error(y_train, y_predict_train)
    mae_test = mean_absolute_error(y_test, y_predict_test)

    return {
        'mae_train': mae_train,
        'mae_test': mae_test
    }
