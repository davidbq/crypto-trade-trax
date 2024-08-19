from os import path

BASE_PATH = path.dirname(path.dirname(path.dirname(__file__)))

SYMBOLS = {
    'BTC_USDT': 'BTCUSDT',
    'FET_USDT': 'FETUSDT'
}

CRYPTO_DF_COLS_NAMES = {
    'OPEN_TIME': 'Open time',
    'DAY_OF_WEEK': 'Day of week',
    'WEEK_NUMBER': 'Week number',
    'OPEN_PRICE': 'Open price',
    'CLOSE_PRICE': 'Close price',
    'PERCENT_CHANGE': 'Percent change',
}

BP_DF_COLS_NAMES = {
  'MODEL_PATH': 'Model path'
}

FETCH_DATA = {
    'HISTORICAL_START_DATE': '2000-01-01',
    'INTERVAL': '1d',
    'RELEVANT_BINANCE_COLS': [
        CRYPTO_DF_COLS_NAMES['OPEN_TIME'],
        CRYPTO_DF_COLS_NAMES['OPEN_PRICE'],
        CRYPTO_DF_COLS_NAMES['CLOSE_PRICE'],
    ]
}

CSV_PATHS = {
    'CRYPTO': {
        'BTC': path.join(BASE_PATH, 'data/crypto/btc_data.csv'),
        'FET': path.join(BASE_PATH, 'data/crypto/fet_data.csv'),
    },
    'OPT_HP': path.join(BASE_PATH, 'data/opt_hp/best_params.csv')
}

MODEL_PATHS = {
    'BTC': {
        'DTREE': {
            'MON_DTREE': path.join(BASE_PATH, 'models/btc_dtree_mon.joblib'),
            'MON_DTREE_TEST': path.join(BASE_PATH, 'models/btc_dtree_mon_test.joblib'),
            'TUE_DTREE': path.join(BASE_PATH, 'models/btc_dtree_tue.joblib'),
            'WED_DTREE': path.join(BASE_PATH, 'models/btc_dtree_wed.joblib'),
            'THU_DTREE': path.join(BASE_PATH, 'models/btc_dtree_thu.joblib'),
            'FRI_DTREE': path.join(BASE_PATH, 'models/btc_dtree_fri.joblib'),
            'SAT_DTREE': path.join(BASE_PATH, 'models/btc_dtree_sat.joblib'),
            'SUN_DTREE': path.join(BASE_PATH, 'models/btc_dtree_sun.joblib')
        },
        'RFOREST': {
            'OPX_RFOREST_NO_HP_OPT': path.join(BASE_PATH, 'models/btc_hist_opx_rforest_no_hp_opt.joblib'),
            'OPX_RFOREST_WITH_HP_OPT': path.join(BASE_PATH, 'models/btc_hist_opx_rforest_with_hp_opt.joblib'),
            'CPX_RFOREST_NO_HP_OPT': path.join(BASE_PATH, 'models/btc_hist_cpx_rforest_no_hp_opt.joblib'),
            'CPX_RFOREST_WITH_HP_OPT': path.join(BASE_PATH, 'models/btc_hist_cpx_rforest_with_hp_opt.joblib')
        }
    },
    'FET': {
        'DTREE': {
            'OPX_DTREE_NO_HP_OPT': path.join(BASE_PATH, 'models/fet_hist_opx_dtree_no_hp_opt.joblib'),
            'OPX_DTREE_WITH_HP_OPT': path.join(BASE_PATH, 'models/fet_hist_opx_dtree_with_hp_opt.joblib'),
            'CPX_DTREE_NO_HP_OPT': path.join(BASE_PATH, 'models/fet_hist_cpx_dtree_no_hp_opt.joblib'),
            'CPX_DTREE_WITH_HP_OPT': path.join(BASE_PATH, 'models/fet_hist_cpx_dtree_with_hp_opt.joblib')
        },
        'RFOREST': {
            'OPX_RFOREST_NO_HP_OPT': path.join(BASE_PATH, 'models/fet_hist_opx_rforest_no_hp_opt.joblib'),
            'OPX_RFOREST_WITH_HP_OPT': path.join(BASE_PATH, 'models/fet_hist_opx_rforest_with_hp_opt.joblib'),
            'CPX_RFOREST_NO_HP_OPT': path.join(BASE_PATH, 'models/fet_hist_cpx_rforest_no_hp_opt.joblib'),
            'CPX_RFOREST_WITH_HP_OPT': path.join(BASE_PATH, 'models/fet_hist_cpx_rforest_with_hp_opt.joblib')
        }
    }
}
