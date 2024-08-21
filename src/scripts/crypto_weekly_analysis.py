from pandas import DataFrame, Series
from sklearn.metrics.pairwise import cosine_similarity
from ..data.loading import load_csv_data
from ..plotting.table import plot_dataframe
from ..plotting.line import plot_similar_weeks, plot_following_weeks
from ..globals.constants import CSV_PATHS

def build_cosine_sim_df(df: DataFrame) -> DataFrame:
    '''
    Calculates the cosine similarity matrix for a given DataFrame, where each row represents a different
    week, and each column represents the percentage change on a specific day of the week.
    '''
    cosine_sim_matrix = cosine_similarity(df.fillna(0))
    return DataFrame(cosine_sim_matrix, index=df.index, columns=df.index)

def find_weekly_cosine_matches(df: DataFrame, reference_week: int, top_n: int = 3) -> Series:
    '''
    Finds the top N most similar weeks to the reference week using cosine similarity.

    Parameters:
        df (DataFrame): The cosine similarity matrix.
        reference_week (int): The index of the reference week (can be -1 for the current week).
        top_n (int): The number of most similar weeks to return (default is 3).

    Returns:
        DataFrame: A DataFrame containing the most similar weeks and their similarity scores.
    '''
    # Get the similarities for the reference week, exclude self-comparison
    similarity_series = df.loc[reference_week].drop(index=reference_week)
    # Return the top N most similar weeks
    return similarity_series.sort_values(ascending=False).head(top_n)

def get_subsequent_weeks_to_similarity(df_weekly_data: DataFrame, week_similarities: Series) -> Series:
    """
    Creates a Series that links each week immediately after the top similar weeks to the similarity
    values of the prior weeks, enabling analysis of how these following weeks compare.

    Parameters:
        df_weekly_data (DataFrame): The DataFrame containing the weekly data.
        week_similarities (Series): A Series containing the top N similar weeks with their similarity scores.

    Returns:
        Series: A Series containing the weeks following the top similar weeks and their similarity scores.
    """
    following_weeks = {}
    for week in week_similarities.index:
        next_week = week + 1
        if next_week in df_weekly_data.index:
            following_weeks[next_week] = next_week  # Store just the week number, not the similarity score
        else:
            print(f'Week {next_week} not found, skipping.')

    return Series(following_weeks)


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

        last_week = df.index[-2]
        reference_week = df.index[-1]
        # If last data update was Monday, no need to consider the previous week, as we already have a full week covered.
        if df.iloc[-1].notna().all(): # Last update was Monday
            last_week = df.index[-1]
            reference_week = None

        top_3_similar_to_last_week = find_weekly_cosine_matches(df_cosine_sim, reference_week=last_week, top_n=3)
        plot_similar_weeks(df, top_3_similar_to_last_week, last_week)
        subsequent_weeks = get_subsequent_weeks_to_similarity(df, top_3_similar_to_last_week)
        plot_following_weeks(df, subsequent_weeks, reference_week)

if __name__ == "__main__":
    run_analysis()
