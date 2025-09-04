import pandas as pd
import numpy as np
import os

def generate_simulated_data(n=100, save_path="data/simulated_data.csv"):
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    level = 50
    data = []

    for t in range(n):
        rainfall = np.random.randint(0, 200)                   # mm
        inflow = rainfall * np.random.uniform(0.5, 1.5)       # inflow depends on rainfall
        release = 0
        if level > 95:
            release = inflow * 0.8
        elif level > 85:
            release = inflow * 0.5
        elif level > 70:
            release = inflow * 0.2
        level += (inflow - release) / 100                     # update water level
        downstream_flow = inflow + release
        data.append([t, rainfall, inflow, level, release, downstream_flow])

    df = pd.DataFrame(data, columns=[
        "time","rainfall","inflow","reservoir_level","release","downstream_flow"
    ])
    df.to_csv(save_path, index=False)
    print(f"Simulated data saved to {save_path}")

if __name__ == "__main__":
    generate_simulated_data()
