@echo off
title Multilingual Chatbot Launcher
echo ========================================================
echo Starting Multilingual Chatbot (Rasa + LangChain)
echo ========================================================

set "PROJECT_DIR=%~dp0"
set "PYTHON_EXE=%PROJECT_DIR%.venv\Scripts\python.exe"

if not exist "%PYTHON_EXE%" (
    echo [ERROR] Virtual environment python was not found at: %PYTHON_EXE%
    echo Please make sure .venv exists.
    pause
    exit /b 1
)

echo 1. Launching Action Server on Port 5055...
start "1. Rasa Action Server (Port 5055)" cmd /k "cd /d "%PROJECT_DIR%action_server" && "%PYTHON_EXE%" -m rasa_sdk.endpoint --actions actions --port 5055"

timeout /t 3 /nobreak >nul

echo 2. Launching Rasa Core Server on Port 5005...
start "2. Rasa Core Server (Port 5005)" cmd /k "cd /d "%PROJECT_DIR%rasa_bot" && "%PYTHON_EXE%" -m rasa run --enable-api --cors * --port 5005 --endpoints endpoints.yml --credentials credentials.yml"

timeout /t 5 /nobreak >nul

echo 3. Launching Streamlit Web UI on Port 8501...
start "3. Streamlit Web Interface (Port 8501)" cmd /k "cd /d "%PROJECT_DIR%" && "%PYTHON_EXE%" -m streamlit run frontend\app.py --server.port 8501"

echo ========================================================
echo All 3 services are launching in separate windows!
echo Please wait 15 seconds for the models to load, then open:
echo http://localhost:8501
echo ========================================================
