from ..data.pipeline import execute_data_pipeline
from ..models.train_models import train_all_models

def daily_update():
    execute_data_pipeline()

    #train_all_models()

if __name__ == "__main__":
    daily_update()
