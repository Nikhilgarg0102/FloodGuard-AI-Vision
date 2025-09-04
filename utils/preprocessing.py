import pandas as pd
import numpy as np

def load_data(file_path):
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None

def clean_data(df):
    df.fillna(0, inplace=True)
    for col in ["rainfall","inflow","release"]:
        df[col] = df[col].apply(lambda x: max(x,0))
    df["time"] = df["time"].astype(int)
    df["rainfall"] = df["rainfall"].astype(float)
    df["inflow"] = df["inflow"].astype(float)
    df["reservoir_level"] = df["reservoir_level"].astype(float)
    df["release"] = df["release"].astype(float)
    df["downstream_flow"] = df["downstream_flow"].astype(float)
    return df

def add_features(df):
    df["prev_inflow"] = df["inflow"].shift(1).fillna(0)
    df["rainfall_3h_avg"] = df["rainfall"].rolling(window=3, min_periods=1).mean()
    return df
