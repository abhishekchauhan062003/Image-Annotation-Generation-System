Write-Host "Starting React + Flask App (Dev Mode)" -ForegroundColor Green

# Full paths (adjust if needed)
$flaskPath = Join-Path $PWD "api"
$flaskVenvActivate = ".\api-env\Scripts\Activate.ps1"
$reactPath = $PWD  # Assuming React app is in current root folder (parent of api)

# Start Flask backend in a new PowerShell window
#hugging-face-api.py
Start-Process powershell -ArgumentList @(
    "-NoExit",
    "-Command",
    "`"cd `"$flaskPath`"; & $flaskVenvActivate;python hugging-face-api.py`""
) -WindowStyle Normal

# Start React frontend in a new PowerShell window
Start-Process powershell -ArgumentList @(
    "-NoExit",
    "-Command",
    "`"cd `"$reactPath`"; npm start -y`""
) -WindowStyle Normal

Write-Host "Launched Flask and React in separate terminal windows!"
