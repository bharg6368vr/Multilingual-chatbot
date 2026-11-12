@echo off
title Multilingual Chatbot Environment Setup
echo ==========================================================
echo  Multilingual Chatbot (Rasa + LangChain) Setup
echo ==========================================================

REM 1. Check for Python 3.10
py -3.10 --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [!] Python 3.10 not detected. Installing via winget...
    winget install Python.Python.3.10 --silent --accept-package-agreements --accept-source-agreements
    py -3.10 --version >nul 2>&1
    if %ERRORLEVEL% neq 0 (
        echo [ERROR] Python 3.10 installation failed or needs a shell restart.
        echo Please download and install Python 3.10 from https://www.python.org/downloads/release/python-31011/
        pause
        exit /b 1
    )
)

echo [OK] Python 3.10 verified.

REM 2. Create Virtual Environment
if not exist .venv (
    echo [*] Creating virtual environment (.venv)...
    py -3.10 -m venv .venv
    echo [OK] Virtual environment created.
) else (
    echo [OK] Virtual environment already exists.
)

REM 3. Install Requirements
echo [*] Upgrading pip and installing requirements.txt...
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\pip.exe install -r requirements.txt

REM 4. Copy .env
if not exist .env (
    copy .env.example .env
    echo [OK] Created .env file.
)

echo ==========================================================
echo Setup complete! You can now run train_bot.ps1 or start_all.bat
echo ==========================================================
pause
