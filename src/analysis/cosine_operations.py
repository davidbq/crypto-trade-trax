from pandas import DataFrame, Series
from sklearn.metrics.pairwise import cosine_similarity
from ..config.logging import info

def build_cosine_sim_df(df: DataFrame) -> DataFrame:
    cosine_sim_matrix = cosine_similarity(df.fillna(0))
    return DataFrame(cosine_sim_matrix, index=df.index, columns=df.index)

def find_weekly_cosine_matches(df: DataFrame, reference_week: int, top_n: int = 3) -> Series:
    # Get the similarities for the reference week, exclude self-comparison
    similarity_series = df.loc[reference_week].drop(index=reference_week)
    return similarity_series.sort_values(ascending=False).head(top_n)

def get_subsequent_weeks_to_similarity(df_weekly_data: DataFrame, week_similarities: Series) -> Series:
    following_weeks = {}
    for week in week_similarities.index:
        next_week = week + 1
        if next_week in df_weekly_data.index:
            following_weeks[next_week] = next_week  # Store just the week number, not the similarity score
        else:
            info(f'Week {next_week} not found, skipping.')

    return Series(following_weeks)
