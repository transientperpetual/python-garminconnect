import pandas as pd
import plotly.express as px
import json
import glob
import os

# Path to your JSON files (update this if your folder is different)
data_folder = "data/stats/*.json"
data_list = []

# Load all JSON files
print("Loading JSON files...")
try:
    for file in glob.glob(data_folder):
        with open(file, 'r') as f:
            data = json.load(f)
            data_list.append({
                "calendarDate": data["calendarDate"],
                "totalSteps": data["totalSteps"],
                "bodyBatteryHighestValue": data["bodyBatteryHighestValue"],
                "averageStressLevel": data["averageStressLevel"],
                "totalKilocalories": data["totalKilocalories"],
                "restingHeartRate": data["restingHeartRate"],
                "avgWakingRespirationValue": data["avgWakingRespirationValue"],
                "bodyBatteryDrainedValue": data["bodyBatteryDrainedValue"],
                "bmrKilocalories": data["bmrKilocalories"],
                "measurableAsleepDuration": data["measurableAsleepDuration"] / 3600  # Convert to hours
            })
    print(f"Successfully loaded {len(data_list)} files.")
except Exception as e:
    print(f"Error loading files: {e}")
    exit()

# Create a DataFrame
if not data_list:
    print("No data loaded. Check your file path or JSON structure.")
    exit()

df = pd.DataFrame(data_list)
df["calendarDate"] = pd.to_datetime(df["calendarDate"])  # Convert to datetime
df = df.sort_values("calendarDate")  # Sort by date

# Create output directory for plots
output_dir = "plots"
os.makedirs(output_dir, exist_ok=True)

# Plot Total Steps
fig_steps = px.line(df, x="calendarDate", y="totalSteps", title="Daily Steps Over Time")
fig_steps.write_html(os.path.join(output_dir, "steps_plot.html"))
print("Steps plot saved as plots/steps_plot.html")

# Plot Body Battery
fig_bb = px.line(df, x="calendarDate", y="bodyBatteryHighestValue", title="Daily Body Battery (Highest Value)")
fig_bb.write_html(os.path.join(output_dir, "body_battery_plot.html"))
print("Body Battery plot saved as plots/body_battery_plot.html")

# Plot Average Stress Level
fig_stress = px.line(df, x="calendarDate", y="averageStressLevel", title="Daily Average Stress Level")
fig_stress.write_html(os.path.join(output_dir, "stress_plot.html"))
print("Stress plot saved as plots/stress_plot.html")

# Plot Total Kilocalories
fig_calories = px.line(df, x="calendarDate", y="totalKilocalories", title="Daily Total Kilocalories")
fig_calories.write_html(os.path.join(output_dir, "calories_plot.html"))
print("Calories plot saved as plots/calories_plot.html")

# Plot Resting Heart Rate
fig_hr = px.line(df, x="calendarDate", y="restingHeartRate", title="Daily Resting Heart Rate")
fig_hr.write_html(os.path.join(output_dir, "heart_rate_plot.html"))
print("Heart Rate plot saved as plots/heart_rate_plot.html")

# Plot Sleep Duration
fig_sleep = px.line(df, x="calendarDate", y="measurableAsleepDuration", title="Daily Sleep Duration (Hours)")
fig_sleep.write_html(os.path.join(output_dir, "sleep_plot.html"))
print("Sleep plot saved as plots/sleep_plot.html")

# Plot Respiration Rate
fig_sleep = px.line(df, x="calendarDate", y="avgWakingRespirationValue", title="Daily Respiration Rate")
fig_sleep.write_html(os.path.join(output_dir, "respiration_plot.html"))
print("Respiration plot saved as plots/respiration_plot.html")

# Plot BMR Calories
fig_sleep = px.line(df, x="calendarDate", y="bmrKilocalories", title="Daily bmrKilocalories")
fig_sleep.write_html(os.path.join(output_dir, "bmrKilocalories_plot.html"))
print("bmrKilocalories plot saved as plotsbmrKilocalories_plot.html")
