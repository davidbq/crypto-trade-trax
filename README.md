# 📈 Crypto Trade Trax

## Overview

Crypto Trade Trax is a Python-based project designed for fetching, processing, and analyzing cryptocurrency data. The project retrieves data from the Binance API, cleans and processes this data, and trains machine learning models to predict future trends in cryptocurrency prices.

## Features

- **Data Fetching:** Automatically retrieves historical and recent cryptocurrency data from Binance.
- **Data Processing:** Cleans and standardizes the data to prepare it for analysis or model training.
- **Model Training:** Trains machine learning models to predict price movements based on historical data.
- **Daily Updates:** Automates the process of updating datasets and retraining models with the latest data.
- **Logging:** Comprehensive logging throughout the project to track the execution of scripts and processes.

## Prerequisites

- Python 3.x
- pip (Python package installer)
- A Binance API account for fetching cryptocurrency data

## Project Structure

```
my_project/

├── src/
│   ├── clients/                # Contains client code for interacting with external APIs
│   │   └── binance_client.py
│
│   ├── config/                 # Configuration files and environment setup
│   │   ├── env.py
│   │   └── logging.py
│
│   ├── data/                   # Data fetching and processing modules
│   │   ├── binance_data_to_csv.py
│   │   ├── csv_data_cleaner.py
│   │   └── fetch_binance_data.py
│
│   ├── globals/                # Global constants used across the project
│   │   └── constants.py
│
│   ├── models/                 # Machine learning model training and evaluation
│   │   ├── model_trainer.py
│   │   └── train_models.py
│
│   ├── scripts/                # Executable scripts for daily updates and analysis
│   │   ├── daily_update.py
│   │   └── run_data_analysis.py
│
│   └── utils/                  # Utility functions for date handling, plotting, etc.
│       ├── date.py
│       └── plot.py
│
├── data/                       # Directory to store the fetched and processed data
│   ├── btc_historical_data.csv
│   ├── btc_recent_data.csv
│   ├── fet_historical_data.csv
│   └── fet_recent_data.csv
│
├── models/                     # Directory to save trained machine learning models
│   ├── btc_hist_model.joblib
│   ├── btc_recent_model.joblib
│   ├── fet_hist_model.joblib
│   └── fet_recent_model.joblib
│
├── .env                        # Environment variables file

├── .gitignore                  # Git ignore file

├── README.md                   # Project README file

└── requirements.txt            # Python dependencies
```

## Installation

1. **Clone the repository:**

```bash
git clone https://github.com/yourusername/crypto-trade-trax.git
cd crypto-trade-trax
```

2.**Create a virtual environment and install dependencies:**

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3.**Set up environment variables:**

```bash
Ensure that the .env file contains your Binance API keys:
API_KEY=your_binance_api_key
SECRET_KEY=your_binance_secret_key
```

## Usage

### Fetching Data and Training Models

The `daily_update.py` script is responsible for both fetching the latest cryptocurrency data from Binance and training machine learning models using the fetched data. This script automates the entire workflow, from data retrieval to model training.

To execute this process, run the following command:

```bash
python -m src.scripts.daily_update
```

This single command will:

- Fetch and save the latest cryptocurrency data from Binance to CSV files.
- Train machine learning models using the newly fetched data.

## Data Features

This section provides detailed explanations of the features used in the data preprocessing pipeline, including daily values, technical indicators, and momentum indicators.

### Daily Dataframe Content explanation

#### 1. Daily Values

These are the fundamental data points captured on a daily basis during the trading session.

- **`OPEN_TIME`:** The time at which the trading session opened.
- **`OPEN_PRICE`:** The price at the start of the trading session.
- **`HIGH_PRICE`:** The highest price reached during the trading session.
- **`LOW_PRICE`:** The lowest price reached during the trading session.
- **`CLOSE_PRICE`:** The price at the close of the trading session.
- **`VOLUME`:** The total amount of the asset traded during the session.
- **`NUMBER_OF_TRADES`:** The total number of trades executed during the session.
- **`TAKER_BUY_BASE_ASSET_VOLUME`:** The volume of the base asset bought by takers (market buyers).

#### 2. Simple Moving Averages (SMA)

Simple Moving Averages (SMA) are calculated by averaging a set of prices over a specific number of days. They smooth out price data to identify trends over time.

- **`SMA_3`:** The simple moving average calculated over the last 3 days.
- **`SMA_7`:** The simple moving average calculated over the last 7 days.
- **`SMA_20`:** The simple moving average calculated over the last 20 days.
- **`SMA_50`:** The simple moving average calculated over the last 50 days.
- **`SMA_200`:** The simple moving average calculated over the last 200 days.

#### 3. Exponential Moving Averages (EMA)

Exponential Moving Averages (EMA) give more weight to recent prices, making them more responsive to new information compared to SMAs.

- **`EMA_3`:** The exponential moving average calculated over the last 3 days.
- **`EMA_7`:** The exponential moving average calculated over the last 7 days.
- **`EMA_20`:** The exponential moving average calculated over the last 20 days.
- **`EMA_50`:** The exponential moving average calculated over the last 50 days.
- **`EMA_200`:** The exponential moving average calculated over the last 200 days.

#### 4. Relative Strength Index (RSI)

The Relative Strength Index (RSI) is a momentum oscillator that measures the speed and change of price movements, used to identify overbought or oversold conditions.

- **`RSI_14`:** The Relative Strength Index calculated over a 14-day period. It measures the speed and change of price movements and is used to identify overbought or oversold conditions.

#### 5. Bollinger Bands (20-day)

Bollinger Bands are volatility bands placed above and below a moving average. They expand and contract based on market volatility.

- **`BBU_20`:** The upper Bollinger Band calculated using a 20-day simple moving average. It is used to identify overbought conditions.
- **`BBL_20`:** The lower Bollinger Band calculated using a 20-day simple moving average. It is used to identify oversold conditions.

#### 6. Moving Average Convergence Divergence (MACD)

The MACD is a trend-following momentum indicator that shows the relationship between two moving averages of a security’s price.

- **`MACD_LINE`:** The MACD line, calculated as the difference between a 12-day EMA and a 26-day EMA.
- **`MACD_SIGNAL_LINE`:** The signal line, which is a 9-day EMA of the MACD line.
- **`MACD_HISTOGRAM`:** The difference between the MACD line and the signal line, used to identify momentum.

#### 7. Volatility Indicators

Volatility indicators measure the degree of variation of a trading price series over time.

- **`TR_CURRENT`:** The current True Range, a measure of the range of price movement in a single day.
- **`ATR_14`:** The Average True Range calculated over 14 days, used to measure market volatility.

#### 8. Volume-Based Indicators

Volume-based indicators assess the strength of price movements by analyzing the trading volume.

- **`OBV`:** On-Balance Volume, which adds volume on up days and subtracts it on down days to measure buying and selling pressure.

#### 9. Momentum Indicators

Momentum indicators measure the speed of price movement and are used to identify the strength of a trend.

- **`MOMENTUM_10`:** The momentum indicator calculated over a 10-day period, measuring the rate of change in prices.
- **`ROC_14`:** The Rate of Change over 14 days, representing the percentage change in price over that period.

#### 10. Oscillators

Oscillators are momentum indicators that fluctuate between fixed points and are used to identify overbought or oversold conditions.

- **`WILLR_14`:** The Williams %R, a momentum indicator that measures overbought and oversold levels over a 14-day period.
- **`STOCH_K`:** The %K line of the Stochastic Oscillator, representing the current close relative to the range of prices over a set period.
- **`STOCH_D`:** The %D line of the Stochastic Oscillator, which is a moving average of %K, providing smoothed values.

### Running Data Analysis

To perform data analysis on the fetched and cleaned data:

```bash
python -m src.scripts.run_data_analysis
```

## Logging

Logging is configured via `src/config/logging.py` to provide detailed execution logs. Logs include timestamps, filenames, log levels, and messages to assist in debugging and tracking script execution.

## Contributing

Contributions are welcome! Feel free to fork the repository, make changes, and submit pull requests. Please ensure that your changes are well-documented and tested.

## License

This project is licensed under the MIT License.
