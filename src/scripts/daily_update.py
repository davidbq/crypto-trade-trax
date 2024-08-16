from ..data.binance_data_to_csv import process_binance_data
from ..models.train_models import train_all_models
from ..config.logging import info

def daily_update():
    process_binance_data()

    train_all_models()

if __name__ == "__main__":
    daily_update()