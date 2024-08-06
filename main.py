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
WEEK_DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

def fetch_historical_data(symbol: str, interval: str, start_date: str, end_date: str) -> List[List[Any]]:
    binance_client = get_binance_client()
    try:
        return binance_client.get_historical_klines(symbol, interval, start_date, end_date)
    except Exception as e:
        print(f"Error fetching historical data: {e}")
        return []

def build_main_df(raw_data: List) -> pd.DataFrame:
    columns_names = ['Start Time', 'Open Price', 'High Price', 'Low Price', 'Close Price', 'Volume', 'Close Time']
    column_indices = [0, 1, 2, 3, 4, 5, 6]

    cleaned_data = [[entry[i] for i in column_indices] for entry in raw_data]
    df = pd.DataFrame(cleaned_data, columns=columns_names)

    for col in ['Open Price', 'High Price', 'Low Price', 'Close Price', 'Volume']:
        df[col] = df[col].astype(float)

    df['Start Time'] = pd.to_datetime(df['Start Time'], unit='ms')
    df['Close Time'] = pd.to_datetime(df['Close Time'], unit='ms')

    df.set_index('Start Time', inplace=True)

    return df

def plot_table(df_data: pd.DataFrame, title: str) -> None:
    aux_data = df_data.reset_index()
    fig = go.Figure(data=[go.Table(
        header=dict(values=list(aux_data.columns),
            fill_color='#3A416C',
            font=dict(color='white'),
            align=['left','center'],
        ),
        cells=dict(values=[aux_data[col].tolist() for col in aux_data.columns],
            fill=dict(color=[['#f5f5f5' if i % 2 == 0 else '#ffffff' for i in range(len(aux_data))]]),
            align=['left','center'],
        )
    )])
    fig.update_layout(title_text=title, title_x=0.5)
    fig.show()

def build_weekly_metrics_df(df_main_data: pd.DataFrame) -> pd.DataFrame:
    df = df_main_data.copy()
    df['Day of Week'] = df.index.day_name()
    df['Week Number'] = df.index.isocalendar().week
    df['Percent Change'] = ((df['Close Price'] - df['Open Price']) / df['Open Price']) * 100
    df = df.pivot_table(index='Week Number', columns='Day of Week', values='Percent Change')
    return df[WEEK_DAYS]

def build_cosine_sim_df(df_weekly_data: pd.DataFrame) -> pd.DataFrame:
    cosine_sim_matrix = cosine_similarity(df_weekly_data.fillna(0))
    return pd.DataFrame(cosine_sim_matrix, index=df_weekly_data.index, columns=df_weekly_data.index)

def extract_top_n_similarities(df_cosine_sim: pd.DataFrame, top_n: int) -> pd.Series:
    # Ignore diagonal (self-comparisons) and lower triangle duplicates
    df_cosine_sim.values[np.tril_indices_from(df_cosine_sim)] = -1
    return df_cosine_sim.unstack().sort_values(ascending=False).head(top_n)

def plot_top_week_similarities(df_weekly_data: pd.DataFrame, top_similarities: pd.Series) -> None:
    df_plot_data = df_weekly_data.reset_index().melt(id_vars='Week Number', var_name='Day of Week', value_name='Percent Change')
    for ((week1, week2), similarity) in top_similarities.items():
        df_filtered = df_plot_data[(df_plot_data['Week Number'] == week1) | (df_plot_data['Week Number'] == week2)]
        fig = px.line(
            df_filtered,
            x='Day of Week',
            y='Percent Change',
            color='Week Number',
            title=f'Cosine Similarity: {similarity:.2f} (Week {week1} vs Week {week2})',
            labels={'Day of Week': 'Day of Week', 'Percent Change': 'Percent Change'},
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