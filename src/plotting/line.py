from pandas import DataFrame, Series
from plotly.express import line
from ..globals.constants import WEEKLY_COL_NAMES

DAY_OF_WEEK = WEEKLY_COL_NAMES['DAY_OF_WEEK']
WEEK_NUMBER = WEEKLY_COL_NAMES['WEEK_NUMBER']
OPEN_PRICE = WEEKLY_COL_NAMES['OPEN_PRICE']
CLOSE_PRICE = WEEKLY_COL_NAMES['CLOSE_PRICE']
PERCENT_CHANGE = WEEKLY_COL_NAMES['PERCENT_CHANGE']

def base_plot(df_filtered_data: DataFrame, title: str, x_col: str, y_col: str, color_col: str) -> None:
    """
    A base plotting function that handles the common plotting logic.
    """
    fig = line(
        df_filtered_data,
        x=x_col,
        y=y_col,
        color=color_col,
        title=title,
        labels={x_col: x_col, y_col: y_col},
        line_shape='linear',
        markers=True
    )
    fig.show()

def prepare_plot_data(df_weekly_data: DataFrame, reference_week: int, week: int) -> DataFrame:
    """
    Prepares the DataFrame for plotting by filtering and reshaping the data.
    """
    df = df_weekly_data.reset_index().melt(id_vars=WEEK_NUMBER, var_name=DAY_OF_WEEK, value_name=PERCENT_CHANGE)
    return df[(df[WEEK_NUMBER] == reference_week) | (df[WEEK_NUMBER] == week)]


def plot_similar_weeks(df_weekly_data: DataFrame, week_similarities: Series, reference_week: int) -> None:
    """
    Plots the weekly data comparing the reference week to the most similar weeks.
    """
    for week, similarity in week_similarities.items():
        df_filtered_data = prepare_plot_data(df_weekly_data, reference_week, week)
        title = f'Cosine Similarity: {similarity:.2f} (Week {reference_week} vs Week {week})'
        base_plot(df_filtered_data, title, x_col=DAY_OF_WEEK, y_col=PERCENT_CHANGE, color_col=WEEK_NUMBER)

def plot_following_weeks(df_weekly_data: DataFrame, following_weeks: Series, reference_week: int) -> None:
    """
    Plots the weekly data comparing the reference week to the weeks following the top similar weeks.
    """
    for week in following_weeks.index:
        df_filtered_data = prepare_plot_data(df_weekly_data, reference_week, week)
        title = (
            f'Comparison of Current Week {reference_week} with Following Week {week}'
            if reference_week
            else f'Following Week {week}'
        )
        base_plot(df_filtered_data, title, x_col=DAY_OF_WEEK, y_col=PERCENT_CHANGE, color_col=WEEK_NUMBER)
