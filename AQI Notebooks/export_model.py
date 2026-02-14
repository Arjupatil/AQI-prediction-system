import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
import joblib
import os

# Define paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "..", "data", "cleaned_city_day.csv")
MODEL_OUTPUT_PATH = os.path.join(BASE_DIR, "..", "backend", "model.pkl")

print(f"Loading data from {DATA_PATH}...")
try:
    df = pd.read_csv(DATA_PATH)
except FileNotFoundError:
    print("Error: content file not found.")
    # Fallback to absolute path if needed, but relative should work
    exit(1)

# Feature selection based on notebook analysis
features = ['PM2.5', 'PM10', 'NO2', 'SO2', 'CO', 'O3', 'AQI']
print(f"Selecting features: {features}")

# Filter and Clean
df_ml = df[features]
initial_count = len(df_ml)
df_ml = df_ml.dropna()
print(f"Dropped {initial_count - len(df_ml)} rows with missing values.")

# Split X and y
X = df_ml.drop('AQI', axis=1)
y = df_ml['AQI']

# Train Model
print("Training XGBoost model...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
xgb_model = XGBRegressor(
    n_estimators=100, 
    max_depth=5, 
    learning_rate=0.1, 
    random_state=42, 
    objective='reg:squarederror'
)
xgb_model.fit(X_train, y_train)

# Evaluate (Minimal)
score = xgb_model.score(X_test, y_test)
print(f"Model R2 Score: {score:.4f}")

# Save Model
print(f"Saving model to {MODEL_OUTPUT_PATH}...")
joblib.dump(xgb_model, MODEL_OUTPUT_PATH)
print("Done.")
