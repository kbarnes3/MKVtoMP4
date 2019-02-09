# Resolve all dependencies that the project requires to run.
param(
    [switch]$DevRequirements,
    [switch]$Verbose
)

. $PSScriptRoot\Write-Status.ps1

if ($Verbose) {
    $quiet = ""
}
else {
    $quiet = "--quiet"
}

$project_root = Split-Path $PSScriptRoot

Push-Location $project_root

$venv = Join-Path $project_root "venv"
if (-Not (Test-Path $venv)) {
    Write-Status "Creating venv in $venv"
    & py -3.7 -m venv $venv
}

$already_activated = . $PSScriptRoot\Ensure-Venv.ps1

Write-Status "Updating pip"
& python -m pip install --upgrade pip $quiet
Write-Status "Updating requirements"
& pip install -r (Join-Path $project_root "requirements.txt") $quiet
if ($DevRequirements) {
    Write-Status "Updating dev requirements"
    & pip install -r (Join-Path $project_root "dev-requirements.txt") $quiet
}

Pop-Location

if (-Not $already_activated) {
    deactivate
}
