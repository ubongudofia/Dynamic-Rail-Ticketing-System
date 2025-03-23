import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns




# Load the cleaned dataset
df = pd.read_csv("cleaned_dataset.csv")  # Make sure this matches the saved filename


# 🔹 1. Find Peak Train Timings

# Convert time columns to datetime.time format
df["Arrival time"] = pd.to_datetime(df["Arrival time"], format="%H:%M:%S", errors="coerce").dt.hour
df["Departure Time"] = pd.to_datetime(df["Departure Time"], format="%H:%M:%S", errors="coerce").dt.hour

# Plot peak arrival and departure times
plt.figure(figsize=(12,5))
sns.histplot(df["Arrival time"], bins=24, kde=True, color="blue", label="Arrival")
sns.histplot(df["Departure Time"], bins=24, kde=True, color="red", label="Departure")
plt.xlabel("Hour of the Day")
plt.ylabel("Number of Trains")
plt.title("Peak Train Arrival & Departure Times")
plt.legend()
plt.show()



# 🔹 2. Find Busiest Source & Destination Stations
# Top 10 busiest source stations
top_sources = df["Source Station"].value_counts().head(10)

# Top 10 busiest destination stations
top_destinations = df["Destination Station"].value_counts().head(10)

# Plot station trends
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

sns.barplot(x=top_sources.values, y=top_sources.index, ax=axes[0], palette="Blues_r")
axes[0].set_title("Top 10 Source Stations")
axes[0].set_xlabel("Number of Trains")

sns.barplot(x=top_destinations.values, y=top_destinations.index, ax=axes[1], palette="Reds_r")
axes[1].set_title("Top 10 Destination Stations")
axes[1].set_xlabel("Number of Trains")

plt.tight_layout()
plt.show()
