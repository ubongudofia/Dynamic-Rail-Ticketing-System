import pandas as pd
import kagglehub
from kagglehub import KaggleDatasetAdapter


# Set the path to the file you'd like to load
file_path = "train-dataset.csv"

# Load the dataset
df = pd.read_csv(file_path)  # Replace with your actual filename

# Display the first few rows
# print(df.head())


# # Check basic info about the dataset
# print(df.info())

# # Show column names
# print(df.columns)

# # Check for missing values
# print(df.isnull().sum())

# DATA CLEAN FOR TRAIN HISTORICAL DATASETS

# ------------------------------------------------------------------------
# 1. Drop unnecessary columns
df.drop(columns=["Unnamed: 0", "primary_key"], inplace=True)

# Display the first few rows
print(df.head())

# --------------------------------------------------------------------------

# ----------------------------------------------------------------------

# 2  Check for Missing Values
print(df.isnull().sum())
# --------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# 3. Convert Time Columns to Proper Format and # 5. Pandas to parse only the time without adding a date

# Convert time columns to proper datetime format
df["Arrival time"] = pd.to_datetime(df["Arrival time"], format="%H:%M:%S").dt.time
df["Departure Time"] = pd.to_datetime(df["Departure Time"], format="%H:%M:%S").dt.time

# # Display the updated types
print(df.dtypes)


print(df.head())
# -----------------------------------------------------------------------------

# 4. Handle the dirty_bit Column

# Keep only clean records
df = df[df["dirty_bit"] == 0]
df.drop(columns=["dirty_bit"], inplace=True)  # Remove the column after filtering

print(df.head())  # Check if it's cleaned

# ---------------------------------------------------------------------------------


# SAVE CLEAN DATASET

# Step 1: Save Your Cleaned Data
df.to_csv("cleaned_train_data.csv", index=False)







# 🔥 Next Step: Data Exploration

