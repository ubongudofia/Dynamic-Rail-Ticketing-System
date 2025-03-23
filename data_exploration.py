import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns




# Load the cleaned dataset
df = pd.read_csv("cleaned_dataset.csv")  # Make sure this matches the saved filename



# General info
print("\n🔹 Dataset Overview:")
print(df.info())

# Summary statistics
print("\n🔹 Summary Statistics:")
print(df.describe(include="all"))

# Check missing values
print("\n🔹 Missing Values:")
print(df.isnull().sum())

# Visualizing Missing Data
plt.figure(figsize=(8, 5))
sns.heatmap(df.isnull(), cmap="viridis", cbar=False, yticklabels=False)
plt.title("Missing Data Heatmap")
plt.show()

# Value counts of categorical features
print("\n🔹 Unique Source Stations:\n", df["Source Station"].value_counts())
print("\n🔹 Unique Destination Stations:\n", df["Destination Station"].value_counts())

# Plot Distribution of Available Seats
plt.figure(figsize=(8, 5))
sns.histplot(df["Available Seats"], bins=20, kde=True, color="blue")
plt.title("Distribution of Available Seats")
plt.xlabel("Available Seats")
plt.ylabel("Count")
plt.show()

# Plot Train Frequency
plt.figure(figsize=(8, 5))
sns.countplot(y=df["Train No"], order=df["Train No"].value_counts().index, palette="coolwarm")
plt.title("Train Frequency")
plt.xlabel("Count")
plt.ylabel("Train No")
plt.show()

# Convert time columns to datetime.time
df["Arrival time"] = pd.to_datetime(df["Arrival time"], format="%H:%M:%S", errors="coerce").dt.time
df["Departure Time"] = pd.to_datetime(df["Departure Time"], format="%H:%M:%S", errors="coerce").dt.time

# Display first few rows after conversion
print("\n🔹 Final Preview After Time Conversion:")
print(df.head())
