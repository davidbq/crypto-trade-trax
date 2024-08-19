import pandas as pd

def store_data(df: pd.DataFrame, file_path: str) -> None:
    df.to_csv(file_path, index=True, encoding='utf-8')
