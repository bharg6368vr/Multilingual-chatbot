# Run Rasa Action Server + LangChain
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " Starting Action Server (LangChain Engine) on Port 5055" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

$projectRoot = $PSScriptRoot
if (-not $projectRoot) { $projectRoot = (Get-Location).Path }
$pythonExe = Join-Path $projectRoot ".venv\Scripts\python.exe"

if (-not (Test-Path $pythonExe)) {
    Write-Host "[ERROR] Virtual environment (.venv) was not found!" -ForegroundColor Red
    Write-Host "Please run .\setup_env.bat first to set up .venv" -ForegroundColor Yellow
    Exit 1
}

$actionDir = Join-Path $projectRoot "action_server"
Push-Location $actionDir
try {
    & $pythonExe -m rasa_sdk.endpoint --actions actions --port 5055
} finally {
    Pop-Location
}
