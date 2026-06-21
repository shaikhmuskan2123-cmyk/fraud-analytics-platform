import pandas as pd
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load dataset
df = pd.read_csv("data/transactions.csv")

print("Dataset Loaded Successfully")
print(df.head())

# Features and Target
X = df.drop("fraud", axis=1)
y = df["fraud"]

# Scaling
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled,
    y,
    test_size=0.2,
    random_state=42
)

# Model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

# Train
model.fit(X_train, y_train)

# Evaluate
predictions = model.predict(X_test)

accuracy = accuracy_score(
    y_test,
    predictions
)

print(f"\nAccuracy: {accuracy:.2f}")

# Create models folder
os.makedirs("models", exist_ok=True)

# Save model and scaler
joblib.dump(
    model,
    "models/fraud_model.pkl"
)

joblib.dump(
    scaler,
    "models/scaler.pkl"
)

print("\nModel saved successfully!")
print("Scaler saved successfully!")