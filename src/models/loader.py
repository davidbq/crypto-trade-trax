import joblib
from typing import Dict, Any
from ..globals.constants import MODEL_PATHS

def load_prediction_models(crypto: str) -> Dict[str, Any]:
    return {
        'DTREE': joblib.load(MODEL_PATHS[crypto]['DTREE']),
        'RFOREST': joblib.load(MODEL_PATHS[crypto]['RFOREST'])
    }
