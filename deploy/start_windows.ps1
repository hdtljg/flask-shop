param(
    [string]$BindAddress = "0.0.0.0",
    [int]$Port = 8000,
    [int]$Threads = 8
)

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

$Python = Join-Path $ProjectRoot ".venv\Scripts\python.exe"
if (-not (Test-Path $Python)) {
    throw "Virtual environment not found: $Python. Run: py -3.12 -m venv .venv; .venv\Scripts\python.exe -m pip install -r requirements.txt"
}

$env:HOST = $BindAddress
$env:PORT = "$Port"
$env:THREADS = "$Threads"

Write-Host "Starting Flask Shop with Waitress on http://${BindAddress}:${Port}"
& $Python serve.py
