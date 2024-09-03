from typing import Any, Callable, Dict

from pandas import DataFrame, Series
from plotly.express import line

from ..globals.constants import WEEKLY_COL_NAMES

def _prepare_plot_data(df_weekly_data: DataFrame, reference_week: int, week: int) -> DataFrame:
    df = df_weekly_data.reset_index().melt(id_vars=WEEKLY_COL_NAMES['WEEK_NUMBER'], var_name=WEEKLY_COL_NAMES['DAY_OF_WEEK'], value_name=WEEKLY_COL_NAMES['PERCENT_CHANGE'])
    return df[(df[WEEKLY_COL_NAMES['WEEK_NUMBER']] == reference_week) | (df[WEEKLY_COL_NAMES['WEEK_NUMBER']] == week)]

def _generate_plot_config(x_col: str, y_col: str, color_col: str, title_generator: Callable[..., str], **kwargs) -> Dict[str, Any]:
    return {
        'x_col': x_col,
        'y_col': y_col,
        'color_col': color_col,
        'title': title_generator(**kwargs)
    }

def _similar_weeks_title(similarity: float, reference_week: int, week: int) -> str:
    return f'Cosine Similarity: {similarity:.2f} (Week {reference_week} vs Week {week})'

def _following_weeks_title(reference_week: int, week: int) -> str:
    return (
        f'Comparison of Current Week {reference_week} with Following Week {week}'
        if reference_week
        else f'Following Week {week}'
    )

def _create_plot(df_filtered_data: DataFrame, plot_config: Dict[str, Any]) -> None:
    fig = line(
        df_filtered_data,
        x=plot_config['x_col'],
        y=plot_config['y_col'],
        color=plot_config['color_col'],
        title=plot_config['title'],
        labels={plot_config['x_col']: plot_config['x_col'], plot_config['y_col']: plot_config['y_col']},
        line_shape='linear',
        markers=True
    )
    fig.show()

def plot_similar_weeks(df_weekly_data: DataFrame, week_similarities: Series, reference_week: int) -> None:
    for week, similarity in week_similarities.items():
        df_filtered_data = _prepare_plot_data(df_weekly_data, reference_week, week)
        plot_config = _generate_plot_config(
            x_col=WEEKLY_COL_NAMES['DAY_OF_WEEK'],
            y_col=WEEKLY_COL_NAMES['PERCENT_CHANGE'],
            color_col=WEEKLY_COL_NAMES['WEEK_NUMBER'],
            title_generator=_similar_weeks_title,
            similarity=similarity,
            reference_week=reference_week,
            week=week
        )
        _create_plot(df_filtered_data, plot_config)

def plot_following_weeks(df_weekly_data: DataFrame, following_weeks: Series, reference_week: int) -> None:
    for week in following_weeks.index:
        df_filtered_data = _prepare_plot_data(df_weekly_data, reference_week, week)
        plot_config = _generate_plot_config(
            x_col=WEEKLY_COL_NAMES['DAY_OF_WEEK'],
            y_col=WEEKLY_COL_NAMES['PERCENT_CHANGE'],
            color_col=WEEKLY_COL_NAMES['WEEK_NUMBER'],
            title_generator=_following_weeks_title,
            reference_week=reference_week,
            week=week
        )
        _create_plot(df_filtered_data, plot_config)
