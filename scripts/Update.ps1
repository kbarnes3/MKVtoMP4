# This script updates the project to run for its current checkout.
param(
    [switch]$DevRequirements,
    [switch]$Verbose
)

. $PSScriptRoot\Write-Status.ps1
$project_root = Split-Path $PSScriptRoot
$already_activated = . $PSScriptRoot\Ensure-Venv.ps1

# Check Python version
$venv_version = & python --version
$installed_version = & py -3.8 --version
if ($venv_version -ne $installed_version) {
    Write-Status "Updating venv from $venv_version to $installed_version"
    deactivate
    $venv = Join-Path $project_root "venv"
    & py -3.8 -m venv $venv --upgrade
    . $PSScriptRoot\Ensure-Venv.ps1 | Out-Null
}

. $PSScriptRoot\Bootstrap.ps1 -DevRequirements:$DevRequirements -Verbose:$Verbose

if (-Not $already_activated) {
    deactivate
}
