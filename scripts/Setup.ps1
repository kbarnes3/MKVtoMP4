# Set up project for the first time after , or set it back to the initial first unused state.
param(
    [switch]$DevRequirements,
    [switch]$GitClean
)

. $PSScriptRoot\Write-Status.ps1
$project_root = Split-Path $PSScriptRoot

if ($env:VIRTUAL_ENV) {
    deactivate
}

if ($GitClean) {
    Write-Status "Running 'git clean -df'"
    & git clean -df
}

# Remove local state if it exists
$venv = Join-Path $project_root "venv"
if (Test-Path $venv) {
    Write-Status "Removing $venv"
    Remove-Item -Recurse -Force -Path $venv
}

. $PSScriptRoot\Bootstrap.ps1 -DevRequirements:$DevRequirements -Verbose

. $PSScriptRoot\Ensure-Venv.ps1 | Out-Null

deactivate
