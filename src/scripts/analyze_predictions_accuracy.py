from src.globals.constants import CRYPTOCURRENCIES
from src.predictions.accuracy import analyze_prediction_accuracy
from src.predictions.plot import plot_error_bars, plot_predictions_and_errors

def analyze_predictions_accuracy():
    results, avg_errors = analyze_prediction_accuracy(CRYPTOCURRENCIES)
    plot_predictions_and_errors(results)
    plot_error_bars(avg_errors)

if __name__ == '__main__':
    analyze_predictions_accuracy()
