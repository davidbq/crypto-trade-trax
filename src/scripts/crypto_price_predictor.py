import traceback
from logging import error

from ..data.preparation import prepare_prediction_data
from ..globals.constants import MODEL_PATHS
from ..models.loader import load_prediction_models
from ..predictions.predictor import generate_predictions
from ..predictions.storage import save_predictions

def generate_and_save_predictions():
    all_predictions = []
    for crypto in MODEL_PATHS.keys():
        try:
            models = load_prediction_models(crypto)
            prediction_input = prepare_prediction_data(crypto)
            prediction = generate_predictions(crypto, models, prediction_input)
            if prediction:
                all_predictions.append(prediction)
        except Exception as e:
            error(f'Error processing {crypto}: {str(e)}')
            error(traceback.format_exc())

        if all_predictions:
            save_predictions(all_predictions)

if __name__ == '__main__':
    generate_and_save_predictions()
