import pandas as pd
import joblib

from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

# Load dataset
df = pd.read_csv("properties.csv")

# Features
X = df[[
    "sqft",
    "bedrooms",
    "school_score",
    "noise"
]]

# Target
y = df["rent"]

# Train/Test split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Create XGBoost model
model = XGBRegressor(
    n_estimators=100,
    learning_rate=0.1,
    max_depth=5,
    random_state=42
)

# Train model
model.fit(X_train, y_train)

# Predict
predictions = model.predict(X_test)

# Evaluate
error = mean_absolute_error(y_test, predictions)

print("XGBoost Model Trained!")
print("Mean Absolute Error:", error)

# Save model
joblib.dump(model, "xgboost_rent_model.pkl")

print("Model saved successfully!")