from pandas import DataFrame
from plotly.graph_objects import Figure, Table

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
