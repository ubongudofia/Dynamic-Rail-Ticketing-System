import pandas as pd
import numpy as np


# Load the cleaned dataset
df = pd.read_csv("cleaned_train_data.csv")  # Make sure this matches the saved filename


# DATA EXPLORATION
# Convert time columns
df["Arrival time"] = pd.to_datetime(df["Arrival time"], format="%H:%M:%S", errors="coerce").dt.time
df["Departure Time"] = pd.to_datetime(df["Departure Time"], format="%H:%M:%S", errors="coerce").dt.time

# Count 00:00:00 occurrences
invalid_arrival = (df["Arrival time"] == pd.to_datetime("00:00:00").time()).sum()
invalid_departure = (df["Departure Time"] == pd.to_datetime("00:00:00").time()).sum()

print(f"🔹 Invalid Arrival Times: {invalid_arrival}")
print(f"🔹 Invalid Departure Times: {invalid_departure}")

# Replace "00:00:00" with NaN
df["Arrival time"] = df["Arrival time"].apply(lambda x: np.nan if x == pd.to_datetime("00:00:00").time() else x)
df["Departure Time"] = df["Departure Time"].apply(lambda x: np.nan if x == pd.to_datetime("00:00:00").time() else x)

# Verify again
print("\nUpdated Data Types:\n", df.dtypes)
print("\nPreview of Cleaned Data:\n", df.head())




# Save cleaned data
df.to_csv("cleaned_dataset.csv", index=False)

