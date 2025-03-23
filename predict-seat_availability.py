import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LinearRegression
import joblib




df = pd.read_csv("cleaned_dataset.csv")


# Ensure the time columns exist
if "Arrival time" in df.columns and "Departure Time" in df.columns:
    # Convert time to datetime format and extract the hour
    df["Arrival Hour"] = pd.to_datetime(df["Arrival time"], format="%H:%M:%S", errors="coerce").dt.hour
    df["Departure Hour"] = pd.to_datetime(df["Departure Time"], format="%H:%M:%S", errors="coerce").dt.hour

else:
    print("Error: 'Arrival time' or 'Departure Time' column is missing.")

# Drop rows where the extracted hour is NaN
df = df.dropna(subset=["Arrival Hour", "Departure Hour"])

# Select features for prediction
X = df[["Train No", "Source Station", "Destination Station", "Arrival Hour", "Departure Hour"]]

# Print for verification
print(X.head())


# Select Features & Target
X = df[["Train No", "Source Station", "Destination Station", "Arrival Hour", "Departure Hour"]]
y = df["Available Seats"]

# Convert categorical variables
X = pd.get_dummies(X, columns=["Source Station", "Destination Station"])

# Split Data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Model
seat_model = LinearRegression()
seat_model.fit(X_train, y_train)

# Predict & Evaluate
y_pred = seat_model.predict(X_test)
print(f"🔹 Predicted Seat Availability (sample): {y_pred[:5]}")






# Save models
joblib.dump(seat_model, "seat_availability_model.pkl")