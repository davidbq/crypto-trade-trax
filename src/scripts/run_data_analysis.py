from pandas import DataFrame, Series
from sklearn.metrics.pairwise import cosine_similarity
from numpy import tril_indices_from
from ..data.loading import load_csv_data
from ..utils.plot import plot_dataframe, plot_week_similarities
from ..globals.constants import CSV_PATHS

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
        'BTC': CSV_PATHS['CRYPTO']['BTC'],
        'FET': CSV_PATHS['CRYPTO']['FET'],
    }

    for key in datasets.keys():
        df = load_csv_data(CSV_PATHS['CRYPTO'][key])
        plot_dataframe(df, f'DataFrame {key}')

        df_cosine_sim = build_cosine_sim_df(df)
        plot_dataframe(df_cosine_sim, f'DataFrame Cosine Similarities {key}')

        top_5_similarities = extract_top_n_similarities(df_cosine_sim, 5)
        plot_week_similarities(df, top_5_similarities)


if __name__ == "__main__":
    run_analysis()
