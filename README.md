# 🌬️ Air Quality Index (AQI) Prediction System

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-v0.68.0+-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An AI-powered web application that predicts Air Quality Index (AQI) based on pollutant concentrations. The system uses Machine Learning to analyze input data and provides real-time visualizations for better environmental insights.

## 🚀 Features

- **AI-Powered Prediction**: Accurate AQI estimation using a trained Random Forest model.
- **Comprehensive City Support**: Interactive dropdown with data for 26+ major Indian cities.
- **Real-time Visualizations**:
  - **Pollutant Breakdown**: Bar chart showing concentrations of PM2.5, PM10, NO2, SO2, CO, and O3.
  - **Historical Trends**: Line chart showing the AQI history for the selected city.
- **Modern UI/UX**: Premium dark-themed interface with glassmorphism effects and responsive design.
- **Data Logging**: All predictions are automatically logged to a CSV file for future analysis.

## 🛠️ Tech Stack

- **Frontend**: HTML5, Vanilla CSS3, JavaScript (ES6+), Chart.js
- **Backend**: Python 3.x, FastAPI, Uvicorn
- **Machine Learning**: Scikit-Learn, Pandas, Joblib
- **Environment Management**: Anaconda/Conda

## 📂 Project Structure

```text
AQI Prediction/
├── frontend/             # Web interface (HTML, CSS, JS)
├── backend/              # FastAPI server and ML model
├── data/                 # Datasets (CSV files)
├── AQI Notebooks/        # Jupyter notebooks for model training
├── start_app.bat         # One-click launcher script
└── README.md             # Project documentation
```

## ⚙️ Installation & Setup

1. **Clone the Project**:
   ```bash
   git clone https://github.com/Arjupatil/AQI-prediction-system.git
   cd "AQI Prediction"
   ```

2. **Run the Application**:
   Simply double-click the `start_app.bat` file. This script will:
   - Check and activate your Python environment.
   - Install required dependencies.
   - Export the latest ML model if needed.
   - Start the backend server.

3. **Access the App**:
   Open your browser and go to:
   [http://127.0.0.1:8000](http://127.0.0.1:8000)

## 📊 How It Works

1. **Input**: Select a city and enter pollutant values (PM2.5, PM10, etc.).
2. **Analysis**: The FastAPI backend sends data to the pre-trained ML model.
3. **Output**: The system returns the predicted AQI value and category (e.g., Good, Moderate, Severe).
4. **Visualize**: Charts are instantly rendered to show the pollutant distribution and history.

## 👤 Author

**Arju Patil**
- 📧 Email: [arju2912003@gmail.com](mailto:arju2912003@gmail.com)
- 🐙 GitHub: [@Arjupatil](https://github.com/Arjupatil)

## 📝 License

This project is licensed under the MIT License - see the LICENSE file (or the footer of this README) for details. Developed for educational and research purposes in air quality analysis.
