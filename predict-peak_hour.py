import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LinearRegression
import joblib


df = pd.read_csv("cleaned_dataset.csv")

# Convert 'Arrival time' to datetime and extract hour
df["Arrival Hour"] = pd.to_datetime(df["Arrival time"], errors="coerce").dt.hour

# Convert 'Arrival Hour' to integer type (to fix grouping issue)
df["Arrival Hour"] = df["Arrival Hour"].astype("Int64")

# Drop NaN values in 'Arrival Hour' (if any exist)
df = df.dropna(subset=["Arrival Hour"])

# Debugging: Check if column exists
print("Columns in dataset:", df.columns)

# Group by 'Arrival Hour' and count the number of trains
hourly_data = df.groupby("Arrival Hour")["Train No"].count().reset_index()

# Display processed data
print(hourly_data.head())



# Count train frequency per hour
hourly_data = df.groupby("Arrival Hour")["Train No"].count().reset_index()
X = hourly_data[["Arrival Hour"]]
y = hourly_data["Train No"]

# Train Model
peak_model = GradientBoostingRegressor()
peak_model.fit(X, y)

# Predict for next day
future_hours = pd.DataFrame({"Arrival Hour": list(range(24))})
future_trains = peak_model.predict(future_hours)

# Show Peak Predictions
import matplotlib.pyplot as plt

plt.plot(future_hours["Arrival Hour"], future_trains, marker="o", linestyle="-", color="green")
plt.xlabel("Hour of the Day")
plt.ylabel("Predicted Train Count")
plt.title("Predicted Peak Train Hours")
plt.show()




# Save models
joblib.dump(peak_model, "peak_hour_model.pkl")