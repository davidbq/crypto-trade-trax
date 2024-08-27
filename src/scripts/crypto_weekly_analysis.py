from pandas import read_csv
from ..analysis.cosine_operations import build_cosine_sim_df, find_weekly_cosine_matches, get_subsequent_weeks_to_similarity
from ..plotting.table import plot_dataframe
from ..plotting.line import plot_similar_weeks, plot_following_weeks
from ..globals.constants import CSV_PATHS, WEEKLY_COL_NAMES

def run_analysis():
    '''
    Orchestrates the data analysis process by loading datasets, calculating weekly metrics, computing
    cosine similarities, and plotting the results.
    '''
    datasets = {
        'BTC': CSV_PATHS['CRYPTO']['WEEKLY']['BTC'],
        'FET': CSV_PATHS['CRYPTO']['WEEKLY']['FET'],
    }

    for key in datasets.keys():
        df = read_csv(CSV_PATHS['CRYPTO']['WEEKLY'][key], index_col=WEEKLY_COL_NAMES['WEEK_NUMBER'])
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
