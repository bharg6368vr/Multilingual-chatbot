# Multilingual Chatbot Environment Setup Script (Windows PowerShell)

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " Multilingual Chatbot (Rasa + LangChain) Setup" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Check for Python 3.10
$pythonFound = $false
$verCheck = & py -3.10 --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] Found Python 3.10: $verCheck" -ForegroundColor Green
    $pythonFound = $true
} else {
    Write-Host "[!] Python 3.10 not found. Attempting installation via winget..." -ForegroundColor Yellow
    winget install Python.Python.3.10 --silent --accept-package-agreements --accept-source-agreements
    $verCheck = & py -3.10 --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[OK] Python 3.10 installed successfully: $verCheck" -ForegroundColor Green
        $pythonFound = $true
    }
}

if (-not $pythonFound) {
    Write-Host "[ERROR] Could not automatically locate or install Python 3.10." -ForegroundColor Red
    Write-Host "Please install Python 3.10 manually from python.org or via: winget install Python.Python.3.10" -ForegroundColor Red
    Exit 1
}

# 2. Create Virtual Environment
$venvPath = ".\.venv"
if (-not (Test-Path $venvPath)) {
    Write-Host "[*] Creating virtual environment at $venvPath using Python 3.10..." -ForegroundColor Cyan
    & py -3.10 -m venv $venvPath
    Write-Host "[OK] Virtual environment created." -ForegroundColor Green
} else {
    Write-Host "[OK] Virtual environment already exists." -ForegroundColor Green
}

# 3. Upgrade Pip and Install Dependencies
Write-Host "[*] Upgrading pip and installing dependencies from requirements.txt..." -ForegroundColor Cyan
& "$venvPath\Scripts\python.exe" -m pip install --upgrade pip
& "$venvPath\Scripts\pip.exe" install -r requirements.txt

# 4. Copy .env if not exists
if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "[OK] Created .env file from .env.example." -ForegroundColor Green
}

Write-Host "`nSetup complete! You can now train the bot using: .\train_bot.ps1" -ForegroundColor Green
