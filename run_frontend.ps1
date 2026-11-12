# Run Streamlit Frontend
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " Starting Multilingual Web Interface on Port 8501" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

$projectRoot = $PSScriptRoot
if (-not $projectRoot) { $projectRoot = (Get-Location).Path }
$pythonExe = Join-Path $projectRoot ".venv\Scripts\python.exe"

if (-not (Test-Path $pythonExe)) {
    Write-Host "[ERROR] Virtual environment (.venv) was not found!" -ForegroundColor Red
    Write-Host "Please run .\setup_env.bat first to set up .venv" -ForegroundColor Yellow
    Exit 1
}

$frontendScript = Join-Path $projectRoot "frontend\app.py"
& $pythonExe -m streamlit run $frontendScript --server.port 8501
