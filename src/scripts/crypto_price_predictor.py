import traceback

from ..data.preparation import prepare_prediction_data
from ..config.logging import info
from ..globals.constants import CRYPTOCURRENCIES
from ..models.loader import load_prediction_models
from ..predictions.predictor import generate_predictions
from ..predictions.storage import save_predictions

def generate_and_save_predictions():
    all_predictions = []
    for crypto in CRYPTOCURRENCIES:
        try:
            models = load_prediction_models(crypto)
            prediction_input = prepare_prediction_data(crypto)
            prediction = generate_predictions(crypto, models, prediction_input)
            if prediction:
                all_predictions.append(prediction)
        except Exception as e:
            info(f'info processing {crypto}: {str(e)}')
            info(traceback.format_exc())

    if all_predictions:
        save_predictions(all_predictions)

if __name__ == '__main__':
    generate_and_save_predictions()
