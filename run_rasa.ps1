# Run Rasa Core Server
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " Starting Rasa Core Server on Port 5005" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

$projectRoot = $PSScriptRoot
if (-not $projectRoot) { $projectRoot = (Get-Location).Path }
$pythonExe = Join-Path $projectRoot ".venv\Scripts\python.exe"

if (-not (Test-Path $pythonExe)) {
    Write-Host "[ERROR] Virtual environment (.venv) was not found!" -ForegroundColor Red
    Write-Host "Please run .\setup_env.bat first to set up .venv" -ForegroundColor Yellow
    Exit 1
}

$rasaDir = Join-Path $projectRoot "rasa_bot"
Push-Location $rasaDir
try {
    & $pythonExe -m rasa run --enable-api --cors "*" --port 5005 --endpoints endpoints.yml --credentials credentials.yml
} finally {
    Pop-Location
}
