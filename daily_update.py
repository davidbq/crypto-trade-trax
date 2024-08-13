from binance_data_to_csv import process_binance_data
from train_models import train_all_models
from logging_config import info

def daily_update():
    info("Starting daily data update.")
    process_binance_data()
    info("Data update completed.")

    info("Starting model training.")
    train_all_models()
    info("Model training completed.")

if __name__ == "__main__":
    daily_update()