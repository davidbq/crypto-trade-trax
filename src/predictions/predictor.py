from datetime import datetime
import traceback
from typing import Dict, Any

from ..config.logging import info
from ..globals.constants import DAILY_COL_NAMES

def generate_predictions(crypto: str, models: Dict[str, Any], prediction_input: Any) -> Dict[str, Any]:
    try:
        model_predictions = {}
        for model_name, model in models.items():
            prediction = model.predict(prediction_input)[0]
            model_predictions[model_name] = prediction

        for model_name, prediction in model_predictions.items():
            info(f'{crypto} {model_name} prediction: {prediction}')

        model_predictions.update({
            'Crypto': crypto,
            'Target': DAILY_COL_NAMES['CLOSE_PRICE'],
            'Date Target': datetime.now().strftime('%d-%m-%Y')
        })
        return model_predictions
    except Exception as e:
        info(f'An info occurred during prediction generation for {crypto}: {str(e)}')
        info(traceback.format_exc())
        return None
