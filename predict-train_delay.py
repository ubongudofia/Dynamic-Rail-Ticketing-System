import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LinearRegression
import joblib



df = pd.read_csv("cleaned_dataset.csv")

# Feature Engineering
df["Arrival Hour"] = pd.to_datetime(df["Arrival time"], format="%H:%M:%S", errors="coerce").dt.hour
df["Departure Hour"] = pd.to_datetime(df["Departure Time"], format="%H:%M:%S", errors="coerce").dt.hour

# Simulated delay column (for training) – replace with real delay data if available
import numpy as np
df["Delayed"] = np.random.choice([0, 1], size=len(df), p=[0.8, 0.2])  # 20% chance of delay

# Select Features & Target
X = df[["Train No", "Source Station", "Destination Station", "Arrival Hour", "Departure Hour"]]
y = df["Delayed"]

# Convert categorical variables to numbers
X = pd.get_dummies(X, columns=["Source Station", "Destination Station"])

# Split Data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Model
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

# Predict & Evaluate
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"🔹 Train Delay Prediction Accuracy: {accuracy * 100:.2f}%")



# Save models to disk
joblib.dump(model, "train_delay_model.pkl")

print("✅ Models saved successfully!")