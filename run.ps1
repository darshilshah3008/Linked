<#
.SYNOPSIS
    Bootstrap and run the Job Search Copilot pipeline.
.DESCRIPTION
    Creates a virtual environment (if missing), installs dependencies,
    and runs the full daily pipeline. Works on any Windows machine
    with Python 3.11+ installed.
.EXAMPLE
    .\run.ps1                  # Full daily pipeline + Word report
    .\run.ps1 -Command seed   # Run a specific command
#>
param(
    [string]$Command = "daily-plan --export dashboard.json",
    [switch]$Fresh
)

$ErrorActionPreference = "Stop"
$ProjectRoot = $PSScriptRoot

# --- Locate Python -----------------------------------------------------------
$PythonExe = $null
foreach ($candidate in @(
    "python",
    "python3",
    "py",
    "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe",
    "$env:LOCALAPPDATA\Programs\Python\Python311\python.exe",
    "$env:LOCALAPPDATA\Programs\Python\Python313\python.exe"
)) {
    if (Get-Command $candidate -ErrorAction SilentlyContinue) {
        $PythonExe = $candidate
        break
    }
    if (Test-Path $candidate) {
        $PythonExe = $candidate
        break
    }
}

if (-not $PythonExe) {
    Write-Host "ERROR: Python 3.11+ not found. Install from https://www.python.org/downloads/" -ForegroundColor Red
    exit 1
}

Write-Host "Using Python: $PythonExe" -ForegroundColor Cyan

# --- Create virtual environment if missing ------------------------------------
$VenvDir = Join-Path $ProjectRoot ".venv"
$VenvPython = Join-Path $VenvDir "Scripts\python.exe"
$VenvPip = Join-Path $VenvDir "Scripts\pip.exe"

if (-not (Test-Path $VenvPython)) {
    Write-Host "Creating virtual environment in .venv ..." -ForegroundColor Yellow
    & $PythonExe -m venv $VenvDir
    if ($LASTEXITCODE -ne 0) { Write-Host "Failed to create venv." -ForegroundColor Red; exit 1 }
}

# --- Install dependencies ----------------------------------------------------
$Marker = Join-Path $VenvDir ".deps-installed"
if (-not (Test-Path $Marker)) {
    Write-Host "Installing dependencies ..." -ForegroundColor Yellow
    & $VenvPython -m pip install --upgrade pip --quiet
    & $VenvPip install -r (Join-Path $ProjectRoot "requirements.txt") --quiet
    & $VenvPip install -e $ProjectRoot --quiet
    if ($LASTEXITCODE -ne 0) { Write-Host "Dependency install failed." -ForegroundColor Red; exit 1 }
    New-Item -Path $Marker -ItemType File -Force | Out-Null
    Write-Host "Dependencies installed." -ForegroundColor Green
} else {
    Write-Host "Dependencies already installed (delete .venv\.deps-installed to reinstall)." -ForegroundColor DarkGray
}

# --- Optionally wipe the database for a fresh run ----------------------------
$DbPath = Join-Path $ProjectRoot "data\app.db"
if ($Fresh -and (Test-Path $DbPath)) {
    Write-Host "Removing old database for fresh run ..." -ForegroundColor Yellow
    Remove-Item -Force $DbPath
}

# --- Run the command ----------------------------------------------------------
Write-Host "`nRunning: python -m src $Command`n" -ForegroundColor Cyan
$argList = $Command -split '\s+'
& $VenvPython -m src @argList

if ($LASTEXITCODE -ne 0) { Write-Host "`nCommand failed." -ForegroundColor Red; exit 1 }

# --- If daily-plan was run, also generate the Word report --------------------
if ($Command -like "*daily-plan*") {
    Write-Host "`nGenerating Word report ..." -ForegroundColor Cyan
    & $VenvPython (Join-Path $ProjectRoot "generate_report_docx.py")
    Write-Host "Verifying database ..." -ForegroundColor Cyan
    & $VenvPython (Join-Path $ProjectRoot "inspect_db.py")
}

Write-Host "`nDone." -ForegroundColor Green
