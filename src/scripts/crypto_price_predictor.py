from ..data.preparation import prepare_prediction_data
from ..models.loader import load_prediction_models
from ..predictions.predictor import generate_predictions
from ..predictions.storage import save_predictions_to_csv
from ..globals.constants import MODEL_PATHS
from logging import error
import traceback

def generate_and_save_predictions():
    for crypto in MODEL_PATHS.keys():
        try:
            models = load_prediction_models(crypto)
            prediction_input = prepare_prediction_data(crypto)
            prediction = generate_predictions(crypto, models, prediction_input)
            if prediction:
                save_predictions_to_csv(prediction)
        except Exception as e:
            error(f'Error processing {crypto}: {str(e)}')
            error(traceback.format_exc())

if __name__ == '__main__':
    generate_and_save_predictions()
