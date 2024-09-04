from pandas import DataFrame, Series
from sklearn.model_selection import cross_val_score

def evaluate_model(model, X: DataFrame, y: Series):
    cv_scores = cross_val_score(model, X, y, cv=5, scoring='neg_mean_absolute_error')
    mae_cv = -cv_scores.mean()

    return { 'mae_cv': mae_cv }
