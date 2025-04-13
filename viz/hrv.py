import pandas as pd
import plotly.express as px
import json
import glob
import os

# Path to your JSON files (update this if your folder is different)
data_folder = "data/hrv/*.json"
data_list = []

# Load all JSON files
print("Loading JSON files...")
for file in glob.glob(data_folder):
    try:
        with open(file, 'r') as f:
            data = json.load(f)
            # Check if hrvSummary exists and has required keys
            if "hrvSummary" in data and data["hrvSummary"] is not None:
                hrv_summary = data["hrvSummary"]
                if all(key in hrv_summary for key in ["calendarDate", "weeklyAvg", "lastNightAvg"]):
                    print(f"DATA (lastNightAvg): {hrv_summary['lastNightAvg']} for file {file}")
                    data_list.append({
                        "calendarDate": hrv_summary["calendarDate"],
                        "weeklyAvg": hrv_summary["weeklyAvg"],
                        "lastNightAvg": hrv_summary["lastNightAvg"],
                    })
                else:
                    print(f"Skipping {file}: Missing required keys in hrvSummary")
            else:
                print(f"Skipping {file}: hrvSummary is missing or None")
    except json.JSONDecodeError:
        print(f"Skipping {file}: Invalid JSON format")
    except Exception as e:
        print(f"Error processing {file}: {e}")

# Check if any data was loaded
if not data_list:
    print("No valid data loaded. Check your files or JSON structure.")
    exit()

df = pd.DataFrame(data_list)
df["calendarDate"] = pd.to_datetime(df["calendarDate"])  # Convert to datetime
df = df.sort_values("calendarDate")  # Sort by date

# Create output directory for plots
output_dir = "hrv_plots"
os.makedirs(output_dir, exist_ok=True)

# Plot Total Steps
fig_steps = px.line(df, x="calendarDate", y="weeklyAvg", title="Weekly avg daily score")
fig_steps.write_html(os.path.join(output_dir, "wavghrv_plot.html"))
print("weeklyAvg plot saved as hrv_plots/wavghrv_plot.html")

# Plot Body Battery
fig_bb = px.line(df, x="calendarDate", y="lastNightAvg", title="lastNightAvg")
fig_bb.write_html(os.path.join(output_dir, "lastNightAvg_plot.html"))
print("lastNightAvg plot saved as hrv_plots/lastNightAvg_plot.html")

