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
│   │   ├── env_setup.py
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
│       ├── date_utils.py
│       └── plot_utils.py

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

2. **Create a virtual environment and install dependencies:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. **Set up environment variables:**
```bash
Ensure that the .env file contains your Binance API keys:
API_KEY=your_binance_api_key
SECRET_KEY=your_binance_secret_key
```

## Usage

#### Fetching Data and Training Models

The `daily_update.py` script is responsible for both fetching the latest cryptocurrency data from Binance and training machine learning models using the fetched data. This script automates the entire workflow, from data retrieval to model training.

To execute this process, run the following command:

```bash
python -m src.scripts.daily_update
```

This single command will:

- Fetch and save the latest cryptocurrency data from Binance to CSV files.
- Train machine learning models using the newly fetched data.


#### Running Data Analysis

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