from pandas import DataFrame, Series
from sklearn.metrics.pairwise import cosine_similarity
from numpy import tril_indices_from
from csv_data_cleaner import load_csv_data
from plot_utils import plot_dataframe, plot_week_similarities
from constants import DATAFRAME_COLUMN_NAMES, CSV_PATHS
from logging_config import info

def build_weekly_metrics_df(df: DataFrame) -> DataFrame:
    DAY_OF_WEEK = DATAFRAME_COLUMN_NAMES['DAY_OF_WEEK']
    WEEK_NUMBER = DATAFRAME_COLUMN_NAMES['WEEK_NUMBER']
    OPEN_PRICE = DATAFRAME_COLUMN_NAMES['OPEN_PRICE']
    CLOSE_PRICE = DATAFRAME_COLUMN_NAMES['CLOSE_PRICE']
    PERCENT_CHANGE = DATAFRAME_COLUMN_NAMES['PERCENT_CHANGE']
    DAY_OF_WEEK_NAMES = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    df[DAY_OF_WEEK] = df.index.day_name()
    df[WEEK_NUMBER] = df.index.isocalendar().week
    df[PERCENT_CHANGE] = ((df[CLOSE_PRICE] - df[OPEN_PRICE]) / df[OPEN_PRICE]) * 100
    df = df.pivot_table(index=WEEK_NUMBER, columns=DAY_OF_WEEK, values=PERCENT_CHANGE)

    return df[DAY_OF_WEEK_NAMES]

def build_cosine_sim_df(df_weekly_data: DataFrame) -> DataFrame:
    cosine_sim_matrix = cosine_similarity(df_weekly_data.fillna(0))
    return DataFrame(cosine_sim_matrix, index=df_weekly_data.index, columns=df_weekly_data.index)

def extract_top_n_similarities(df_cosine_sim: DataFrame, top_n: int) -> Series:
    # Ignore diagonal (self-comparisons) and lower triangle duplicates
    df_cosine_sim.values[tril_indices_from(df_cosine_sim)] = -1
    return df_cosine_sim.unstack().sort_values(ascending=False).head(top_n)

def run_analysis():
    info("Starting data analysis process.")
    datasets = {
        'BTC_HISTORICAL': CSV_PATHS['BTC_HISTORICAL'],
        'BTC_RECENT': CSV_PATHS['BTC_RECENT'],
        'FET_HISTORICAL': CSV_PATHS['FET_HISTORICAL'],
        'FET_RECENT': CSV_PATHS['FET_RECENT']
    }

    for key in datasets.keys():
        df_main_data = load_csv_data(CSV_PATHS[key])
        plot_dataframe(df_main_data, f'DataFrame {key}')
        info(f"Loaded and plotted data for {key}.")

        df_weekly_data = build_weekly_metrics_df(df_main_data)
        plot_dataframe(df_weekly_data, f'DataFrame Weekly Data {key}')
        info(f"Calculated and plotted weekly metrics for {key}.")

        df_cosine_sim = build_cosine_sim_df(df_weekly_data)
        plot_dataframe(df_cosine_sim, f'DataFrame Cosine Similarities {key}')
        info(f"Calculated and plotted cosine similarities for {key}.")

        top_5_similarities = extract_top_n_similarities(df_cosine_sim, 5)
        plot_week_similarities(df_weekly_data, top_5_similarities)
        info(f"Plotted top 5 week similarities for {key}.")

    info("Data analysis process completed.")

if __name__ == "__main__":
    run_analysis()