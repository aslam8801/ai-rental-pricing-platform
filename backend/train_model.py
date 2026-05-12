import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import joblib

# Load dataset
df = pd.read_csv("properties.csv")

# Features (inputs)
X = df[[
    "sqft",
    "bedrooms",
    "school_score",
    "noise"
]]

# Target (output)
y = df["rent"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Create model
model = LinearRegression()

# Train model
model.fit(X_train, y_train)

# Predictions
predictions = model.predict(X_test)

# Evaluate
error = mean_absolute_error(y_test, predictions)

print("Model trained successfully!")
print("Mean Absolute Error:", error)

# Save model
joblib.dump(model, "rent_model.pkl")

print("Model saved as rent_model.pkl")