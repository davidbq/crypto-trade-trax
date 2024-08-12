SYMBOLS = {
    'BTC_USDT': 'BTCUSDT',
    'FET_USDT': 'FETUSDT'
}

DATAFRAME_COLUMN_NAMES = {
    'DAY_OF_WEEK': 'Day of week',
    'WEEK_NUMBER': 'Week number',
    'OPEN_PRICE': 'Open price',
    'CLOSE_PRICE': 'Close price',
    'PERCENT_CHANGE': 'Percent change',
    'HIGH_PRICE': 'High price',
    'LOW_PRICE': 'Low price',
    'CLOSE_PRICE': 'Close price',
    'VOLUME': 'Volume',
    'OPEN_TIME': 'Open time',
    'CLOSE_TIME': 'Close time'
}

DATAFRAME_UNUSED_COLUMN_NAMES = {
    'QUOTE_ASSET_VOLUME': 'Quote asset volume',
    'NUMBER_OF_TRADES': 'Number of trades',
    'TAKER_BUY_BASE_ASSET_VOLUME': 'Taker buy base asset volume',
    'TAKER_BUY_QUOTE_ASSET_VOLUME': 'Taker buy quote asset volume',
    'IGNORE': 'Ignore'
}

DATAFRAME_UNUSED_COLUMNS = [
    DATAFRAME_UNUSED_COLUMN_NAMES['QUOTE_ASSET_VOLUME'],
    DATAFRAME_UNUSED_COLUMN_NAMES['NUMBER_OF_TRADES'],
    DATAFRAME_UNUSED_COLUMN_NAMES['TAKER_BUY_BASE_ASSET_VOLUME'],
    DATAFRAME_UNUSED_COLUMN_NAMES['TAKER_BUY_QUOTE_ASSET_VOLUME'],
    DATAFRAME_UNUSED_COLUMN_NAMES['IGNORE']
]

FETCH_DATA = {
    'HISTORICAL_START_DATE': '2000-01-01',
    'INTERVAL': '1d',
    'BINANCE_COLUMNS': [
        DATAFRAME_COLUMN_NAMES['OPEN_TIME'],
        DATAFRAME_COLUMN_NAMES['OPEN_PRICE'],
        DATAFRAME_COLUMN_NAMES['HIGH_PRICE'],
        DATAFRAME_COLUMN_NAMES['LOW_PRICE'],
        DATAFRAME_COLUMN_NAMES['CLOSE_PRICE'],
        DATAFRAME_COLUMN_NAMES['VOLUME'],
        DATAFRAME_COLUMN_NAMES['CLOSE_TIME'],
        DATAFRAME_UNUSED_COLUMN_NAMES['QUOTE_ASSET_VOLUME'],
        DATAFRAME_UNUSED_COLUMN_NAMES['NUMBER_OF_TRADES'],
        DATAFRAME_UNUSED_COLUMN_NAMES['TAKER_BUY_BASE_ASSET_VOLUME'],
        DATAFRAME_UNUSED_COLUMN_NAMES['TAKER_BUY_QUOTE_ASSET_VOLUME'],
        DATAFRAME_UNUSED_COLUMN_NAMES['IGNORE']
    ]
}

CSV_PATHS = {
  'BTC_HISTORICAL': 'data/btc_historical_data.csv',
  'BTC_RECENT': 'data/btc_recent_data.csv',
  'FET_HISTORICAL': 'data/fet_historical_data.csv',
  'FET_RECENT': 'data/fet_recent_data.csv',
}

MODEL_PATHS = {
    'BTC_HISTORICAL': {
        'OPX_DTREE_NO_HP_OPT': 'models/btc_hist_opx_dtree_no_hp_opt.joblib',
        'OPX_DTREE_WITH_HP_OPT': 'models/btc_hist_opx_dtree_with_hp_opt.joblib',
        'CPX_DTREE_NO_HP_OPT': 'models/btc_hist_cpx_dtree_no_hp_opt.joblib',
        'CPX_DTREE_WITH_HP_OPT': 'models/btc_hist_cpx_dtree_with_hp_opt.joblib'
    },
    'BTC_RECENT': {
        'OPX_DTREE_NO_HP_OPT': 'models/btc_rcnt_opx_dtree_no_hp_opt.joblib',
        'OPX_DTREE_WITH_HP_OPT': 'models/btc_rcnt_opx_dtree_with_hp_opt.joblib',
        'CPX_DTREE_NO_HP_OPT': 'models/btc_rcnt_cpx_dtree_no_hp_opt.joblib',
        'CPX_DTREE_WITH_HP_OPT': 'models/btc_rcnt_cpx_dtree_with_hp_opt.joblib'
    },
    'FET_HISTORICAL': {
        'OPX_DTREE_NO_HP_OPT': 'models/fet_hist_opx_dtree_no_hp_opt.joblib',
        'OPX_DTREE_WITH_HP_OPT': 'models/fet_hist_opx_dtree_with_hp_opt.joblib',
        'CPX_DTREE_NO_HP_OPT': 'models/fet_hist_cpx_dtree_no_hp_opt.joblib',
        'CPX_DTREE_WITH_HP_OPT': 'models/fet_hist_cpx_dtree_with_hp_opt.joblib'
    },
    'FET_RECENT': {
        'OPX_DTREE_NO_HP_OPT': 'models/fet_rcnt_opx_dtree_no_hp_opt.joblib',
        'OPX_DTREE_WITH_HP_OPT': 'models/fet_rcnt_opx_dtree_with_hp_opt.joblib',
        'CPX_DTREE_NO_HP_OPT': 'models/fet_rcnt_cpx_dtree_no_hp_opt.joblib',
        'CPX_DTREE_WITH_HP_OPT': 'models/fet_rcnt_cpx_dtree_with_hp_opt.joblib'
    }
}
