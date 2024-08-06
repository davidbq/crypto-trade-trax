from binance_client import get_binance_client
from constants import SYMBOLS
from datetime import datetime, timedelta
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from typing import List, Any

DATA_FETCH_START_DATE = '2024-01-01'
INTERVAL = '1d'
DATA_FETCH_END_DATE = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d') # 1 day ago
# Dataframe Columns
DAY_OF_WEEK = 'Day of Week'
WEEK_NUMBER = 'Week Number'
OPEN_PRICE = 'Open Price'
CLOSE_PRICE = 'Close Price'
PERCENT_CHANGE = 'Percent Change'

def fetch_historical_data(symbol: str, interval: str, start_date: str, end_date: str) -> List[List[Any]]:
    binance_client = get_binance_client()
    try:
        return binance_client.get_historical_klines(symbol, interval, start_date, end_date)
    except Exception as e:
        print(f"Error fetching historical data: {e}")
        return []

def build_main_df(raw_data: List) -> pd.DataFrame:
    columns_names = ['Start Time', OPEN_PRICE, 'High Price', 'Low Price', CLOSE_PRICE, 'Volume', 'Close Time']
    column_indices = [0, 1, 2, 3, 4, 5, 6]

    cleaned_data = [[entry[i] for i in column_indices] for entry in raw_data]
    df = pd.DataFrame(cleaned_data, columns=columns_names)

    for col in [OPEN_PRICE, 'High Price', 'Low Price', CLOSE_PRICE, 'Volume']:
        df[col] = df[col].astype(float)

    df['Start Time'] = pd.to_datetime(df['Start Time'], unit='ms')
    df['Close Time'] = pd.to_datetime(df['Close Time'], unit='ms')

    df.set_index('Start Time', inplace=True)

    return df

def plot_table(df_data: pd.DataFrame, title: str) -> None:
    blue = '#3A416C'
    grey = '#f5f5f5'
    aux_data = df_data.reset_index()
    fig = go.Figure(data=[go.Table(
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

def build_weekly_metrics_df(df_main_data: pd.DataFrame) -> pd.DataFrame:
    df = df_main_data.copy()

    df[DAY_OF_WEEK] = df.index.day_name()
    df[WEEK_NUMBER] = df.index.isocalendar().week
    df[PERCENT_CHANGE] = ((df[CLOSE_PRICE] - df[OPEN_PRICE]) / df[OPEN_PRICE]) * 100
    df = df.pivot_table(index=WEEK_NUMBER, columns=DAY_OF_WEEK, values=PERCENT_CHANGE)
    day_of_week_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    return df[day_of_week_names]

def build_cosine_sim_df(df_weekly_data: pd.DataFrame) -> pd.DataFrame:
    cosine_sim_matrix = cosine_similarity(df_weekly_data.fillna(0))
    return pd.DataFrame(cosine_sim_matrix, index=df_weekly_data.index, columns=df_weekly_data.index)

def extract_top_n_similarities(df_cosine_sim: pd.DataFrame, top_n: int) -> pd.Series:
    # Ignore diagonal (self-comparisons) and lower triangle duplicates
    df_cosine_sim.values[np.tril_indices_from(df_cosine_sim)] = -1
    return df_cosine_sim.unstack().sort_values(ascending=False).head(top_n)

def plot_top_week_similarities(df_weekly_data: pd.DataFrame, top_similarities: pd.Series) -> None:
    df_plot_data = df_weekly_data.reset_index().melt(id_vars=WEEK_NUMBER, var_name=DAY_OF_WEEK, value_name=PERCENT_CHANGE)
    for ((week1, week2), similarity) in top_similarities.items():
        df_filtered_data = df_plot_data[(df_plot_data[WEEK_NUMBER] == week1) | (df_plot_data[WEEK_NUMBER] == week2)]
        fig = px.line(
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

def main_function():
    raw_data = fetch_historical_data(SYMBOLS['BTC_USDT'], INTERVAL, DATA_FETCH_START_DATE, DATA_FETCH_END_DATE)
    df_main_data = build_main_df(raw_data)
    plot_table(df_main_data, 'DataFrame Main Data')

    df_weekly_data = build_weekly_metrics_df(df_main_data)
    plot_table(df_weekly_data, 'DataFrame Weekly Data')

    df_cosine_sim = build_cosine_sim_df(df_weekly_data)
    plot_table(df_cosine_sim, 'DataFrame Cosine Similarities')

    top_15_similarities = extract_top_n_similarities(df_cosine_sim, 15)

    plot_top_week_similarities(df_weekly_data, top_15_similarities)

main_function()