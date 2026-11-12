# Train Rasa Bot Script
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " Training Rasa Multilingual Model" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

$projectRoot = $PSScriptRoot
if (-not $projectRoot) { $projectRoot = (Get-Location).Path }
$pythonExe = Join-Path $projectRoot ".venv\Scripts\python.exe"

if (-not (Test-Path $pythonExe)) {
    Write-Host "[ERROR] Virtual environment (.venv) was not found!" -ForegroundColor Red
    Write-Host "Please run .\setup_env.bat first to install Rasa and dependencies into .venv" -ForegroundColor Yellow
    Exit 1
}

$rasaDir = Join-Path $projectRoot "rasa_bot"
Push-Location $rasaDir
try {
    & $pythonExe -m rasa train --config config.yml --domain domain.yml --data data --out models
} finally {
    Pop-Location
}
