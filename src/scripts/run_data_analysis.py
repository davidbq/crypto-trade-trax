from pandas import DataFrame, Series
from sklearn.metrics.pairwise import cosine_similarity
from numpy import tril_indices_from
from ..data.csv_data_cleaner import load_csv_data
from ..utils.plot import plot_dataframe, plot_week_similarities
from ..globals.constants import DATAFRAME_COLUMN_NAMES, CSV_PATHS

def build_weekly_metrics_df(df: DataFrame) -> DataFrame:
    '''
    Processes a DataFrame containing daily cryptocurrency price data to calculate weekly percentage changes,
    starting from the first complete week (Monday to Sunday) in the dataset. The resulting DataFrame provides
    a pivot table with the percentage change for each day of the week, indexed by week number.
    '''

    DAY_OF_WEEK = DATAFRAME_COLUMN_NAMES['DAY_OF_WEEK']
    WEEK_NUMBER = DATAFRAME_COLUMN_NAMES['WEEK_NUMBER']
    OPEN_PRICE = DATAFRAME_COLUMN_NAMES['OPEN_PRICE']
    CLOSE_PRICE = DATAFRAME_COLUMN_NAMES['CLOSE_PRICE']
    PERCENT_CHANGE = DATAFRAME_COLUMN_NAMES['PERCENT_CHANGE']
    DAY_OF_WEEK_NAMES = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    # Find the first Monday in the dataset
    first_monday_idx = df.index[df.index.day_name() == 'Monday'][0]

    # Filter out the data before this first Monday
    df = df[df.index >= first_monday_idx]

    df[DAY_OF_WEEK] = df.index.day_name()
    # Week number relative to the first week in the dataset
    df[WEEK_NUMBER] = (df.index - df.index.min()).days // 7 + 1
    df[PERCENT_CHANGE] = ((df[CLOSE_PRICE] - df[OPEN_PRICE]) / df[OPEN_PRICE]) * 100

    df = df.pivot_table(index=WEEK_NUMBER, columns=DAY_OF_WEEK, values=PERCENT_CHANGE)

    return df[DAY_OF_WEEK_NAMES]

def build_cosine_sim_df(df: DataFrame) -> DataFrame:
    '''
    Calculates the cosine similarity matrix for a given DataFrame, where each row represents a different
    week, and each column represents the percentage change on a specific day of the week.
    '''

    cosine_sim_matrix = cosine_similarity(df.fillna(0))
    return DataFrame(cosine_sim_matrix, index=df.index, columns=df.index)

def extract_top_n_similarities(df: DataFrame, top_n: int) -> Series:
    '''
    Extracts the top N cosine similarities from the cosine similarity matrix, ignoring self-comparisons
    and duplicate comparisons.
    '''

    # Ignore diagonal (self-comparisons) and lower triangle duplicates
    df.values[tril_indices_from(df)] = -1
    return df.unstack().sort_values(ascending=False).head(top_n)

def run_analysis():
    '''
    Orchestrates the data analysis process by loading datasets, calculating weekly metrics, computing
    cosine similarities, and plotting the results.
    '''

    datasets = {
        'BTC_HISTORICAL': CSV_PATHS['CRYPTO']['BTC_HISTORICAL'],
        'BTC_RECENT': CSV_PATHS['CRYPTO']['BTC_RECENT'],
        'FET_HISTORICAL': CSV_PATHS['CRYPTO']['FET_HISTORICAL'],
        'FET_RECENT': CSV_PATHS['CRYPTO']['FET_RECENT']
    }

    for key in datasets.keys():
        df_main_data = load_csv_data(CSV_PATHS[key])
        plot_dataframe(df_main_data, f'DataFrame {key}')

        df_weekly_data = build_weekly_metrics_df(df_main_data)
        plot_dataframe(df_weekly_data, f'DataFrame Weekly Data {key}')

        df_cosine_sim = build_cosine_sim_df(df_weekly_data)
        plot_dataframe(df_cosine_sim, f'DataFrame Cosine Similarities {key}')

        top_5_similarities = extract_top_n_similarities(df_cosine_sim, 5)
        plot_week_similarities(df_weekly_data, top_5_similarities)


if __name__ == "__main__":
    run_analysis()