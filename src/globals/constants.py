from os import path

BASE_PATH = path.dirname(path.dirname(path.dirname(__file__)))

FETCH_DATA = {
    'HISTORICAL_START_DATE': '2000-01-01',
    'INTERVAL': '1d',
}

SYMBOLS = {
    'BTC_USDT': 'BTCUSDT',
    'FET_USDT': 'FETUSDT'
}

BINANCE_COL_NAMES = {
    'OPEN_TIME': 'Open Time',
    'OPEN_PRICE': 'Open Price',
    'HIGH_PRICE': 'High Price',
    'LOW_PRICE': 'Low Price',
    'CLOSE_PRICE': 'Close Price',
    'VOLUME': 'Volume',
    'CLOSE_TIME': 'Close Time',
    'QUOTE_ASSET_VOLUME': 'Quote Asset Volume',
    'NUMBER_OF_TRADES': 'Number of Trades',
    'TAKER_BUY_BASE_VOLUME': 'Taker Buy Base Volume',
    'TAKER_BUY_QUOTE_VOLUME': 'Taker Buy Quote Volume',
    'IGNORE': 'Ignore'
}

BINANCE_COLS = [
    BINANCE_COL_NAMES['OPEN_TIME'], BINANCE_COL_NAMES['OPEN_PRICE'], BINANCE_COL_NAMES['HIGH_PRICE'], BINANCE_COL_NAMES['LOW_PRICE'],
    BINANCE_COL_NAMES['CLOSE_PRICE'], BINANCE_COL_NAMES['VOLUME'], BINANCE_COL_NAMES['CLOSE_TIME'],
    BINANCE_COL_NAMES['QUOTE_ASSET_VOLUME'], BINANCE_COL_NAMES['NUMBER_OF_TRADES'],
    BINANCE_COL_NAMES['TAKER_BUY_BASE_VOLUME'], BINANCE_COL_NAMES['TAKER_BUY_QUOTE_VOLUME'], 'IGNORE'
]

CLEAN_DATA = {
  'WEEKLY_RELEVANT_COLS': [
        BINANCE_COL_NAMES['OPEN_TIME'],
        BINANCE_COL_NAMES['OPEN_PRICE'],
        BINANCE_COL_NAMES['CLOSE_PRICE'],
    ],
    'DAILY_RELEVANT_COLS': [
        BINANCE_COL_NAMES['OPEN_TIME'],
        BINANCE_COL_NAMES['OPEN_PRICE'],
        BINANCE_COL_NAMES['HIGH_PRICE'],
        BINANCE_COL_NAMES['LOW_PRICE'],
        BINANCE_COL_NAMES['CLOSE_PRICE'],
        BINANCE_COL_NAMES['VOLUME'],
        BINANCE_COL_NAMES['NUMBER_OF_TRADES'],
        BINANCE_COL_NAMES['TAKER_BUY_BASE_VOLUME']
    ]
}

WEEKLY_COL_NAMES = {
    'OPEN_TIME': BINANCE_COL_NAMES['OPEN_TIME'],
    'DAY_OF_WEEK': 'Day of Week',
    'WEEK_NUMBER': 'Week Number',
    'OPEN_PRICE': BINANCE_COL_NAMES['OPEN_PRICE'],
    'CLOSE_PRICE': BINANCE_COL_NAMES['CLOSE_PRICE'],
    'PERCENT_CHANGE': 'Percent Change',
}

DAILY_COL_NAMES = {
    # =========================
    # 1. Daily Values
    # =========================
    'OPEN_TIME': BINANCE_COL_NAMES['OPEN_TIME'],
    'OPEN_PRICE': BINANCE_COL_NAMES['OPEN_PRICE'],
    'HIGH_PRICE': BINANCE_COL_NAMES['HIGH_PRICE'],
    'LOW_PRICE': BINANCE_COL_NAMES['LOW_PRICE'],
    'CLOSE_PRICE': BINANCE_COL_NAMES['CLOSE_PRICE'],
    'VOLUME': BINANCE_COL_NAMES['VOLUME'],
    'NUMBER_OF_TRADES': BINANCE_COL_NAMES['NUMBER_OF_TRADES'],
    'TAKER_BUY_BASE_VOLUME': BINANCE_COL_NAMES['TAKER_BUY_BASE_VOLUME'],
    'PERCENT_CHANGE': 'Percent Change',

    # =========================
    # 2. Last Day Values
    # =========================
    'LD_OPEN_PRICE': 'Last Day Open Price',
    'LD_HIGH_PRICE': 'Last Day High Price',
    'LD_LOW_PRICE': 'Last Day Low Price',
    'LD_CLOSE_PRICE': 'Last Day Close Price',
    'LD_VOLUME': 'Last Day Volume',
    'LD_NUMBER_OF_TRADES': 'Last Day Number of Trades',
    'LD_TAKER_BUY_BASE_VOLUME': 'Last Day Taker Buy Base Volume',
    'LD_PERCENT_CHANGE': 'Last Day Percent Change',

    # =========================
    # 3. Last 3 Days Values
    # =========================
    'L3D_TOTAL_TRADES': 'Last 3 Days Total Trades',
    'L3D_AVG_TAKER_BUY_BASE_VOLUME': 'Last 3 Days Avg Taker Buy Base Volume',

    # =========================
    # 4. Last 7 Days Values
    # =========================
    'L7D_TOTAL_TRADES': 'Last 7 Days Total Trades',
    'L7D_AVG_TAKER_BUY_BASE_VOLUME': 'Last 7 Days Avg Taker Buy Base Volume',

    # =========================
    # 5. Simple Moving Averages (SMA)
    # =========================
    'SMA_3': 'SMA 3',
    'SMA_7': 'SMA 7',
    'SMA_20': 'SMA 20',

    # Last Day SMAs
    'LD_SMA_3': 'Last Day SMA 3',
    'LD_SMA_7': 'Last Day SMA 7',
    'LD_SMA_20': 'Last Day SMA 20',

    # =========================
    # 6. Exponential Moving Averages (EMA)
    # =========================
    'EMA_3': 'EMA 3',
    'EMA_7': 'EMA 7',
    'EMA_20': 'EMA 20',

    # Last Day EMAs
    'LD_EMA_3': 'Last Day EMA 3',
    'LD_EMA_7': 'Last Day EMA 7',
    'LD_EMA_20': 'Last Day EMA 20',

    # =========================
    # 7. Relative Strength Index (RSI)
    # =========================
    'RSI_14': 'RSI 14',
    'LD_RSI_14': 'Last Day RSI 14',

    # =========================
    # 8. Bollinger Bands (20-day)
    # =========================
    'BBU_20': 'Bollinger Band Upper 20',
    'BBL_20': 'Bollinger Band Lower 20',

    # Last Day Bollinger Bands
    'LD_BBU_20': 'Last Day Bollinger Band Upper 20',
    'LD_BBL_20': 'Last Day Bollinger Band Lower 20',

    # =========================
    # 9. Moving Average Convergence Divergence (MACD)
    # =========================
    'MACD_LINE': 'MACD Line (12,26)',
    'MACD_SIGNAL_LINE': 'MACD Signal Line (9)',
    'MACD_HISTOGRAM': 'MACD Histogram',

    # Last Day MACD
    'LD_MACD_LINE': 'Last Day MACD Line (12,26)',
    'LD_MACD_SIGNAL_LINE': 'Last Day MACD Signal Line (9)',
    'LD_MACD_HISTOGRAM': 'Last Day MACD Histogram',

    # =========================
    # 10. Volatility Indicators
    # =========================
    'TR_CURRENT': 'Current True Range',
    'ATR_14': 'ATR 14',

    # Last Day Volatility Indicators
    'LD_TR_CURRENT': 'Last Day True Range',
    'LD_ATR_14': 'Last Day ATR 14',

    # =========================
    # 11. Volume-Based Indicators
    # =========================
    'OBV': 'On-Balance Volume',

    # Last Day Volume Indicators
    'LD_OBV': 'Last Day On-Balance Volume',

    # =========================
    # 12. Momentum Indicators
    # =========================
    'MOMENTUM_10': 'Momentum 10',
    'ROC_14': 'Rate of Change 14',

    # Last Day Momentum Indicators
    'LD_MOMENTUM_10': 'Last Day Momentum 10',
    'LD_ROC_14': 'Last Day Rate of Change 14',

    # =========================
    # 13. Oscillators
    # =========================
    'WILLR_14': 'Williams %R 14',
    'STOCH_K': 'Stochastic %K',
    'STOCH_D': 'Stochastic %D',

    # Last Day Oscillators
    'LD_WILLR_14': 'Last Day Williams %R 14',
    'LD_STOCH_K': 'Last Day Stochastic %K',
    'LD_STOCH_D': 'Last Day Stochastic %D'
}

BEST_PARAMS_DF_COL_NAMES = {
  'MODEL_PATH': 'Model Path'
}

CSV_PATHS = {
    'CRYPTO': {
        'WEEKLY': {
            'BTC': path.join(BASE_PATH, 'data/crypto/btc_weekly_data.csv'),
            'FET': path.join(BASE_PATH, 'data/crypto/fet_weekly_data.csv'),
        },
        'DAILY': {
            'BTC': path.join(BASE_PATH, 'data/crypto/btc_daily_data.csv'),
            'FET': path.join(BASE_PATH, 'data/crypto/fet_daily_data.csv')
        }
    },
    'MODEL_TUNING_RESULTS': path.join(BASE_PATH, 'data/models/tuning_results.csv'),
    'PREDICTIONS': path.join(BASE_PATH, 'data/predictions/crypto_price_predictions.csv')
}

MODEL_TYPES = ['DTREE', 'RFOREST', 'XGBOOST']
CRYPTOCURRENCIES = ['BTC', 'FET']

MODEL_PATHS = {
    crypto: {
        model_type: path.join(BASE_PATH, f'models/{crypto.lower()}_{model_type.lower()}_close_price.joblib')
        for model_type in MODEL_TYPES
    }
    for crypto in CRYPTOCURRENCIES
}

# Output example:
# MODEL_PATHS = {
#     'BTC': {
#         'DTREE': path.join(BASE_PATH, 'models/btc_dtree_close_price.joblib'),
#         'RFOREST': path.join(BASE_PATH, 'models/btc_rforest_close_price.joblib')
#     },
#     'FET': {
#         'DTREE': path.join(BASE_PATH, 'models/fet_dtree_close_price.joblib'),
#         'RFOREST': path.join(BASE_PATH, 'models/fet_rforest_close_price.joblib')
#     }
# }
