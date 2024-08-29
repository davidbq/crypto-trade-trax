from pandas import DataFrame, Series
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import cross_val_score

def evaluate_model(model, X_train: DataFrame, y_train: Series, X_test: DataFrame, y_test: Series):
    y_predict_train = model.predict(X_train)
    y_predict_test = model.predict(X_test)

    cv_score = cross_val_score(model, X_train, y_train, cv=5, scoring='neg_mean_absolute_error')
    mae_train = mean_absolute_error(y_train, y_predict_train)
    mae_test = mean_absolute_error(y_test, y_predict_test)

    return {
        'cv_score': -cv_score.mean(),
        'mae_train': mae_train,
        'mae_test': mae_test
    }
