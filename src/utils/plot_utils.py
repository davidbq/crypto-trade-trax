from plotly.graph_objects import Figure, Table
from plotly.express import line
from pandas import DataFrame, Series
from ..globals.constants import DATAFRAME_COLUMN_NAMES

DAY_OF_WEEK = DATAFRAME_COLUMN_NAMES['DAY_OF_WEEK']
WEEK_NUMBER = DATAFRAME_COLUMN_NAMES['WEEK_NUMBER']
OPEN_PRICE = DATAFRAME_COLUMN_NAMES['OPEN_PRICE']
CLOSE_PRICE = DATAFRAME_COLUMN_NAMES['CLOSE_PRICE']
PERCENT_CHANGE = DATAFRAME_COLUMN_NAMES['PERCENT_CHANGE']

def plot_dataframe(df_data: DataFrame, title: str) -> None:
    blue = '#3A416C'
    grey = '#f5f5f5'
    aux_data = df_data.reset_index()
    fig = Figure(data=[Table(
        header=dict(values=list(aux_data.columns),
            fill_color=blue,
            font=dict(color='white'),
            align=['left','center'],
        ),
        cells=dict(values=[aux_data[col].tolist() for col in aux_data.columns],
            fill=dict(color=[[grey if i % 2 == 0 else 'white' for i in range(len(aux_data))]]),
            align=['left','center'],
        )
    )])
    fig.update_layout(title_text=title, title_x=0.5)
    fig.show()

def plot_week_similarities(df_weekly_data: DataFrame, week_similarities: Series) -> None:
    df = df_weekly_data.reset_index().melt(id_vars=WEEK_NUMBER, var_name=DAY_OF_WEEK, value_name=PERCENT_CHANGE)
    for ((week1, week2), similarity) in week_similarities.items():
        df_filtered_data = df[(df[WEEK_NUMBER] == week1) | (df[WEEK_NUMBER] == week2)]
        fig = line(
            df_filtered_data,
            x=DAY_OF_WEEK,
            y=PERCENT_CHANGE,
            color=WEEK_NUMBER,
            title=f'Cosine Similarity: {similarity:.2f} (Week {week1} vs Week {week2})',
            labels={DAY_OF_WEEK: DAY_OF_WEEK, PERCENT_CHANGE: PERCENT_CHANGE},
            line_shape='linear',
            markers=True
        )
        fig.show()