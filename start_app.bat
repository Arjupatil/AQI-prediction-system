@echo off
echo ==========================================
echo      AQI Prediction App Launcher
echo ==========================================

rem Check for Python and activate Conda if needed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    if exist "C:\anaconda\Scripts\activate.bat" (
        echo [Auto-Fix] Activating Anaconda Environment...
        call C:\anaconda\Scripts\activate.bat
    )
)

echo [1/3] Installing Dependencies...
pip install -r backend/requirements.txt
if %errorlevel% neq 0 (
    echo Warning: pip failed. Trying 'py -m pip'...
    py -m pip install -r backend/requirements.txt
)

echo.
echo [2/3] Exporting Machine Learning Model...
python "AQI Notebooks/export_model.py"
if %errorlevel% neq 0 (
    echo Warning: python failed. Trying 'py'...
    py "AQI Notebooks/export_model.py"
)

echo.
echo [3/3] Starting Backend Server...
echo Please leave this window OPEN.
echo Open 'http://127.0.0.1:8000' in your browser to use the app.
echo.
python backend/main.py
if %errorlevel% neq 0 (
    echo Retrying with 'py'...
    py backend/main.py
)

pause
