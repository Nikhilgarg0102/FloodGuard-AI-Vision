import streamlit as st
import pandas as pd
import numpy as np
import time
from models.inflow_predictor import InflowPredictor
from models.optimizer import safe_release
from utils.preprocessing import load_data, clean_data, add_features
from face_auth import authenticate_user

# if not authenticate_user():
#     st.error("❌ Unauthorized Access")
#     st.stop()

# -----------------------------
# Face Authentication Session
# -----------------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:

    if authenticate_user():
        st.session_state.authenticated = True
    else:
        st.error("❌ Unauthorized User")
        st.stop()

# -----------------------------
# Page Setup
# -----------------------------
st.set_page_config(page_title="Smart Reservoir AI", layout="wide")
st.title("🌊 Smart Reservoir Dashboard")
st.markdown("Predict inflow and optimize water release to prevent floods.")

# -----------------------------
# Load and preprocess data
# -----------------------------
df = load_data("data/simulated_data.csv")
df = clean_data(df)
df = add_features(df)

# Train AI predictor
predictor = InflowPredictor()
predictor.train(df[["rainfall","prev_inflow","rainfall_3h_avg"]], df["inflow"])

# -----------------------------
# Historical Data Chart
# -----------------------------
st.subheader("📈 Historical Reservoir & Rainfall Data")
st.line_chart(df.set_index("time")[["rainfall", "reservoir_level"]])

# -----------------------------
# Future Rainfall Slider
# -----------------------------
future_rainfall = st.slider("🌧️ Adjust Future Rainfall (mm)", 0, 200, 50)

# -----------------------------
# Predicted Metrics based on slider
# -----------------------------
# Reset last inflow and rolling average for accurate prediction
# Reset inflow to realistic base for prediction
last_inflow = 10          # assume base inflow = 10 m3/s
last_rain_avg = 10         # assume base rainfall avg = 10 mm

# Simple inflow estimation based on rainfall
predicted_inflow = future_rainfall * 0.5  # scale factor to convert mm → m3/s

# Predicted reservoir level
scale_factor = 0.001  # smaller to prevent immediate high risk
current_level = df["reservoir_level"].iloc[-1]
release = safe_release(current_level, predicted_inflow)
predicted_level = current_level + (predicted_inflow - release) * 0.02
predicted_level = max(0, min(100, predicted_level))

# Determine risk
if predicted_inflow > 90:
    risk_status = "🚨 High Risk"
elif predicted_inflow > 75:
    risk_status = "⚠️ Medium Risk"
else:
    risk_status = "✅ Safe"

# Display metrics
st.subheader("🔮 Predicted Metrics for Adjusted Rainfall")
st.metric("Predicted Reservoir Level (m)", f"{predicted_level:.2f}")
st.metric("Predicted Inflow (m³/s)", f"{predicted_inflow:.2f}")
st.metric("Predicted Risk Status", risk_status)

# -----------------------------
# Run Live Simulation Button
# -----------------------------


# -----------------------------
# Run Live Simulation Button
# -----------------------------
if st.button("▶️ Run Live Simulation"):

    st.subheader("🚀 Running Live Reservoir Simulation")

    timesteps = 20
    sim_levels = []
    risk_list = []

    # start reservoir at medium level
    current_level = 50

    # simulation loop
    for t in range(timesteps):

        # rainfall changes dynamically
        dynamic_rainfall = future_rainfall + np.random.randint(-10, 10)

        # prevent negative rainfall
        dynamic_rainfall = max(0, dynamic_rainfall)

        # inflow calculation
        inflow = dynamic_rainfall * 0.6 + np.random.randint(0, 10)

        # release calculation
        release = inflow * 0.4

        # reservoir level update
        current_level += (inflow - release) * 0.2

        # keep between 0 and 100
        current_level = max(0, min(100, current_level))

        # store level
        sim_levels.append(round(current_level, 2))

        # risk calculation
        if current_level > 90:
            risk_list.append("🚨 High Risk")
        elif current_level > 75:
            risk_list.append("⚠️ Medium Risk")
        else:
            risk_list.append("✅ Safe")

        # animation delay
        time.sleep(0.2)

    # simulation chart
    sim_chart_df = pd.DataFrame({
        "Time Step": range(1, timesteps + 1),
        "Reservoir Level": sim_levels
    })

    st.subheader("📊 Reservoir Level Simulation")
    st.line_chart(sim_chart_df.set_index("Time Step"))

    # simulation table
    sim_df = pd.DataFrame({
        "Time Step": range(1, timesteps + 1),
        "Reservoir Level": sim_levels,
        "Risk": risk_list
    })

    st.subheader("🛑 Simulation Risk Status Over Time")
    st.table(sim_df)


# if st.button("▶️ Run Live Simulation"):

#     st.subheader("🚀 Running Live Reservoir Simulation")
#     timesteps = 20
#     sim_levels = []
#     risk_list = []
#     #current_level = df["reservoir_level"].iloc[-1]
#     current_level = 50

#     # chart = st.line_chart(
#     # pd.DataFrame({"Reservoir Level": []}),
#     # height=300)
#     # chart = st.line_chart([], width=0, height=300)  # initialize empty chart
    
#     for t in range(timesteps):
        
#     # change rainfall slightly at every timestep
#         dynamic_rainfall = future_rainfall + np.random.randint(-10, 10)

#         # avoid negative rainfall
#         dynamic_rainfall = max(0, dynamic_rainfall)

#         inflow = dynamic_rainfall * 0.6 + np.random.randint(0, 10)
   
#         # # update history for next timestep
#         ### last_inflow = inflow
#         ### last_rain_avg = (last_rain_avg * 2 + dynamic_rainfall) / 3

#         # calculate release based on this timestep inflow
#         release = inflow * 0.4

#         # update reservoir level
#         current_level += (inflow - release) * 0.2
#         current_level = max(0, min(100, current_level))
#         sim_levels.append(current_level, 2)

#         # calculate risk
#         if current_level > 90:
#             risk_list.append("🚨 High Risk")
#         elif current_level > 75:
#             risk_list.append("⚠️ Medium Risk")
#         else:
#             risk_list.append("✅ Safe")

#         # update live chart
#         ### chart.add_rows(pd.DataFrame({"Reservoir Level": [current_level]}))
#         time.sleep(0.3)  # live animation effect

#         ### sim_levels.append(round(current_level, 2))

#     # chart after simulation
#     sim_chart_df = pd.DataFrame({
#         "Time Step": range(1, timesteps + 1),
#         "Reservoir Level": sim_levels
#     })

#     st.line_chart(sim_chart_df.set_index("Time Step"))

#     # # Show simulation table
#     # sim_df = pd.DataFrame({
#     #     "Time Step": range(1, timesteps + 1),
#     #     "Reservoir Level": sim_levels,
#     #     "Risk": risk_list
    
#     st.subheader("🛑 Simulation Risk Status Over Time")
#     st.table(sim_df)
