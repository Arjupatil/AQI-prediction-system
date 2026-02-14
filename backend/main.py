from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import joblib
import os
from datetime import datetime

# Initialize App
app = FastAPI()

# CORS (Allow Frontend to connect)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")
# Use the known path to the CSV file
DATA_PATH = os.path.join(BASE_DIR, "..", "AQI_Final_Predictions_For_PowerBI.csv")

# Load Model
model = None
try:
    model = joblib.load(MODEL_PATH)
    print("Model loaded successfully.")
except Exception as e:
    print(f"Warning: Could not load model from {MODEL_PATH}. Prediction will fail until model is exported.")
    print(e)

# Input Schema
class AQIInput(BaseModel):
    city: str
    pm2_5: float
    pm10: float
    no2: float
    so2: float
    co: float
    o3: float



@app.post("/predict")
def predict_aqi(data: AQIInput):
    if model is None:
        raise HTTPException(status_code=500, detail="Model is not loaded. Please run export_model.py first.")

    # Prepare features: ['PM2.5', 'PM10', 'NO2', 'SO2', 'CO', 'O3']
    features = [[data.pm2_5, data.pm10, data.no2, data.so2, data.co, data.o3]]
    
    try:
        prediction = float(model.predict(features)[0])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

    # Update CSV
    try:
        # Determine AQI Category (Simple logic based on Indian standards, can be improved)
        category = "Unknown"
        if prediction <= 50: category = "Good"
        elif prediction <= 100: category = "Satisfactory"
        elif prediction <= 200: category = "Moderate"
        elif prediction <= 300: category = "Poor"
        elif prediction <= 400: category = "Very Poor"
        else: category = "Severe"

        # Create new row
        new_row = {
            "City": data.city,
            "Date": datetime.now().strftime("%Y-%m-%d"),
            "PM2.5": data.pm2_5,
            "PM10": data.pm10,
            "NO2": data.no2,
            "SO2": data.so2,
            "CO": data.co,
            "O3": data.o3,
            "AQI": prediction, # Using predicted as actual for simple logging or keep blank? 
            # Notebook target was AQI. Let's assume we log the prediction as the 'Predicted_AQI' if the CSV has that structure.
            # Let's check CSV structure again.
            # CSV header: City,Date,PM2.5,PM10,NO2,SO2,CO,O3,AQI,Predicted_AQI,AQI_Category
            "AQI": prediction, # Placeholder handling
            "Predicted_AQI": prediction,
            "AQI_Category": category
        }
        
        # Append to CSV
        # Note: If file doesn't exist, this creates it. If it does, it appends.
        df = pd.DataFrame([new_row])
        # Check if file exists to determine header
        header = not os.path.exists(DATA_PATH)
        df.to_csv(DATA_PATH, mode='a', header=header, index=False)
        
    except Exception as e:
        # Don't fail the request if saving data fails, but log it
        print(f"Error saving to CSV: {e}")
        # raise HTTPException(status_code=500, detail="Error updating database")

    return {
        "aqi": prediction,
        "category": category,
        "message": "Prediction successful and data logged."
    }

@app.get("/cities")
def get_cities():
    all_cities = set()
    print("DEBUG: Fetching cities...")
    
    # Files to check for cities
    data_files = [
        os.path.join(BASE_DIR, "..", "data", "cleaned_city_day.csv"),
        os.path.join(BASE_DIR, "..", "data", "city_day.csv"),
        DATA_PATH # The history/output CSV
    ]
    
    for file_path in data_files:
        print(f"DEBUG: Checking file: {file_path}")
        if os.path.exists(file_path):
            try:
                # Read only the 'City' column if it exists
                df = pd.read_csv(file_path, usecols=["City"])
                cities = df["City"].dropna().unique().astype(str).tolist()
                print(f"DEBUG: Found {len(cities)} cities in {os.path.basename(file_path)}")
                all_cities.update(cities)
            except Exception as e:
                print(f"DEBUG: Error loading cities from {file_path}: {e}")
    
    if not all_cities:
        print("DEBUG: No cities found in files, using fallback.")
        return ["Ahmedabad", "Bengaluru", "Chennai", "Delhi", "Hyderabad", "Kolkata", "Mumbai"]
    
    result = sorted(list(all_cities))
    print(f"DEBUG: Returning {len(result)} unique cities.")
    return result

@app.get("/history")
def get_history():
    if not os.path.exists(DATA_PATH):
        return []
    
    try:
        df = pd.read_csv(DATA_PATH)
        # return last 20 records, reversed (newest first)
        last_20 = df.tail(20).iloc[::-1].fillna(0).to_dict(orient="records")
        return last_20
    except Exception as e:
        print(f"Error reading history: {e}")
        return []

# Serve Static Files (Frontend)
# Mount at root MUST be after specific API routes to avoid blocking them
app.mount("/", StaticFiles(directory=os.path.join(BASE_DIR, "..", "frontend"), html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
