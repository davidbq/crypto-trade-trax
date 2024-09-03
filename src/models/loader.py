from typing import Dict, Any

import joblib

from ..config.logging import info
from ..globals.constants import MODEL_PATHS, MODEL_TYPES

def load_prediction_models(crypto: str) -> Dict[str, Any]:
    models = {}
    for model_type in MODEL_TYPES:
        try:
            models[model_type] = joblib.load(MODEL_PATHS[crypto][model_type])
        except KeyError:
            info(f'Warning: {model_type} model not found for {crypto}')
    return models
