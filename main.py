# Main pipeline to generate data, predict, optimize, and launch dashboard
from utils.data_simulator import generate_simulated_data

# Step 1: generate simulated data
generate_simulated_data(n=100)

# Step 2: launch Streamlit dashboard
import subprocess
subprocess.run(["python","-m","streamlit","run","dashboard/app.py"])
