from src.globals.constants import MODEL_PATHS
from src.predictions.accuracy import analyze_prediction_accuracy
from src.predictions.plot import plot_error_bars, plot_predictions_and_errors

def analyze_predictions_accuracy():
    cryptos_to_analyze = list(MODEL_PATHS.keys())
    results, avg_errors = analyze_prediction_accuracy(cryptos_to_analyze)
    plot_predictions_and_errors(results)
    plot_error_bars(avg_errors)

if __name__ == '__main__':
    analyze_predictions_accuracy()
