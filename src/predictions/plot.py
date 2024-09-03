from typing import Dict, List

from pandas import DataFrame
from plotly.express import line, bar
from plotly.graph_objs import Figure
from plotly.subplots import make_subplots

def _create_melted_dataframe(df: DataFrame, id_vars: List[str], value_vars: List[str], var_name: str, value_name: str) -> DataFrame:
    return df.melt(id_vars=id_vars, value_vars=value_vars, var_name=var_name, value_name=value_name)

def _create_line_plot(df: DataFrame, x: str, y: str, color: str, labels: Dict[str, str], hover_data: Dict[str, str]) -> Figure:
    return line(df, x=x, y=y, color=color, labels=labels, hover_data=hover_data)

def _add_traces_to_subplot(fig: Figure, source_fig: Figure, row: int, col: int, legendgroup: str):
    for trace in source_fig.data:
        trace.showlegend = True
        trace.legendgroup = legendgroup
        fig.add_trace(trace, row=row, col=col)

def _update_layout_and_axes(fig: Figure, crypto: str):
    fig.update_layout(height=800, title_text=f'{crypto} Predictions and Errors', legend_tracegroupgap=330)
    fig.update_xaxes(title_text='Date', row=1, col=1)
    fig.update_xaxes(title_text='Date', row=2, col=1)
    fig.update_yaxes(title_text=f'{crypto} Price', row=1, col=1)
    fig.update_yaxes(title_text='Error Percentage', row=2, col=1)

def plot_predictions_and_errors(results: Dict[str, DataFrame]) -> None:
    for crypto, df in results.items():
        fig = make_subplots(rows=2, cols=1, subplot_titles=(f'{crypto} Price Predictions',f'{crypto} Prediction Error Percentages'))

        df_melted = _create_melted_dataframe(df, ['Date'], ['Actual', 'DTREE', 'RFOREST'], 'Prediction Type', 'Price')
        price_fig = _create_line_plot(df_melted, 'Date', 'Price', 'Prediction Type',
                                     {'Price': f'{crypto} Price', 'Date': 'Date'},
                                     {'Date': '|%Y-%m-%d'})
        _add_traces_to_subplot(fig, price_fig, 1, 1, 'price')

        df_error_melted = _create_melted_dataframe(df, ['Date'], ['DTREE_Error%', 'RFOREST_Error%'], 'Model', 'Error Percentage')
        error_fig = _create_line_plot(df_error_melted, 'Date', 'Error Percentage', 'Model',
                                     {'Error Percentage': 'Error %', 'Date': 'Date'},
                                     {'Date': '|%Y-%m-%d'})
        _add_traces_to_subplot(fig, error_fig, 2, 1, 'error')

        _update_layout_and_axes(fig, crypto)
        fig.show()

def plot_error_bars(avg_errors: DataFrame) -> None:
    fig = bar(avg_errors, x='Crypto', y=['DTREE_Avg_Error%', 'RFOREST_Avg_Error%'],
                 title='Average Error % by Crypto and Model',
                 labels={'value': 'Average Error %', 'variable': 'Model'},
                 barmode='group')
    fig.show()
